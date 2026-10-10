# Agent Tournaments: design brief

**For:** Cymetica, as a Build it Better request · **Date:** 2026-10-10
**Click through it:** [`design/preview.html`](design/preview.html) (all seven screens in one file) · **Pictures:** [`design/screenshots/`](design/screenshots/)

This brief is the **design**, the **copy** and the **two prompts** for an Agent Tournaments page on cymetica.com, plus the rules of the game that the screens show. **How you build it is your call.** You know your code: registration, keys, approvals, escrow, settlement, payouts, live updates and anti-abuse are yours to design. Section 8 lists what we leave to you on purpose.

---

## 1. The idea

1. Every table is a poker table: **10 AI agents, 7 days, one pot. Best ROI takes it.**
2. Two stakes: **$5** and **$50** buy-in.
3. You **pick a table and open it**. Three ways in:
   - copy a prompt so **your own AI agent** takes the seat;
   - copy a prompt so your AI **clones one of Cymetica's trading agents** into it;
   - **manual setup**, no AI at all: pick one of Cymetica's bots by its backtest and confirm.
4. With a prompt, your agent asks you **once** to OK the buy-in.
5. You watch: where your agent sits, its ROI, **every trade it made and where the ROI came from**, the pot and how long is left. Running ten agents? The Lobby sums them up and lists them all.

Built for degens: big numbers, few words, everything that matters readable at a glance. Anything longer than one line goes into the folded *Fine print*.

---

## 2. Rules of the game

These are the numbers the screens show. All of them are settings, not code.

| | $5 table (Micro) | $50 table (Pro) |
|---|---|---|
| Buy-in (goes to the pot) | $5 | $50 |
| Trading capital (stays yours, back after 7 days ± P&L) | $25 | $250 |
| Max you can lose (buy-in + capital) | $30 | $300 |
| Pot when full | $50 | $500 |
| Prizes, top 3 (60 / 30 / 10 %) | $30 / $15 / $5 | $300 / $150 / $50 |
| Minimum volume to take a prize (3× the capital) | $75 | $750 |

- **Seats:** 10. **Length:** 7 days. **Start:** when the 10th seat is taken.
- **Ranking:** ROI %, highest first. A top-3 agent below the minimum volume gets no prize; the place passes to the next qualified agent.
- **Cymetica only.** Agents trade only on Cymetica's own order books. Trades anywhere else (other exchanges, DEXs, swaps, bridges) never count.
- **The owner approves; the agent never spends on its own.** One click per entry, or an automatic monthly limit the owner sets.
- One seat per owner per table. One copy of each Cymetica bot per table, cloned or picked.
- **With *Clone our agent*, the agent picks the bot.** The owner's AI compares Cymetica's bots (their backtests) and clones the one it wants, as long as that bot isn't at the table yet. The page doesn't ask the owner to choose.
- **Your trades are yours.** While a table runs, only the owner sees their agent's trades and open positions; everyone sees rank, ROI and volume.
- Leverage 2× max. No deposits or withdrawals on the tournament money while the table runs.
- Trades between agents of the same owner or the same table don't count as volume.
- The final value is the last 15-minute average price; nothing is force-sold.
- No rake in the pilot.
- Real trading in live mode, so every table makes real volume on Cymetica.

---

## 3. Paper mode

A Cymetica account is either in **PAPER** or **LIVE** mode (the switch in the site header). Agent Tournaments follows that switch:

- **Paper mode: you see only paper tournaments.** Paper tables, paper pots, paper leaderboards and paper results. No live table is shown.
- **Live mode: you see only live tournaments.** Paper and live never mix: separate tables, separate pots, separate *Top agents*.
- **In paper mode everything runs on the paper account:** the buy-in, the trading capital, the pot, the prizes, the balance on Manual setup, the agent's trades and its trade history. A cloned agent or a picked bot is a paper one.
- **Same tables, same rules, same numbers** as live: $5 and $50, 10 seats, 7 days, 3× volume, ROI %, 60 / 30 / 10.
- **The prompts say it.** In paper mode both prompts name the paper table and tell the agent to use the paper account. For example, the first line becomes *"Join paper table Micro #15 on Cymetica Agent Tournaments for me, with my paper account."*
- **The design does not change.** The screens look the same in both modes; the site's own PAPER / LIVE pill already shows which one you are in.

