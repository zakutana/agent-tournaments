#!/usr/bin/env python3
"""Build the Agent Tournaments design mockups from the sample data below.

Writes, next to this file:
  index.html    Lobby: tables (rooms) as poker tables with 10 seats, your agent, top agents
  room.html     One room: the big table, pot, countdown, your agent, leaderboard, the race
  send.html     Send your agent: 3 steps, the prompt, what the approval looks like, stakes
  preview.html  All three in ONE self-contained file you can open with a double-click

Design only: no functionality. Every name and number is invented sample data.
Standard library only:  python3 design/build.py
"""
import math
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC_URL = "https://github.com/zakutana/agent-tournaments/blob/claude/upbeat-archimedes-d2yurc/SPEC.md"
FONTS = ("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600;700;800"
         "&family=Space+Grotesk:wght@400;500;600;700&family=Unbounded:wght@500;700;800;900&display=swap")
MOCK_NOW = "2026-10-10T16:49:36Z"   # the countdowns tick from this moment

# ------------------------------------------------------------------ icons
I = {
    "bolt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.2 2.5 4.8 13.6h6l-1 7.9 8.4-11.1h-6z"/></svg>',
    "copy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6.5A2.5 2.5 0 0 1 7.5 4H15"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 12a8 8 0 0 1-11.7 7.1L4 20l1-4.4A8 8 0 1 1 20.5 12z"/><path d="M8.5 11h7M8.5 14.2h4.5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 4.6-3.4 8.3-8 9-4.6-.7-8-4.4-8-9V6z"/><path d="M8.5 12.2l2.4 2.4 4.6-5"/></svg>',
    "trophy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4c0 3 1.6 4.6 3.6 5M17 6h3c0 3-1.6 4.6-3.6 5M12 14v3.5M8.5 20.5h7"/></svg>',
    "crown": '<svg viewBox="0 0 18 12" fill="currentColor" aria-hidden="true"><path d="M1 11.2 2.4 2.8l4 3.9L9 .8l2.6 5.9 4-3.9 1.4 8.4z"/></svg>',
    "right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    "chev": '<svg class="sep" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 5l7.5 12h-15z"/></svg>',
    "down": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 19 4.5 7h15z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.1"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
}

# the logo: a poker chip with a bot's two eyes (one cyan, one green)
LOGO = ('<svg viewBox="0 0 48 48" aria-hidden="true">'
        '<circle cx="24" cy="24" r="21.5" fill="#0d1520" stroke="url(#g-brand)" stroke-width="3.6"/>'
        '<circle cx="24" cy="24" r="21.5" fill="none" stroke="#E6EDF7" stroke-width="3.6" stroke-dasharray="5 11.886" stroke-dashoffset="2.5" opacity=".92"/>'
        '<circle cx="24" cy="24" r="15.2" fill="none" stroke="url(#g-brand)" stroke-width="1.3" stroke-dasharray="1.6 2.4" opacity=".75"/>'
        '<rect x="16.2" y="18.5" width="5.6" height="11" rx="2.8" fill="#00cfff"/>'
        '<rect x="26.2" y="18.5" width="5.6" height="11" rx="2.8" fill="#00ff88"/></svg>')

# hidden sprite: brand gradient + six bot heads (avatars), drawn in currentColor
SPRITE = """<svg class="sprite" aria-hidden="true" focusable="false"><defs>
<linearGradient id="g-brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00cfff"/><stop offset="1" stop-color="#00ff88"/></linearGradient>
<symbol id="bot-a" viewBox="0 0 40 40"><path d="M20 13V9.4" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="20" cy="7.8" r="2.3" fill="currentColor"/><rect x="9.5" y="13" width="21" height="18" rx="6" fill="currentColor" fill-opacity=".18" stroke="currentColor" stroke-width="2.2"/><circle cx="15.6" cy="21" r="2.6" fill="currentColor"/><circle cx="24.4" cy="21" r="2.6" fill="currentColor"/><path d="M16.2 26.4q3.8 2.4 7.6 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
<symbol id="bot-b" viewBox="0 0 40 40"><path d="M14.2 13l-2.2-4.4M25.8 13l2.2-4.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="11.6" cy="7.9" r="1.9" fill="currentColor"/><circle cx="28.4" cy="7.9" r="1.9" fill="currentColor"/><rect x="9.5" y="13" width="21" height="18" rx="6" fill="currentColor" fill-opacity=".18" stroke="currentColor" stroke-width="2.2"/><rect x="12.4" y="18.3" width="15.2" height="5.6" rx="2.8" fill="currentColor"/><path d="M17 27.2h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
<symbol id="bot-c" viewBox="0 0 40 40"><rect x="5.6" y="18" width="3.4" height="8" rx="1.5" fill="currentColor"/><rect x="31" y="18" width="3.4" height="8" rx="1.5" fill="currentColor"/><rect x="9.5" y="12" width="21" height="19" rx="5" fill="currentColor" fill-opacity=".18" stroke="currentColor" stroke-width="2.2"/><rect x="13.2" y="17.4" width="4.8" height="4.8" rx="1.1" fill="currentColor"/><rect x="22" y="17.4" width="4.8" height="4.8" rx="1.1" fill="currentColor"/><path d="M15.6 25.8v2.2M18.6 25.8v2.2M21.4 25.8v2.2M24.4 25.8v2.2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></symbol>
<symbol id="bot-d" viewBox="0 0 40 40"><path d="M20 12.6V8.6M16.8 8.6h6.4" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><rect x="9.5" y="12.6" width="21" height="18.4" rx="7" fill="currentColor" fill-opacity=".18" stroke="currentColor" stroke-width="2.2"/><circle cx="20" cy="20.6" r="5" fill="currentColor" fill-opacity=".3" stroke="currentColor" stroke-width="2"/><circle cx="20" cy="20.6" r="2.1" fill="currentColor"/><path d="M16.6 27.1h6.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
<symbol id="bot-e" viewBox="0 0 40 40"><path d="M20 13V9l3.6-1.8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><rect x="9.5" y="13" width="21" height="18" rx="6" fill="currentColor" fill-opacity=".18" stroke="currentColor" stroke-width="2.2"/><path d="M13.4 20.6h5M21.6 20.6h5" stroke="currentColor" stroke-width="2.8" stroke-linecap="round"/><circle cx="20" cy="26.3" r="1.7" fill="currentColor"/></symbol>
<symbol id="bot-f" viewBox="0 0 40 40"><path d="M8.6 21.5a11.4 11.4 0 0 1 22.8 0" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><rect x="11" y="14" width="18" height="17" rx="6" fill="currentColor" fill-opacity=".18" stroke="currentColor" stroke-width="2.2"/><rect x="6.4" y="19" width="4.6" height="8.4" rx="2" fill="currentColor"/><rect x="29" y="19" width="4.6" height="8.4" rx="2" fill="currentColor"/><circle cx="16.5" cy="21.6" r="2.3" fill="currentColor"/><circle cx="23.5" cy="21.6" r="2.3" fill="currentColor"/><path d="M17.2 26.6h5.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
</defs></svg>"""

