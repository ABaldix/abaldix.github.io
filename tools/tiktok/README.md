# TikToks (story videos)

Story-style vertical videos (1080x1920, 30 fps) with voiceover, one per article.
Not published with the site; videos are rendered locally and uploaded to TikTok by hand.

- `gen_scripts.py` writes `scripts/NN-slug.json` (on-screen lines + `say` voiceover per scene).
- `tts.py` synthesizes the voiceover with Kokoro (voice `af_heart`) and fits scene durations.
- `make_tiktok.js` draws each scene in Chromium (Playwright) and encodes it with ffmpeg.
- `render_one.sh scripts/NN-slug.json` runs the whole chain (expects assets in ../assets).
