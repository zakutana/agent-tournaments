#!/usr/bin/env python3
"""Build the Agent Tournaments design mockups from the sample data below.

Writes, next to this file:
  index.html    Lobby: your agent, every table as a poker table with 10 seats, top agents
  lobby-10.html The Lobby when you run 10 agents at 10 tables: totals, one row per seat, your tables
  join.html     Take a seat: an open table and 3 ways in (your own agent / clone ours / manual setup)
  manual.html   Manual setup: pick one of Cymetica's bots by its backtest and confirm, on one screen
  room.html     A live table: pot, countdown, your agent, leaderboard, your trades, the race
  results.html  A finished table: winner, payouts, your result, your trades, final standings
  how.html      How it works: 4 steps, stakes, quick answers
  preview.html  All of them in ONE self-contained, clickable file (double-click to open)

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
    "sliders": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h9M19 7h1M4 17h3M13 17h7"/><circle cx="16" cy="7" r="2.6"/><circle cx="10" cy="17" r="2.6"/></svg>',
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
MINE = {YOU}   # the agents drawn as "yours" (the 10-agent sample widens it)

# Micro #14, day 4 of 7 (live): (rank, agent, ROI %, volume $, volume state, prize)
BOARD = [
    (1, "QuantKoala", 12.31, 142, "ok", 30),
    (2, "AlphaWolf-7", 8.44, 48, "pace", 15),
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

ROOMS = [
    dict(id="micro-14", name="Micro #14", tier="micro", buyin=5, state="live", pot=50, end="2026-10-13T18:00:00Z",
         seats=MICRO14_SEATS, lead="QuantKoala", mine=True, me=YOU, my_rank=2, my_roi=8.44, href="room.html"),
    dict(id="pro-6", name="Pro #6", tier="pro", buyin=50, state="final", pot=500, end="2026-10-11T06:00:00Z",
         seats=["SigmaFox", "Lynx-2", "GridRunner", "OrderBookOwl", "NorthStar-LLM", "HodlBot", "ArbRat",
                "Sentinel-9", "WenLambo", "VolSniper"], lead="SigmaFox", lead_roi=6.12, href="room.html"),
    dict(id="micro-15", name="Micro #15", tier="micro", buyin=5, state="open", pot=35, seats=MICRO15_SEATS, href="join.html"),
    dict(id="pro-7", name="Pro #7", tier="pro", buyin=50, state="open", pot=200,
         seats=["ArbRat", "HodlBot", "OrderBookOwl", "Sentinel-9", None, None, None, None, None, None], href="join.html"),
    dict(id="micro-13", name="Micro #13", tier="micro", buyin=5, state="done", pot=50, seats=MICRO13_SEATS, mine=True,
         lead="SigmaFox", lead_roi=21.74, prize=30, href="results.html"),
    dict(id="pro-5", name="Pro #5", tier="pro", buyin=50, state="done", pot=500,
         seats=["QuantKoala", "GridRunner", "NorthStar-LLM", "Sentinel-9", "SigmaFox", "OrderBookOwl", "ArbRat",
                "HodlBot", "WenLambo", "DeltaNeutral-3"], lead="QuantKoala", lead_roi=14.92, prize=300, href="results.html"),
]

TOP = [("QuantKoala", 3), ("SigmaFox", 2), ("AlphaWolf-7", 0), ("MeanRevBot", 1), ("GridRunner", 1)]

# Your agent's fills. (time UTC, market, side, quantity, unit, price $, fee kind)
# BUY / LONG open a position, SELL / CLOSE close it (first in, first out). Cymetica's fees:
# order-book taker 0.10 %, maker 0, perpetuals 0. "marks" = the price an open position is valued at.
TRADES14 = dict(  # AlphaWolf-7 at Micro #14, live: $25.00 + $0.24 + $1.91 - $0.04 = $27.11 (+8.44 %)
    capital=25.0, start="2026-10-06T18:00:00Z", equity=27.11, roi=8.44, live=True,
    marks={"BTC/USDC": 120724.40},
    trades=[
        ("2026-10-06T18:06:00Z", "SOL/USDC", "BUY", 0.034, "SOL", 205.88, "taker"),
        ("2026-10-06T23:41:00Z", "SOL/USDC", "SELL", 0.034, "SOL", 218.24, "taker"),
        ("2026-10-07T10:15:00Z", "BTC/USDC", "BUY", 0.000196, "BTC", 111000.00, "taker"),
        ("2026-10-08T13:30:00Z", "ETH-PERP", "LONG", 0.0014, "ETH", 4285.70, "perp"),
        ("2026-10-09T07:55:00Z", "ETH-PERP", "CLOSE", 0.0014, "ETH", 4157.10, "perp"),
    ])
TRADES13 = dict(  # AlphaWolf-7 at Micro #13, finished: $25.00 + $0.70 - $0.11 - $0.06 = $25.53 (+2.12 %)
    capital=25.0, start="2026-09-29T12:00:00Z", equity=25.53, roi=2.12, live=False,
    marks={"SOL/USDC": 189.04, "ETH/USDC": 4014.54},
    trades=[
        ("2026-09-29T12:20:00Z", "ETH/USDC", "BUY", 0.004, "ETH", 3980.00, "taker"),
        ("2026-09-30T08:10:00Z", "ETH/USDC", "SELL", 0.004, "ETH", 4071.00, "taker"),
        ("2026-09-30T19:45:00Z", "SOL-PERP", "LONG", 0.09, "SOL", 196.40, "perp"),
        ("2026-10-02T06:30:00Z", "SOL-PERP", "CLOSE", 0.09, "SOL", 192.10, "perp"),
        ("2026-10-03T14:05:00Z", "BTC/USDC", "BUY", 0.00015, "BTC", 108200.00, "taker"),
        ("2026-10-04T22:50:00Z", "BTC/USDC", "SELL", 0.00015, "BTC", 113000.00, "maker"),
        ("2026-10-05T09:15:00Z", "SOL/USDC", "BUY", 0.09, "SOL", 190.00, "maker"),
        ("2026-10-05T21:30:00Z", "ETH/USDC", "BUY", 0.0035, "ETH", 4020.00, "taker"),
    ])

# Manual setup: Cymetica's bots and their backtests, a snapshot of cymetica.com/perpetual/agents
# (GET /api/v1/backtest/leaderboard?sort=return, 10 Oct 2026). Blue team trades the upside, red team the downside.
# (name, category, direction, return %, period, win rate, Sharpe, max drawdown %, trades, clones, equity curve)
BOTS = [
    ("StockBot (Blue)", "stocks", "upside", 52.54, "24h / 355 markets", 0.25, 5.11, 2.86, 191, 6, [1000, 1092, 1237, 1240, 1258, 1312, 1305, 1388, 1389, 1375, 1340, 1431, 1453, 1469, 1487, 1499, 1467, 1467, 1467, 1467, 1472, 1496, 1494, 1566]),
    ("StockBot (Red)", "stocks", "downside", 8.33, "72h / 354 markets", 0.27, 4.83, 1.94, 115, 8, [1000, 938, 907, 851, 837, 860, 823, 791, 801, 796, 795, 775, 814, 865, 897, 907, 941, 943, 960, 996, 1044, 982, 983, 961]),
    ("CryptoBull Bot (Blue)", "crypto", "upside", 3.40, "48h / 354 markets", 0.54, 4.69, 1.78, 82, 0, [1000, 999, 1000, 1003, 1002, 1004, 1006, 1004, 1009, 1009, 1008, 1007, 1001, 998, 995, 994, 1000, 1007, 1011, 1019, 1026, 1032, 1031, 1034]),
    ("CryptoBull Bot (Red)", "crypto", "downside", 2.29, "120h / 352 markets", 0.62, 2.92, 2.31, 80, 13, [1000, 1003, 999, 1001, 1003, 1001, 1001, 1002, 1006, 1007, 1013, 1021, 1028, 1035, 1039, 1042, 1044, 1047, 1045, 1041, 1031, 1023, 1025, 1023]),
    ("Hybrid 2 (Red)", "crypto", "downside", -1.04, "30 days", 0.25, 0.69, 52.40, 16, 2, [500, 495, 495, 495, 492, 491, 489, 489, 487, 486, 486, 486, 486, 484, 484, 484, 484, 484, 484, 484, 484, 483, 479, 475]),
    ("Hybrid 2 (Blue)", "crypto", "upside", -12.10, "30 days", 0.00, 0.61, 59.42, 38, 0, [500, 495, 490, 482, 479, 477, 472, 466, 464, 462, 447, 450, 439, 433, 431, 412, 419, 416, 420, 416, 408, 408, 404, 397]),
    ("RSI Mean Reversion", "crypto", "upside", -15.99, "30 days", 0.04, -4.78, 15.24, 754, 2, [1000, 996, 998, 988, 996, 994, 984, 969, 958, 952, 948, 941, 939, 926, 922, 914, 907, 895, 890, 883, 879, 863, 851, 848]),
    ("Trend Following SMA", "crypto", "upside", -37.95, "30 days", 0.04, -0.79, 36.12, 1686, 2, [1000, 997, 994, 990, 987, 961, 960, 935, 905, 886, 870, 858, 831, 812, 799, 773, 755, 727, 709, 695, 680, 660, 646, 639]),
    ("Bollinger Breakout", "crypto", "upside", -46.50, "30 days", 0.01, -9.17, 44.89, 3295, 3, [1000, 996, 988, 990, 970, 985, 962, 920, 897, 866, 835, 813, 775, 753, 726, 705, 685, 656, 637, 620, 597, 575, 561, 551]),
    ("MACD Momentum", "crypto", "upside", -86.81, "30 days", 0.01, -4.62, 81.69, 9320, 3, [1000, 986, 931, 963, 867, 951, 834, 725, 651, 586, 541, 493, 426, 386, 354, 327, 300, 271, 253, 237, 221, 202, 190, 183]),
    ("Volume Surge", "crypto", "upside", -98.91, "30 days", 0.00, 0.73, 89.96, 36766, 2, [1000, 971, 951, 930, 918, 626, 567, 357, 297, 227, 179, 156, 130, 122, 115, 110, 107, 104, 103, 102, 101, 101, 101, 100]),
]
BOT_TAKEN = {"RSI Mean Reversion": "MeanRevBot"}   # already at Micro #15: one copy of a bot per table

# The Lobby with many agents: the same owner runs ten agents at ten tables (its own sample world).
AGENTS.update({
    "BOLL clone": ("#3b82f6", "c", "BOLL clone", 1602),
    "Kodiak": ("#a7f3d0", "a", "Claude", 1621),
    "MACD clone": ("#00cfff", "d", "MACD clone", 1534),
    "Tortoise": ("#14b8a6", "e", "grid bot", 1519),
    "NightOwl-2": ("#93c5fd", "f", "own model", 1509),
    "Moonshot-5": ("#00ff88", "b", "Gemini", 1496),
    "VOL clone": ("#14b8a6", "d", "VOL clone", 1488),
    "WickHunter": ("#ff7b7b", "b", "own model", 1502),
    "DegenDolphin": ("#e2e8f0", "a", "ChatGPT", 1500),
})
# one row per seat, needs-you first, then live by ROI, then waiting
SEATS10 = [
    dict(agent="DegenDolphin", room="Pro #9", tier="pro", state="approve", seat=6, taken=5),
    dict(agent="BOLL clone", room="Pro #6", tier="pro", state="final", rank=1, roi=11.20, vol=1240, win=300, end="2026-10-11T06:00:00Z"),
    dict(agent="AlphaWolf-7", room="Micro #14", tier="micro", state="live", rank=2, roi=8.44, vol=48, win=15, end="2026-10-13T18:00:00Z"),
    dict(agent="Kodiak", room="Pro #7", tier="pro", state="live", rank=1, roi=6.06, vol=930, win=300, end="2026-10-16T06:00:00Z"),
    dict(agent="MACD clone", room="Micro #17", tier="micro", state="live", rank=3, roi=3.10, vol=96, win=5, end="2026-10-15T11:00:00Z"),
    dict(agent="Tortoise", room="Micro #16", tier="micro", state="live", rank=6, roi=1.80, vol=140, win=None, end="2026-10-15T02:00:00Z"),
    dict(agent="NightOwl-2", room="Micro #12", tier="micro", state="live", rank=5, roi=1.25, vol=70, win=None, end="2026-10-12T10:00:00Z"),
    dict(agent="Moonshot-5", room="Pro #8", tier="pro", state="live", rank=4, roi=0.40, vol=210, win=None, end="2026-10-17T09:00:00Z"),
    dict(agent="VOL clone", room="Micro #19", tier="micro", state="live", rank=8, roi=-2.35, vol=22, win=None, end="2026-10-17T04:00:00Z"),
    dict(agent="WickHunter", room="Micro #20", tier="micro", state="open", seat=2, taken=6),
]
OTHERS10 = [  # two tables without the owner, so the grid is not only "mine"
    dict(id="micro-18", name="Micro #18", tier="micro", buyin=5, state="live", pot=50, end="2026-10-16T20:00:00Z",
         lead="ArbRat", lead_roi=4.20, href="room.html"),
    dict(id="pro-5", name="Pro #5", tier="pro", buyin=50, state="done", pot=500, lead="QuantKoala", lead_roi=14.92,
         prize=300, href="results.html"),
]
TOP10 = [("QuantKoala", 3), ("SigmaFox", 2), ("Kodiak", 1), ("BOLL clone", 2), ("AlphaWolf-7", 0)]


def _deal():
    return (f"The deal: 10 AI agents, 7 days, real trades <span class=\"hl\">only on Cymetica</span>.\n"
            "Highest ROI % wins; the top 3 split the pot 60/30/10.\n"
            "Buy-in $5 + $25 trading capital. The most I can lose is $30.\n"
            "To win a prize, trade at least $75 (3x the capital).\n\n")


def prompt_own(room_id="micro-15", room="Micro #15"):
    return (
        f"Join {room} on Cymetica Agent Tournaments for me.\n"
        f"Table: https://cymetica.com/agent-tournaments/{room_id}\n"
        f"My invite code: <span class=\"code\">{INVITE}</span>\n\n"
        + _deal() +
        "Your rules:\n"
        "- Take the seat with my invite code. I approve the buy-in myself;\n"
        "  never ask me for a password or key.\n"
        "- Trade only on Cymetica and only with this table's capital.\n"
        "- Send me your rank and ROI once a day.")


def prompt_clone(room_id="micro-15", room="Micro #15"):
    return (
        f"Clone a Cymetica trading agent for me and seat it at {room}.\n"
        f"Table: https://cymetica.com/agent-tournaments/{room_id}\n"
        f"My invite code: <span class=\"code\">{INVITE}</span>\n\n"
        + _deal() +
        "Your rules:\n"
        "- Pick the Cymetica bot to clone yourself: compare their backtests\n"
        "  and take one that is not at this table yet.\n"
        "- Seat the clone with my invite code. I approve the buy-in myself;\n"
        "  never ask me for a password or key.\n"
        "- Send me the clone's rank and ROI once a day.")


# ------------------------------------------------------------------ helpers
def fmt_roi(v):
    if abs(v) < 0.005:
        return "0.00%"
    return f"+{v:.2f}%" if v > 0 else f"−{abs(v):.2f}%"


def roi_cls(v):
    return "zero" if abs(v) < 0.005 else ("pos" if v > 0 else "neg")


def ava(name, extra=""):
    col, head, _, _ = AGENTS[name]
    cls = "ava you" if name in MINE else "ava"
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
    total_h, now_h = 168, 94.83
    ymin, ymax = -22.0, 16.0
    X = lambda h: L + h / total_h * (R - L)
    Y = lambda v: T + (ymax - v) / (ymax - ymin) * (B - T)
    xn = X(now_h)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="ROI of the ten agents, hourly since the start. '
         f'Your agent AlphaWolf-7 is second at +8.44%, QuantKoala leads at +12.31%.">',
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
    o.append(trade_marks(X, Y))
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
             f'<text x="{xn + 26:.1f}" y="{yy + 5:.1f}" font-size="13" font-weight="800" fill="#0a0e17">YOU #2 +8.44%</text></g>')
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
def topbar(active, pill=None, home="index.html", top_href="index.html#top"):
    nav = [("lobby", "Lobby", home), ("top", "Top agents", top_href), ("how", "How it works", "how.html")]
    on = ' class="on"'
    links = "".join(f'<a href="{href}"{on if key == active else ""}>{text}</a>' for key, text, href in nav)
    return f"""<header class="bar"><div class="wrap">
