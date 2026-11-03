// VivaVoltia newsletter signup – Cloudflare Worker
//
// Receives { email, token } from the signup form on vivavoltia.com, checks the
// Cloudflare Turnstile token, and only then adds the email to MailerLite.
//
// Settings (Cloudflare dashboard → Workers → this worker → Settings → Variables and Secrets):
//   TURNSTILE_SECRET     (Secret)  Turnstile secret key
//   MAILERLITE_API_KEY   (Secret)  MailerLite API token (Integrations → API)
//   MAILERLITE_GROUP_ID  (Text)    203130222331037630  (group "vivavoltia-subscribers")

const ALLOWED_ORIGINS = ["https://vivavoltia.com", "https://www.vivavoltia.com"];
const ALLOWED_HOSTNAMES = ["vivavoltia.com", "www.vivavoltia.com"];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function reply(data, status, cors) {
    return new Response(JSON.stringify(data), {
        status,
        headers: { "Content-Type": "application/json", ...cors },
    });
}

export default {
    async fetch(request, env) {
        const origin = request.headers.get("Origin") || "";
        const cors = {
            "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
            "Vary": "Origin",
        };

        if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
        if (request.method !== "POST") return reply({ success: false, error: "method" }, 405, cors);
        if (!ALLOWED_ORIGINS.includes(origin)) return reply({ success: false, error: "origin" }, 403, cors);

        let body;
        try {
            body = await request.json();
        } catch {
            return reply({ success: false, error: "bad_request" }, 400, cors);
        }

        const email = String(body.email || "").trim().toLowerCase();
        const token = String(body.token || "");
        if (!EMAIL_RE.test(email) || email.length > 254) return reply({ success: false, error: "email" }, 400, cors);
        if (!token) return reply({ success: false, error: "captcha" }, 400, cors);

        // 1) Verify the Turnstile token with Cloudflare
        const form = new FormData();
        form.append("secret", env.TURNSTILE_SECRET);
        form.append("response", token);
        const ip = request.headers.get("CF-Connecting-IP");
        if (ip) form.append("remoteip", ip);
        const check = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form })
            .then((r) => r.json())
            .catch(() => ({ success: false }));
        if (!check.success || (check.hostname && !ALLOWED_HOSTNAMES.includes(check.hostname))) {
            return reply({ success: false, error: "captcha" }, 400, cors);
        }

        // 2) Add (or update) the subscriber in MailerLite and put them in the group
        const ml = await fetch("https://connect.mailerlite.com/api/subscribers", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": `Bearer ${env.MAILERLITE_API_KEY}`,
            },
            body: JSON.stringify({ email, groups: [String(env.MAILERLITE_GROUP_ID || "203130222331037630")] }),
        }).catch(() => null);

        if (!ml || !ml.ok) return reply({ success: false, error: "provider" }, 502, cors);
        return reply({ success: true }, 200, cors);
    },
};
