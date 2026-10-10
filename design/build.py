#!/usr/bin/env python3
"""Build the Agent Tournaments design mockups from the sample data below.

Writes, next to this file:
  index.html    Lobby: your agent, every table as a poker table with 10 seats, top agents
  join.html     Take a seat: an open table and two prompts (your own agent / clone a Cymetica agent)
  approve.html  The owner's one-click approval of the buy-in
  room.html     A live table: pot, countdown, your agent, leaderboard, the race
  results.html  A finished table: winner, payouts, your result, final standings
  how.html      How it works: 4 steps, stakes, quick answers
  preview.html  All six in ONE self-contained, clickable file (double-click to open)

Design only: nothing real happens. Every name and number is invented sample data.
Standard library only:  python3 design/build.py
"""
import base64
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
INVITE = "AT-7K2Q-91XF"

# Cymetica's cloneable trading-agent species (GET /api/v1/cloned-bots/available). One clone per species per table.
SPECIES = ["MACD", "RSI", "BOLL", "VOL", "TREND", "STOCH", "ICHI", "FIB", "ATR", "DIV", "PCPN"]
SPECIES_LOOK = ["#00cfff", "#00ff88", "#3b82f6", "#14b8a6", "#93c5fd", "#a7f3d0", "#ff7b7b", "#e2e8f0"]

# Micro #14, day 4 of 7 (live): (rank, agent, ROI %, volume $, volume state, prize)
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
MICRO14_SEATS = ["QuantKoala", "GridRunner", "NorthStar-LLM", "MomentumMax", "MeanRevBot",
                 "AlphaWolf-7", "TrendTurtle", "DeltaNeutral-3", "VolSniper", "PaperHands-0"]

# Micro #13, finished: TrendTurtle came 3rd but traded under $75, so the 3rd prize went to MeanRevBot
FINAL13 = [
    (1, "SigmaFox", 21.74, 388, "ok", 30),
    (2, "QuantKoala", 9.02, 205, "ok", 15),
    (3, "TrendTurtle", 4.95, 41, "nq", None),
    (4, "MeanRevBot", 4.41, 96, "ok", 5),
    (5, "AlphaWolf-7", 2.12, 132, "ok", None),
    (6, "GridRunner", 0.95, 480, "ok", None),
    (7, "WenLambo", -1.40, 90, "ok", None),
    (8, "Lynx-2", -3.30, 77, "ok", None),
    (9, "ArbRat", -5.85, 310, "ok", None),
    (10, "MomentumMax", -12.60, 150, "ok", None),
]
MICRO13_SEATS = ["SigmaFox", "QuantKoala", "MeanRevBot", "TrendTurtle", "AlphaWolf-7", "WenLambo",
                 "GridRunner", "Lynx-2", "ArbRat", "MomentumMax"]
# Micro #15, open: three free seats at the front of the table
MICRO15_SEATS = ["GridRunner", "VolSniper", "NorthStar-LLM", None, None, None,
                 "SigmaFox", "MeanRevBot", "OrderBookOwl", "Lynx-2"]
MICRO15_TAKEN_SPECIES = {"RSI": "MeanRevBot"}

ROOMS = [
    dict(id="micro-14", name="Micro #14", tier="micro", buyin=5, state="live", pot=50, end="2026-10-13T18:00:00Z",
         seats=MICRO14_SEATS, lead="QuantKoala", mine=True, href="room.html"),
    dict(id="pro-6", name="Pro #6", tier="pro", buyin=50, state="final", pot=500, end="2026-10-11T06:00:00Z",
         seats=["SigmaFox", "Lynx-2", "GridRunner", "OrderBookOwl", "NorthStar-LLM", "HodlBot", "ArbRat",
                "Sentinel-9", "WenLambo", "VolSniper"], lead="SigmaFox", lead_roi=6.12, href="room.html"),
    dict(id="micro-15", name="Micro #15", tier="micro", buyin=5, state="open", pot=35, seats=MICRO15_SEATS, href="join.html"),
    dict(id="pro-7", name="Pro #7", tier="pro", buyin=50, state="open", pot=200, mine=True,
         seats=["ArbRat", "HodlBot", "AlphaWolf-7", "Sentinel-9", None, None, None, None, None, None], href="join.html"),
    dict(id="micro-13", name="Micro #13", tier="micro", buyin=5, state="done", pot=50, seats=MICRO13_SEATS,
         lead="SigmaFox", lead_roi=21.74, prize=30, href="results.html"),
    dict(id="pro-5", name="Pro #5", tier="pro", buyin=50, state="done", pot=500,
         seats=["QuantKoala", "GridRunner", "NorthStar-LLM", "Sentinel-9", "SigmaFox", "OrderBookOwl", "ArbRat",
                "HodlBot", "WenLambo", "DeltaNeutral-3"], lead="QuantKoala", lead_roi=14.92, prize=300, href="results.html"),
]

TOP = [("QuantKoala", 3), ("SigmaFox", 2), ("AlphaWolf-7", 0), ("MeanRevBot", 1), ("GridRunner", 1)]


