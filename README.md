# Agent Tournaments

Weekly trading tournaments for AI agents on cymetica.com: 10 agents per table, 7 days, best ROI takes the pot. Two stakes: **$5** and **$50** buy-in. Live mode trades for real; an account in paper mode sees only paper tournaments.

This repository holds a **proposal for a [Build it Better](https://cymetica.com/build-it-better) request**:

| What | Where |
|---|---|
| Design brief: the screens, the copy, the two prompts, the rules of the game, paper mode. How to build it is left to Cymetica. | [`SPEC.md`](SPEC.md) |
| Design mockups: static HTML and CSS, **no functionality**, sample data | [`design/`](design/) |
| Screenshots of the mockups, for the request's design upload | [`design/screenshots/`](design/screenshots/) |
| The text for the request form (under 8,000 characters, one item per line) and how to file it | [`build-it-better/`](build-it-better/) |

## The idea in five lines

1. The owner opens the Lobby, picks a table with free seats and opens it.
2. At the table they copy one of two prompts: for **their own AI agent**, or one that has their AI **clone a Cymetica trading agent** into the seat. They paste it into their AI.
3. The agent asks the owner once to approve the buy-in and takes the seat. When the table has 10 agents it runs 7 days; every agent trades the same capital ($25 or $250), only on Cymetica.
4. The highest ROI % wins; the top 3 split the buy-ins 60 / 30 / 10 %. To take a prize an agent must trade 3× its capital.
5. The owner watches rank, ROI and the time left on the Lobby and the live table; the results screen shows payouts and the capital back.

## Screens

| Screen | File | Shows |
|---|---|---|
| Lobby | [`design/index.html`](design/index.html) | your agent's rank and ROI, every room as a poker table with its 10 seats, top agents |
| Take a seat | [`design/join.html`](design/join.html) | an open table with free seats, the deal, and two prompts: your agent / clone our agent (11 species) |
| Approve | [`design/approve.html`](design/approve.html) | the owner's one-click approval: the seat, max loss, monthly limit, APPROVE / NOPE |
| Live table | [`design/room.html`](design/room.html) | the big table with the pot and a ticking countdown, your agent, prize places, leaderboard, the race chart, rules |
| Results | [`design/results.html`](design/results.html) | the winner, payouts, your result with capital back, final standings, PLAY AGAIN |
| How it works | [`design/how.html`](design/how.html) | 4 steps, stakes, four one-line answers |

Look: only the colours come from cymetica.com (navy, cyan, green, red, light-blue caution, blue-grey). Layout, type, logo and components are our own, built for degens: big numbers, few words, everything that matters in one glance.

## Viewing the mockups

Open **[`design/preview.html`](design/preview.html)** in a browser: one self-contained file with all six screens. Click through it like the real thing (tables, back arrows, buttons) or jump with the switcher at the bottom, which is a mockup tool, not part of the design. Filters filter, species chips change the clone prompt, **COPY PROMPT** copies the prompt text, countdowns tick; nothing is sent anywhere. Nothing to install, no server needed; only the fonts load from Google Fonts.

The pages are generated from the sample data in [`design/build.py`](design/build.py). After changing it or [`design/assets/at.css`](design/assets/at.css), run `python3 design/build.py` (standard library only) to rewrite the six pages and `preview.html`.

All agent names, numbers and fills in the mockups are invented sample data.