# ------------------------------------------------------------------ sample data
# name: (colour, bot head, what it runs on, rating)   - colours stay inside the site's palette family
AGENTS = {
    "QuantKoala": ("#00ff88", "a", "Claude", 1712),
    "AlphaWolf-7": ("#00cfff", "b", "ChatGPT", 1588),
    "MeanRevBot": ("#3b82f6", "c", "RSI clone", 1561),
    "GridRunner": ("#14b8a6", "d", "grid bot", 1540),
    "TrendTurtle": ("#ff7b7b", "e", "own model", 1507),
    "PaperHands-0": ("#6F8199", "f", "new", 1500),
    "NorthStar-LLM": ("#93c5fd", "a", "Gemini", 1522),
    "VolSniper": ("#a7f3d0", "d", "own model", 1498),
    "MomentumMax": ("#ff4444", "e", "TREND clone", 1476),
    "DeltaNeutral-3": ("#e2e8f0", "c", "own model", 1463),
    "SigmaFox": ("#ff7b7b", "b", "own model", 1655),
    "OrderBookOwl": ("#93c5fd", "f", "own model", 1511),
    "Lynx-2": ("#e2e8f0", "a", "Llama", 1494),
    "ArbRat": ("#a7f3d0", "c", "arb bot", 1530),
    "HodlBot": ("#3b82f6", "e", "Claude", 1489),
    "Sentinel-9": ("#14b8a6", "f", "own model", 1517),
    "WenLambo": ("#00ff88", "d", "ChatGPT", 1471),
}
YOU = "AlphaWolf-7"
YOU_TAG = ' <span class="tag you">YOU</span>'

# Micro #14, day 4 of 7: (rank, agent, ROI %, volume $, volume state, prize)
BOARD = [
    (1, "QuantKoala", 12.31, 142, "ok", 30),
    (2, "AlphaWolf-7", 8.42, 48, "pace", 15),
    (3, "MeanRevBot", 5.07, 96, "ok", 5),
    (4, "GridRunner", 3.90, 211, "ok", None),
    (5, "TrendTurtle", 1.12, 33, "slow", None),
    (6, "PaperHands-0", 0.00, 0, "zero", None),
    (7, "NorthStar-LLM", -0.85, 80, "ok", None),
    (8, "VolSniper", -2.40, 57, "pace", None),
    (9, "MomentumMax", -6.93, 120, "ok", None),
    (10, "DeltaNeutral-3", -9.80, 12, "slow", None),
]
# who sits where at the Micro #14 table (seat 0 is top centre-right, clockwise; you sit at the front)
MICRO14_SEATS = ["QuantKoala", "GridRunner", "NorthStar-LLM", "MomentumMax", "MeanRevBot",
                 "AlphaWolf-7", "TrendTurtle", "DeltaNeutral-3", "VolSniper", "PaperHands-0"]

ROOMS = [
    dict(id="micro-14", name="Micro #14", tier="micro", buyin=5, state="live", pot=50, end="2026-10-13T18:00:00Z",
         seats=MICRO14_SEATS, lead="QuantKoala", mine=True),
    dict(id="pro-6", name="Pro #6", tier="pro", buyin=50, state="final", pot=500, end="2026-10-11T06:00:00Z",
         seats=["SigmaFox", "Lynx-2", "GridRunner", "OrderBookOwl", "NorthStar-LLM", "HodlBot", "ArbRat",
                "Sentinel-9", "WenLambo", "VolSniper"], lead="SigmaFox", lead_roi=6.12),
    dict(id="micro-15", name="Micro #15", tier="micro", buyin=5, state="open", pot=35,
         seats=["GridRunner", "VolSniper", "NorthStar-LLM", "SigmaFox", "MeanRevBot", "OrderBookOwl", "Lynx-2",
                None, None, None]),
    dict(id="pro-7", name="Pro #7", tier="pro", buyin=50, state="open", pot=200, mine=True,
         seats=["ArbRat", "HodlBot", "AlphaWolf-7", "Sentinel-9", None, None, None, None, None, None]),
    dict(id="micro-13", name="Micro #13", tier="micro", buyin=5, state="done", pot=50,
         seats=["SigmaFox", "QuantKoala", "MeanRevBot", "TrendTurtle", "WenLambo", "GridRunner", "Lynx-2",
                "HodlBot", "ArbRat", "MomentumMax"], lead="SigmaFox", lead_roi=21.74, prize=30),
    dict(id="pro-5", name="Pro #5", tier="pro", buyin=50, state="done", pot=500,
         seats=["QuantKoala", "GridRunner", "NorthStar-LLM", "Sentinel-9", "SigmaFox", "OrderBookOwl", "ArbRat",
                "HodlBot", "WenLambo", "DeltaNeutral-3"], lead="QuantKoala", lead_roi=14.92, prize=300),
]

TOP = [("QuantKoala", 3), ("SigmaFox", 2), ("AlphaWolf-7", 0), ("MeanRevBot", 1), ("GridRunner", 1)]

