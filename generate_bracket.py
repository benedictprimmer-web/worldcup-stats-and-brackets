#!/usr/bin/env python3
"""Generate an SVG knockout bracket from a tournament JSON file.

Usage:
    python3 generate_bracket.py data/wc2022_knockout.json bracket.svg
"""
import json
import sys


# ---- visual constants ----------------------------------------------------
BOX_W, BOX_H = 150, 46          # match box size
COL_GAP = 70                    # horizontal gap between rounds
PAD_X, PAD_Y = 40, 90           # outer padding
TITLE_H = 60

GOLD = "#d4af37"
INK = "#15233b"
LINE = "#9fb0c7"
BG = "#f4f6fb"
BOX_BG = "#ffffff"
WIN = "#1b6b3a"


def winner(m):
    """Return the name of the winning team for a match dict."""
    h, a = m["home"], m["away"]
    if "pens" in m:
        ph, pa = (int(x) for x in m["pens"].split("–"))
        return h if ph > pa else a
    sh, sa = (int(x) for x in m["score"].split("–"))
    return h if sh > sa else a


def match_box(x, y, m):
    """SVG for a single match box with two team rows."""
    w = winner(m)
    rows = []
    for i, side in enumerate(("home", "away")):
        team = m[side]
        ty = y + (BOX_H / 2) * i
        is_win = team == w
        fill = WIN if is_win else INK
        weight = "700" if is_win else "500"
        rows.append(
            f'<text x="{x + 10}" y="{ty + BOX_H/4 + 4}" '
            f'fill="{fill}" font-weight="{weight}" font-size="13">{team}</text>'
        )
    score = m["score"] + (f' ({m["pens"]} p)' if "pens" in m else "")
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="6" '
        f'fill="{BOX_BG}" stroke="{LINE}" stroke-width="1"/>'
        f'<line x1="{x}" y1="{y + BOX_H/2}" x2="{x + BOX_W}" y2="{y + BOX_H/2}" '
        f'stroke="{BG}" stroke-width="1"/>'
        + "".join(rows)
        + f'<text x="{x + BOX_W - 8}" y="{y + BOX_H/2 + 4}" text-anchor="end" '
        f'fill="{GOLD}" font-weight="700" font-size="11">{score}</text>'
        f'</g>'
    )


def connector(x1, y1, x2, y2):
    midx = (x1 + x2) / 2
    return (
        f'<path d="M {x1} {y1} H {midx} V {y2} H {x2}" '
        f'fill="none" stroke="{LINE}" stroke-width="1.5"/>'
    )


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "data/wc2022_knockout.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "bracket.svg"
    data = json.load(open(src, encoding="utf-8"))
    r = data["rounds"]

    cols = [r["round_of_16"], r["quarter_finals"], r["semi_finals"], r["final"]]
    labels = ["Round of 16", "Quarter-finals", "Semi-finals", "Final"]

    n0 = len(cols[0])
    full_h = n0 * BOX_H + (n0 - 1) * (BOX_H / 2)   # round-of-16 stack height
    height = TITLE_H + PAD_Y + full_h + PAD_Y
    width = PAD_X * 2 + len(cols) * BOX_W + (len(cols) - 1) * COL_GAP

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        f'<text x="{width/2}" y="38" text-anchor="middle" fill="{INK}" '
        f'font-size="24" font-weight="800">{data["tournament"]}</text>',
        f'<text x="{width/2}" y="{height-18}" text-anchor="middle" fill="{GOLD}" '
        f'font-size="15" font-weight="700">\U0001F3C6 Champion: {data["champion"]}</text>',
    ]

    # vertical centre of each box, per column
    centres = []
    top = TITLE_H + PAD_Y
    for col_i, col in enumerate(cols):
        x = PAD_X + col_i * (BOX_W + COL_GAP)
        parts.append(
            f'<text x="{x + BOX_W/2}" y="{TITLE_H + PAD_Y - 30}" text-anchor="middle" '
            f'fill="{INK}" font-size="13" font-weight="700" opacity="0.7">{labels[col_i]}</text>'
        )
        col_centres = []
        n = len(col)
        # spacing so each column is vertically centred against the first
        slot = full_h / n
        for i, m in enumerate(col):
            cy = top + slot * i + slot / 2
            y = cy - BOX_H / 2
            parts.append(match_box(x, y, m))
            col_centres.append(cy)
        centres.append(col_centres)

    # connectors between adjacent rounds
    for col_i in range(len(cols) - 1):
        x_right = PAD_X + col_i * (BOX_W + COL_GAP) + BOX_W
        x_next = PAD_X + (col_i + 1) * (BOX_W + COL_GAP)
        nxt = centres[col_i + 1]
        for j, cy_next in enumerate(nxt):
            for k in (2 * j, 2 * j + 1):
                if k < len(centres[col_i]):
                    parts.append(connector(x_right, centres[col_i][k], x_next, cy_next))

    parts.append("</svg>")
    open(out, "w", encoding="utf-8").write("\n".join(parts))
    print(f"wrote {out} ({width}x{height})")


if __name__ == "__main__":
    main()