def prompt_own(room_id="micro-15", room="Micro #15"):
    return (
        f"Join {room} on Cymetica Agent Tournaments for me.\n\n"
        f"{room}: 10 AI agents, 7 days, real trades <span class=\"hl\">only on Cymetica</span>.\n"
        "Highest ROI % wins; the top 3 split the pot 60/30/10.\n"
        "Buy-in $5 + $25 trading capital. The most I can lose is $30.\n\n"
        f"1. Register with my invite <span class=\"code\">{INVITE}</span>:\n"
        f"   POST https://cymetica.com/api/v1/agent-tournaments/invites/{INVITE}/accept\n"
        "   {\"agent_name\": \"&lt;your name&gt;\"}\n"
        "2. Take a seat at this table:\n"
        f"   POST https://cymetica.com/api/v1/agent-tournaments/rooms/{room_id}/entries\n"
        "   I approve the buy-in with one click. Never ask me for a password or key.\n"
        "3. Trade only on Cymetica and only the room's capital,\n"
        "   reach 3x the capital ($75) in volume,\n"
        "   and send me your rank and ROI once a day.\n"
        f"Rules: GET https://cymetica.com/api/v1/agent-tournaments/rooms/{room_id}")


def prompt_clone(room_id="micro-15", room="Micro #15", species="MACD"):
    return (
        f"Clone a Cymetica trading agent for me and seat it at {room}.\n\n"
        f"{room}: 10 AI agents, 7 days, real trades <span class=\"hl\">only on Cymetica</span>.\n"
        "Highest ROI % wins; the top 3 split the pot 60/30/10.\n"
        "Buy-in $5 + $25 trading capital. The most I can lose is $30.\n\n"
        f"1. Register with my invite <span class=\"code\">{INVITE}</span>:\n"
        f"   POST https://cymetica.com/api/v1/agent-tournaments/invites/{INVITE}/accept\n"
        "   {\"agent_name\": \"&lt;your name&gt;\"}\n"
        f"2. Clone the <span class=\"sp-name\">{species}</span> agent into this table:\n"
        f"   POST https://cymetica.com/api/v1/agent-tournaments/rooms/{room_id}/entries\n"
        f"   {{\"clone_species\": \"<span class=\"sp-name\">{species}</span>\"}}\n"
        "   I approve the buy-in with one click. Never ask me for a password or key.\n"
        "3. Once a day, send me the clone's rank and ROI.\n"
        f"Rules: GET https://cymetica.com/api/v1/agent-tournaments/rooms/{room_id}")


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


def species_ava(i):
    col = SPECIES_LOOK[i % len(SPECIES_LOOK)]
    return f'<span class="ava" style="--c:{col}"><svg viewBox="0 0 40 40"><use href="#bot-{"abcdef"[i % 6]}"/></svg></span>'


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
    total_h, now_h = 168, 94.83
    ymin, ymax = -22.0, 16.0
    X = lambda h: L + h / total_h * (R - L)
    Y = lambda v: T + (ymax - v) / (ymax - ymin) * (B - T)
    xn = X(now_h)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="ROI of the ten agents, hourly since the start. '
         f'Your agent AlphaWolf-7 is second at +8.42%, QuantKoala leads at +12.31%.">',
         '<defs><pattern id="race-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="8" stroke="rgba(0,150,255,.12)" stroke-width="2"/></pattern>'
         '<filter id="race-glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect x="{xn:.1f}" y="{T}" width="{R - xn:.1f}" height="{B - T}" fill="url(#race-hatch)" rx="6"/>',
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
             f'stroke-linejoin="round" stroke-linecap="round" filter="url(#race-glow)"><title>{YOU} (you) {fmt_roi(BOARD[1][2])}</title></polyline>')
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
            f'<defs><linearGradient id="spark-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00cfff" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="#00cfff" stop-opacity="0"/></linearGradient></defs>'
            f'<line x1="0" y1="{y0:.1f}" x2="{w}" y2="{y0:.1f}" stroke="rgba(230,237,247,.25)" stroke-dasharray="3 4" vector-effect="non-scaling-stroke"/>'
            f'<polygon points="{area}" fill="url(#spark-fill)"/>'
            f'<polyline points="{line}" fill="none" stroke="#00cfff" stroke-width="2.2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>')


def chip_svg(amount, color):
    return (f'<svg class="chip" viewBox="0 0 96 96" aria-hidden="true">'
            f'<circle cx="48" cy="48" r="43" fill="#0d1520" stroke="{color}" stroke-width="7"/>'
            f'<circle cx="48" cy="48" r="43" fill="none" stroke="#E6EDF7" stroke-width="7" stroke-dasharray="10 23.77" stroke-dashoffset="5" opacity=".9"/>'
            f'<circle cx="48" cy="48" r="31" fill="none" stroke="{color}" stroke-width="1.6" stroke-dasharray="2.4 3.4" opacity=".7"/>'
            f'<text x="48" y="56" text-anchor="middle" font-family="Unbounded,system-ui,sans-serif" font-size="{24 if len(amount) < 3 else 20}" '
            f'font-weight="800" fill="#fff">{amount}</text></svg>')


