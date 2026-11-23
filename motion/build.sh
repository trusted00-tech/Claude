#!/usr/bin/env bash
# ./build.sh configs/<name>.json out.mp4 [voiceover.mp3]
set -euo pipefail
cd "$(dirname "$0")"; CFG=$1; OUT=$2; VO=${3:-}
W=$(mktemp -d)
node render.js "$CFG" "$W/frames"
python3 audio.py "$W/frames/cues.json" "$W/music.wav"
if [ -n "$VO" ]; then
  ffmpeg -y -loglevel error -i "$W/music.wav" -i "$VO" -filter_complex \
   "[1:a]aresample=44100,asplit[v1][v2];[0:a]volume=0.35[m];[m][v1]sidechaincompress=threshold=0.05:ratio=8[d];[d][v2]amix=inputs=2:duration=first:normalize=0[a]" \
   -map "[a]" "$W/mix.wav"; A="$W/mix.wav"; else A="$W/music.wav"; fi
ffmpeg -y -loglevel error -framerate 30 -i "$W/frames/f%04d.jpg" -i "$A" -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
rm -rf "$W"; echo "OK -> $OUT"
