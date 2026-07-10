"""Find each camera file's offset against the master mic timeline by
cross-correlating audio energy envelopes.

The mic WAVs are the master clock (that's what the transcript is timed
against). Each camera MP4 carries scratch audio of the same room, so the
lag that maximizes envelope correlation is that file's start offset:

    master_time = offset + camera_time

Envelopes are RMS at ENV_HZ (50 Hz), giving 20 ms resolution — more than
enough for cut points since final audio comes from the mics, not the cams.
"""
import argparse
import os
import subprocess
import tempfile

import numpy as np

from .common import ffprobe_duration, load_json, log, save_json

SR = 4000      # extraction sample rate
ENV_HZ = 50    # envelope rate


def extract_pcm(path, sr=SR):
    with tempfile.NamedTemporaryFile(suffix=".f32", delete=False) as tmp:
        tmppath = tmp.name
    try:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", path, "-vn",
             "-ac", "1", "-ar", str(sr), "-f", "f32le", tmppath],
            check=True)
        return np.fromfile(tmppath, dtype=np.float32)
    finally:
        os.unlink(tmppath)


def envelope(pcm, sr=SR, env_hz=ENV_HZ):
    hop = sr // env_hz
    n = len(pcm) // hop * hop
    frames = pcm[:n].reshape(-1, hop)
    env = np.sqrt((frames ** 2).mean(axis=1))
    env -= env.mean()
    std = env.std()
    return env / std if std > 0 else env


def best_lag(master_env, cam_env, env_hz=ENV_HZ):
    """Return (offset_seconds, confidence). offset = master_time - cam_time."""
    n = len(master_env) + len(cam_env)
    nfft = 1 << (n - 1).bit_length()
    corr = np.fft.irfft(
        np.fft.rfft(master_env, nfft) * np.conj(np.fft.rfft(cam_env, nfft)),
        nfft)
    # lags: index i => master leads cam by i (wrap for negative lags)
    lags = np.concatenate([np.arange(0, len(master_env)),
                           np.arange(-len(cam_env) + 1, 0)])
    vals = np.concatenate([corr[: len(master_env)], corr[-len(cam_env) + 1:]])
    i = int(np.argmax(vals))
    peak = vals[i]
    noise = np.median(np.abs(vals)) + 1e-9
    return float(lags[i]) / env_hz, float(peak / noise)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--media", default="media")
    ap.add_argument("--out", default="work/offsets.json")
    args = ap.parse_args(argv)

    manifest = load_json(args.manifest)
    mics = [f for f in manifest["files"] if f["role"] == "mic"]
    log("building master envelope from mic tracks ...")
    master = None
    for f in mics:
        pcm = extract_pcm(os.path.join(args.media, f["name"]))
        master = pcm if master is None else (
            master[: len(pcm)] + pcm[: len(master)])
    master_env = envelope(master)

    offsets = {}
    for f in manifest["files"]:
        if f["role"] not in ("cam", "wide"):
            continue
        path = os.path.join(args.media, f["name"])
        if not os.path.exists(path):
            log(f"skipping {f['name']} (not downloaded)")
            continue
        cam_env = envelope(extract_pcm(path))
        offset, conf = best_lag(master_env, cam_env)
        dur = ffprobe_duration(path)
        offsets[f["name"]] = {"offset": round(offset, 3),
                              "duration": round(dur, 3),
                              "confidence": round(conf, 1)}
        log(f"{f['name']}: offset {offset:+.2f}s conf {conf:.0f} dur {dur:.0f}s")
        if conf < 8:
            log(f"WARNING: low sync confidence for {f['name']} — verify manually")

    save_json(args.out, offsets)


if __name__ == "__main__":
    main()