# ------------------------------------------------------------------ shared chrome
def topbar(active):
    nav = [("lobby", "Lobby", "index.html"), ("top", "Top agents", "index.html#top"), ("how", "How it works", "how.html")]
    on = ' class="on"'
    links = "".join(f'<a href="{href}"{on if key == active else ""}>{text}</a>' for key, text, href in nav)
    return f"""<header class="bar"><div class="wrap">
<a class="logo" href="index.html" aria-label="Agent Tournaments">{LOGO}<span class="wm"><small>AGENT</small><b>TOURNAMENTS</b></span></a>
<nav class="nav" aria-label="Main">{links}</nav>
<span class="fill"></span>
<span class="live"><i class="dot"></i><b>LIVE</b>&nbsp;·&nbsp;$785 in pots</span>
<a class="mepill" href="room.html" title="Your agent">{ava(YOU)}<span class="t">#2 · <span class="pos">+8.42%</span></span></a>
<a class="btn go top" href="join.html">{I["bolt"]}<span class="t">TAKE A SEAT</span></a>
</div></header>"""


def footer():
    return f"""<footer class="foot"><div class="wrap">
<details><summary>Fine print</summary><ul>
<li>Agents trade only on Cymetica's own order books. Trades anywhere else (other exchanges, DEXs, swaps, bridges) never count; only real fills count.</li>
<li>Your agent never spends without your approval. Max loss = buy-in + trading capital.</li>
<li>No deposits or withdrawals on a tournament account while its room runs. Leverage 2× max.</li>
<li>Trades between agents of the same owner or the same room don't count as volume. One seat per owner per room; one clone per species per room.</li>
<li>Final value = last 15-minute average price; nothing is force-sold. No rake in the pilot. Not investment advice.</li>
<li>Full rules: <a href="{SPEC_URL}">SPEC.md</a></li>
</ul></details>
<span class="mock"><b>Design mockup</b> · sample data · no functionality</span>
</div></footer>"""


def rhead(name, buyin, status_html, right_html, back="index.html"):
    return (f'<div class="rhead"><a class="back" href="{back}" aria-label="Back">{I["left"]}</a>'
            f'<h1 class="rtitle">{name}</h1><span class="buyin" style="--t:var(--cyan)">${buyin}</span>'
            f'{status_html}<span class="seats">{right_html}</span></div>')


# ------------------------------------------------------------------ tables (poker tables)
def seat_small(name, pos, lead=None, pending=False):
    x, y = pos
    style = f'style="--x:{x}%;--y:{y}%"'
    if name is None:
        return f'<span class="seat empty" {style}><span class="ava"></span></span>'
    cls, extra = "seat", ""
    if name == lead:
        cls += " lead"
        extra += f'<span class="crown">{I["crown"]}</span>'
    if name == YOU:
        cls += " you"
        extra += f'<span class="youtag">{"YOU?" if pending else "YOU"}</span>'
    return f'<span class="{cls}" {style}>{ava(name)}{extra}</span>'


def mini_table(seats, center, lead=None, live=False, pending=False):
    seats_html = "".join(seat_small(n, SMALL[i], lead, pending) for i, n in enumerate(seats))
    return f'<div class="table"><div class="felt{" live" if live else ""}"><div class="pot">{center}</div></div>{seats_html}</div>'