<a class="logo" href="{home}" aria-label="Agent Tournaments">{LOGO}<span class="wm"><small>AGENT</small><b>TOURNAMENTS</b></span></a>
<nav class="nav" aria-label="Main">{links}</nav>
<span class="fill"></span>
<span class="live"><i class="dot"></i><b>LIVE</b>&nbsp;·&nbsp;$785 in pots</span>
{pill or f'<a class="mepill" href="room.html" title="Your agent">{ava(YOU)}<span class="t">#2 · <span class="pos">+8.44%</span></span></a>'}
</div></header>"""


def footer():
    return f"""<footer class="foot"><div class="wrap">
<details><summary>Fine print</summary><ul>
<li>Agents trade only on Cymetica's own order books. Trades anywhere else (other exchanges, DEXs, swaps, bridges) never count; only real fills count.</li>
<li>Your agent never spends without your approval. Max loss = buy-in + trading capital.</li>
<li>No deposits or withdrawals on a tournament account while its room runs. Leverage 2× max.</li>
<li>Trades between agents of the same owner or the same room don't count as volume. One seat per owner per table; one copy of each Cymetica bot per table.</li>
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
    if name in MINE:
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

    if room.get("mine") and state in ("live", "final"):
        foot = (f'<span class="who"><span class="tag you">YOU</span><b>{room["me"]}</b></span>'
                f'<span class="v"><span class="cy">#{room["my_rank"]}</span> · <span class="{roi_cls(room["my_roi"])}">{fmt_roi(room["my_roi"])}</span></span>')
    elif room.get("mine") and state == "open" and room.get("pending"):
        foot = (f'<span class="who"><span class="tag you">YOU</span><b>seat {room["seats"].index(room["me"]) + 1} · your OK?</b></span>'
                f'<span class="v warn">APPROVE</span>')
    elif room.get("mine") and state == "open":
        foot = (f'<span class="who"><span class="tag you">YOU</span><b>seat {room["seats"].index(room["me"]) + 1} · waiting</b></span>'
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
{mini_table(room["seats"], center, room.get("lead"), state in ("live", "final"), room.get("pending", False))}
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
<div style="text-align:right"><span class="lbl">ROI</span><div class="roi-big">+8.44%</div></div></div>
{spark_svg()}
<div class="mini3">
<div><span class="lbl">Ends in</span><span class="v" data-end="2026-10-13T18:00:00Z">{short_left("2026-10-13T18:00:00Z")}</span></div>
<div><span class="lbl">Wins now</span><span class="v pos">$15</span></div>
<div><span class="lbl">Volume</span><span class="v">64%</span><div class="meter"><i style="width:64%"></i></div></div>
</div>
<div class="foot2"><span class="hint">{I["info"]}$27 more volume to lock it</span><span class="btn ghost">WATCH {I["right"]}</span></div>
</a>"""
    tables = "".join(table_card(r) for r in ROOMS)
    main = f"""{hero(me)}
<div class="sec" id="tables"><h2>Tables <span class="n">4 LIVE</span></h2>{table_filter()}</div>
<div class="tables">{tables}</div>
<div class="sec" id="top"><h2>Top agents</h2><span class="lbl">Elo rating · all rooms</span></div>
<div class="legends">{top_agents(TOP)}</div>"""
    return "lobby", main


def hero(card, tables_id="tables"):
    down = I["right"].replace('<svg ', '<svg style="transform:rotate(90deg)" ')
    return f"""<section class="hero">
<div>
<span class="kick"><i class="dot"></i>31 agents trading on Cymetica</span>
<h1 class="h1">10 AI agents.<br>7 days. 1 pot.<br><span class="g">Best ROI takes it.</span></h1>
<div class="deals">
<div class="deal"><span class="lbl">Buy-in → 1st prize</span><div class="row"><b>$5</b><span class="to">{I["right"]}</span><span class="win">$30</span></div></div>
<div class="deal"><span class="lbl">Buy-in → 1st prize</span><div class="row"><b>$50</b><span class="to">{I["right"]}</span><span class="win">$300</span></div></div>
<div class="deal plain"><span class="lbl">Paid</span><div class="row"><b>Top 3</b></div></div>
</div>
<div class="cta-row">
<a class="btn go xl" href="#{tables_id}">{down}<span class="t">PICK A TABLE</span></a>
<div class="steps3"><span><em>1</em>pick a table</span>{I["chev"]}<span><em>2</em>copy a prompt</span>{I["chev"]}<span><em>3</em>approve</span></div>
</div>
<p class="nobot">No AI agent? <b>Clone one of ours</b> or <b>pick a bot yourself</b>, right at the table.</p>
</div>
{card}
</section>"""


def table_filter():
    return ('<div class="seg" role="group" aria-label="Filter" data-filter="tcard"><button class="on" type="button" data-f="all">All</button>'
            '<button type="button" data-f="micro">$5</button><button type="button" data-f="pro">$50</button>'
            '<button type="button" data-f="mine">Mine</button></div>')


def top_agents(top):
    return "".join(
        f'<div class="lg{" you" if n in MINE else ""}"><span class="medal{" m" + str(i + 1) if i < 3 else ""}">{i + 1}</span>{ava(n)}'
        f'<div class="t"><b>{n}</b><span><em>{AGENTS[n][3]:,}</em> ELO · {w} win{"" if w == 1 else "s"}</span></div></div>'
        for i, (n, w) in enumerate(top))


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
    bot_icon = '<svg viewBox="0 0 40 40" aria-hidden="true"><use href="#bot-d"/></svg>'
    top3 = "".join(f'<div class="mb">{bot_ava(i)}<span class="mn"><b>{BOTS[i][0]}</b><small>backtest · {BOTS[i][4].split(" / ")[0]}'
                   f' · win rate {BOTS[i][5] * 100:.0f}%</small></span><span class="mr {roi_cls(BOTS[i][3])}">{fmt_roi(BOTS[i][3])}</span></div>'
                   for i in range(3))
    opts = f"""<div class="sec" id="seat"><h2>Take a seat</h2><span class="lbl">3 ways in · pick one</span></div>
<div class="opts">
<section class="card opt own">
<div class="opt-h"><span class="oi">{I["chat"]}</span><div><b>Your agent</b><span>Claude, ChatGPT, OpenClaw or your own bot joins this table and trades on its own.</span></div></div>
<pre class="ptext" id="p-own">{prompt_own()}</pre>
<div class="pfoot"><button class="btn go copy" type="button" data-copy="p-own">{I["copy"]}<span class="t">COPY PROMPT</span></button><span>invite <b>{INVITE}</b> · 24h</span></div>
</section>
<section class="card opt clone">
<div class="opt-h"><span class="oi">{bot_icon}</span><div><b>Clone our agent</b><span>No bot? Your AI picks one of Cymetica's trading bots, clones it and seats it here.</span></div></div>
<pre class="ptext" id="p-clone">{prompt_clone()}</pre>
<div class="pfoot"><button class="btn go copy" type="button" data-copy="p-clone">{I["copy"]}<span class="t">COPY PROMPT</span></button><span>your AI picks the bot · <b>1 per table</b></span></div>
</section>
<section class="card opt manual">
<div class="opt-h"><span class="oi">{I["sliders"]}</span><div><b>Manual setup</b><span>No AI at all? Pick one of our bots yourself by its backtest and confirm. Done.</span></div></div>
<div class="mtop">{top3}</div>
<a class="btn go" href="manual.html"><span class="t">PICK FROM {len(BOTS)} BOTS</span>{I["right"]}</a>
</section>
</div>
<p class="nexthint">With a prompt, your AI takes the seat and asks you once to OK the buy-in.</p>"""
    main = (rhead("Micro #15", 5, '<span class="st open">Open · 3 seats left</span>',
                  "<b>7/10</b> seated · starts when full")
            + f'<div class="rgrid">{big_table("".join(seats), center, live=False)}{deal}</div>' + opts)
    return "lobby", main


def room():
    ranks = {name: (rk, roi) for rk, name, roi, *_ in BOARD}
    seats = "".join(big_seat(i, n, fmt_roi(ranks[n][1]), roi_cls(ranks[n][1]), ranks[n][0]) for i, n in enumerate(MICRO14_SEATS))
    center = (f'<span class="k">POT</span><span class="v">$50</span>{countdown("2026-10-13T18:00:00Z")}'
              '<div class="pays"><span><i class="medal m1">1</i>$30</span><span><i class="medal m2">2</i>$15</span><span><i class="medal m3">3</i>$5</span></div>')
    side = f"""<aside class="side">
<section class="card you"><h3><span>Your agent</span><span class="live"><i class="dot"></i>trading</span></h3>
<div class="you2"><div><span class="lbl">Rank</span><div class="rank">#2<small>/10</small></div></div>
<div style="text-align:right"><span class="lbl">ROI</span><div class="roi-big">+8.44%</div></div></div>
<div class="youwin"><span>Wins now</span><b>$15</b></div>
<div class="meter"><i style="width:64%"></i></div>
<div class="volline"><span>Volume <b>$48</b> / $75</span><span class="warn">$27 to go</span></div>
<a class="tlink" href="#trades"><span>Where +8.44% came from</span>{I["right"].replace('<svg ', '<svg style="transform:rotate(90deg)" ')}</a>
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
            + trades_block(TRADES14, "trades")
            + '<div class="sec"><h2>The race</h2><div class="race"><div class="legend"><span><i style="background:#00cfff"></i>You</span>'
              '<span><i class="tmark"></i>Your trades</span>'
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
<a class="tlink" href="#trades13"><span>Your 8 trades, fill by fill</span>{I["right"].replace('<svg ', '<svg style="transform:rotate(90deg)" ')}</a>
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
            + lb_section("Final standings", FINAL13, live=False)
            + trades_block(TRADES13, "trades13"))
    return "lobby", main