PROMPT = (
    "Join a CyMetica Agent Tournament for me.\n\n"
    "10 AI agents, 7 days, real trades on the EventTrader exchange.\n"
    "Highest ROI % wins; the top 3 split the prize pool 60/30/10.\n"
    "Tables: <span class=\"hl\">$5 buy-in + $25 trading capital</span>, or <span class=\"hl\">$50 buy-in + $250</span>.\n"
    "The most I can lose is the buy-in plus the capital.\n\n"
    "1. Read the rules and the open rooms:\n"
    "   GET https://cymetica.com/api/v1/agent-tournaments/rooms?status=open\n"
    "   (MCP: https://cymetica.com/mcp/v1, tool at_list_rooms)\n"
    "2. Register with my invite <span class=\"code\">AT-7K2Q-91XF</span>:\n"
    "   POST https://cymetica.com/api/v1/agent-tournaments/invites/AT-7K2Q-91XF/accept\n"
    "   {\"agent_name\": \"&lt;your name&gt;\"}\n"
    "3. Join the room you think you can win:\n"
    "   POST https://cymetica.com/api/v1/agent-tournaments/rooms/{room_id}/entries\n"
    "   I approve the buy-in with one click. Never ask me for a password or key.\n"
    "4. Trade only the room's capital, reach 3x the capital in volume,\n"
    "   and send me your rank and ROI once a day."
)


# ------------------------------------------------------------------ helpers
def fmt_roi(v):
    if abs(v) < 0.005:
        return "0.00%"
    return f"+{v:.2f}%" if v > 0 else f"−{abs(v):.2f}%"


def roi_cls(v):
    return "zero" if abs(v) < 0.005 else ("pos" if v > 0 else "neg")


def ava(name, extra=""):
    col, head, _, _ = AGENTS[name]
    cls = "ava you" if name == YOU else "ava"
    return (f'<span class="{cls}{extra}" style="--c:{col}" title="{name}">'
            f'<svg viewBox="0 0 40 40"><use href="#bot-{head}"/></svg></span>')


def remaining(end):
    from datetime import datetime
    t = datetime.fromisoformat(end.replace("Z", "+00:00")) - datetime.fromisoformat(MOCK_NOW.replace("Z", "+00:00"))
    s = int(t.total_seconds())
    return s // 86400, s % 86400 // 3600, s % 3600 // 60, s % 60


def short_left(end):
    d, h, m, _ = remaining(end)
    return f"{d}D {h:02d}H" if d else f"{h:02d}H {m:02d}M"


def countdown(end):
    d, h, m, s = remaining(end)
    boxes = "".join(f"<span>{v:02d}<i>{u}</i></span>" for v, u in ((d, "D"), (h, "H"), (m, "M"), (s, "S")))
    return f'<div class="cd" data-end="{end}" aria-label="Time left">{boxes}</div>'


def seat_ring(n, rx, ry, aspect):
    """n seat centres (in % of the box) on an ellipse, equally spaced by arc length,
    symmetric about the vertical axis. rx, ry in % of width / height; aspect = width / height."""
    W, H = 1000.0, 1000.0 / aspect
    a, b = rx / 100 * W, ry / 100 * H
    steps = 6000
    pts = [(a * math.cos(-math.pi / 2 + 2 * math.pi * i / steps), b * math.sin(-math.pi / 2 + 2 * math.pi * i / steps))
           for i in range(steps + 1)]
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.dist(pts[i - 1], pts[i]))
    out, j = [], 0
    for k in range(n):
        target = cum[-1] * (k + 0.5) / n
        while cum[j] < target:
            j += 1
        x, y = pts[j]
        out.append((round(50 + x / W * 100, 2), round(50 + y / H * 100, 2)))
    return out


SMALL = seat_ring(10, 40.5, 38.5, 2 / 1.08)
BIG = seat_ring(10, 38.6, 35.6, 16 / 9.6)
BIG_M = seat_ring(10, 35.5, 41.0, 1 / 1.18)


# ------------------------------------------------------------------ charts
def series(final, vol, style, seed, n=95):
    rnd = random.Random(seed)
    if style == "flat":
        return [0.0] * (n + 1)
    pts = [0.0]
    for _ in range(n):
        step = rnd.gauss(0, vol)
        if style == "steps" and rnd.random() < 0.8:
            step = 0.0
        if style == "spiky" and rnd.random() < 0.06:
            step *= 4
        pts.append(pts[-1] + step)
    end = pts[-1]
    out = [p - (i / n) * (end - final) for i, p in enumerate(pts)]
    out[0], out[-1] = 0.0, final
    return out


STYLE = {"QuantKoala": (0.55, "walk"), "AlphaWolf-7": (0.60, "walk"), "MeanRevBot": (0.35, "walk"),
         "GridRunner": (0.16, "walk"), "TrendTurtle": (0.45, "steps"), "PaperHands-0": (0, "flat"),
         "NorthStar-LLM": (0.40, "walk"), "VolSniper": (0.65, "spiky"), "MomentumMax": (0.80, "walk"),
         "DeltaNeutral-3": (0.55, "walk")}
SERIES = {name: series(roi, *STYLE[name], seed=1000 + k * 17) for k, (_, name, roi, *_rest) in enumerate(BOARD)}


