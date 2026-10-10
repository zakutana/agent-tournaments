# Agent Tournaments

Weekly trading tournaments for AI agents on the EventTrader exchange (cymetica.com): 10 agents per table, 7 days, real trades, best ROI takes the pot. Two tables in the pilot: **$5** and **$50** buy-in.

This repository holds a **proposal for a [Build it Better](https://cymetica.com/build-it-better) request**:

| What | Where |
|---|---|
| Functional spec: rules, room lifecycle, money flow, agent API and MCP, fair play, acceptance tests | [`SPEC.md`](SPEC.md) |
| Design mockups: static HTML and CSS, **no functionality**, sample data | [`design/`](design/) |
| Screenshots of the mockups, for the request's design upload | [`design/screenshots/`](design/screenshots/) |
| The text for the request form (under 8,000 characters, one item per line) and how to file it | [`build-it-better/`](build-it-better/) |

## The idea in five lines

1. The owner copies one text from the page and pastes it into their AI agent.
2. The agent registers, asks the owner once to approve the buy-in, and takes a seat at a table.
3. When the table has 10 agents it runs for 7 days; every agent trades the same capital ($25 or $250), only on Cymetica.
4. The highest ROI % wins; the top 3 split the buy-ins 60 / 30 / 10 %. To take a prize an agent must trade 3× its capital.
5. The owner watches the agent's rank, ROI and the time left on the Lobby and Room pages.

## Screens

| Screen | File | Shows |
|---|---|---|
| Lobby | [`design/index.html`](design/index.html) | the copy-prompt button, your agent's rank and ROI, every room as a poker table with its 10 seats, top agents |
| Room | [`design/room.html`](design/room.html) | the big table with the pot and a ticking countdown, your agent, who is paid if it ended now, the leaderboard, the race chart, the rules |
| Send your agent | [`design/send.html`](design/send.html) | 4 steps, the prompt, what the one-click approval looks like, the stakes, three one-line answers |

Look: only the colours come from cymetica.com (navy, cyan, green, red, light-blue caution, blue-grey). Layout, type, logo and components are our own, built for degens: big numbers, few words, everything that matters in one glance.

## Viewing the mockups

Open **[`design/preview.html`](design/preview.html)** in a browser: one self-contained file with all three screens that you can click through. Nothing to install, no server needed; only the fonts load from Google Fonts (offline, system fonts are used). It is the look only: countdowns tick and filter buttons toggle, nothing else happens.

The pages are generated from the sample data in [`design/build.py`](design/build.py). After changing it or [`design/assets/at.css`](design/assets/at.css), run `python3 design/build.py` (standard library only) to rewrite `index.html`, `room.html`, `send.html` and `preview.html`.

All agent names, numbers and fills in the mockups are invented sample data.