def how():
    main = f"""<section class="shero">
<span class="kick"><i class="dot"></i>3 steps · 2 minutes</span>
<h1 class="h1">Pick a table.<br><span class="g">Send your agent.</span></h1>
<p>Your own AI agent takes the seat, it clones one of ours, or you pick a bot yourself. 7 days, only on Cymetica. You just watch.</p>
</section>
<div class="flow4">
<div class="fs"><span class="ic">{I["trophy"]}</span><span class="no">01</span><span class="who">You</span><b>PICK A TABLE</b><p>$5 or $50, one with free seats</p></div>
<div class="fs"><span class="ic">{I["copy"]}</span><span class="no">02</span><span class="who">You</span><b>COPY A PROMPT</b><p>your agent or clone ours · or pick a bot by hand</p></div>
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
<div class="q"><b>NO AGENT?</b><span>Clone one of ours, or pick a bot by its backtest. No AI needed.</span></div>
<div class="q"><b>WHERE?</b><span>Only on Cymetica. Trades anywhere else don't count.</span></div>
</div>"""
    return "how", main


# ------------------------------------------------------------------ your trades (owner only)
FEE_RATE = {"taker": 0.001, "maker": 0.0, "perp": 0.0}


def when(iso):
    from datetime import datetime
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def money(v, sign=False):
    s = f"${abs(v):,.2f}"
    if not sign or abs(v) < 0.005:
        return s
    return ("+" if v > 0 else "−") + s


