// Sends the newsletter form to MailerLite without leaving the page.
(function () {
    document.querySelectorAll(".nl-form").forEach(function (form) {
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
            if (!window.fetch || !window.FormData) return; // fall back to a normal submit in a new tab
            e.preventDefault();
            btn.disabled = true;
            msg.textContent = "Sending…";
            msg.className = "nl-msg";
            fetch(form.action, { method: "POST", body: new FormData(form) })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data && data.success) {
                        form.reset();
                        msg.textContent = "Almost done! Check your inbox and click the confirmation link.";
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