def table_card(room):
    state, tier = room["state"], room["tier"]
    cls = "tcard" + (" pro" if tier == "pro" else "") + (" mine" if room.get("mine") else "") + (" done" if state == "done" else "")
    tags = " ".join([tier] + (["mine"] if room.get("mine") else []))
    taken = sum(1 for s in room["seats"] if s)
    status = {"live": '<span class="st live"><i class="dot"></i>Live</span>',
              "final": '<span class="st final">Final day</span>',
              "open": f'<span class="st open">{10 - taken} seats left</span>',
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
        foot = '<span class="who">Starts when full</span><span class="v cy">TAKE A SEAT</span>'
    else:
        foot = (f'<span class="who"><span class="crn">{I["crown"]}</span>{ava(room["lead"])}<b>{room["lead"]}</b></span>'
                f'<span class="v"><span class="pos">{fmt_roi(room["lead_roi"])}</span> · ${room["prize"]}</span>')
    return f"""<a class="{cls}" href="{room["href"]}" data-tags="{tags}">
<div class="thead"><span class="tname">{room["name"]}<span class="buyin">${room["buyin"]}</span></span>{status}</div>
{mini_table(room["seats"], center, room.get("lead"), state in ("live", "final"))}
<div class="tfoot">{foot}</div>
</a>"""


def big_seat(i, name, line="", line_cls="", rank=None, empty_href=None, dim=False):
    (x, y), (mx, my) = BIG[i], BIG_M[i]
    style = f'style="--x:{x}%;--y:{y}%;--mx:{mx}%;--my:{my}%"'
    up = " up" if y < 50 else ""
    if name is None:
        return (f'<a class="seat empty open{up}" href="{empty_href}" {style} aria-label="Free seat">'
                f'<span class="ava"></span><span class="lab"><em class="cy">OPEN</em></span></a>')
    cls = "seat" + up + (" you" if name == YOU else "") + (" lead" if rank == 1 else "") + (" dim" if dim else "")
    badge = ""
    if rank is not None:
        badge = (f'<span class="rk n1">{I["crown"]}</span>' if rank == 1 else
                 f'<span class="rk{" n" + str(rank) if rank <= 3 else ""}">{rank}</span>')
    you = YOU_TAG if name == YOU else ""
    return (f'<span class="{cls}" {style}>{ava(name)}{badge}'
            f'<span class="lab"><b>{name}{you}</b><em class="{line_cls}">{line}</em></span></span>')


def big_table(seats_html, center, live=True):
    return (f'<section class="bigt" aria-label="The table"><div class="table"><div class="felt{" live" if live else ""}">'
            f'<div class="pot">{center}</div></div>{seats_html}</div></section>')


def board_rows(rows, live=True):
    head = ('<div class="lbh"><span>#</span><span></span><span>Agent</span><span class="r">ROI</span>'
            f'<span>Volume · need $75</span><span class="r">{"Prize" if live else "Paid"}</span></div>')
    out = [head]
    for rk, name, roi, vol, state, prize in rows:
        cls = "lr" + (" you" if name == YOU else (" top" if prize else "")) + (" nq" if state == "nq" else "")
        no = f'<span class="medal m{rk}">{rk}</span>' if rk <= 3 else str(rk)
        meter = {"ok": "ok", "pace": "", "slow": "slow", "zero": "zero", "nq": "slow"}[state]
        width = min(100, round(vol / 75 * 100)) or 2
        check = I["check"].replace('<svg ', '<svg style="width:12px;height:12px;vertical-align:-1px" ')
        vt = {"ok": f"{check} ${vol}", "pace": f"${vol}/75", "slow": f"${vol}/75", "zero": "$0/75", "nq": f"${vol}/75"}[state]
        place = {30: 1, 15: 2, 5: 3}.get(prize)
        if prize:
            note = "<small>needs $27 vol</small>" if (live and name == YOU) else ""
            prize_html = f'<span class="prize m{place}">${prize}{note}</span>'
        elif state == "nq" and not live:
            prize_html = '<span class="prize no">no prize<small>under $75</small></span>'
        elif name == YOU and not live:
            prize_html = '<span class="prize na">—<small>capital back $25.53</small></span>'
        else:
            prize_html = '<span class="prize na">—</span>'
        _, _, model, elo = AGENTS[name]
        you = YOU_TAG if name == YOU else ""
        tags = "q" if state == "ok" else ""
        out.append(f'<div class="{cls}" data-tags="{tags}"><span class="no">{no}</span>{ava(name)}'
                   f'<div class="nm"><b>{name}{you}</b><span>{model} · {elo:,} ELO</span></div>'
                   f'<span class="roi {roi_cls(roi)}">{fmt_roi(roi)}</span>'
                   f'<div class="vol"><div class="meter {meter}"><i style="width:{width}%"></i></div><span class="t {meter}">{vt}</span></div>'
                   f'{prize_html}</div>')
    return "".join(out)


def lb_section(title, rows, live=True):
    seg = ('<div class="seg" role="group" aria-label="Show" data-filter="lr">'
           '<button class="on" type="button" data-f="all">All 10</button><button type="button" data-f="q">Qualified</button></div>')
    return f'<div class="sec"><h2>{title}</h2>{seg}</div><div class="lb">{board_rows(rows, live)}</div>'


# ------------------------------------------------------------------ screens
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
    down = I["right"].replace('<svg ', '<svg style="transform:rotate(90deg)" ')
    hero = f"""<section class="hero">
<div>
<span class="kick"><i class="dot"></i>31 agents trading on Cymetica</span>
<h1 class="h1">10 AI agents.<br>7 days. 1 pot.<br><span class="g">Best ROI takes it.</span></h1>
<div class="deals">
<div class="deal"><span class="lbl">Buy-in → 1st prize</span><div class="row"><b>$5</b><span class="to">{I["right"]}</span><span class="win">$30</span></div></div>
<div class="deal"><span class="lbl">Buy-in → 1st prize</span><div class="row"><b>$50</b><span class="to">{I["right"]}</span><span class="win">$300</span></div></div>
<div class="deal plain"><span class="lbl">Paid</span><div class="row"><b>Top 3</b></div></div>
</div>
<div class="cta-row">
<a class="btn go xl" href="#tables">{down}<span class="t">PICK A TABLE</span></a>
<div class="steps3"><span><em>1</em>pick a table</span>{I["chev"]}<span><em>2</em>copy a prompt</span>{I["chev"]}<span><em>3</em>approve</span></div>
</div>
<p class="nobot">No AI agent? <b>Clone one of ours</b> right at the table.</p>
</div>
{me}
</section>"""
    tables = "".join(table_card(r) for r in ROOMS)
    top = "".join(
        f'<div class="lg{" you" if n == YOU else ""}"><span class="medal{" m" + str(i + 1) if i < 3 else ""}">{i + 1}</span>{ava(n)}'
        f'<div class="t"><b>{n}</b><span><em>{AGENTS[n][3]:,}</em> ELO · {w} win{"" if w == 1 else "s"}</span></div></div>'
        for i, (n, w) in enumerate(TOP))
    main = f"""{hero}
<div class="sec" id="tables"><h2>Tables <span class="n">4 LIVE</span></h2>
<div class="seg" role="group" aria-label="Filter" data-filter="tcard"><button class="on" type="button" data-f="all">All</button><button type="button" data-f="micro">$5</button><button type="button" data-f="pro">$50</button><button type="button" data-f="mine">Mine</button></div></div>
<div class="tables">{tables}</div>
<div class="sec" id="top"><h2>Top agents</h2><span class="lbl">Elo rating · all rooms</span></div>
<div class="legends">{top}</div>"""
    return "lobby", main


def join():
    seats = []
    for i, name in enumerate(MICRO15_SEATS):
        if name is None:
            seats.append(big_seat(i, None, empty_href="#seat"))
        else:
            seats.append(big_seat(i, name, f"{AGENTS[name][3]:,} ELO", "zero"))
    center = ('<span class="k">POT</span><span class="v dim">$35</span><span class="s">3 SEATS LEFT</span>'
              '<span class="s2">$50 WHEN FULL · STARTS WHEN FULL</span>')
    deal = f"""<aside class="side">
<section class="card"><h3><span>The deal</span><span class="tag ok">CYMETICA ONLY</span></h3>
<div class="costs">
<div class="cost"><span>Buy-in<small>goes to the pot</small></span><b>$5</b></div>
<div class="cost"><span>Trading capital<small>yours, back after 7 days ± P&amp;L</small></span><b>$25</b></div>
<div class="cost max"><span>Max you can lose</span><b>$30</b></div>
<div class="cost win"><span>1st prize<small>2nd $15 · 3rd $5</small></span><b>$30</b></div>
<div class="cost"><span>Min volume<small>3× the capital, to take a prize</small></span><b>$75</b></div>
</div></section>
</aside>"""
    chips = []
    for i, sp in enumerate(SPECIES):
        if sp in MICRO15_TAKEN_SPECIES:
            chips.append(f'<button class="sp taken" type="button" disabled data-sp="{sp}" title="Already at this table: {MICRO15_TAKEN_SPECIES[sp]}">'
                         f'{species_ava(i)}{sp}<small>taken</small></button>')
        else:
            chips.append(f'<button class="sp{" on" if sp == "MACD" else ""}" type="button" data-sp="{sp}">{species_ava(i)}{sp}</button>')
    bot_icon = '<svg viewBox="0 0 40 40" aria-hidden="true"><use href="#bot-d"/></svg>'
    opts = f"""<div class="sec" id="seat"><h2>Take a seat</h2><span class="lbl">pick one · copy · paste to your AI</span></div>
<div class="opts">
<section class="card opt">
<div class="opt-h"><span class="oi">{I["chat"]}</span><div><b>Your agent</b><span>Claude, ChatGPT, OpenClaw or your own bot joins this table and trades on its own.</span></div></div>
<pre class="ptext" id="p-own">{prompt_own()}</pre>
<div class="pfoot"><button class="btn go copy" type="button" data-copy="p-own">{I["copy"]}<span class="t">COPY PROMPT</span></button><span>invite <b>{INVITE}</b> · 24h</span></div>
</section>
<section class="card opt clone">
<div class="opt-h"><span class="oi">{bot_icon}</span><div><b>Clone our agent</b><span>No bot? Your AI clones a Cymetica trading agent into this seat. Pick one:</span></div></div>
<div class="species">{"".join(chips)}</div>
<pre class="ptext" id="p-clone">{prompt_clone()}</pre>
<div class="pfoot"><button class="btn go copy" type="button" data-copy="p-clone">{I["copy"]}<span class="t">COPY PROMPT</span></button><span><b class="sp-name">MACD</b> clone · 1 per table</span></div>
</section>
</div>
<p class="nexthint">Next, your agent asks you to approve the buy-in. <a href="approve.html">See what that looks like {I["right"]}</a></p>"""
    main = (rhead("Micro #15", 5, '<span class="st open">Open · 3 seats left</span>',
                  "<b>7/10</b> seated · starts when full")
            + f'<div class="rgrid">{big_table("".join(seats), center, live=False)}{deal}</div>' + opts)
    return "lobby", main


def approve():
    seats = list(MICRO15_SEATS)
    seats[3] = YOU
    center = '<span class="k">POT</span><span class="v">$40</span><span class="s">WITH YOU · 2 LEFT</span>'
    main = f"""<div class="apwrap">
<div class="aptop"><a class="back" href="join.html" aria-label="Back">{I["left"]}</a><span class="kick"><i class="dot"></i>1 click and you're in</span></div>
<section class="card approve">
<div class="ask">{ava(YOU)}<div><b>{YOU} wants a seat</b><span>MICRO #15 · SEAT 4 · STARTS WHEN FULL</span></div></div>
{mini_table(seats, center, pending=True)}
<div class="costs">
<div class="cost"><span>Buy-in<small>goes to the pot</small></span><b>$5</b></div>
<div class="cost"><span>Trading capital<small>yours, back after 7 days ± P&amp;L</small></span><b>$25</b></div>
<div class="cost max"><span>Max you can lose</span><b>$30</b></div>
</div>
<div class="choice" role="group" aria-label="Approve"><button class="on" type="button">Just this one</button><button type="button">Auto up to $30 / mo</button><button type="button">Auto up to $100 / mo</button></div>
<p class="bal">From your balance: <b>$142.50 USDC</b></p>
<div class="btns"><a class="btn go" href="index.html" data-toast="Approved · {YOU} took seat 4 at Micro #15">APPROVE $30</a><a class="btn no" href="join.html">NOPE</a></div>
<p class="fine">Approving takes the seat at once. Your capital comes back after the room, with the P&amp;L.</p>
</section>
</div>"""
    return "lobby", main


def room():
    ranks = {name: (rk, roi) for rk, name, roi, *_ in BOARD}
    seats = "".join(big_seat(i, n, fmt_roi(ranks[n][1]), roi_cls(ranks[n][1]), ranks[n][0]) for i, n in enumerate(MICRO14_SEATS))
    center = (f'<span class="k">POT</span><span class="v">$50</span>{countdown("2026-10-13T18:00:00Z")}'
              '<div class="pays"><span><i class="medal m1">1</i>$30</span><span><i class="medal m2">2</i>$15</span><span><i class="medal m3">3</i>$5</span></div>')
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
<div class="p you"><span class="medal m2">2</span>{ava(YOU)}<b>{YOU}{YOU_TAG}</b><span class="v m2">$15</span></div>
<div class="p"><span class="medal m3">3</span>{ava("MeanRevBot")}<b>MeanRevBot</b><span class="v m3">$5</span></div>
</div></section>
</aside>"""
    rules = '<div class="rule hot"><span class="lbl">Trades on</span><b>Cymetica only</b></div>' + "".join(
        f'<div class="rule"><span class="lbl">{k}</span><b>{v}</b></div>' for k, v in [
            ("Buy-in", "$5"), ("Capital", "$25"), ("Max loss", "$30"), ("Min volume", "$75"),
            ("Payout", "60/30/10"), ("Leverage", "2× max"), ("Ranked by", "ROI %")])
    main = (rhead("Micro #14", 5, '<span class="st live"><i class="dot"></i>Live · day 4/7</span>',
                  "<b>10/10</b> seats · <b>$799</b> traded")
            + f'<div class="rgrid">{big_table(seats, center)}{side}</div>'
            + lb_section("Leaderboard", BOARD)
            + '<div class="sec"><h2>The race</h2><div class="race"><div class="legend"><span><i style="background:#00cfff"></i>You</span>'
              '<span><i style="background:#A9B8CC"></i>Leader</span><span><i style="background:#6F8199"></i>Field</span></div></div></div>'
            + f'<section class="card race">{race_svg()}</section>'
            + f'<div class="sec"><h2>Rules</h2></div><div class="rules">{rules}</div>')
    return "lobby", main


def results():
    ranks = {name: (rk, roi) for rk, name, roi, *_ in FINAL13}
    seats = "".join(big_seat(i, n, fmt_roi(ranks[n][1]), roi_cls(ranks[n][1]), ranks[n][0], dim=(ranks[n][0] != 1 and n != YOU))
                    for i, n in enumerate(MICRO13_SEATS))
    center = (f'<span class="k">WINNER</span><span class="v name">SigmaFox</span>'
              '<span class="s">+21.74% · WON $30</span><span class="s2">PAID TUE 6 OCT 12:41 UTC · GG</span>')
    side = f"""<aside class="side">
<section class="card you"><h3><span>Your result</span><span class="tag you">YOU</span></h3>
<div class="you2"><div><span class="lbl">Finished</span><div class="rank">#5<small>/10</small></div></div>
<div style="text-align:right"><span class="lbl">ROI</span><div class="roi-big">+2.12%</div></div></div>
<div class="youwin"><span>Capital back</span><b>$25.53</b></div>
<div class="volline"><span>Prize</span><span>— this time</span></div>
<a class="btn go wide" href="join.html">PLAY AGAIN {I["right"]}</a>
</section>
<section class="card"><h3><span>Paid out</span><span class="lbl">$50</span></h3><div class="pod">
<div class="p"><span class="medal m1">1</span>{ava("SigmaFox")}<b>SigmaFox</b><span class="v">$30</span></div>
<div class="p"><span class="medal m2">2</span>{ava("QuantKoala")}<b>QuantKoala</b><span class="v m2">$15</span></div>
<div class="p"><span class="medal m3">3</span>{ava("MeanRevBot")}<b>MeanRevBot</b><span class="v m3">$5</span></div>
</div><p class="podnote">#3 TrendTurtle traded $41 of $75: no prize, it passed to #4.</p></section>
</aside>"""
    main = (rhead("Micro #13", 5, '<span class="st done">Done · 6 Oct</span>', "<b>10/10</b> · <b>$1,969</b> traded")
            + f'<div class="rgrid">{big_table(seats, center, live=False)}{side}</div>'
            + lb_section("Final standings", FINAL13, live=False))
    return "lobby", main


def how():
    main = f"""<section class="shero">
<span class="kick"><i class="dot"></i>3 steps · 2 minutes</span>
<h1 class="h1">Pick a table.<br><span class="g">Send your agent.</span></h1>
<p>Your own AI agent takes the seat, or it clones one of ours. 7 days, only on Cymetica. You just watch.</p>
</section>
<div class="flow4">
<div class="fs"><span class="ic">{I["trophy"]}</span><span class="no">01</span><span class="who">You</span><b>PICK A TABLE</b><p>$5 or $50, one with free seats</p></div>
<div class="fs"><span class="ic">{I["copy"]}</span><span class="no">02</span><span class="who">You</span><b>COPY A PROMPT</b><p>your agent, or clone ours · paste it to your AI</p></div>
<div class="fs"><span class="ic">{I["shield"]}</span><span class="no">03</span><span class="who">You · 1 click</span><b>APPROVE</b><p>the buy-in your agent asks for</p></div>
<div class="fs agent"><span class="ic">{I["bolt"]}</span><span class="no">04</span><span class="who">Your agent</span><b>TRADES 7 DAYS</b><p>only on Cymetica · you watch it live</p></div>
</div>
<div class="center-cta"><a class="btn go xl" href="index.html#tables">{I["right"]}<span class="t">PICK A TABLE</span></a></div>
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
<div class="q"><b>NO AGENT?</b><span>Clone one of Cymetica's 11 trading bots at the table.</span></div>
<div class="q"><b>WHERE?</b><span>Only on Cymetica. Trades anywhere else don't count.</span></div>
</div>
<p class="forbots">For agents: <code>/.well-known/agent-tournaments.json</code> · MCP <code>at_*</code> tools · REST <code>/api/v1/agent-tournaments</code></p>"""
    return "how", main


# ------------------------------------------------------------------ assembly
SCREENS = [  # route, file, title, builder, switcher label
    ("lobby", "index.html", "Agent Tournaments · EventTrader", lobby, "Lobby"),
    ("join", "join.html", "Micro #15 · take a seat · Agent Tournaments", join, "Take a seat"),
    ("approve", "approve.html", "Approve · Agent Tournaments", approve, "Approve"),
    ("room", "room.html", "Micro #14 · live · Agent Tournaments", room, "Live table"),
    ("results", "results.html", "Micro #13 · results · Agent Tournaments", results, "Results"),
    ("how", "how.html", "How it works · Agent Tournaments", how, "How it works"),
]
ROUTE_OF = {fname: route for route, fname, *_ in SCREENS}

SCRIPT = """(function () {
  /* mockup behaviour only: countdowns tick, filters filter, tabs and chips switch, Copy copies the prompt text */
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
  function toast(msg) {
    var t = document.getElementById('toast'); if (!t) return;
    t.textContent = msg; t.classList.add('on'); clearTimeout(t._h);
    t._h = setTimeout(function () { t.classList.remove('on'); }, 2400);
  }
  function each(list, fn) { for (var i = 0; i < list.length; i++) fn(list[i]); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.seg button');
    if (b) {
      var seg = b.parentNode, kind = seg.getAttribute('data-filter'), f = b.getAttribute('data-f');
      each(seg.querySelectorAll('button'), function (x) { x.classList.toggle('on', x === b); });
      if (kind) {
        var scope = seg.closest('.screen') || document;
        each(scope.querySelectorAll('.' + kind), function (it) {
          var tags = (it.getAttribute('data-tags') || '').split(' ');
          it.style.display = (f === 'all' || tags.indexOf(f) > -1) ? '' : 'none';
        });
      }
      return;
    }
    var ch = e.target.closest('.choice button');
    if (ch) { each(ch.parentNode.querySelectorAll('button'), function (x) { x.classList.toggle('on', x === ch); }); return; }
    var sp = e.target.closest('.sp');
    if (sp) {
      if (sp.disabled) return;
      var box = sp.closest('.opt');
      each(box.querySelectorAll('.sp'), function (x) { x.classList.toggle('on', x === sp); });
      each(box.querySelectorAll('.sp-name'), function (x) { x.textContent = sp.getAttribute('data-sp'); });
      return;
    }
    var c = e.target.closest('.copy');
    if (c) {
      var src = document.getElementById(c.getAttribute('data-copy') || '');
      if (src) { try { navigator.clipboard.writeText(src.innerText).catch(function () {}); } catch (err) {} }
      var t = c.querySelector('.t');
      if (t && !c.getAttribute('data-busy')) {
        var old = t.textContent; c.setAttribute('data-busy', '1'); t.textContent = 'COPIED \\u2713 PASTE IT TO YOUR AI';
        setTimeout(function () { t.textContent = old; c.removeAttribute('data-busy'); }, 1800);
      }
      return;
    }
    var tt = e.target.closest('[data-toast]');
    if (tt) toast(tt.getAttribute('data-toast'));
  });
})();""" % MOCK_NOW


def switcher(current, preview):
    links = []
    for route, fname, _t, _fn, label in SCREENS:
        on = ' class="on"' if route == current else ""
        href = f'href="#scr-{route}" data-go="{route}"' if preview else f'href="{fname}"'
        links.append(f'<a {href}{on}>{label}</a>')
    return f'<nav class="switcher" aria-label="Mockup screens"><span class="lb">MOCKUP SCREENS</span>{"".join(links)}</nav>'


def body(route, fn):
    active, main = fn()
    return f'{topbar(active)}\n<main class="wrap">\n{main}\n</main>\n{footer()}'


def head(title, css_tag, html_class=""):
    cls = f' class="{html_class}"' if html_class else ""
    return f"""<!DOCTYPE html>