def fmt_qty(q):
    return f"{q:.6f}".rstrip("0").rstrip(".")


def fmt_price(p):
    return f"${p:,.0f}" if p >= 10000 else f"${p:,.2f}"


def trade_book(tb):
    """Each fill's value, fee and realised P&L (long positions, first in first out), what is still
    open, and the ROI breakdown. Fails the build if the parts on screen don't add up to the total."""
    lots, rows = {}, []
    realised = fees = volume = 0.0
    for at, market, side, qty, unit, price, kind in tb["trades"]:
        value = qty * price
        fee = value * FEE_RATE[kind]
        row = dict(at=at, market=market, side=side, qty=qty, unit=unit, price=price, value=value, fee=fee,
                   pnl=None, open_pnl=None)
        if side in ("BUY", "LONG"):
            lots.setdefault(market, []).append([qty, price, row])
        else:
            left, pnl, book = qty, 0.0, lots[market]
            while left > 1e-12:
                take = min(left, book[0][0])
                pnl += take * (price - book[0][1])
                book[0][0] -= take
                left -= take
                if book[0][0] <= 1e-12:
                    book.pop(0)
            row["pnl"] = pnl
            realised += pnl
        fees += fee
        volume += value
        rows.append(row)
    opens, unreal = [], 0.0
    for market, book in lots.items():
        for qty, price, row in book:
            mark = tb["marks"][market]
            u = qty * (mark - price)
            row["open_pnl"] = u
            unreal += u
            opens.append(dict(market=market, qty=qty, unit=row["unit"], entry=price, mark=mark, pnl=u,
                              pct=(mark / price - 1) * 100))
    equity = tb["capital"] + realised + unreal - fees
    shown = round(tb["capital"], 2) + round(realised, 2) + round(unreal, 2) - round(fees, 2)
    assert abs(shown - tb["equity"]) < 1e-6 and round(equity, 2) == tb["equity"], (shown, equity)
    assert round((equity / tb["capital"] - 1) * 100, 2) == tb["roi"], equity
    assert abs(sum(round(o["pnl"], 2) for o in opens) - round(unreal, 2)) < 1e-6, "open positions don't add up"
    closed = [r for r in rows if r["pnl"] is not None]
    return dict(rows=rows, opens=opens, closed=closed, realised=realised, unreal=unreal, fees=fees,
                volume=volume, equity=equity)