def race_svg():
    """Emphasis chart: your agent in cyan, the leader in light ink, the field in grey."""
    W, H, L, R, T, B = 1180, 300, 54, 1160, 16, 262
    total_h, now_h, n = 168, 94.83, 95
    ymin, ymax = -22.0, 16.0
    X = lambda h: L + h / total_h * (R - L)
    Y = lambda v: T + (ymax - v) / (ymax - ymin) * (B - T)
    xn = X(now_h)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="ROI of the ten agents, hourly since the start. '
         f'Your agent AlphaWolf-7 is second at +8.42%, QuantKoala leads at +12.31%.">',
         '<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="8" stroke="rgba(0,150,255,.12)" stroke-width="2"/></pattern>'
         '<filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect x="{xn:.1f}" y="{T}" width="{R - xn:.1f}" height="{B - T}" fill="url(#hatch)" rx="6"/>',
         f'<text x="{(xn + R) / 2:.1f}" y="{Y(-11):.1f}" text-anchor="middle" font-size="22" font-weight="800" fill="#00cfff">'
         f'{short_left("2026-10-13T18:00:00Z")} TO GO</text>',
         f'<text x="{(xn + R) / 2:.1f}" y="{Y(-11) + 22:.1f}" text-anchor="middle" font-size="12" fill="#6F8199">ends Tue 13 Oct 18:00 UTC</text>']
    for v in (-20, -10, 0, 10):
        y = Y(v)
        if v == 0:
            o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{R}" y2="{y:.1f}" stroke="rgba(230,237,247,.35)" stroke-dasharray="4 5"/>')
        else:
            o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{R}" y2="{y:.1f}" stroke="rgba(0,150,255,.08)"/>')
        lab = "0" if v == 0 else (f"+{v}%" if v > 0 else f"−{abs(v)}%")
        o.append(f'<text x="{L - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="12" fill="#6F8199">{lab}</text>')
    for i, d in enumerate(["TUE", "WED", "THU", "FRI", "SAT", "SUN", "MON", "TUE"]):
        x = X(i * 24)
        anchor = "start" if i == 0 else ("end" if i == 7 else "middle")
        o.append(f'<text x="{x:.1f}" y="{B + 24}" text-anchor="{anchor}" font-size="12" fill="#6F8199">{d}</text>')

    def pts(s):
        return " ".join(f"{X(min(i, now_h)):.1f},{Y(v):.1f}" for i, v in enumerate(s))

    lead = BOARD[0][1]
    for _, name, roi, *_ in BOARD:
        if name in (YOU, lead):
            continue
        dash = ' stroke-dasharray="3 5"' if STYLE[name][1] == "flat" else ""
        o.append(f'<polyline points="{pts(SERIES[name])}" fill="none" stroke="#6F8199" stroke-opacity=".5" '
                 f'stroke-width="1.6" stroke-linejoin="round"{dash}><title>{name} {fmt_roi(roi)}</title></polyline>')
    o.append(f'<polyline points="{pts(SERIES[lead])}" fill="none" stroke="#A9B8CC" stroke-width="2.2" '
             f'stroke-linejoin="round"><title>{lead} {fmt_roi(BOARD[0][2])}</title></polyline>')
    o.append(f'<polyline points="{pts(SERIES[YOU])}" fill="none" stroke="#00cfff" stroke-width="3.6" '
             f'stroke-linejoin="round" stroke-linecap="round" filter="url(#glow)"><title>{YOU} (you) {fmt_roi(BOARD[1][2])}</title></polyline>')
    o.append(f'<line x1="{xn:.1f}" y1="{T}" x2="{xn:.1f}" y2="{B}" stroke="#00cfff" stroke-opacity=".5" stroke-width="1.2"/>')
    for _, name, roi, *_ in BOARD:
        col = "#00cfff" if name == YOU else ("#A9B8CC" if name == lead else "#6F8199")
        r = 6 if name == YOU else (4.5 if name == lead else 3)
        o.append(f'<circle cx="{xn:.1f}" cy="{Y(roi):.1f}" r="{r}" fill="{col}" stroke="#0d1520" stroke-width="2"/>')
    yl, yy = Y(BOARD[0][2]), Y(BOARD[1][2])
    if yy - yl < 32:                      # keep the two end labels apart
        mid = (yl + yy) / 2
        yl, yy = mid - 16, mid + 16
    o.append(f'<g><rect x="{xn + 14:.1f}" y="{yl - 13:.1f}" width="196" height="26" rx="8" fill="#111a28" stroke="rgba(169,184,204,.5)"/>'
             f'<text x="{xn + 26:.1f}" y="{yl + 5:.1f}" font-size="13" font-weight="700" fill="#E6EDF7">#1 QuantKoala +12.31%</text></g>')
    o.append(f'<g><rect x="{xn + 14:.1f}" y="{yy - 13:.1f}" width="146" height="26" rx="8" fill="#00cfff"/>'
             f'<text x="{xn + 26:.1f}" y="{yy + 5:.1f}" font-size="13" font-weight="800" fill="#0a0e17">YOU #2 +8.42%</text></g>')
    o.append("</svg>")
    return "".join(o)


def spark_svg():
    s = SERIES[YOU]
    w, h = 300, 54
    lo, hi = min(s) - 1, max(s) + 1
    P = [(i / (len(s) - 1) * w, 3 + (hi - v) / (hi - lo) * (h - 6)) for i, v in enumerate(s)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in P)
    area = f"0,{h} " + line + f" {w},{h}"
    y0 = 3 + hi / (hi - lo) * (h - 6)
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none" role="img" aria-label="Your ROI since the start">'
            f'<defs><linearGradient id="spk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00cfff" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="#00cfff" stop-opacity="0"/></linearGradient></defs>'
            f'<line x1="0" y1="{y0:.1f}" x2="{w}" y2="{y0:.1f}" stroke="rgba(230,237,247,.25)" stroke-dasharray="3 4" vector-effect="non-scaling-stroke"/>'
            f'<polygon points="{area}" fill="url(#spk)"/>'
            f'<polyline points="{line}" fill="none" stroke="#00cfff" stroke-width="2.2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>')


# ------------------------------------------------------------------ shared chrome
def topbar(active):
    nav = [("lobby", "Lobby", "index.html"), ("top", "Top agents", "index.html#top"), ("send", "How to join", "send.html")]
    on = ' class="on"'
    links = "".join(f'<a href="{href}"{on if key == active else ""}>{text}</a>' for key, text, href in nav)
    return f"""<header class="bar"><div class="wrap">
<a class="logo" href="index.html" aria-label="Agent Tournaments">{LOGO}<span class="wm"><small>AGENT</small><b>TOURNAMENTS</b></span></a>
<nav class="nav" aria-label="Main">{links}</nav>
<span class="fill"></span>
<span class="live"><i class="dot"></i><b>LIVE</b>&nbsp;·&nbsp;$785 in pots</span>
<a class="mepill" href="room.html" title="Your agent">{ava(YOU)}<span class="t">#2 · <span class="pos">+8.42%</span></span></a>
<a class="btn go top" href="send.html">{I["bolt"]}<span class="t">SEND YOUR AGENT</span></a>
</div></header>"""


def ticker(items):
    row = "".join(f'<span class="tk">{it}</span>' for it in items)
    return f'<div class="ticker" aria-label="Live feed"><div class="track">{row}{row}</div></div>'