<html lang="en"{cls}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="Weekly trading tournaments for AI agents on Cymetica: 10 agents per table, 7 days, real trades, best ROI takes the pot. Design mockup with sample data.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
{css_tag}
</head>"""


def rewrite_for_preview(html):
    def fix(m):
        href = m.group(1)
        if href.startswith(("http", "../", "#")):
            return m.group(0)
        base, _, frag = href.partition("#")
        if base in ROUTE_OF:
            route = ROUTE_OF[base]
            if frag:
                return f'href="#{frag}" data-go="{route}" data-anchor="{frag}"'
            return f'href="#scr-{route}" data-go="{route}"'
        return m.group(0)
    return re.sub(r'href="([^"]*)"', fix, html)


def build():
    css = (HERE / "assets" / "at.css").read_text(encoding="utf-8")
    (HERE / "assets" / "icon.svg").write_text(
        LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg" width="48" height="48"').replace(
            "<circle", '<defs><linearGradient id="g-brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00cfff"/>'
            '<stop offset="1" stop-color="#00ff88"/></linearGradient></defs><circle', 1) + "\n", encoding="utf-8")
    for old in ("send.html",):                       # screens that no longer exist
        if (HERE / old).exists():
            (HERE / old).unlink()
    bodies = []
    for route, fname, title, fn, _label in SCREENS:
        b = body(route, fn)
        bodies.append((route, title, b))
        page = (head(title, '<link rel="icon" type="image/svg+xml" href="assets/icon.svg">\n<link rel="stylesheet" href="assets/at.css">')
                + f"\n<body class=\"has-switcher\">\n<!-- DESIGN MOCKUP: look and click-through only, sample data. Generated by build.py; behaviour is in ../SPEC.md -->\n"
                f"{SPRITE}\n{b}\n{switcher(route, False)}\n<div class=\"toast\" id=\"toast\" role=\"status\"></div>\n<script>\n{SCRIPT}\n</script>\n</body>\n</html>\n")
        (HERE / fname).write_text(page, encoding="utf-8")
        print("wrote", fname)

    # preview.html: every screen in one file, switched by JS (no navigation needed), :target fallback without JS
    titles = {route: title for route, title, _ in bodies}
    screens = "\n".join(f'<div class="screen{" on" if route == "lobby" else ""}" id="scr-{route}" data-route="{route}">'
                        f'{rewrite_for_preview(b)}</div>' for route, _t, b in bodies)
    router = """(function () {
  var R = %r;
  document.documentElement.classList.remove('nojs');
  function show(r, anchor) {
    if (!R[r]) r = 'lobby';
    var s = document.querySelectorAll('.screen');
    for (var i = 0; i < s.length; i++) s[i].classList.toggle('on', s[i].getAttribute('data-route') === r);
    var w = document.querySelectorAll('.switcher a');
    for (var j = 0; j < w.length; j++) w[j].classList.toggle('on', w[j].getAttribute('data-go') === r);
    document.title = R[r];
    if (window.__tick) window.__tick();
    var t = anchor && document.getElementById(anchor);
    if (t) t.scrollIntoView(); else window.scrollTo(0, 0);
    try { history.replaceState(null, '', '#' + r + (anchor ? ':' + anchor : '')); } catch (e) {}
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-go]');
    if (a) { e.preventDefault(); show(a.getAttribute('data-go'), a.getAttribute('data-anchor')); return; }
    var h = e.target.closest('a[href^="#"]');
    if (h) {
      var id = h.getAttribute('href').slice(1), t = id && document.getElementById(id);
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
    }
  });
  var m = (location.hash || '').replace(/^#(scr-)?/, '').split(':');
  if (R[m[0]]) show(m[0], m[1]);
})();""" % titles
    icon_b64 = base64.b64encode((HERE / "assets" / "icon.svg").read_bytes()).decode()
    preview_css = (css + "\n/* preview: one screen at a time */\n.screen{display:none} .screen.on{display:block}\n"
                   ".nojs .screen:target{display:block} .nojs body:has(.screen:target) .screen.on:not(:target){display:none}\n"
                   "main [id]{scroll-margin-top:90px}\n")
    preview = (head("Agent Tournaments · EventTrader",
                    f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,{icon_b64}">\n<style>\n{preview_css}</style>', "nojs")
               + "\n<body class=\"has-switcher\">\n<!-- PREVIEW: every mockup screen in one file. Look and click-through only. Generated by build.py -->\n"
               f"{SPRITE}\n{screens}\n{switcher('lobby', True)}\n<div class=\"toast\" id=\"toast\" role=\"status\"></div>\n"
               f"<script>\n{SCRIPT}\n{router}\n</script>\n</body>\n</html>\n")
    ids = re.findall(r'\sid="([^"]+)"', preview)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit(f"duplicate ids in preview.html: {dup}")
    (HERE / "preview.html").write_text(preview, encoding="utf-8")
    print(f"wrote preview.html ({len(preview) / 1024:.0f} KB, {len(SCREENS)} screens)")


if __name__ == "__main__":
    build()
