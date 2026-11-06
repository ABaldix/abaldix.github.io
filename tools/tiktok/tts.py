# Adds narration to a TikTok script: synthesizes each scene's "say" text with Kokoro,
# sets each scene's duration to fit its line, and writes the narration track.
# Usage: python3 tts.py script.json resolved.json narration.wav [voice]
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
src, dst, wav = sys.argv[1:4]; voice = sys.argv[4] if len(sys.argv) > 4 else 'af_heart'
k = Kokoro('/home/claude/tts/model.onnx', '/home/claude/tts/voices.npz')
S = json.load(open(src)); sr = 24000; LEAD, TAIL = 0.25, 0.45; track = []
for sc in S['scenes']:
    a, sr = k.create(sc['say'], voice=voice, speed=1.08, lang='en-us')
    a = np.asarray(a, dtype=np.float32)
    dur = max(sc.get('min', 2.6), LEAD + len(a) / sr + TAIL)
    dur = round(dur * 30) / 30  # whole frames
    sc['dur'] = dur
    seg = np.zeros(int(round(dur * sr)), dtype=np.float32)
    s0 = int(LEAD * sr); seg[s0:s0 + len(a)] = a[:len(seg) - s0]
    track.append(seg)
sf.write(wav, np.concatenate(track), sr)
json.dump(S, open(dst, 'w'), indent=1, ensure_ascii=False)
print('total', round(sum(sc['dur'] for sc in S['scenes']), 2), 's', [sc['dur'] for sc in S['scenes']])