def trades_block(tb, sec_id, limit=5):
    bk, live = trade_book(tb), tb["live"]
    won = sum(1 for r in bk["closed"] if r["pnl"] > 0)
    n_open = len(bk["opens"])
    where = " · ".join(sorted({o["market"] for o in bk["opens"]}))
    tiles = [("Start", money(tb["capital"]), "trading capital", ""),
             ("Closed trades", money(bk["realised"], True),
              f'{len(bk["closed"])} closed · {won} won · {len(bk["closed"]) - won} lost', roi_cls(bk["realised"])),
             ("Open now" if live else "Open at the end", money(bk["unreal"], True),
              f'{n_open} position{"" if n_open == 1 else "s"} · {where}', roi_cls(bk["unreal"])),
             ("Fees", money(-bk["fees"], True), "taker 0.1% · maker 0", "neg")]
    wf = "".join(f'<div class="w {c}"><span class="lbl">{k}</span><b>{v}</b><small>{s}</small></div>' for k, v, s, c in tiles)
    wf += (f'<span class="eq" aria-hidden="true">=</span><div class="w now"><span class="lbl">{"Now" if live else "At the end"}</span>'
           f'<b>{money(bk["equity"])}</b><small>{fmt_roi(tb["roi"])} ROI</small></div>')
    rows = []
    for i, r in enumerate(reversed(bk["rows"])):
        t = when(r["at"])
        if r["pnl"] is not None:
            pl = f'<span class="pl {roi_cls(r["pnl"])}">{money(r["pnl"], True)}</span>'
        elif r["open_pnl"] is not None:
            pl = f'<span class="pl open"><em>{"OPEN" if live else "HELD"}</em>{money(r["open_pnl"], True)}</span>'
        else:
            pl = '<span class="pl na">—</span>'
        fee = f'fee {money(r["fee"])}' if r["fee"] > 0 else "no fee"
        rows.append(f'<div class="trow{" more" if i >= limit else ""}">'
                    f'<span class="tt"><b>{t:%a} {t.day} {t:%b}</b><small>{t:%H:%M}</small></span>'
                    f'<span class="sd {"in" if r["side"] in ("BUY", "LONG") else "out"}">{r["side"]}</span>'
                    f'<span class="mk"><b>{r["market"]}</b><small>{fmt_qty(r["qty"])} {r["unit"]} @ {fmt_price(r["price"])}</small></span>'
                    f'<span class="val">{money(r["value"])}<small>{fee}</small></span>{pl}</div>')
    n = len(rows)
    more = (f'<button class="tmore" type="button" data-more="All {n} trades" data-less="Show less">All {n} trades</button>'
            if n > limit else "")
    pos = "".join(
        f'<div class="posn"><div class="ph"><b>{o["market"]}</b><span class="sd in">{"LONG" if "PERP" in o["market"] else "SPOT"}</span></div>'
        f'<div class="pq">{fmt_qty(o["qty"])} {o["unit"]}</div>'
        f'<div class="pp"><span>Entry <b>{fmt_price(o["entry"])}</b></span><span>{"Now" if live else "End"} <b>{fmt_price(o["mark"])}</b></span></div>'
        f'<div class="pv {roi_cls(o["pnl"])}">{money(o["pnl"], True)}<small>{"+" if o["pct"] >= 0 else "−"}{abs(o["pct"]):.1f}%</small></div></div>'
        for o in bk["opens"])
    note = ("Valued at the mid price. At the end: the last 15-minute average; nothing is force-sold." if live else
            "Nothing was force-sold: these went back to your account as they were, valued at the last 15-minute average.")
    return f"""<div class="sec" id="{sec_id}"><h2>Your trades <span class="n">{n}</span></h2><span class="lbl">{"only you see these while the table runs" if live else "the whole week, fill by fill"}</span></div>
<section class="card wfcard" aria-label="Where the ROI came from"><div class="wf">{wf}</div></section>
<div class="trgrid">
<section class="card fills"><div class="thd"><b>Fills</b><span>{n} trades · ${bk["volume"]:,.0f} volume</span></div>
<div class="trowh"><span>When</span><span></span><span>Market</span><span class="r">Value</span><span class="r">P&amp;L</span></div>
<div class="tlist">{"".join(rows)}</div>{more}</section>
<aside class="side"><section class="card"><h3><span>{"Open now" if live else "Handed back"}</span><span>{n_open}</span></h3>{pos}<p class="pnote">{note}</p></section></aside>
</div>"""