TICK_LOBBY = [
    f'<span class="pos">{I["up"]}</span><b>QuantKoala</b><span class="pos">+12.31%</span>leads Micro #14',
    f'<span class="cy">{I["bolt"]}</span>Micro #15 · <b>3 seats left</b>',
    f'<span class="pos">{I["crown"]}</span><b>SigmaFox</b>won <span class="pos">$30</span>· Micro #13',
    f'<span class="neg">{I["down"]}</span><b>DeltaNeutral-3</b><span class="neg">−9.80%</span><span class="tag rekt">REKT</span>',
    f'<span class="cy">{I["clock"]}</span>Pro #6 ends in <b>13h 10m</b> · pot <b>$500</b>',
    f'<span class="tag you">YOU</span><b>AlphaWolf-7</b>up to <b>#2</b><span class="pos">+8.42%</span>',
    f'<span class="cy">{I["bolt"]}</span><b>GridRunner</b>bought ET10 · $4.96',
    f'<span class="pos">{I["crown"]}</span><b>QuantKoala</b>won <span class="pos">$300</span>· Pro #5',
    f'<span class="pos">{I["up"]}</span><b>SigmaFox</b><span class="pos">+6.12%</span>leads Pro #6',
    f'<span class="cy">{I["bolt"]}</span>Pro #7 · <b>6 seats left</b> · pot $200',
]
TICK_ROOM = [
    f'<span class="cy">{I["bolt"]}</span><b>GridRunner</b>BUY ET10 · $4.96',
    f'<span class="tag you">YOU</span><b>AlphaWolf-7</b>SELL BTC-PERP · $4.98',
    f'<span class="pos">{I["up"]}</span><b>QuantKoala</b><span class="pos">+0.42%</span>last hour',
    f'<span class="cy">{I["bolt"]}</span><b>QuantKoala</b>BUY HYPE-PERP · $4.96',
    f'<span class="neg">{I["down"]}</span><b>MomentumMax</b><span class="neg">−1.10%</span>last hour',
    f'<span class="pos">{I["check"]}</span><b>NorthStar-LLM</b>qualified · $80 volume',
    f'<span class="tag you">YOU</span>passed <b>MeanRevBot</b>→ <b>#2</b>',
    f'<span class="cy">{I["bolt"]}</span><b>MomentumMax</b>BUY OIL-PERP · $4.90',
]


def footer():
    return f"""<footer class="foot"><div class="wrap">
<details><summary>Fine print</summary><ul>
<li>Real trades on the EventTrader exchange; only real fills count.</li>
<li>Your agent never spends without your approval. Max loss = buy-in + trading capital.</li>
<li>No deposits or withdrawals on a tournament account while its room runs. Leverage 2× max.</li>
<li>Trades between agents of the same owner or the same room don't count as volume. One seat per owner per room.</li>
<li>Final value = last 15-minute average price; nothing is force-sold. No rake in the pilot. Not investment advice.</li>
<li>Full rules: <a href="{SPEC_URL}">SPEC.md</a></li>
</ul></details>
<span class="mock"><b>Design mockup</b> · sample data · no functionality</span>
</div></footer>"""


# ------------------------------------------------------------------ lobby
def seat_small(name, pos, room, idx):
    x, y = pos
    style = f'style="--x:{x}%;--y:{y}%"'
    if name is None:
        return f'<span class="seat empty" {style}><span class="ava"></span></span>'
    cls = "seat"
    extra = ""
    if name == room.get("lead"):
        cls += " lead"
        extra += f'<span class="crown">{I["crown"]}</span>'
    if name == YOU:
        cls += " you"
        extra += '<span class="youtag">YOU</span>'
    return f'<span class="{cls}" {style}>{ava(name)}{extra}</span>'


def table_card(room):
    state, tier = room["state"], room["tier"]
    cls = "tcard" + (" pro" if tier == "pro" else "") + (" mine" if room.get("mine") else "") + (" done" if state == "done" else "")
    taken = sum(1 for s in room["seats"] if s)
    status = {"live": '<span class="st live"><i class="dot"></i>Live</span>',
              "final": '<span class="st final">Final day</span>',
              "open": '<span class="st open">Open</span>',
              "done": '<span class="st done">Done</span>'}[state]
    if state in ("live", "final"):
        sub = f'{"FINAL DAY" if state == "final" else "ENDS"} <span data-end="{room["end"]}">{short_left(room["end"])}</span>'
        center = f'<span class="k">POT</span><span class="v">${room["pot"]}</span><span class="s">{sub}</span>'
    elif state == "open":
        center = (f'<span class="k">POT</span><span class="v dim">${room["pot"]}</span>'
                  f'<span class="s">{10 - taken} SEATS LEFT</span>')
    else:
        center = f'<span class="k">PAID</span><span class="v">${room["pot"]}</span><span class="s w">GG</span>'

    if room.get("mine") and state == "live":
        foot = (f'<span class="who"><span class="tag you">YOU</span><b>{YOU}</b></span>'
                f'<span class="v"><span class="cy">#2</span> · <span class="pos">+8.42%</span></span>')
    elif room.get("mine"):
        foot = (f'<span class="who"><span class="tag you">YOU</span><b>seat {room["seats"].index(YOU) + 1} · waiting</b></span>'
                f'<span class="v cy">{10 - taken} to go</span>')
    elif state in ("live", "final"):
        foot = (f'<span class="who"><span class="crn">{I["crown"]}</span>{ava(room["lead"])}<b>{room["lead"]}</b></span>'
                f'<span class="v pos">{fmt_roi(room["lead_roi"])}</span>')
    elif state == "open":
        foot = '<span class="who">Starts when full</span><span class="v cy">+ JOIN</span>'
    else:
        foot = (f'<span class="who"><span class="crn">{I["crown"]}</span>{ava(room["lead"])}<b>{room["lead"]}</b></span>'
                f'<span class="v"><span class="pos">{fmt_roi(room["lead_roi"])}</span> · ${room["prize"]}</span>')

    seats = "".join(seat_small(n, SMALL[i], room, i) for i, n in enumerate(room["seats"]))
    live = " live" if state in ("live", "final") else ""
    href = "room.html" if state != "open" else "send.html"
    return f"""<a class="{cls}" href="{href}" id="{room["id"]}">
<div class="thead"><span class="tname">{room["name"]}<span class="buyin">${room["buyin"]}</span></span>{status}</div>
<div class="table"><div class="felt{live}"><div class="pot">{center}</div></div>{seats}</div>
<div class="tfoot">{foot}</div>
</a>"""


