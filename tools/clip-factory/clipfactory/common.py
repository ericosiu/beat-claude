"""Shared helpers for the clip-factory pipeline."""
import json
import os
import subprocess
import sys


def log(msg):
    print(f"[clip-factory] {msg}", file=sys.stderr)


def run(cmd, **kw):
    log(" ".join(str(c) for c in cmd))
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    log(f"wrote {path}")


def media_path(media_dir, name):
    p = os.path.join(media_dir, name)
    if not os.path.exists(p):
        raise FileNotFoundError(f"expected media file missing: {p}")
    return p


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def fmt_ts(seconds):
    h = int(seconds // 3600)
    m = int(seconds % 3600 // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"