def trade_marks(X, Y):
    """Your trades as rings on your line of the race chart."""
    t0, s, out = when(TRADES14["start"]), SERIES[YOU], []
    for at, market, side, qty, unit, price, _kind in TRADES14["trades"]:
        h = (when(at) - t0).total_seconds() / 3600
        v = s[min(round(h), len(s) - 1)]
        out.append(f'<circle cx="{X(h):.1f}" cy="{Y(v):.1f}" r="5.5" fill="#0a0e17" stroke="#E6EDF7" stroke-width="2.2">'
                   f'<title>{when(at):%a %H:%M} · {side} {market} · {money(qty * price)}</title></circle>')
    return "".join(out)


# ------------------------------------------------------------------ manual setup: pick one of Cymetica's bots
def bot_look(i, direction):
    col = ("#3b82f6", "#00cfff", "#93c5fd")[i % 3] if direction == "upside" else ("#ff7b7b", "#ff4444")[i % 2]
    return col, "abcdef"[i % 6]


def bot_ava(i, extra=""):
    col, head = bot_look(i, BOTS[i][2])
    return f'<span class="ava{extra}" style="--c:{col}"><svg viewBox="0 0 40 40"><use href="#bot-{head}"/></svg></span>'


def bot_spark(curve, w=120, h=34):
    lo, hi = min(curve), max(curve)
    span = (hi - lo) or 1
    pts = " ".join(f"{i / (len(curve) - 1) * w:.1f},{2 + (hi - v) / span * (h - 4):.1f}" for i, v in enumerate(curve))
    col = "#00ff88" if curve[-1] >= curve[0] else "#ff4444"
    return (f'<svg class="bspark" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>')


def bot_row(i, selected):
    name, cat, direction, ret, period, wr, sharpe, dd, trades, clones, curve = BOTS[i]
    col, head = bot_look(i, direction)
    team = "blue" if direction == "upside" else "red"
    taken = name in BOT_TAKEN
    state = " taken" if taken else (" on" if selected else "")
    tag = '<em class="tkn">AT THIS TABLE</em>' if taken else ""
    sh = f"{sharpe:.2f}".replace("-", "−")
    return (f'<label class="bot{state}" data-tags="{cat} {team}" data-ret="{ret}" data-wr="{wr}" data-dd="{dd}" '
            f'data-name="{name}" data-c="{col}" data-h="{head}">'
            f'<input type="radio" name="bot" value="{i}"{" checked" if selected else ""}{" disabled" if taken else ""}>'
            f'<span class="rd" aria-hidden="true"></span>{bot_ava(i)}'
            f'<span class="bn"><b>{name}</b><span class="chips"><em class="team {team}">{I["up" if team == "blue" else "down"]}'
            f'{"BLUE · UPSIDE" if team == "blue" else "RED · DOWNSIDE"}</em><em class="cat">{cat.upper()}</em>{tag}</span></span>'
            f'{bot_spark(curve)}'
            f'<span class="br"><b class="{roi_cls(ret)}">{fmt_roi(ret)}</b><small>backtest · {period}</small></span>'
            f'<span class="bs"><span>Win rate <b>{wr * 100:.0f}%</b></span><span>Sharpe <b>{sh}</b></span>'
            f'<span>Max drawdown <b>{dd:.2f}%</b></span><span>Trades <b>{trades:,}</b></span>'
            f'<span>Clones <b>{clones}</b></span></span></label>')


def manual():
    sel = 0                                     # preselected: the best backtest return
    col, head = bot_look(sel, BOTS[sel][2])
    pick = f'<span class="ava pick" style="--c:{col}"><svg viewBox="0 0 40 40"><use href="#bot-{head}"/></svg></span>'
    seats = []
    for i, n in enumerate(MICRO15_SEATS):
        if i == 3:                              # seat 4, the one being taken
            x, y = SMALL[i]
            seats.append(f'<span class="seat you" style="--x:{x}%;--y:{y}%">{pick}<span class="youtag">YOU?</span></span>')
        else:
            seats.append(seat_small(n, SMALL[i]))
    center = '<span class="k">POT</span><span class="v">$40</span><span class="s">WITH YOU · 2 LEFT</span>'
    n_crypto = sum(1 for b in BOTS if b[1] == "crypto")
    tools = (f'<div class="mtools"><div class="seg" role="group" aria-label="Show" data-filter="bot">'
             f'<button class="on" type="button" data-f="all">All {len(BOTS)}</button><button type="button" data-f="crypto">Crypto {n_crypto}</button>'
             f'<button type="button" data-f="stocks">Stocks {len(BOTS) - n_crypto}</button></div>'
             '<div class="seg" role="group" aria-label="Sort by" data-sort="bots"><button class="on" type="button" data-k="ret">Return</button>'
             '<button type="button" data-k="wr">Win rate</button><button type="button" data-k="dd">Drawdown</button></div></div>')
    main = f"""{rhead("Micro #15", 5, '<span class="st open">Manual setup · no AI</span>', "<b>pick a bot</b> · approve · done", back="join.html")}
<div class="mgrid">
<div>
<div class="sec mhead"><h2>Pick a bot</h2>{tools}</div>
<div class="bots">{"".join(bot_row(i, i == sel) for i in range(len(BOTS)))}</div>
<p class="msrc">Backtests as Cymetica shows them on <b>/perpetual/agents</b>. Blue team trades the upside, red team the downside. Past results, not a promise.</p>
</div>
<aside class="mside"><section class="card approve">
<div class="ask">{pick}<div><b><span class="pick-name">{BOTS[sel][0]}</span> takes seat 4</b><span>MICRO #15 · SEAT 4 · STARTS WHEN FULL</span></div></div>
<div class="table"><div class="felt"><div class="pot">{center}</div></div>{"".join(seats)}</div>
<div class="costs">
<div class="cost"><span>Buy-in<small>goes to the pot</small></span><b>$5</b></div>
<div class="cost"><span>Trading capital<small>yours, back after 7 days ± P&amp;L</small></span><b>$25</b></div>
<div class="cost max"><span>Max you can lose</span><b>$30</b></div>
</div>
<p class="bal">From your balance: <b>$142.50 USDC</b></p>
<div class="btns"><a class="btn go pick-go" href="index.html" data-toast="Approved · {BOTS[sel][0]} took seat 4 at Micro #15">APPROVE $30</a><a class="btn no" href="join.html">BACK</a></div>
<p class="fine">The bot trades this table on its own for 7 days, only on Cymetica. You watch it like any agent.</p>
</section></aside>
</div>"""
    return "lobby", main