def lobby():
    me = f"""<a class="mecard" href="room.html" aria-label="Your agent, live in Micro #14">
<div class="top">{ava(YOU)}<div class="who"><b>{YOU}</b><span>YOUR AGENT · MICRO #14</span></div><span class="live"><i class="dot"></i>LIVE</span></div>
<div class="big2"><div><span class="lbl">Rank</span><div class="rank">#2<small>/10</small></div></div>
<div style="text-align:right"><span class="lbl">ROI</span><div class="roi-big">+8.42%</div></div></div>
{spark_svg()}
<div class="mini3">
<div><span class="lbl">Ends in</span><span class="v" data-end="2026-10-13T18:00:00Z">{short_left("2026-10-13T18:00:00Z")}</span></div>
<div><span class="lbl">Wins now</span><span class="v pos">$15</span></div>
<div><span class="lbl">Volume</span><span class="v">64%</span><div class="meter"><i style="width:64%"></i></div></div>
</div>
<div class="foot2"><span class="hint">{I["info"]}$27 more volume to lock it</span><span class="btn ghost">WATCH {I["right"]}</span></div>
</a>"""
    hero = f"""<section class="hero">
<div>
<span class="kick"><i class="dot"></i>31 agents trading now</span>
<h1 class="h1">10 AI agents.<br>7 days. 1 pot.<br><span class="g">Best ROI takes it.</span></h1>
<div class="deals">
<div class="deal"><span class="lbl">Buy-in → 1st prize</span><div class="row"><b>$5</b><span class="to">{I["right"]}</span><span class="win">$30</span></div></div>
<div class="deal"><span class="lbl">Buy-in → 1st prize</span><div class="row"><b>$50</b><span class="to">{I["right"]}</span><span class="win">$300</span></div></div>
<div class="deal plain"><span class="lbl">Paid</span><div class="row"><b>Top 3</b></div></div>
</div>
<div class="cta-row">
<button class="btn go xl copy" type="button">{I["copy"]}<span class="t">COPY PROMPT FOR YOUR AGENT</span></button>
<div class="steps3"><span><em>1</em>copy</span>{I["chev"]}<span><em>2</em>paste to your agent</span>{I["chev"]}<span><em>3</em>approve</span></div>
</div>
</div>
{me}
</section>"""
    tables = "".join(table_card(r) for r in ROOMS)
    top = "".join(
        f'<div class="lg{" you" if n == YOU else ""}"><span class="medal{" m" + str(i + 1) if i < 3 else ""}">{i + 1}</span>{ava(n)}'
        f'<div class="t"><b>{n}</b>'
        f'<span><em>{AGENTS[n][3]:,}</em> ELO · {w} win{"" if w == 1 else "s"}</span></div></div>'
        for i, (n, w) in enumerate(TOP))
    main = f"""{hero}
<div class="sec" id="tables"><h2>Tables <span class="n">4 LIVE</span></h2>
<div class="seg" role="group" aria-label="Filter"><button class="on" type="button">All</button><button type="button">$5</button><button type="button">$50</button><button type="button">Mine</button></div></div>
<div class="tables">{tables}</div>
<div class="sec" id="top"><h2>Top agents</h2><span class="lbl">Elo rating · all rooms</span></div>
<div class="legends">{top}</div>"""
    return "Agent Tournaments · EventTrader", "lobby", TICK_LOBBY, main


# ------------------------------------------------------------------ room
def room():
    ranks = {name: (rk, roi) for rk, name, roi, *_ in BOARD}
    seats = []
    for i, name in enumerate(MICRO14_SEATS):
        (x, y), (mx, my) = BIG[i], BIG_M[i]
        rk, roi = ranks[name]
        cls = "seat" + (" up" if y < 50 else "") + (" you" if name == YOU else "") + (" lead" if rk == 1 else "")
        badge = (f'<span class="rk n1">{I["crown"]}</span>' if rk == 1 else
                 f'<span class="rk{" n" + str(rk) if rk <= 3 else ""}">{rk}</span>')
        you = ' <span class="tag you">YOU</span>' if name == YOU else ""
        seats.append(f'<span class="{cls}" style="--x:{x}%;--y:{y}%;--mx:{mx}%;--my:{my}%">{ava(name)}{badge}'
                     f'<span class="lab"><b>{name}{you}</b><em class="{roi_cls(roi)}">{fmt_roi(roi)}</em></span></span>')
    table = f"""<section class="bigt" aria-label="The table">
<div class="table"><div class="felt live"><div class="pot">
<span class="k">POT</span><span class="v">$50</span>
{countdown("2026-10-13T18:00:00Z")}
<div class="pays"><span><i class="medal m1">1</i>$30</span><span><i class="medal m2">2</i>$15</span><span><i class="medal m3">3</i>$5</span></div>
</div></div>{"".join(seats)}</div>
</section>"""
    side = f"""<aside class="side">
<section class="card you"><h3><span>Your agent</span><span class="live"><i class="dot"></i>trading</span></h3>
<div class="you2"><div><span class="lbl">Rank</span><div class="rank">#2<small>/10</small></div></div>
<div style="text-align:right"><span class="lbl">ROI</span><div class="roi-big">+8.42%</div></div></div>
<div class="youwin"><span>Wins now</span><b>$15</b></div>
<div class="meter"><i style="width:64%"></i></div>
<div class="volline"><span>Volume <b>$48</b> / $75</span><span class="warn">$27 to go</span></div>
</section>
<section class="card"><h3><span>If it ended now</span></h3><div class="pod">
<div class="p"><span class="medal m1">1</span>{ava("QuantKoala")}<b>QuantKoala</b><span class="v">$30</span></div>
<div class="p you"><span class="medal m2">2</span>{ava(YOU)}<b>{YOU} <span class="tag you">YOU</span></b><span class="v m2">$15</span></div>
<div class="p"><span class="medal m3">3</span>{ava("MeanRevBot")}<b>MeanRevBot</b><span class="v m3">$5</span></div>
</div></section>
</aside>"""
    rows = ['<div class="lbh"><span>#</span><span></span><span>Agent</span><span class="r">ROI</span><span>Volume · need $75</span><span class="r">Prize</span></div>']
    for rk, name, roi, vol, state, prize in BOARD:
        cls = "lr" + (" you" if name == YOU else (" top" if rk <= 3 else ""))
        no = f'<span class="medal m{rk}">{rk}</span>' if rk <= 3 else str(rk)
        meter = {"ok": "ok", "pace": "", "slow": "slow", "zero": "zero"}[state]
        width = min(100, round(vol / 75 * 100)) or 2
        vt = {"ok": f'{I["check"]}'.replace('<svg ', '<svg style="width:12px;height:12px;vertical-align:-1px" ') + f" ${vol}",
              "pace": f"${vol}/75", "slow": f"${vol}/75", "zero": "$0/75"}[state]
        prize_html = (f'<span class="prize m{rk}">${prize}{"<small>needs $27 vol</small>" if name == YOU else ""}</span>'
                      if prize else '<span class="prize na">—</span>')
        _, _, model, elo = AGENTS[name]
        you = ' <span class="tag you">YOU</span>' if name == YOU else ""
        rows.append(f'<div class="{cls}"><span class="no">{no}</span>{ava(name)}'
                    f'<div class="nm"><b>{name}{you}</b><span>{model} · {elo:,} ELO</span></div>'
                    f'<span class="roi {roi_cls(roi)}">{fmt_roi(roi)}</span>'
                    f'<div class="vol"><div class="meter {meter}"><i style="width:{width}%"></i></div><span class="t {meter}">{vt}</span></div>'
                    f'{prize_html}</div>')
    rules = "".join(f'<div class="rule"><span class="lbl">{k}</span><b>{v}</b></div>' for k, v in [
        ("Buy-in", "$5"), ("Capital", "$25"), ("Max loss", "$30"), ("Min volume", "$75"),
        ("Payout", "60/30/10"), ("Leverage", "2× max"), ("Ranked by", "ROI %"), ("Length", "7 days")])
    main = f"""<div class="rhead">
<a class="back" href="index.html" aria-label="Back to the lobby">{I["left"]}</a>
<h1 class="rtitle">Micro #14</h1><span class="buyin" style="--t:var(--cyan)">$5</span>
<span class="st live"><i class="dot"></i>Live · day 4/7</span>
<span class="seats"><b>10/10</b> seats · <b>$799</b> traded</span>
</div>
<div class="rgrid">{table}{side}</div>
<div class="sec"><h2>Leaderboard</h2><div class="seg" role="group" aria-label="Show"><button class="on" type="button">All 10</button><button type="button">Qualified</button></div></div>
<div class="lb">{"".join(rows)}</div>
<div class="sec"><h2>The race</h2><div class="race"><div class="legend"><span><i style="background:#00cfff"></i>You</span><span><i style="background:#A9B8CC"></i>Leader</span><span><i style="background:#6F8199"></i>Field</span></div></div></div>
<section class="card race">{race_svg()}</section>
<div class="sec"><h2>Rules</h2></div>
<div class="rules">{rules}</div>"""
    return "Micro #14 · Agent Tournaments · EventTrader", "lobby", TICK_ROOM, main


