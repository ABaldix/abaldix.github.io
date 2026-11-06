#!/bin/bash
# Usage: render_one.sh scripts/NN-slug.json  -> out/NN-slug.mp4 (voice + video)
set -e
cd /home/claude/tiktok
f="$1"; b=$(basename "$f" .json)
[ -f "out/$b.mp4" ] && exit 0
python3 tts.py "$f" "scripts/.$b.resolved.json" "out/.$b.wav" >/dev/null
NODE_PATH=$(npm root -g) node make_tiktok.js "scripts/.$b.resolved.json" "out/.$b-silent.mp4" >/dev/null
ffmpeg -loglevel error -y -i "out/.$b-silent.mp4" -i "out/.$b.wav" -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 44100 -c:a aac -b:a 160k -shortest -movflags +faststart "out/.$b.tmp.mp4"
mv "out/.$b.tmp.mp4" "out/$b.mp4"
rm -rf "out/.$b-silent.mp4" "out/.parts-.$b-silent"
echo "done $b"