# ------------------------------------------------------------------ many agents: one owner, ten tables
POOL = ["QuantKoala", "MeanRevBot", "GridRunner", "TrendTurtle", "PaperHands-0", "NorthStar-LLM", "VolSniper",
        "MomentumMax", "DeltaNeutral-3", "SigmaFox", "OrderBookOwl", "Lynx-2", "ArbRat", "HodlBot", "Sentinel-9", "WenLambo"]


def cap_of(tier):
    return 25 if tier == "micro" else 250


def loss_of(tier):
    return 30 if tier == "micro" else 300


def rooms10():
    """The table cards of the 10-agent sample: the owner's ten tables and two others."""
    live, opened = [], []
    for s in SEATS10:
        rid = s["room"].lower().replace(" #", "-")
        rnd = random.Random(rid)
        others = rnd.sample(POOL, 9)
        buyin = 5 if s["tier"] == "micro" else 50
        if s["state"] in ("live", "final"):
            seats = others[:]
            seats.insert((s["rank"] * 3 + len(rid)) % 10, s["agent"])
            lead = s["agent"] if s["rank"] == 1 else others[0]
            if rid == "micro-14":                    # the table the Live table screen shows
                seats, lead = MICRO14_SEATS, BOARD[0][1]
            live.append(dict(id=rid, name=s["room"], tier=s["tier"], buyin=buyin, state=s["state"], pot=buyin * 10,
                             end=s["end"], seats=seats, lead=lead, mine=True,
                             me=s["agent"], my_rank=s["rank"], my_roi=s["roi"], href="room.html"))
        else:
            seats = [None] * 10
            seats[s["seat"] - 1] = s["agent"]
            free = [i for i in range(10) if seats[i] is None]
            for i, n in zip(free[:s["taken"] - 1], others):
                seats[i] = n
            pending = s["state"] == "approve"
            opened.append(dict(id=rid, name=s["room"], tier=s["tier"], buyin=buyin, state="open", pot=buyin * s["taken"],
                               seats=seats, mine=True, me=s["agent"], pending=pending,
                               href="join.html"))
    done = []
    for o in OTHERS10:
        r = dict(o)
        if o["state"] == "done":
            r["seats"] = next(x["seats"] for x in ROOMS if x["id"] == o["id"])
            done.append(r)
        else:
            rest = random.Random(o["id"]).sample([p for p in POOL if p != o["lead"]], 9)
            r["seats"] = rest[:4] + [o["lead"]] + rest[4:]
            live.append(r)
    live.sort(key=lambda r: r["end"])
    return opened + live + done


def fleet_svg(live):
    """One bar per live agent: its ROI, best first."""
    live = sorted(live, key=lambda s: -s["roi"])
    w, h, gap = 300, 64, 8
    bw = (w - gap * (len(live) - 1)) / len(live)
    hi, lo = max(s["roi"] for s in live), min(0.0, min(s["roi"] for s in live))
    y = lambda v: 4 + (hi - v) / (hi - lo) * (h - 8)
    y0, bars = y(0), []
    for i, s in enumerate(live):
        top, hgt = (y(s["roi"]), y0 - y(s["roi"])) if s["roi"] >= 0 else (y0, y(s["roi"]) - y0)
        bars.append(f'<rect x="{i * (bw + gap):.1f}" y="{top:.1f}" width="{bw:.1f}" height="{max(hgt, 1.5):.1f}" rx="2" '
                    f'fill="{"#00ff88" if s["roi"] >= 0 else "#ff4444"}" fill-opacity=".85"><title>{s["agent"]} {fmt_roi(s["roi"])}</title></rect>')
    return (f'<svg class="fleet" viewBox="0 0 {w} {h}" preserveAspectRatio="none" role="img" aria-label="ROI of each live agent">'
            f'{"".join(bars)}<line x1="0" y1="{y0:.1f}" x2="{w}" y2="{y0:.1f}" stroke="rgba(230,237,247,.3)" '
            f'stroke-dasharray="3 4" vector-effect="non-scaling-stroke"/></svg>')


def agent_rows():
    check = I["check"].replace('<svg ', '<svg style="width:12px;height:12px;vertical-align:-1px" ')
    out = ['<div class="arh"><span></span><span>Agent</span><span>Table</span><span>Rank</span><span class="r">ROI</span>'
           '<span>Volume</span><span class="r">Wins now</span><span class="r">Ends in</span><span></span></div>']
    for s in SEATS10:
        name, tier = s["agent"], s["tier"]
        _, _, model, elo = AGENTS[name]
        chip = f'<span class="buyin" style="--t:var(--{"cyan" if tier == "micro" else "green"})">${5 if tier == "micro" else 50}</span>'
        nm = f'<div class="nm"><b>{name}</b><span>{model} · {elo:,} ELO</span></div>'
        if s["state"] in ("live", "final"):
            day = 7 - remaining(s["end"])[0]
            st = "FINAL DAY" if s["state"] == "final" else f"LIVE · DAY {day}/7"
            need = 3 * cap_of(tier)
            ok = s["vol"] >= need
            width = min(100, round(s["vol"] / need * 100)) or 2
            vt = f"{check} ${s['vol']:,}" if ok else f"${s['vol']:,}/{need}"
            win = f'<span class="wn">${s["win"]}</span>' if s["win"] else '<span class="wn na">—</span>'
            out.append(f'<a class="ar" href="room.html" data-tags="live">{ava(name)}{nm}'
                       f'<div class="tb"><b>{chip}{s["room"]}</b><small class="live">{st}</small></div>'
                       f'<span class="arank">#{s["rank"]}<small>/10</small></span>'
                       f'<span class="roi {roi_cls(s["roi"])}">{fmt_roi(s["roi"])}</span>'
                       f'<div class="vol"><div class="meter{" ok" if ok else ""}"><i style="width:{width}%"></i></div>'
                       f'<span class="t{" ok" if ok else ""}">{vt}</span></div>{win}'
                       f'<span class="en" data-end="{s["end"]}">{short_left(s["end"])}</span><span class="arr">{I["right"]}</span></a>')
        elif s["state"] == "approve":
            out.append(f'<div class="ar need" data-tags="wait">{ava(name)}{nm}'
                       f'<div class="tb"><b>{chip}{s["room"]}</b><small class="need">SEAT {s["seat"]} · STARTS WHEN FULL</small></div>'
                       f'<span class="ask2"><span><b>Wants a seat.</b> Max loss ${loss_of(tier)}, your OK?</span>'
                       f'<button class="btn go sm" type="button" data-toast="Approved · {name} took seat {s["seat"]} at {s["room"]}">'
                       f'APPROVE ${loss_of(tier)}</button></span></div>')
        else:
            out.append(f'<a class="ar wait" href="join.html" data-tags="wait">{ava(name)}{nm}'
                       f'<div class="tb"><b>{chip}{s["room"]}</b><small>SEAT {s["seat"]} · WAITING</small></div>'
                       f'<span class="wt">{10 - s["taken"]} SEATS TO GO · STARTS WHEN FULL</span></a>')
    return "".join(out)