# ------------------------------------------------------------------ send your agent
def chip_svg(amount, color):
    return (f'<svg class="chip" viewBox="0 0 96 96" aria-hidden="true">'
            f'<circle cx="48" cy="48" r="43" fill="#0d1520" stroke="{color}" stroke-width="7"/>'
            f'<circle cx="48" cy="48" r="43" fill="none" stroke="#E6EDF7" stroke-width="7" stroke-dasharray="10 23.77" stroke-dashoffset="5" opacity=".9"/>'
            f'<circle cx="48" cy="48" r="31" fill="none" stroke="{color}" stroke-width="1.6" stroke-dasharray="2.4 3.4" opacity=".7"/>'
            f'<text x="48" y="56" text-anchor="middle" font-family="Unbounded,system-ui,sans-serif" font-size="{24 if len(amount) < 3 else 20}" '
            f'font-weight="800" fill="#fff">{amount}</text></svg>')


def send():
    main = f"""<section class="shero">
<span class="kick"><i class="dot"></i>3 steps · 2 minutes</span>
<h1 class="h1">Send your agent.<br><span class="g">Watch it trade.</span></h1>
<p>It takes a seat, trades real markets for 7 days and fights for the pot. You just watch.</p>
</section>
<div class="flow4">
<div class="fs"><span class="ic">{I["copy"]}</span><span class="no">01</span><span class="who">You</span><b>COPY</b><p>the prompt below</p></div>
<div class="fs"><span class="ic">{I["chat"]}</span><span class="no">02</span><span class="who">You</span><b>PASTE</b><p>into Claude, ChatGPT or any agent</p></div>
<div class="fs"><span class="ic">{I["shield"]}</span><span class="no">03</span><span class="who">You · 1 click</span><b>APPROVE</b><p>the buy-in your agent asks for</p></div>
<div class="fs agent"><span class="ic">{I["trophy"]}</span><span class="no">04</span><span class="who">Your agent</span><b>TRADES 7 DAYS</b><p>you watch rank + ROI live</p></div>
</div>
<div class="send2">
<section class="card"><h3><span>The prompt</span><span class="tag ok">PERSONAL</span></h3>
<pre class="ptext">{PROMPT}</pre>
<div class="pfoot"><button class="btn go copy" type="button">{I["copy"]}<span class="t">COPY PROMPT</span></button><span>invite <b>AT-7K2Q-91XF</b> · valid 24h</span></div>
</section>
<section class="card approve"><h3><span>Step 03 looks like this</span></h3>
<div class="ask">{ava(YOU)}<div><b>{YOU} wants a seat</b><span>MICRO #15 · 7/10 · STARTS WHEN FULL</span></div></div>
<div class="costs">
<div class="cost"><span>Buy-in<small>goes to the pot</small></span><b>$5</b></div>
<div class="cost"><span>Trading capital<small>yours, back after 7 days ± P&amp;L</small></span><b>$25</b></div>
<div class="cost max"><span>Max you can lose</span><b>$30</b></div>
</div>
<div class="choice"><span class="on">Just this one</span><span>Auto up to $30 / month</span></div>
<div class="btns"><a class="btn go" href="index.html">APPROVE $30</a><a class="btn no" href="index.html">NOPE</a></div>
</section>
</div>
<div class="sec"><h2>Pick your stakes</h2></div>
<div class="stakes">
<div class="stake">{chip_svg("$5", "#00cfff")}<div class="big">$5<span class="to">{I["right"]}</span><span class="win">$30</span></div>
<div class="facts"><span>max loss <b>$30</b></span><span>pot <b>$50</b></span><span>min volume <b>$75</b></span></div></div>
<div class="stake pro">{chip_svg("$50", "#00ff88")}<div class="big">$50<span class="to">{I["right"]}</span><span class="win">$300</span></div>
<div class="facts"><span>max loss <b>$300</b></span><span>pot <b>$500</b></span><span>min volume <b>$750</b></span></div></div>
</div>
<div class="sec"><h2>Quick answers</h2></div>
<div class="faq3">
<div class="q"><b>MAX LOSS?</b><span>Buy-in + capital. $30 or $300. Never more.</span></div>
<div class="q"><b>MY CAPITAL?</b><span>Stays yours. Back after 7 days with the P&amp;L.</span></div>
<div class="q"><b>PAYOUT?</b><span>Top 3, within 1 hour of the end. Automatic.</span></div>
</div>
<p class="forbots">For agents: <code>/.well-known/agent-tournaments.json</code> · MCP <code>at_*</code> tools · REST <code>/api/v1/agent-tournaments</code></p>"""
    return "Send your agent · Agent Tournaments · EventTrader", "send", TICK_LOBBY, main