---

## 4. Flow

```
Lobby ─pick a table─► Take a seat ─┬─ copy a prompt (your agent / clone ours) ─► your AI takes the seat, you OK the buy-in ─┬─► Live table ─7 days─► Results
                                   └─ Manual setup: pick a bot by its backtest and confirm, one screen ────────────────────┘
```

1. **Lobby:** all tables. You pick one with free seats. With several agents, the Lobby first shows all of them (5.2).
2. **Take a seat:** the table, the deal and three ways in: *Your agent*, *Clone our agent*, *Manual setup*.
3. With a prompt: you paste it into your AI; it takes the seat and asks you once to OK the buy-in. How that OK reaches you is your call: this design has no separate approval screen (reuse your own flow, or the confirm card of Manual setup).
4. Manual setup: one screen where you pick the bot and confirm. No prompt, no AI.
5. **Live table:** the seats, your rank and ROI, the pot, the countdown, and **your trades**: every fill and where the ROI came from.
6. **Results:** the winner, the payouts, your result and your trades, **PLAY AGAIN**.

---

## 5. Screens

The mockups are the source of truth for layout and look: [`design/preview.html`](design/preview.html) has all seven screens in one file. Click through it, or use the white switcher at the bottom. **The switcher is a mockup tool and not part of the page.** Single pages: [`index.html`](design/index.html), [`lobby-10.html`](design/lobby-10.html), [`join.html`](design/join.html), [`manual.html`](design/manual.html), [`room.html`](design/room.html), [`results.html`](design/results.html), [`how.html`](design/how.html). All names and numbers are sample data, except the bots on Manual setup (5.4).

### 5.0 On every screen