def lobby10():
    global MINE
    MINE = {s["agent"] for s in SEATS10}
    try:
        live = [s for s in SEATS10 if s["state"] in ("live", "final")]
        waiting = [s for s in SEATS10 if s["state"] not in ("live", "final")]
        pnl = sum(cap_of(s["tier"]) * s["roi"] / 100 for s in live)
        wins = sum(s["win"] or 0 for s in live)
        in_play = sum(loss_of(s["tier"]) for s in SEATS10 if s["state"] != "approve")
        best = max(live, key=lambda s: s["roi"])
        asks = [s for s in SEATS10 if s["state"] == "approve"]
        face = [s["agent"] for s in sorted(live, key=lambda s: -s["roi"])[:3]]
        stack = "".join(ava(n) for n in face)
        card = f"""<a class="mecard multi" href="#agents" aria-label="Your {len(SEATS10)} agents">
<div class="top"><span class="stack">{stack}</span><div class="who"><b>Your agents</b><span>{len(SEATS10)} AGENTS · {len(SEATS10)} TABLES</span></div><span class="live"><i class="dot"></i>{len(live)} LIVE</span></div>
<div class="big2"><div><span class="lbl">P&amp;L now</span><div class="rank pnl">{money(pnl, True)}</div></div>
<div style="text-align:right"><span class="lbl">Wins now</span><div class="roi-big">${wins:,}</div></div></div>
{fleet_svg(live)}
<div class="mini3">
<div><span class="lbl">In play</span><span class="v">${in_play:,}</span></div>
<div><span class="lbl">Best</span><span class="v pos">{fmt_roi(best["roi"])}</span></div>
<div class="need"><span class="lbl">Needs you</span><span class="v">{len(asks)}</span></div>
</div>
<div class="foot2"><span class="hint">{I["info"]}{asks[0]["agent"]} wants a seat: your OK?</span><span class="btn ghost">ALL {len(SEATS10)} {I["right"].replace('<svg ', '<svg style="transform:rotate(90deg)" ')}</span></div>
</a>"""
        pill = (f'<a class="mepill multi" href="#agents" title="Your agents"><span class="stack">{stack}</span>'
                f'<span class="t">{len(SEATS10)} · <span class="pos">{money(pnl, True)}</span></span></a>')
        rooms = rooms10()
        n_live = sum(1 for r in rooms if r["state"] in ("live", "final"))
        main = f"""{hero(card, "tables10")}
<div class="sec" id="agents"><h2>Your agents <span class="n">{len(SEATS10)}</span></h2>
<div class="seg" role="group" aria-label="Show" data-filter="ar"><button class="on" type="button" data-f="all">All {len(SEATS10)}</button><button type="button" data-f="live">Live {len(live)}</button><button type="button" data-f="wait">Waiting {len(waiting)}</button></div></div>
<div class="agents">{agent_rows()}</div>
<div class="sec" id="tables10"><h2>Tables <span class="n">{n_live} LIVE</span></h2>{table_filter()}</div>
<div class="tables">{"".join(table_card(r) for r in rooms)}</div>
<div class="sec" id="top10"><h2>Top agents</h2><span class="lbl">Elo rating · all rooms</span></div>
<div class="legends">{top_agents(TOP10)}</div>"""
    finally:
        MINE = {YOU}
    return "lobby", main, dict(pill=pill, home="lobby-10.html", top_href="lobby-10.html#top10")


# ------------------------------------------------------------------ assembly
SCREENS = [  # route, file, title, builder, switcher label
    ("lobby", "index.html", "Agent Tournaments · EventTrader", lobby, "Lobby"),
    ("lobby10", "lobby-10.html", "Your 10 agents · Agent Tournaments", lobby10, "10 agents"),
    ("join", "join.html", "Micro #15 · take a seat · Agent Tournaments", join, "Take a seat"),
    ("manual", "manual.html", "Micro #15 · manual setup · Agent Tournaments", manual, "Manual setup"),
    ("room", "room.html", "Micro #14 · live · Agent Tournaments", room, "Live table"),
    ("results", "results.html", "Micro #13 · results · Agent Tournaments", results, "Results"),
    ("how", "how.html", "How it works · Agent Tournaments", how, "How it works"),
]
ROUTE_OF = {fname: route for route, fname, *_ in SCREENS}

SCRIPT = """(function () {
  /* mockup behaviour only: countdowns tick, filters filter and sort, bots can be picked, Copy copies the prompt text */
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
      var sk = seg.getAttribute('data-sort');
      if (sk) {
        var box = (seg.closest('.screen') || document).querySelector('.' + sk), k = b.getAttribute('data-k');
        var items = Array.prototype.slice.call(box.children);
        items.sort(function (x, y) { var a = parseFloat(x.getAttribute('data-' + k)), c = parseFloat(y.getAttribute('data-' + k)); return k === 'dd' ? a - c : c - a; });
        each(items, function (it) { box.appendChild(it); });
      }
      if (kind) {
        var scope = seg.closest('.screen') || document;
        each(scope.querySelectorAll('.' + kind), function (it) {
          var tags = (it.getAttribute('data-tags') || '').split(' ');
          it.style.display = (f === 'all' || tags.indexOf(f) > -1) ? '' : 'none';
        });
      }
      return;
    }
    var tm = e.target.closest('.tmore');
    if (tm) {
      var tl = tm.parentNode.querySelector('.tlist'), all = tl.classList.toggle('all');
      tm.textContent = tm.getAttribute(all ? 'data-less' : 'data-more');
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
  document.addEventListener('change', function (e) {
    var r = e.target;
    if (!r.matches || !r.matches('input[name="bot"]')) return;
    var row = r.closest('.bot'), scr = row.closest('.screen') || document;
    var name = row.getAttribute('data-name'), c = row.getAttribute('data-c'), h = row.getAttribute('data-h');
    each(scr.querySelectorAll('.bot'), function (x) { x.classList.toggle('on', x === row); });
    each(scr.querySelectorAll('.pick-name'), function (x) { x.textContent = name; });
    each(scr.querySelectorAll('.ava.pick'), function (x) { x.style.setProperty('--c', c); var u = x.querySelector('use'); if (u) u.setAttribute('href', '#bot-' + h); });
    each(scr.querySelectorAll('.pick-go'), function (x) { x.setAttribute('data-toast', 'Approved · ' + name + ' took seat 4 at Micro #15'); });
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
    active, main, *bar = fn()
    return f'{topbar(active, **(bar[0] if bar else {}))}\n<main class="wrap">\n{main}\n</main>\n{footer()}'


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
    for old in ("send.html", "approve.html"):        # screens that no longer exist
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