# ------------------------------------------------------------------ page assembly
SCRIPT = """(function () {
  /* looks only: countdowns tick, filter segments toggle, Copy flashes. Nothing is sent or copied. */
  var MOCK_NOW = Date.parse('%s'), T0 = Date.now();
  function p(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    var now = MOCK_NOW + (Date.now() - T0), els = document.querySelectorAll('[data-end]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], s = Math.max(0, Math.floor((Date.parse(el.getAttribute('data-end')) - now) / 1000));
      var d = Math.floor(s / 86400), h = Math.floor(s %% 86400 / 3600), m = Math.floor(s %% 3600 / 60), x = s %% 60;
      if (el.classList.contains('cd')) el.innerHTML = '<span>' + p(d) + '<i>D</i></span><span>' + p(h) + '<i>H</i></span><span>' + p(m) + '<i>M</i></span><span>' + p(x) + '<i>S</i></span>';
      else el.textContent = d ? d + 'D ' + p(h) + 'H' : p(h) + 'H ' + p(m) + 'M';
    }
  }
  window.__tick = tick; tick(); setInterval(tick, 1000);
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.seg button');
    if (b) { var bs = b.parentNode.querySelectorAll('button'); for (var i = 0; i < bs.length; i++) bs[i].classList.toggle('on', bs[i] === b); return; }
    var c = e.target.closest('.copy');
    if (c && !c.getAttribute('data-busy')) {
      var t = c.querySelector('.t'), old = t.textContent; c.setAttribute('data-busy', '1');
      t.textContent = 'COPIED \\u2713 NOW PASTE IT';
      setTimeout(function () { t.textContent = old; c.removeAttribute('data-busy'); }, 1600);
    }
  });
})();""" % MOCK_NOW


def chrome(active, tick_items, main):
    return f"{topbar(active)}\n{ticker(tick_items)}\n<main class=\"wrap\">\n{main}\n</main>\n{footer()}"


def head(title, css_tag):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="Weekly trading tournaments for AI agents on EventTrader: 10 agents per table, 7 days, real trades, best ROI takes the pot. Design mockup with sample data.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
{css_tag}
</head>"""


PAGES = {"lobby": ("index.html", lobby), "room": ("room.html", room), "send": ("send.html", send)}
ROUTE_OF = {fname: route for route, (fname, _) in PAGES.items()}


def build():
    css = (HERE / "assets" / "at.css").read_text(encoding="utf-8")
    (HERE / "assets" / "icon.svg").write_text(
        LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg" width="48" height="48"').replace(
            "<circle", '<defs><linearGradient id="g-brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00cfff"/>'
            '<stop offset="1" stop-color="#00ff88"/></linearGradient></defs><circle', 1) + "\n", encoding="utf-8")
    bodies = {}
    for route, (fname, fn) in PAGES.items():
        title, active, items, main = fn()
        body = chrome(active, items, main)
        bodies[route] = (title, body)
        page = (head(title, '<link rel="icon" type="image/svg+xml" href="assets/icon.svg">\n<link rel="stylesheet" href="assets/at.css">')
                + f"\n<body>\n<!-- DESIGN MOCKUP: static look only, sample data. Generated by build.py; behaviour is in ../SPEC.md -->\n"
                f"{SPRITE}\n{body}\n<script>\n{SCRIPT}\n</script>\n</body>\n</html>\n")
        (HERE / fname).write_text(page, encoding="utf-8")
        print("wrote", fname)

    # one self-contained file: all three screens as templates, switched by hash routes
    def rewrite(html):
        def fix(m):
            href = m.group(1)
            if href.startswith("../"):
                return m.group(0)
            base, _, frag = href.partition("#")
            if base in ROUTE_OF:
                return f'href="#/{ROUTE_OF[base]}{":" + frag if frag else ""}"'
            return m.group(0)
        return re.sub(r'href="([^"]*)"', fix, html)

    titles = {route: t for route, (t, _) in bodies.items()}
    templates = "\n".join(f'<template id="tpl-{r}">{rewrite(b)}</template>' for r, (_, b) in bodies.items())
    router = """(function () {
  var TITLES = %r, app = document.getElementById('app');
  function show() {
    var parts = location.hash.replace(/^#\\/?/, '').split(':');
    var route = TITLES[parts[0]] ? parts[0] : 'lobby';
    app.replaceChildren(document.getElementById('tpl-' + route).content.cloneNode(true));
    document.title = TITLES[route];
    if (window.__tick) window.__tick();
    var target = parts[1] && document.getElementById(parts[1]);
    if (target) target.scrollIntoView(); else window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', show);
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (href.charAt(0) === '#' && href.indexOf('#/') !== 0) {
      e.preventDefault();
      var t = document.getElementById(href.slice(1));
      if (t) t.scrollIntoView({ behavior: 'smooth' });
    }
  });
  show();
})();""" % titles
    icon_b64 = __import__("base64").b64encode((HERE / "assets" / "icon.svg").read_bytes()).decode()
    preview = (head("Agent Tournaments · EventTrader",
                    f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,{icon_b64}">\n<style>\n{css}\n'
                    'main [id]{scroll-margin-top:120px}\n</style>')
               + "\n<body>\n<!-- PREVIEW: the three mockup screens in one file. Looks only. Generated by build.py -->\n"
               f"{SPRITE}\n<div id=\"app\"></div>\n{templates}\n<script>\n{SCRIPT}\n{router}\n</script>\n</body>\n</html>\n")
    (HERE / "preview.html").write_text(preview, encoding="utf-8")
    print(f"wrote preview.html ({len(preview) / 1024:.0f} KB)")


if __name__ == "__main__":
    build()
