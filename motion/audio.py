"""python3 audio.py cues.json out.wav  -- synth beat + whoosh/pop SFX on cue points (placeholder music; swap for trending sound on upload)."""
import json, sys, wave, numpy as np
cues = json.load(open(sys.argv[1])); SR = 44100; D = cues['duration']; N = int(SR * D)
out = np.zeros(N); rng = np.random.default_rng(1)
def add(sig, t, g=1.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); out[i:j] += sig[:j - i] * g
def env(n, k): return np.exp(-np.arange(n) / SR * k)
def kick():
    n = int(.35 * SR); tt = np.arange(n) / SR; f = 50 + 120 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 9)
def hat():
    n = int(.06 * SR); x = np.diff(np.r_[0, rng.standard_normal(n)]); return x * env(n, 70) * .5
def snare():
    n = int(.2 * SR); tt = np.arange(n) / SR
    return rng.standard_normal(n) * env(n, 22) * .6 + np.sin(2 * np.pi * 190 * tt) * env(n, 30) * .5
def whoosh(d=.45):
    n = int(d * SR); x = rng.standard_normal(n); e = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return (np.convolve(x, np.ones(8) / 8, 'same') - np.convolve(x, np.ones(60) / 60, 'same')) * e * 1.4
def pop():
    n = int(.12 * SR); tt = np.arange(n) / SR; f = 900 - 500 * tt / .12
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 35) * .7
def riser(d=1.0):
    n = int(d * SR); tt = np.arange(n) / SR; f = 200 + 900 * (tt / d) ** 2
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * .25 + np.convolve(rng.standard_normal(n), np.ones(10) / 10, 'same') * .3) * (tt / d) ** 2
b = .5; notes = [55, 55, 65.4, 49]; t = 0.0; k = 0
while t < D - .3:
    add(kick(), t, .9); add(hat(), t + b / 2, .35)
    if k % 2: add(snare(), t, .45)
    n = int(b * SR * .9); tt = np.arange(n) / SR
    add(np.sin(2 * np.pi * notes[(k // 4) % 4] * tt) * np.exp(-tt * 3) * .35, t); t += b; k += 1
for tr in cues['transitions']: add(whoosh(), tr - .25, .8)
for p in cues['pops']: add(pop(), p, .6)
add(riser(1.0), cues['riser'], .8)
out = out / np.max(np.abs(out)) * .85; f = int(.6 * SR); out[-f:] *= np.linspace(1, 0, f)
w = wave.open(sys.argv[2], 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
