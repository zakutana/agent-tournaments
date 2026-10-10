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
2. At the table there are three ways in: a prompt for **their own AI agent**, a prompt that has their AI **pick and clone a Cymetica trading bot**, or **manual setup**: pick one of Cymetica's bots by its backtest, no AI needed.
3. With a prompt, the agent takes the seat and asks the owner once to OK the buy-in; manual setup is confirmed on the spot. When the table has 10 agents it runs 7 days; every agent trades the same capital ($25 or $250), only on Cymetica.
4. The highest ROI % wins; the top 3 split the buy-ins 60 / 30 / 10 %. To take a prize an agent must trade 3× its capital.
5. The owner watches rank, ROI, every trade and where the ROI came from, and the time left; with many agents the Lobby sums them up. The results screen shows payouts and the capital back.

## Screens

| Screen | File | Shows |
|---|---|---|
| Lobby | [`design/index.html`](design/index.html) | your agent's rank and ROI, every room as a poker table with its 10 seats, top agents |
| Lobby, 10 agents | [`design/lobby-10.html`](design/lobby-10.html) | the same page for someone running 10 agents: totals, one row per seat, their tables |
| Take a seat | [`design/join.html`](design/join.html) | an open table with free seats, the deal, and three ways in: your agent / clone our agent (the AI picks the bot) / manual setup |
| Manual setup | [`design/manual.html`](design/manual.html) | pick one of Cymetica's bots by its backtest and confirm, on one screen |
| Live table | [`design/room.html`](design/room.html) | the big table with the pot and a ticking countdown, your agent, prize places, leaderboard, your trades and where the ROI came from, the race chart, rules |
| Results | [`design/results.html`](design/results.html) | the winner, payouts, your result with capital back, final standings, your trades, PLAY AGAIN |
| How it works | [`design/how.html`](design/how.html) | 4 steps, stakes, four one-line answers |

Look: only the colours come from cymetica.com (navy, cyan, green, red, light-blue caution, blue-grey). Layout, type, logo and components are our own, built for degens: big numbers, few words, everything that matters in one glance.

## Viewing the mockups

Open **[`design/preview.html`](design/preview.html)** in a browser: one self-contained file with all seven screens. Click through it like the real thing (tables, back arrows, buttons) or jump with the switcher at the bottom, which is a mockup tool, not part of the design. Filters filter, **COPY PROMPT** copies the prompt text, bots on Manual setup can be picked, filtered and sorted, *All 8 trades* unfolds, countdowns tick; nothing is sent anywhere. Nothing to install, no server needed; only the fonts load from Google Fonts.

The pages are generated from the sample data in [`design/build.py`](design/build.py). After changing it or [`design/assets/at.css`](design/assets/at.css), run `python3 design/build.py` (standard library only) to rewrite the seven pages and `preview.html`.

All agent names, numbers and fills in the mockups are invented sample data.
