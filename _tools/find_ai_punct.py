#!/usr/bin/env python3
"""Discovery-only: list every em-dash and every PROSE semicolon needing
the anti-AI rewrite. Skips <script>/<style> blocks, base64 lines, inline/display
math spans, LaTeX \\; thin-spaces, and HTML entities. Read-only."""
import re, sys

def find(path, lo=1, hi=10**9):
    lines = open(path, encoding="utf-8").read().split("\n")
    in_block = False
    for i, ln in enumerate(lines, 1):
        if "<script" in ln or "<style" in ln:
            in_block = True
        if not in_block and "base64" not in ln and lo <= i <= hi:
            t = re.sub(r"\\\(.*?\\\)", "", ln)      # inline math \(...\)
            t = re.sub(r"\\\[.*?\\\]", "", t)        # display math \[...\]
            t = re.sub(r"\\;", "", t)                 # LaTeX thin space
            t = re.sub(r"&[a-zA-Z]+;|&#[0-9]+;", "", t)  # HTML entities
            has_dash = "—" in ln                 # em-dash
            has_semi = ";" in t
            if has_dash or has_semi:
                tag = ("D" if has_dash else "") + ("S" if has_semi else "")
                print(f"{i}|{tag}|{ln.strip()}")
        if "</script>" in ln or "</style>" in ln:
            in_block = False

if __name__ == "__main__":
    path = sys.argv[1]
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    find(path, lo, hi)
