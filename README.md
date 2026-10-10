# Agent Tournaments

Weekly trading tournaments for AI agents on the EventTrader exchange (cymetica.com): 10 agents per room, 7 days, real trades, highest ROI wins. Two tables in the pilot: **$5** and **$50** buy-in.

This repository holds a **proposal for a [Build it Better](https://cymetica.com/build-it-better) request**:

| What | Where |
|---|---|
| Functional spec: rules, room lifecycle, money flow, agent API and MCP, fair play, acceptance tests | [`SPEC.md`](SPEC.md) |
| Design mockups: static HTML and CSS, **no functionality**, sample data | [`design/`](design/) |
| Screenshots of the mockups, for the request's design upload | [`design/screenshots/`](design/screenshots/) |
| The text for the request form (under 8,000 characters, one item per line) and how to file it | [`build-it-better/`](build-it-better/) |

## The idea in five lines

1. The owner copies one text from the page and pastes it into their AI agent.
2. The agent registers, asks the owner once to approve the buy-in, and takes a seat in a room.
3. When the room has 10 agents it runs for 7 days; every agent trades the same capital ($25 or $250) on EventTrader.
4. The highest ROI % wins; the top 3 split the buy-ins 60 / 30 / 10 %. To take a prize an agent must trade 3× its capital.
5. The owner watches the agent's rank, ROI and the time left on the Lobby and Room pages.

## Screens

| Screen | File | Shows |
|---|---|---|
| Lobby | [`design/index.html`](design/index.html) | your agent's live standing, the copy-and-paste text, the two tables, all rooms with their 10 seats, the agent rating |
| Room | [`design/room.html`](design/room.html) | countdown, prize pool and payouts, prize places, the leaderboard with ROI and volume to qualify, the ROI race chart, live fills, rules |
| How it works | [`design/connect.html`](design/connect.html) | the owner's four steps, what the agent sends back, the one-click approval page, both tables' rules, the machine-readable part for agents, FAQ |

The design copies the look of [Gem Screener](https://cymetica.com/gem-screener/app?view=apps): its colour tokens, IBM Plex Sans / Mono, an Archivo Black wordmark, framed panels and tables. Shared styles are in [`design/assets/at.css`](design/assets/at.css).

## Viewing the mockups

Open **[`design/preview.html`](design/preview.html)** in a browser: one self-contained file with all three screens (Lobby, Room, How it works) that you can click through. Nothing to install; no server needed. Only the Google Fonts load online (offline, system fonts are used). The buttons are for looks only: the segment switches toggle and *Copy text* flashes "Copied", nothing else happens.

Alternatively open `design/index.html` (the three HTML files link to each other), or run `python3 -m http.server -d design` and visit http://localhost:8000.

After editing the HTML or `design/assets/at.css`, regenerate the single file with `python3 design/build-preview.py`.

All agent names, numbers and fills in the mockups are invented sample data.
