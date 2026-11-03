// VivaVoltia newsletter form.
// If the form has data-endpoint and data-sitekey, it uses Cloudflare Turnstile and sends
// { email, token } to our Cloudflare Worker, which verifies the captcha and adds the email
// to MailerLite. Otherwise it posts straight to the MailerLite form endpoint.
(function () {
    var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    var tsLoading = null;

    function loadTurnstile() {
        if (window.turnstile) return Promise.resolve(window.turnstile);
        if (tsLoading) return tsLoading;
        tsLoading = new Promise(function (resolve, reject) {
            var s = document.createElement("script");
            s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
            s.async = true; s.defer = true;
            s.onload = function () { resolve(window.turnstile); };
            s.onerror = reject;
            document.head.appendChild(s);
        });
        return tsLoading;
    }

    document.querySelectorAll(".nl-form").forEach(function (form) {
        var email = form.querySelector('input[type="email"]');
        var msg = form.querySelector(".nl-msg");
        var btn = form.querySelector("button");
        var box = form.querySelector(".nl-captcha");
        var endpoint = form.getAttribute("data-endpoint");
        var sitekey = form.getAttribute("data-sitekey");
        var useCaptcha = !!(endpoint && sitekey && box);
        var widgetId = null;
        form.setAttribute("data-t", String(Date.now()));

        function say(text, cls) { msg.textContent = text; msg.className = "nl-msg" + (cls ? " " + cls : ""); }

        function ensureWidget() {
            if (!useCaptcha || widgetId !== null) return Promise.resolve();
            return loadTurnstile().then(function (ts) {
                if (widgetId === null) {
                    widgetId = ts.render(box, { sitekey: sitekey, size: "flexible", appearance: "interaction-only", action: "newsletter" });
                }
            });
        }
        // Load the captcha as soon as someone shows interest, not on every page view
        if (useCaptcha) {
            email.addEventListener("focus", function () { ensureWidget().catch(function () {}); }, { once: true });
        }

        form.addEventListener("submit", function (e) {
            var hp = form.querySelector('input[name="nl_website"]');
            if (hp && hp.value) { e.preventDefault(); form.reset(); return; } // bot filled the hidden field
            var started = parseInt(form.getAttribute("data-t") || "0", 10);
            if (started && Date.now() - started < 2500) { e.preventDefault(); return; } // faster than a human could type
            if (!EMAIL_RE.test(email.value.trim())) {
                e.preventDefault();
                say("Please enter a valid email address.", "nl-err");
                email.focus();
                return;
            }
            if (!window.fetch || !window.FormData) return; // very old browsers: normal submit
            e.preventDefault();

            function done(ok, text) {
                say(text, ok ? "nl-ok" : "nl-err");
                btn.disabled = false;
                if (ok) form.reset();
                if (useCaptcha && window.turnstile && widgetId !== null) window.turnstile.reset(widgetId);
            }

            btn.disabled = true;
            say("Sending…");

            if (useCaptcha) {
                ensureWidget().then(function () {
                    var token = window.turnstile.getResponse(widgetId);
                    if (!token) {
                        btn.disabled = false;
                        say("Please complete the quick check above, then press Subscribe again.", "nl-err");
                        return;
                    }
                    return fetch(endpoint, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ email: email.value.trim(), token: token })
                    }).then(function (r) { return r.json(); }).then(function (d) {
                        if (d && d.success) done(true, "You're in! Check your inbox for our welcome email with the best guides to start.");
                        else if (d && d.error === "captcha") done(false, "We couldn't verify you're human. Please try again.");
                        else done(false, "Sorry, something went wrong. Please try again in a moment.");
                    });
                }).catch(function () { done(false, "Sorry, something went wrong. Please try again in a moment."); });
                return;
            }

            var fd = new FormData(form); fd.delete("nl_website");
            fetch(form.action, { method: "POST", body: fd })
                .then(function (r) { return r.json(); })
                .then(function (d) {
                    if (d && d.success) done(true, "You're in! Check your inbox for our welcome email with the best guides to start.");
                    else throw new Error("rejected");
                })
                .catch(function () { done(false, "Sorry, something went wrong. Please try again in a moment."); });
        });
    });
})();
