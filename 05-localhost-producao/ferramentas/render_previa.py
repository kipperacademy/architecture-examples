#!/usr/bin/env python3
"""Renderiza prévias SVG dos quadros para revisão rápida do deck."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = json.loads((ROOT / "apresentacao.excalidraw").read_text(encoding="utf-8"))
PREVIEW = ROOT.parent / ".context" / "aula05-preview"
PREVIEW.mkdir(parents=True, exist_ok=True)
FRAMES = [e for e in SCENE["elements"] if e["type"] == "frame" and not e.get("isDeleted")]


def render(frame, slide_no):
    x0, y0, width, height = frame["x"], frame["y"], frame["width"], frame["height"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1600" viewBox="0 0 1600 1600">',
           '<rect x="0" y="0" width="100%" height="100%" fill="#fff"/>',
           '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#9c36b5"/></marker></defs>',
           f'<g transform="translate({-x0},{350-y0})">']
    children = [e for e in SCENE["elements"] if e.get("frameId") == frame["id"] and not e.get("isDeleted")]
    for e in children:
        typ = e["type"]
        if typ == "rectangle":
            fill = e.get("backgroundColor", "transparent")
            out.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["width"]}" height="{e["height"]}" rx="10" fill="{fill}" stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}"/>')
        elif typ == "arrow":
            x1, y1 = e["x"], e["y"]
            x2, y2 = x1 + e["width"], y1 + e["height"]
            out.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}" marker-end="url(#arrow)"/>')
        elif typ == "text":
            size = e["fontSize"]
            line_h = size * e.get("lineHeight", 1.25)
            align = e.get("textAlign", "left")
            anchor = {"left": "start", "center": "middle", "right": "end"}.get(align, "start")
            text_x = e["x"] if align == "left" else e["x"] + e["width"] / 2 if align == "center" else e["x"] + e["width"]
            lines = e.get("text", "").split("\n")
            out.append(f'<text x="{text_x}" y="{e["y"]}" fill="{e["strokeColor"]}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" dominant-baseline="hanging">')
            for i, line in enumerate(lines):
                out.append(f'<tspan x="{text_x}" dy="{0 if i == 0 else line_h}">{html.escape(line)}</tspan>')
            out.append('</text>')
    out.extend(['</g>', '</svg>'])
    path = PREVIEW / f"slide-{slide_no:02d}.svg"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


for i, frame in enumerate(FRAMES, 1):
    print(render(frame, i))
