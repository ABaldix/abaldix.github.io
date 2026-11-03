// Sends the newsletter form to MailerLite without leaving the page.
(function () {
    document.querySelectorAll(".nl-form").forEach(function (form) {
        form.setAttribute("data-t", String(Date.now()));
        form.addEventListener("submit", function (e) {
            var email = form.querySelector('input[type="email"]');
            var msg = form.querySelector(".nl-msg");
            var btn = form.querySelector("button");
            if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
                e.preventDefault();
                msg.textContent = "Please enter a valid email address.";
                msg.className = "nl-msg nl-err";
                email.focus();
                return;
            }
            var hp = form.querySelector('input[name="nl_website"]');
            if (hp && hp.value) { e.preventDefault(); form.reset(); return; } // bot filled the hidden field
            var started = parseInt(form.getAttribute("data-t") || "0", 10);
            if (started && Date.now() - started < 2500) { e.preventDefault(); return; } // submitted faster than a human could type
            if (!window.fetch || !window.FormData) return; // fall back to a normal submit in a new tab
            e.preventDefault();
            btn.disabled = true;
            msg.textContent = "Sending…";
            msg.className = "nl-msg";
            var fd = new FormData(form); fd.delete("nl_website");
            fetch(form.action, { method: "POST", body: fd })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data && data.success) {
                        form.reset();
                        msg.textContent = "You're in! Check your inbox for our welcome email with the best guides to start.";
                        msg.className = "nl-msg nl-ok";
                    } else {
                        throw new Error("rejected");
                    }
                })
                .catch(function () {
                    msg.textContent = "Sorry, something went wrong. Please try again in a moment.";
                    msg.className = "nl-msg nl-err";
                })
                .then(function () { btn.disabled = false; });
        });
    });
})();