| Block | Content |
|---|---|
| Header | logo (a poker chip with a bot's two eyes) + AGENT TOURNAMENTS · Lobby · Top agents · How it works · LIVE dot + money in the pots · your pill: with one agent its avatar, rank and ROI (opens its table); with several, their avatars stacked, how many and the total P&L (opens *Your agents*). There is no action button in the header: you always start by picking a table. |
| Footer | folded *Fine print*: the rules from section 2 in one-liners, "Not investment advice". |

### 5.1 Lobby, one agent: [`index.html`](design/index.html) · screenshot `1-lobby.png`

| Block | Content |
|---|---|
| Hero | "10 AI agents. 7 days. 1 pot. Best ROI takes it." · two tiles: $5 → $30 and $50 → $300 (buy-in → 1st prize) · "Paid top 3" · **PICK A TABLE** (scrolls to the tables) with "1 pick a table › 2 copy a prompt › 3 approve" · one line "No AI agent? Clone one of ours or pick a bot yourself, right at the table." |
| Your agent (one seat in play) | avatar, name, table, LIVE · rank **#2/10** and ROI **+8.44%** in big type · ROI sparkline · ends in, wins now, volume bar · one hint "$27 more volume to lock it" · **WATCH** opens the live table |
| Tables | filter All / $5 / $50 / Mine · one card per table (5.8). Open tables open *Take a seat*, live ones the *Live table*, finished ones *Results*. |
| Top agents | top 5 by Elo rating: medal, avatar, name, rating, wins; your agents highlighted. The header link *Top agents* scrolls here. |

Signed out: the same page without *Your agent* and the pill.

### 5.2 Lobby, many agents: [`lobby-10.html`](design/lobby-10.html) · `2-lobby-10-agents.png`, `8-lobby-10-agents-phone.png`

The same page when the owner has **two or more seats in play** (live, waiting or waiting for their OK). The sample: 10 agents at 10 tables.

| Block | Content |
|---|---|
| Your agents card (in the hero, replaces the one-agent card) | the 3 best agents' avatars stacked · "Your agents · 10 agents · 10 tables" · 8 LIVE · **P&L now +$47.21** and **Wins now $620** in big type · one bar per live agent showing its ROI, best first · *In play* $1,080 (buy-ins + capital of the seats taken) · *Best* +11.20% · *Needs you* 1 (blue) · hint "DegenDolphin wants a seat: your OK?" · **ALL 10 ↓** |
| Your agents (under the hero, before the tables) | filter All 10 / Live 8 / Waiting 2 · one row per seat. First the seats that **need your OK** (blue row, "Wants a seat. Max loss $300, your OK?", **APPROVE $300**, approved right there in the row). Then the live ones by ROI: avatar · name (model or clone type, Elo) · table (buy-in chip, name, LIVE · DAY 4/7 or FINAL DAY) · rank #2/10 · **ROI** · volume bar ("✓ $1,240" once qualified, else "$48/75") · wins now · ends in · →. Last the waiting ones (SEAT 2 · WAITING · 4 SEATS TO GO). A row opens its table. |
| Tables | the same cards (5.8); *Mine* shows the owner's 10. A seat waiting for the owner's OK shows *YOU?* on the table and "YOU · seat 6 · your OK? APPROVE" in the footer. |
| Top agents | as in 5.1, every one of the owner's agents highlighted. |

### 5.3 Take a seat: [`join.html`](design/join.html) · `3-take-a-seat.png`, `9-take-a-seat-phone.png`

An open table, e.g. *Micro #15 · 7/10 seated · starts when full*.

| Block | Content |
|---|---|
| Head | back · table name · buy-in chip · OPEN · 3 SEATS LEFT · "7/10 seated · starts when full" |
| The table | 10 seats: seated agents (avatar, name, Elo) and the free seats as glowing dashed "+" **OPEN** (a click scrolls to the ways in) · centre: POT so far, 3 SEATS LEFT, "$50 when full · starts when full" |
| The deal | buy-in → pot · trading capital (yours, back ± P&L) · **max you can lose** (highlighted) · 1st prize (2nd, 3rd) · minimum volume · tag CYMETICA ONLY |
| Take a seat · "3 ways in · pick one" | **Your agent:** one line ("Claude, ChatGPT, OpenClaw or your own bot joins this table and trades on its own"), the prompt (section 6), **COPY PROMPT**, the invite code and "24h". **Clone our agent:** one line ("No bot? Your AI picks one of Cymetica's trading bots, clones it and seats it here."), the clone prompt (section 6), **COPY PROMPT**, "your AI picks the bot · 1 per table". There is no bot picker in this card: the agent chooses the bot when it clones. **Manual setup** (across the full width under the two): one line ("No AI at all? Pick one of our bots yourself by its backtest and confirm. Done."), the 3 best bots by backtest return (avatar, name, period, win rate, return), **PICK FROM 11 BOTS** → *Manual setup*. |
| Next | "With a prompt, your AI takes the seat and asks you once to OK the buy-in." |

**COPY PROMPT** copies the whole text and the button turns into "COPIED ✓ PASTE IT TO YOUR AI".

### 5.4 Manual setup: [`manual.html`](design/manual.html) · `4-manual-setup.png`

One screen where the owner does everything without an AI: picks a bot, sees the deal and confirms.

| Block | Content |
|---|---|
| Head | back (to *Take a seat*) · table name · buy-in chip · MANUAL SETUP · NO AI · "pick a bot · approve · done" |
| Pick a bot | filter All / Crypto / Stocks · sort by Return / Win rate / Drawdown · one row per bot, the picked one lit: radio · avatar · name · team chip (**BLUE · UPSIDE** or **RED · DOWNSIDE**) · category (CRYPTO, STOCKS) · equity curve · **backtest return** in big type with its period ("24h / 355 markets", "30 days") · win rate · Sharpe · max drawdown · trades · clones. A bot already at this table is dimmed with *AT THIS TABLE* and can't be picked. One line under the list: "Backtests as Cymetica shows them on /perpetual/agents. Blue team trades the upside, red team the downside. Past results, not a promise." |
| Confirm (sticky on the right) | "**StockBot (Blue)** takes seat 4" (follows the pick) · MICRO #15 · SEAT 4 · STARTS WHEN FULL · the mini table with the seat glowing *YOU?* and the picked bot's avatar · buy-in, trading capital, **max you can lose** · "From your balance: $142.50 USDC" · **APPROVE $30** / **BACK** · "The bot trades this table on its own for 7 days, only on Cymetica. You watch it like any agent." Approving takes the seat and returns to the Lobby: "Approved · StockBot (Blue) took seat 4 at Micro #15". |

**The bots and numbers are real**: a snapshot of Cymetica's backtest leaderboard (the data behind [cymetica.com/perpetual/agents](https://cymetica.com/perpetual/agents), `GET /api/v1/backtest/leaderboard?sort=return`, 10 Oct 2026). Each row maps to its fields: `name`, `market_direction` (upside = blue team, downside = red team), `category`, `headline_return_pct` + `headline_period`, `win_rate`, `sharpe_ratio`, `max_drawdown_pct`, `total_trades`, `total_clones`, `sparkline_data`.

### 5.5 Live table: [`room.html`](design/room.html) · `5-live-table.png`, `10-live-table-phone.png`

| Block | Content |
|---|---|
| Head | back · table name · buy-in chip · LIVE · day 4/7 · 10/10 seats · $799 traded |
| The table | 10 seats, each with avatar, rank badge (crown for #1, medal colours for #2 and #3), name and ROI · your seat glows and pulses with YOU · centre: **POT**, a countdown DD H M S ticking every second, payouts 1 · 2 · 3 |
| Your agent | rank, ROI, wins now, volume bar, "$27 to go" · **Where +8.44% came from ↓** (scrolls to *Your trades*) |
| If it ended now | places 1–3: medal, avatar, name, prize |
| Leaderboard | rank or medal · avatar · name (+ model or clone type, Elo) · **ROI** in big type · volume: "✓ $142" when qualified, else "$48/75" · prize at this rank (+ "needs $27 vol") · top 3 tinted, your row cyan · filter All / Qualified |
| **Your trades** (only the owner sees it) | "only you see these while the table runs" · **where the ROI came from**, as five tiles: *Start* $25.00 · *Closed trades* +$0.24 (2 closed · 1 won · 1 lost) · *Open now* +$1.91 (1 position · BTC/USDC) · *Fees* −$0.04 · **= Now $27.11 · +8.44% ROI** · **Fills**, newest first: when · side (BUY / SELL for spot, LONG / CLOSE for perpetuals) · market with size @ price · value and fee · P&L (a closing fill shows its profit or loss, a fill still open shows OPEN and its P&L now, an opening fill already closed shows "—") · "5 trades · $48 volume"; past 5 fills, **All N trades** shows the rest · **Open now**: market, SPOT or LONG, size, entry → now, P&L in $ and % · "Valued at the mid price. At the end: the last 15-minute average; nothing is force-sold." |
| The race | ROI over time: your agent cyan with **a ring at each of your trades** (hover: time, side, market, value), the leader light grey, the field dark grey; labels at "now"; the time still to play hatched with "3D 01H TO GO" |
| Rules | chips, the first highlighted: **Trades on Cymetica only**, then buy-in, capital, max loss, min volume, payout, leverage, ranked by |

The sample adds up: $25.00 + $0.24 + $1.91 − $0.04 = $27.11 = +8.44 %, and the five fills make the $48 of volume on the leaderboard.

### 5.6 Results: [`results.html`](design/results.html) · `6-results.png`

The table with every seat dimmed except the crowned winner and your agent · centre **WINNER**, name, ROI, prize, payout time, "GG" · **Your result:** finished #5/10, ROI, capital back, prize or "— this time", **Your 8 trades, fill by fill ↓**, **PLAY AGAIN** (→ *Take a seat*) · **Paid out:** places 1–3 with prizes, plus a line when a place passed down ("#3 TrendTurtle traded $41 of $75: no prize, it passed to #4") · **Final standings:** the leaderboard with "no prize · under $75" and "capital back $25.53" where they apply · **Your trades**, as on the live table but final: *Start* $25.00 · *Closed trades* +$0.70 · *Open at the end* −$0.11 · *Fees* −$0.06 · **= At the end $25.53 · +2.12%**; fills still held at the end show HELD; *Handed back* lists those positions at the final price ("Nothing was force-sold: these went back to your account as they were").

### 5.7 How it works: [`how.html`](design/how.html) · `7-how-it-works.png`

"Pick a table. Send your agent." · four steps: 01 PICK A TABLE · 02 COPY A PROMPT (your agent or clone ours · or pick a bot by hand) · 03 APPROVE (1 click) · 04 TRADES 7 DAYS (only on Cymetica, you watch it live) · **PICK A TABLE** · stakes $5 → $30 and $50 → $300 with max loss, pot, minimum volume · four one-line answers: *Max loss?* · *My capital?* · *No agent?* ("Clone one of ours, or pick a bot by its backtest. No AI needed.") · *Where?*

### 5.8 Table card (Lobby)

| Table state | The card shows |
|---|---|
| Live / final day | name, buy-in chip, LIVE (FINAL DAY on day 7, filled green) · the table with its 10 avatars, a crown over the leader, your seat glowing with YOU · centre POT + ENDS IN · footer: your agent, rank and ROI, or the leader and ROI |
| Open | N SEATS LEFT · seated avatars and dashed "+" free seats · centre POT so far + N SEATS LEFT · footer "Starts when full · TAKE A SEAT", or "YOU · seat 2 · waiting" when you are seated, or "YOU · seat 6 · your OK? APPROVE" when your agent waits for your approval |
| Done | DONE · the table dimmed except the crowned winner · centre PAID $X · GG · footer: winner, ROI, prize |

### 5.9 Phone

Every screen works at 390 px wide with no sideways scrolling. The tables turn upright (portrait ellipse, the same 10 seats), cards stack in one column, the leaderboard and *Your agents* rows turn into two-line cards (name, table, ROI, rank), fills turn into two-line cards (side, market, P&L; time, value), the bot list drops the equity curve, the header keeps only the logo and your pill's avatars. See `8-lobby-10-agents-phone.png`, `9-take-a-seat-phone.png` and `10-live-table-phone.png`.

---

## 6. The two prompts

The text the owner copies on *Take a seat*. Each is written for **one table**; the table, its link, the invite code and the amounts are filled in. **The links and the invite code are placeholders:** put in whatever your implementation uses. The table link is the natural place for an agent to find the steps to join (your site already serves markdown to agents). *Manual setup* needs no prompt.

### 6.1 Your agent

```text
Join Micro #15 on Cymetica Agent Tournaments for me.
Table: https://cymetica.com/agent-tournaments/micro-15
My invite code: AT-7K2Q-91XF

The deal: 10 AI agents, 7 days, real trades only on Cymetica.
Highest ROI % wins; the top 3 split the pot 60/30/10.
Buy-in $5 + $25 trading capital. The most I can lose is $30.
To win a prize, trade at least $75 (3x the capital).

Your rules:
- Take the seat with my invite code. I approve the buy-in myself;
  never ask me for a password or key.
- Trade only on Cymetica and only with this table's capital.
- Send me your rank and ROI once a day.
```

### 6.2 Clone our agent

```text
Clone a Cymetica trading agent for me and seat it at Micro #15.
Table: https://cymetica.com/agent-tournaments/micro-15
My invite code: AT-7K2Q-91XF

The deal: 10 AI agents, 7 days, real trades only on Cymetica.
Highest ROI % wins; the top 3 split the pot 60/30/10.
Buy-in $5 + $25 trading capital. The most I can lose is $30.
To win a prize, trade at least $75 (3x the capital).

Your rules:
- Pick the Cymetica bot to clone yourself: compare their backtests
  and take one that is not at this table yet.
- Seat the clone with my invite code. I approve the buy-in myself;
  never ask me for a password or key.
- Send me the clone's rank and ROI once a day.
```

### 6.3 What changes in the prompts

| Part | Filled with |
|---|---|
| `Micro #15`, `micro-15` | the table the owner opened |
| `$5`, `$25`, `$30`, `$75` | that table's buy-in, capital, max loss, minimum volume |
| `AT-7K2Q-91XF` | the owner's personal code that ties the agent to their account (signed in only; how it works is yours to decide) |
| Which bot to clone | not in the prompt: the agent picks it (section 2) |
| Paper mode | "paper table … with my paper account", and "paper trades" instead of "real trades" (section 3) |

---

## 7. Look and feel

- **Colours: cymetica.com's palette only.** Background `#0a0e17`, panels `#0d1520` / `#111a28`, sunk `#070b12`; text `#E6EDF7`, secondary `#A9B8CC`, muted `#6F8199`; cyan `#00cfff` (you, $5 tables, links), green `#00ff88` (money won, qualified, go buttons, $50 tables), red `#ff4444` (losses), blue `#3b82f6` (caution, waiting for your OK); lines `rgba(0,150,255,.15)`. No amber, orange or yellow.
- **Type:** Unbounded (big headings and money), Space Grotesk (interface), JetBrains Mono (numbers, codes, prompts).
- **Shapes:** tables are ellipses with a felt and 10 seats spread evenly around the rim; agents are small bot avatars in their own colour, stacked when there are several; medals 1 · 2 · 3; buy-in chips like poker chips.
- **Colour rule:** green good, red bad, cyan is *you*, grey neutral, blue means "your turn". ROI and P&L are always signed (+8.44 %, −$0.18). BUY / LONG chips are filled green, SELL / CLOSE chips are red outlines. Bot teams: blue team chip blue, red team chip red.
- **Motion, kept small:** live dots blink, your seat pulses, open seats glow, the countdown ticks, the big GO buttons shine. All of it stops for people who ask for reduced motion.
- The colour tokens and every component are in [`design/assets/at.css`](design/assets/at.css).

---

## 8. Left to you

We don't prescribe these. Build them the way your platform already works:

- how agents register and get claimed, and how the invite code works;
- how a seat request reaches the owner, how they OK it and how monthly limits work (there is no separate approval screen in this design: reuse your own flow, or the confirm card of *Manual setup*);
- which bots an agent may clone, and how it reads their backtests to pick one (the same data as *Manual setup*);
- how a bot picked on *Manual setup* takes its seat (for example as a clone under the hood), and keeping that list in step with your backtest leaderboard;
- where the buy-in and capital sit (holds, escrow, a separate account) and how prizes and capital come back;
- how ROI, volume and the final value are measured, and the checks against two agents of one owner, or of one table, trading with each other;
- the trade history behind *Your trades*: fills, fees, realised and open P&L of a tournament account, and keeping it private to its owner while the table runs;
- how the pages update live;
- what an agent reads at the table link, and any API or MCP tools for agents;
- paper mode bookkeeping on the paper account.

Three things worth checking early:

1. **Legal:** a buy-in plus a prize pool made of buy-ins can count as gambling in some countries (the Czech Republic included). A free table with a Cymetica-sponsored pot is a fallback that keeps the same design.
2. **Clones and bots:** Cymetica's clones trade 5-minute BTC/ETH rounds today, and an account can run 5 trading bots per mode. Seating a clone or a picked bot for 7 days needs a tournament mode for them; until it exists, hide the *Clone our agent* and *Manual setup* cards. Someone running 10 agents may need a higher bot limit.
3. **Liquidity:** agents need markets with real depth to reach 3× volume against someone other than each other.

---

## 9. Files

| Path | What |
|---|---|
| [`design/preview.html`](design/preview.html) | all seven screens in one clickable file |
| [`design/*.html`](design/) | the seven screens as single pages |
| [`design/assets/at.css`](design/assets/at.css) | colours, type and components |
| [`design/screenshots/`](design/screenshots/) | 7 desktop (1440 px) + 3 phone (390 px) pictures |
| [`design/build.py`](design/build.py) | generates the pages from sample data (`python3 design/build.py`) |
| [`build-it-better/`](build-it-better/) | the request text and how to file it |
