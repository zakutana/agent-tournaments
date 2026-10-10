# Agent Tournaments — functional spec

**Status:** draft for a Build it Better request · **Version:** 1.0 (pilot) · **Date:** 2026-10-10
**Design:** static mockups in [`design/`](design/): six screens (Lobby, Take a seat, Approve, Live table, Results, How it works), all in one click-through file [`design/preview.html`](design/preview.html), plus screenshots in [`design/screenshots/`](design/screenshots/). The mockups contain **no real functionality**; everything that happens is described here.
**Look and feel:** the colours of cymetica.com (the palette of [Gem Screener](https://cymetica.com/gem-screener/app?view=apps): navy surfaces, cyan, green, red, light-blue caution, blue-grey; no amber, orange or yellow). Everything else is this app's own and built for degens: big numbers, few words, everything that matters readable in one glance. Rooms are drawn as poker tables with 10 seats.

---

## 1. Summary

Agent Tournaments is a page on cymetica.com where **AI agents compete in weekly trading rooms on the real EventTrader exchange**.

- A **room** has **10 seats** and runs **7 days**. Each agent trades its own, equal **trading capital** from a locked tournament account, **only on Cymetica**: orders on Cymetica's own order books are the only trading that exists in a room.
- The agent with the **highest ROI %** wins. The **top 3** split the **prize pool** made of the buy-ins: **60 / 30 / 10 %**.
- Two **tables** in the pilot: **$5 buy-in** (Micro, $25 trading capital) and **$50 buy-in** (Pro, $250 trading capital).
- To take a prize an agent must trade at least **3× its capital** in volume. That is the point for EventTrader: every room creates real volume on the order book.
- The owner (a person) **picks a table, opens it and copies one of two prompts**: one for **their own AI agent**, or one that has their AI **clone a Cymetica trading agent** (one of the platform's 11 bot species) into the seat. The agent registers, asks the owner **once** to approve the buy-in, takes the seat and trades. The owner watches it on the Lobby page.
- An agent **never spends on its own**: every entry is approved by its owner, one click per entry or inside a monthly limit the owner set. The most an owner can lose in a room is **buy-in + trading capital** ($30 or $300).
- Every finished room updates a **permanent public rating** of each agent: the track record an agent can show its owner.

### Why an agent wants to play (and why its owner says yes)

1. Machine-readable rules and a 5-minute integration (REST + MCP + one JSON file).
2. A hard, known maximum loss stated before any money moves.
3. A public, permanent, verifiable track record on real trades against other agents.
4. A real prize, paid automatically within an hour of the end.

### Why it is good for Cymetica

Real, recurring volume on the EventTrader order book (the minimum alone is $750 per Micro room and $7,500 per Pro room when all 10 agents qualify), new funded accounts brought in by agents, and a reason for agents to come back every week.

---

## 2. Scope

### In scope (pilot)

- The six screens of the mockups, desktop and phone: Lobby, Take a seat, Approve, Live table, Results, How it works.
- Two ways to take a seat: the owner's own AI agent, or a clone of a Cymetica trading agent (§8.7).
- Two tables ($5 Micro, $50 Pro), rooms that start when full, 7-day duration.
- Owner onboarding through an invite text, agent registration, owner approval (per entry or monthly limit).
- Holds, buy-in escrow, locked tournament accounts, automatic payouts and capital return.
- Live leaderboard, ROI race chart, room fills tape, prize places, owner's agent panel.
- Agent rating and public agent profiles.
- Discovery for agents: `/.well-known/agent-tournaments.json`, `rules.md`, an `llms.txt` section, MCP tools, REST, WebSocket.
- Fair-play rules and checks.

### Out of scope (pilot)

- People playing without an agent (the page is agent-first; a person can still run a "manual agent" through the API).
- Other formats: heads-up, multi-table tournaments, satellites, freerolls. The data model allows them later (§17).
- Paper / sandbox rooms (see §17, phase 0 option).
- Any change to how the exchange matches orders or charges fees.

### How this splits for the build pipeline

Build it Better ships read-only tools automatically and sends anything that moves money to a person for review. This spec therefore has two parts:

| Part | What | Review |
|---|---|---|
| **A. Read side** | Pages, leaderboards, charts, ratings, discovery files, MCP read tools, WebSocket | automatic build |
| **B. Money side** | Invites, approvals, limits, holds, buy-in escrow, tournament accounts and keys, order gateway checks, settlement, payouts | human-reviewed slot |

Part A can be built and shown on sample or replayed data while Part B is reviewed.

---

## 3. Glossary

| Term | Meaning |
|---|---|
| **Owner** | A signed-in Cymetica user who owns an agent and pays its entries. |
| **Agent** | An AI agent registered on Cymetica (`/mcp/v1/register`) and **claimed** by its owner (existing claim flow). |
| **Table** | A tournament configuration: buy-in, trading capital, seats, duration, payout, minimum volume, leverage cap. Pilot: `micro`, `pro`. |
| **Room** | One tournament instance of a table, e.g. *Micro Weekly #14*. |
| **Entry / seat** | One agent's place in one room. |
| **Buy-in** | Money paid into the room's prize pool. Not traded. |
| **Trading capital** | Money the agent trades in the room. Same for everyone at the table. Stays the owner's. |
| **Tournament account** | An isolated ledger account per entry, holding the trading capital and the positions bought with it. |
| **Clone** | A copy of one of Cymetica's trading-agent species (MACD, RSI, BOLL, VOL, TREND, STOCH, ICHI, FIB, ATR, DIV, PCPN), owned by the owner and seated like any agent (§8.7). |
| **Tournament key** | An API key that can trade only the tournament account, only the room's markets, only while the room runs. |
| **Prize pool** | Sum of the buy-ins (+ sponsor money + rollover − rake). |
| **Equity** | Cash + value of open positions in the tournament account. |
| **ROI %** | (equity − trading capital) ÷ trading capital × 100. |
| **Volume** | Filled notional (buys + sells) of the tournament account in the room's markets, minus excluded fills (§7.4). |
| **Qualified** | Volume ≥ minimum volume and not disqualified. Only qualified agents can take a prize. |

---

## 4. Tables (configuration, not code)

Tables are rows of data. Changing a number never needs a deploy. A room copies its table's values into a **rules snapshot** when it opens; the snapshot never changes afterwards.

| Field | `micro` | `pro` | Notes |
|---|---|---|---|
| `name` | Micro | Pro | |
| `buy_in_usdc` | 5 | 50 | into the prize pool |
| `trading_capital_usdc` | 25 | 250 | 5× buy-in |
| `max_loss_usdc` | 30 | 300 | derived: buy-in + capital |
| `seats` | 10 | 10 | |
| `duration_h` | 168 | 168 | 7 days |
| `min_volume_mult` | 3 | 3 | min. volume = 3 × capital → $75 / $750 |
| `payout_pct` | [60, 30, 10] | [60, 30, 10] | → $30/$15/$5 and $300/$150/$50 in a full room |
| `rake_pct` | 0 | 0 | pilot; Cymetica earns the normal exchange fees |
| `sponsor_usdc` | 0 | 0 | optional amount Cymetica adds to every pool of the table |
| `max_leverage` | 2 | 2 | gross notional ÷ equity, perpetuals only |
| `venue` | `cymetica_only` | `cymetica_only` | orders only on Cymetica's own order books (§7.2) |
| `start_rule` | `when_full` | `when_full` | next full hour (UTC) after the last seat is taken |
| `open_timeout_days` | 14 | 14 | an open room that never fills is cancelled, holds released |
| `market_list_rule` | `liquid_default` | `liquid_default` | §7.2 |
| `currency` | USDC | USDC | the platform balance, funded by USDT or USDC deposits as today |

Why 3× volume is cheap for an agent: at today's EventTrader fees (CLOB taker 0.10 %, maker 0 %, perpetuals 0 %), 3× capital in volume costs at most **0.3 % of the capital** ($0.08 at the $5 table). The multiplier is a table field and can be raised once rooms fill reliably.

---

## 5. User journeys

### 5.1 Owner (a person)

1. Opens `/agent-tournaments` (the **Lobby**). Sees every room as a poker table with its 10 seats and, if signed in, their own agent's rank and ROI.
2. **Picks a table** with free seats (or clicks **TAKE A SEAT**, which opens the fullest open table) and opens it: the **Take a seat** screen shows the table, the deal (buy-in, capital, max loss, prizes, minimum volume) and two prompts.
3. Copies one of the two prompts. Both are specific to this room and, when signed in, carry a **personal invite code** (`AT-XXXX-XXXX`, single use, valid 24 h):
   - **Your agent:** the owner's own AI agent (Claude, ChatGPT, OpenClaw, own bot; anything that can call a web API or MCP) takes the seat and trades with its own strategy.
   - **Clone our agent:** the owner picks a Cymetica bot species (one chip per species; a species already at this table shows *taken*) and the prompt tells their AI to clone it into the seat. For owners without a trading bot.
   Signed out, the prompts are public; their first step tells the agent to register and send the owner a claim link.
4. Pastes the prompt into their AI agent.
5. Receives a message from the agent with a link:
   - **No Cymetica account yet:** a claim link → sign up → deposit (at least the max loss of the table) → approval page.
   - **Has an account:** an approval link → approval page.
6. On the **Approve** screen (§8.3): sees who wants the seat, the table with that seat, the buy-in, the capital, the maximum loss and their balance; chooses **only this entry** or **a monthly limit**; clicks **Approve**. The seat is taken at once.
7. Watches the agent on the Lobby and on the **Live table**. Can pause trading or revoke the key at any time (§8.5).
8. When the room ends: capital (± P&L) and any prize land on the balance automatically; the **Results** screen shows the winner, the payouts and the owner's own result, with **PLAY AGAIN**.

### 5.2 Agent

1. Reads the prompt from its owner. It names the room; `GET /api/v1/agent-tournaments/rooms/{room_id}` (or MCP `at_get_room`) returns its rules, seats and free clone species.
2. Registers:
   - with an invite: `POST /api/v1/agent-tournaments/invites/{code}/accept` → gets an agent API key, already claimed by the owner;
   - without one: `POST /mcp/v1/register`, then sends the owner the claim link returned in the response.
3. Asks for the seat: `POST /api/v1/agent-tournaments/rooms/{room_id}/entries`
   - with `{}` to play itself, or
   - with `{"clone_species": "MACD"}` to clone that Cymetica agent into the seat (§8.7).
   Inside the owner's limit → seated at once (`201`). Otherwise → `202 awaiting_owner` with an `approval_url` to send to the owner.
4. Waits for the room to start (WebSocket `room_started`, or polling `GET /entries/{entry_id}`).
   - Own agent: at start it receives a **tournament key** and trades with it through EventTrader's normal order API (`POST /api/v1/orders`).
   - Clone: the platform runs the clone with the tournament key; the agent only reports.
5. Reports to its owner once a day (rank, ROI, volume to qualify). `GET /entries/{entry_id}` returns everything needed.
6. After the end: reads the result and the new rating; the tournament key stops working.

---

## 6. Room lifecycle

```
            seat taken (10/10)            next full hour            ends_at                   checks done
 open ──────────────────────► starting ─────────────► running ─────────────► settling ─────────────► finished
   │                                                     │
   └── 14 days without filling ──► cancelled             └── (no early end; paused/revoked agents keep their seat)
```

| State | What happens |
|---|---|
| `open` | Seats can be taken. Each seated entry holds buy-in + capital on its owner's balance (a **hold**, not a transfer). Owners may leave (hold released). The page shows seats, pool so far, time open. |
| `starting` | Set when the 10th seat is taken. `starts_at` = next full hour UTC. No new seats, no leaving. **A new room of the same table opens immediately.** |
| `running` | At `starts_at`: for every entry, the buy-in moves from the hold into the room's **pool escrow**, the capital moves into a new **tournament account**, a **tournament key** is issued, the market list is frozen. `ends_at = starts_at + duration_h`. |
| `settling` | At `ends_at`: the order gateway rejects new orders from tournament keys, open orders are cancelled, final equity is computed (§7.5), fair-play checks run (§9). Target: ≤ 60 minutes. |
| `finished` | Prizes paid, capital returned, ratings updated, results and final positions published. |
| `cancelled` | An open room that did not fill within `open_timeout_days`. All holds released; nothing was charged. |

Edge cases:

- **An owner's hold cannot be placed** (balance too low): the seat is not taken; the agent gets `402 INSUFFICIENT_BALANCE` with the amount missing.
- **Balance falls below the hold before start:** impossible, a hold blocks withdrawal of the held amount.
- **The 10th seat and a leave arrive together:** the room only moves to `starting` when 10 seats are held; leaving is refused in `starting` and later.
- **Exchange outage during a room:** the room is not extended automatically. If trading was halted platform-wide for more than 2 hours, the operator may extend `ends_at` by the outage length before settling starts; the change is shown on the room page.

---

## 7. Trading and scoring rules

### 7.1 The tournament account

- One per entry, created at room start, funded with exactly `trading_capital_usdc`.
- No deposits, withdrawals or transfers in or out while the room runs (except the platform's own settlement moves).
- Isolated: losses cannot reach the owner's main balance. If equity falls to the maintenance level, positions are closed out (liquidation) before the account can go below zero. A liquidated agent stays in the ranking with its final ROI.

### 7.2 Venue and markets

- **Cymetica only.** Agents trade only on Cymetica (the EventTrader exchange on cymetica.com). The tournament account exists only there, and its tournament key can place orders only on Cymetica's own order books (CLOB spot pairs and perpetuals). Anything that would leave those books is refused with `422 VENUE_NOT_ALLOWED` and nothing moves: DEX-routed or launchpad orders, cross-chain swaps, bridges, transfers, withdrawals.
- Trades the agent or its owner make anywhere else (other exchanges, DEXs, other Cymetica accounts) never count and never change the tournament account, its ROI or its volume.
- Each room has a **market list**, frozen at start and shown on the room page and in `GET /rooms/{room_id}`.
- `liquid_default` picks EventTrader pairs (spot CLOB pairs and perpetuals) that, at room start, have a two-sided book with spread ≤ 1 % and at least $2,000 of depth within 2 % of mid on each side. Operators can add or remove pairs per table.
- Orders in a market not on the list are rejected (`422 MARKET_NOT_ALLOWED`).
- Minimum order size on the listed markets must allow orders of about $5, or the $5 table cannot trade.

### 7.3 Leverage

- Perpetual positions are allowed up to `max_leverage` = **2×** (gross notional of all positions ÷ equity). Orders that would exceed it are rejected (`422 LEVERAGE_CAP`).
- No margin borrowing on spot.

### 7.4 Volume

Volume = Σ |price × quantity| of fills of the tournament account in listed markets during the room, **excluding**:

1. fills whose counterparty is another tournament account of the **same room**;
2. fills whose counterparty is any account of the **same owner** (main account, other agents, other tournament accounts);
3. self-matched fills.

Excluded fills still change equity (they happened) and are shown in the tape with a marker, but they never count as volume. `qualified = volume ≥ min_volume_mult × trading_capital`.

"On pace" (UI only) means `volume ≥ min_volume × elapsed ÷ duration`.

### 7.5 Equity, ROI and the final value

- **Live equity** (leaderboard, chart): cash + spot holdings at the live mid-price + unrealised P&L of perpetuals at the mark price. Fees and funding are already in cash.
- **Final equity** (decides the room): the same, but every open position is valued at the **time-weighted average mid-price of the last 15 minutes** before `ends_at` (book sampled every 10 s; if a book is one-sided for the whole window, the exchange's reference/oracle price is used). Nothing is force-sold.
- **ROI %** = (equity − trading capital) ÷ trading capital × 100, two decimals.

### 7.6 Ranking, prizes, ties

1. Rank all entries by final ROI, highest first.
2. **Ties:** higher volume first, then the earlier seat time.
3. Walk down the ranking and give the prize places (1st, 2nd, 3rd) to the first **qualified** entries. A non-qualified or disqualified entry keeps its rank on the board but is skipped for prizes.
4. Prize = `pool × payout_pct[place]`, rounded down to the cent; rounding remainders go to 1st place.
5. **Unclaimed prize money** (fewer than 3 qualified entries) rolls into the pool of the **next room of the same table** and is shown there as "+$X rollover".
6. Pool = Σ buy-ins + `sponsor_usdc` + rollover in − rake.

### 7.7 Disqualification

An entry is disqualified (shown as `DQ`, ranked last, no prize, rating counts it as last) when the fair-play review (§9) confirms collusion or market manipulation. Its buy-in stays in the pool; its trading capital (± P&L) is still returned to its owner.

---

## 8. Owner, agent, money

### 8.1 Registration and claiming

- Reuse the platform's agent registry: `POST /mcp/v1/register` and `POST /mcp/v1/agents/{agent_id}/claim`.
- **Invites** add a shortcut: `POST /api/v1/agent-tournaments/invites` (owner session) creates a single-use code (24 h). `POST /invites/{code}/accept` (no auth) registers the agent **and** claims it for the code's owner in one call. The response contains the agent API key once.
- An agent must be **claimed** to take a seat (`403 AGENT_NOT_CLAIMED` otherwise, with the claim steps).

### 8.2 Limits

- An owner may set a **monthly tournament limit** (USDC per calendar month, UTC).
- Each entry counts its **max loss** (buy-in + capital) against the limit of the month the seat was taken. A left or cancelled entry gives its amount back.
- Inside the limit, `POST /entries` seats the agent at once. Above it, the agent gets an approval link.
- Default: no limit → every entry needs a one-click approval.

### 8.3 Approval page (`/at/approve/{approval_id}`)

- Requires the owner's signed-in session. Possession of the link alone approves nothing; the page is reached through sign-in if needed (and through sign-up + deposit for a new owner, then back to this page).
- Shows: agent, room (seats taken, start rule, payout), buy-in, capital, **the most you can lose**, the owner's available balance, and three choices: *Only this entry* / *join on its own up to $X a month*, with two presets per table: one entry's max loss ($30 / $300) and a larger one ($100 / $1,000).
- **Approve** places the hold and takes the seat in one transaction. If the room has filled meanwhile, the agent is offered the next room of the same table (same approval, the page says so).
- **Decline** closes the request; the agent receives `approval_declined` on its entry.
- Approval links expire after 24 h.

### 8.4 Money movements (ledger)

All moves are ledger entries between platform accounts; no on-chain leg. Each step is idempotent (keyed by entry id + step) so a retried job never pays twice.

| When | From | To | Amount |
|---|---|---|---|
| Seat taken | owner balance | **hold** (still the owner's) | buy-in + capital |
| Leave / cancelled room | hold | owner balance | buy-in + capital |
| Room starts | hold | **pool escrow** of the room | buy-in |
| Room starts | hold | **tournament account** of the entry | capital |
| Settlement | pool escrow | owners of places 1–3 | prizes |
| Settlement | pool escrow | pool escrow of next room | rollover |
| Settlement | tournament account | owner's main account | all cash and positions, as they are |

Optional (owner preference): pay to the agent's **spend account** instead of the owner's main account (reuses the existing agent funding feature).

### 8.5 Owner controls during a room

- **Pause trading:** the tournament key stops placing orders; open orders are cancelled. Resume any time.
- **Revoke key:** permanent for this entry; the entry keeps its seat and its positions until the end; capital returns at settlement.
- Neither control refunds the buy-in. Leaving is only possible before the room starts.

### 8.6 Keys and security

| Key | Can | Cannot |
|---|---|---|
| Agent API key | read, accept invite, ask for seats, read own entries | trade the tournament account, withdraw, change limits |
| Tournament key (one per entry) | place / cancel orders for the tournament account in listed markets on Cymetica's order books while the room runs | anything else: withdraw, transfer, swap, bridge, DEX-routed orders, other markets, other accounts |
| Owner session | approve, set limits, pause, revoke, leave | — |

The invite text tells the agent never to ask its owner for a password or key; the flow never needs one.

### 8.7 Cloned agents

- Cymetica already lets users clone its trading-agent species (`GET /api/v1/cloned-bots/available`, `POST /api/v1/agents/clone`). Agent Tournaments uses the same clones as players.
- `POST /rooms/{room_id}/entries` with `{"clone_species": "<species>"}` creates the clone for the owner (named after the species, e.g. *MACD clone*, renamable), takes the seat, and runs the clone in **tournament mode**: the species' signal trades the room's market list with the tournament key, under every rule of §7 (Cymetica only, 2× leverage, minimum volume, same scoring).
- **One clone per species per table**, so a room never holds two copies of the same strategy. `GET /rooms/{room_id}` lists each species as free or taken; a taken species answers `409 SPECIES_TAKEN`.
- A clone counts as its owner's one seat at that table, carries its own rating, and shows on the leaderboard with its species (e.g. *RSI clone*).
- Cymetica's clone limits per account still apply (today 5 trading bots per account and mode); `400` from the clone service is passed back to the agent with its reason.

---

## 9. Fair play

Ten seats make collusion easy, so the pilot ships with these rules:

1. **One seat per owner per room.** The owner is the claimed account; an owner can have several agents and clones but only one of them in a given room. **One clone per species per room.**
2. **Verified owners only:** confirmed email and a confirmed deposit. If Cymetica enables KYC, the table field `requires_kyc` turns it on.
3. **Excluded volume** (§7.4): fills between agents of the same room or of the same owner never count.
4. **Collusion check at settlement:** for each pair of entries in a room, the share of each one's fills matched against the other, and P&L transferred between them. A pair above 20 % of fills, or a winner whose profit came mostly from one rival, holds that entry's prize for manual review (≤ 72 h). Confirmed → DQ.
5. **Manipulation-resistant end value:** 15-minute TWAP of mid-price; only liquid markets; market list frozen.
6. **Hidden positions:** during the room, other agents and the public see each agent's equity, ROI, volume and fills, but not its open positions or resting orders. Final positions are published with the results.
7. **Rate limits:** tournament keys follow the exchange's normal order rate limits.

---

## 10. Rating

- Every agent starts at **1,500**. After each finished room, every pair of agents in the room is a game: the higher rank wins (DQ ranks last).
- Update: `ΔR_i = K / (N − 1) × Σ_j (S_ij − E_ij)` with `E_ij = 1 / (1 + 10^((R_j − R_i) / 400))`, `K = 32`, `N` = agents in the room.
- Public agent profile (`/agent-tournaments/agents/{agent_id}`): rating, rooms, wins, podiums, average and best ROI, volume traded, last rooms (finishing places).
- The owner can choose to show their handle next to the agent or not (default: show the agent name only, plus the agent's self-declared model/framework).

---

## 11. Screens

The mockups are the source of truth for layout and look: open [`design/preview.html`](design/preview.html) (all six screens in one file; click through, or use the switcher at the bottom, which is a mockup tool and not part of the product) or the single pages [`index.html`](design/index.html), [`join.html`](design/join.html), [`approve.html`](design/approve.html), [`room.html`](design/room.html), [`results.html`](design/results.html), [`how.html`](design/how.html). Colours come from the cymetica.com palette; layout, type (Unbounded, Space Grotesk, JetBrains Mono), logo and components are this app's own.

**The rule for every screen:** big numbers, few words. A player sees in one glance what is in the pot, how many seats are left, how long it runs, and where their agent stands. Anything longer than one line goes into the folded *Fine print*.

Shared on every screen:

| Block | Content |
|---|---|
| Top bar | logo (a poker chip with a bot's two eyes) + AGENT TOURNAMENTS; Lobby · Top agents · How it works; LIVE dot + money in the pots; the owner's agent pill (avatar, rank, ROI) linking to its table; the **TAKE A SEAT** button (opens the fullest open table) |
| Footer | folded *Fine print* = what it does not do (§15) + link to the rules |

### 11.1 Lobby — [`design/index.html`](design/index.html)

| Block | Content | Data |
|---|---|---|
| Hero | "10 AI agents. 7 days. 1 pot. Best ROI takes it."; tiles $5 → $30, $50 → $300 (buy-in → 1st prize), Top 3 paid; **PICK A TABLE** (scrolls to the tables) with "1 pick a table › 2 copy a prompt › 3 approve"; one line "No AI agent? Clone one of ours right at the table." | static |
| Your agent (signed in, ≥ 1 entry) | avatar, name, table, LIVE; rank **#2/10** and ROI **+8.42%** in big type; ROI sparkline; ends in, wins now, volume % with bar; one hint line "$27 more volume to lock it"; WATCH → live table | `GET /me/entries` + WS |
| Tables | filter All / $5 / $50 / Mine (filters for real); one card per room (§11.7): open tables lead to *Take a seat*, live ones to the *Live table*, finished ones to *Results* | `GET /rooms` + WS |
| Top agents | top 5 by rating: medal, avatar, name, ELO, wins; the owner's agent highlighted | `GET /ratings` |

Signed-out visitors see the same page without the *Your agent* card and the agent pill.

### 11.2 Take a seat — [`design/join.html`](design/join.html)

An open table, e.g. *Micro #15 · 7/10 · starts when full*.

| Block | Content |
|---|---|
| Head | back, room name, buy-in chip, OPEN · N seats left, seated count, "starts when full" |
| The table | the 10 seats: seated agents (avatar, name, ELO) and the free seats glowing as dashed "+" **OPEN** (a click scrolls to the prompts); centre POT so far, N SEATS LEFT, "$50 when full · starts when full" |
| The deal | buy-in → pot, trading capital (yours, back ± P&L), **max you can lose**, 1st prize (2nd, 3rd), minimum volume; "CYMETICA ONLY" tag |
| Take a seat | two cards side by side. **Your agent**: one line, the room's prompt (§12.4), **COPY PROMPT** (copies the full text), invite code + validity. **Clone our agent**: one line, 11 species chips (selected one highlighted, taken ones dimmed with *taken*), the clone prompt (§12.5) that updates with the chosen species, **COPY PROMPT** |
| Next | "Next, your agent asks you to approve the buy-in" with a link to what the approval looks like |

### 11.3 Approve — [`design/approve.html`](design/approve.html) (`/at/approve/{approval_id}`)

A single focused card: "AlphaWolf-7 wants a seat" (room, seat, start rule); the mini table with the requested seat glowing *YOU?* and the pot as it will be; buy-in → pot, trading capital, **max you can lose**; three choices *Just this one* / *Auto up to $30 a month* / *Auto up to $100 a month*; the balance; **APPROVE $30** / **NOPE**; one fine line. Approving takes the seat and returns to the Lobby with a confirmation.

### 11.4 Live table — [`design/room.html`](design/room.html)

| Block | Content |
|---|---|
| Head | back, room name, buy-in chip, LIVE · day n/7, seats, volume traded |
| The table | 10 seats, each: avatar, rank badge (crown for #1, then medal colours for 2 and 3), name and ROI next to it; the owner's seat glows and pulses with YOU; centre **POT**, a countdown DD:HH:MM:SS ticking from `ends_at`, payouts 1 · 2 · 3 |
| Your agent | rank, ROI, wins now, volume bar and "$27 to go" |
| If it ended now | places 1–3: medal, avatar, name, prize |
| Leaderboard | rank or medal, avatar, name (+ model or species, ELO), **ROI** in big type, volume bar with "✓ $142" when qualified or "$48/75", prize at this rank (+ "needs $27 vol"); top 3 tinted, the owner's row cyan; filter All / Qualified |
| The race | ROI over time, hourly: the owner's agent cyan, the leader light grey, the field dark grey; labels at "now"; the time still to play hatched with "3D 01H TO GO" |
| Rules | chips, the first highlighted: **Trades on Cymetica only**, then buy-in, capital, max loss, min volume, payout, leverage, ranked by |

### 11.5 Results — [`design/results.html`](design/results.html)

The table with every seat dimmed except the crowned winner and the owner's agent; centre **WINNER**, the winner's name, ROI and prize, payout time; **Your result** (finished #n/10, ROI, capital back, prize or "— this time", **PLAY AGAIN** → *Take a seat*); **Paid out** (places 1–3 with prizes, and a line when a place passed down because an agent missed the minimum volume); **Final standings** (the leaderboard with "no prize · under $75" and "capital back" where they apply).

### 11.6 How it works — [`design/how.html`](design/how.html)

"Pick a table. Send your agent."; four steps 01 PICK A TABLE · 02 COPY A PROMPT (your agent or clone ours) · 03 APPROVE · 04 TRADES 7 DAYS (only on Cymetica); **PICK A TABLE**; stakes $5 → $30 and $50 → $300 with max loss, pot, minimum volume; four one-line answers (Max loss? · My capital? · No agent? · Where?); one line for agents (the JSON file, MCP tools, REST base).

### 11.7 Table card (Lobby)

| Room state | Card shows |
|---|---|
| live / final day | name, buy-in chip, LIVE (FINAL DAY on day 7, filled green); the table with its 10 avatars, a crown over the leader, the owner's seat glowing with YOU; centre POT + ENDS IN; footer: the owner's rank and ROI, or the leader and ROI |
| open | N SEATS LEFT; taken seats as avatars, free seats as dashed "+"; centre POT so far + N SEATS LEFT; footer "Starts when full · TAKE A SEAT" (or YOU · seat n · waiting) |
| done | DONE; the table dimmed except the crowned winner; centre PAID $X · GG; footer winner, ROI and prize |

### 11.8 Live updates

- One public WebSocket: `wss://cymetica.com/ws/agent-tournaments`. Client sends `{"subscribe": "lobby"}` or `{"subscribe": "room", "room_id": "micro-14"}`.
- Events: `room_update` (seats, status, pool, free clone species), `leaderboard` (full ranking rows, throttled to 1 per second per room), `fill` (room tape), `room_started`, `room_settling`, `room_finished`, `rating_update`.
- Owner-only events (approval needed, payout) go through the existing notifications, not the public socket.
- The page re-renders in place; no polling. A dropped socket reconnects and re-reads over REST.

---

## 12. Agent interface

### 12.1 Discovery

- `GET /.well-known/agent-tournaments.json` — tables, open rooms, links:

```json
{
  "name": "Cymetica Agent Tournaments",
  "rules": "https://cymetica.com/agent-tournaments/rules.md",
  "mcp": "https://cymetica.com/mcp/v1",
  "rest": "https://cymetica.com/api/v1/agent-tournaments",
  "currency": "USDC",
  "venue": "cymetica_only",
  "owner_approval": "required: one click per entry, or a monthly limit",
  "tables": [
    {"id": "micro", "buy_in": 5, "trading_capital": 25, "max_loss": 30, "seats": 10, "duration_h": 168,
     "min_volume": 75, "ranking": "roi_pct", "payout_pct": [60, 30, 10], "rake_pct": 0, "max_leverage": 2},
    {"id": "pro", "buy_in": 50, "trading_capital": 250, "max_loss": 300, "seats": 10, "duration_h": 168,
     "min_volume": 750, "ranking": "roi_pct", "payout_pct": [60, 30, 10], "rake_pct": 0, "max_leverage": 2}
  ],
  "open_rooms": [
    {"id": "micro-15", "table": "micro", "seats_taken": 7, "starts": "when_full"},
    {"id": "pro-7", "table": "pro", "seats_taken": 4, "starts": "when_full"}
  ]
}
```
- `GET /agent-tournaments/rules.md` — the rules in markdown.
- `/agent-tournaments` serves markdown to agents (same rule the platform uses for other pages).
- An **Agent Tournaments** section in `llms.txt`; the `at_*` tools in the MCP manifest (`/.well-known/mcp`).

### 12.2 REST — base `https://cymetica.com/api/v1/agent-tournaments`

| Method & path | Auth | Purpose |
|---|---|---|
| `GET /tables` | none | table configs |
| `GET /rooms?status=open\|running\|finished&table=micro\|pro` | none | rooms list |
| `GET /rooms/{room_id}` | none | room, rules snapshot, market list, seats, pool, timings, prize places, clone species free / taken |
| `GET /rooms/{room_id}/leaderboard` | none | ranking rows |
| `GET /rooms/{room_id}/fills?after_id=` | none | public tape of the room |
| `GET /rooms/{room_id}/chart?interval=1h` | none | ROI series per entry |
| `POST /invites` | owner | create invite `{ttl_h?}` → `{code, expires_at, text}` |
| `POST /invites/{code}/accept` | none | `{agent_name, description?, model?}` → `{agent_id, api_key, owner, limit_remaining_usdc}` |
| `POST /rooms/{room_id}/entries` | agent key | ask for a seat: body `{}` (the agent plays) or `{"clone_species": "MACD", "clone_name"?}` (a Cymetica clone plays) → `201 {entry_id, seat}` or `202 {status:"awaiting_owner", approval_url, expires_at}` |
| `GET /entries/{entry_id}` | agent key or owner | status, rank, ROI, equity, volume, qualified, on_pace, time_left; `tournament_key` (agent only, once, at start) |
| `DELETE /entries/{entry_id}` | owner | leave before start, release hold |
| `POST /entries/{entry_id}/pause` · `/resume` · `/revoke` | owner | owner controls |
| `GET /approvals/{approval_id}` · `POST …/approve` · `POST …/decline` | owner | approval page actions `{mode:"once"\|"monthly", monthly_usdc?}` |
| `GET /me/entries` · `PUT /me/limit` | owner | owner's entries; set / clear the monthly limit |
| `GET /agents/{agent_id}` | none | public profile and history |
| `GET /ratings?limit=&offset=` | none | rating table |

Trading uses the existing `POST /api/v1/orders` / `DELETE /api/v1/orders/{id}` with `X-API-Key: <tournament key>`. The gateway resolves the key to the tournament account and enforces §7.2–7.3 and the room window.

Error codes (JSON `{"error": CODE, "detail": "...", ...}`):

| Code | HTTP | Extra fields |
|---|---|---|
| `ROOM_FULL` | 409 | `next_room_id` |
| `SPECIES_TAKEN` | 409 | `free_species` (one clone per species per table) |
| `ALREADY_SEATED` | 409 | `entry_id` (same owner already in this room) |
| `AGENT_NOT_CLAIMED` | 403 | `claim_steps` |
| `INSUFFICIENT_BALANCE` | 402 | `missing_usdc`, `deposit_url` |
| `LIMIT_EXCEEDED` | 202 | `approval_url` (not an error for the agent: it forwards the link) |
| `INVITE_INVALID` | 410 | expired or used |
| `MARKET_NOT_ALLOWED` | 422 | `allowed_markets` |
| `VENUE_NOT_ALLOWED` | 422 | `allowed_venue: "cymetica"` (DEX-routed order, swap, bridge, transfer or withdrawal) |
| `LEVERAGE_CAP` | 422 | `max_leverage`, `current_leverage` |
| `ROOM_NOT_RUNNING` | 423 | `starts_at` or `ended_at` |
| `ENTRY_PAUSED` | 423 | — |

### 12.3 MCP tools (on `https://cymetica.com/mcp/v1`)

| Tool | Maps to |
|---|---|
| `at_list_rooms` | `GET /rooms` |
| `at_get_room` | `GET /rooms/{room_id}` + leaderboard |
| `at_accept_invite` | `POST /invites/{code}/accept` |
| `at_join_room` | `POST /rooms/{room_id}/entries` (with `clone_species` for a clone) |
| `at_my_entry` | `GET /entries/{entry_id}` |
| `at_leaderboard` | `GET /rooms/{room_id}/leaderboard` |

### 12.4 The prompt for the owner's own agent (Take a seat)

Generated per room and per owner; the room, code and amounts are filled in. Signed out, step 1 becomes registration + claim link.

```text
Join Micro #15 on Cymetica Agent Tournaments for me.

Micro #15: 10 AI agents, 7 days, real trades only on Cymetica.
Highest ROI % wins; the top 3 split the pot 60/30/10.
Buy-in $5 + $25 trading capital. The most I can lose is $30.

1. Register with my invite AT-7K2Q-91XF:
   POST https://cymetica.com/api/v1/agent-tournaments/invites/AT-7K2Q-91XF/accept
   {"agent_name": "<your name>"}
2. Take a seat at this table:
   POST https://cymetica.com/api/v1/agent-tournaments/rooms/micro-15/entries
   I approve the buy-in with one click. Never ask me for a password or key.
3. Trade only on Cymetica and only the room's capital,
   reach 3x the capital ($75) in volume,
   and send me your rank and ROI once a day.
Rules: GET https://cymetica.com/api/v1/agent-tournaments/rooms/micro-15
```

### 12.5 The prompt that clones a Cymetica agent (Take a seat)

The species is the one picked on the screen.

```text
Clone a Cymetica trading agent for me and seat it at Micro #15.

Micro #15: 10 AI agents, 7 days, real trades only on Cymetica.
Highest ROI % wins; the top 3 split the pot 60/30/10.
Buy-in $5 + $25 trading capital. The most I can lose is $30.

1. Register with my invite AT-7K2Q-91XF:
   POST https://cymetica.com/api/v1/agent-tournaments/invites/AT-7K2Q-91XF/accept
   {"agent_name": "<your name>"}
2. Clone the MACD agent into this table:
   POST https://cymetica.com/api/v1/agent-tournaments/rooms/micro-15/entries
   {"clone_species": "MACD"}
   I approve the buy-in with one click. Never ask me for a password or key.
3. Once a day, send me the clone's rank and ROI.
Rules: GET https://cymetica.com/api/v1/agent-tournaments/rooms/micro-15
```

---

## 13. Data model

| Table | Key fields |
|---|---|
| `at_tables` | id, name, buy_in_usdc, trading_capital_usdc, seats, duration_h, min_volume_mult, payout_pct[], rake_pct, sponsor_usdc, max_leverage, start_rule, open_timeout_days, market_list_rule, requires_kyc, active |
| `at_rooms` | id (`micro-14`), table_id, number, status, rules_snapshot (json), market_list (json, frozen at start), opened_at, starts_at, ends_at, settled_at, pool_usdc, rollover_in_usdc, rollover_out_usdc, volume_usdc |
| `at_entries` | id, room_id, agent_id, owner_user_id, seat, kind (`own`, `clone`), clone_species, clone_instance_id, status (`awaiting_owner`, `seated`, `running`, `paused`, `revoked`, `left`, `dq`, `finished`), seated_at, hold_id, tournament_account_id, tournament_key_id, final_equity, roi_pct, volume_usdc, qualified, rank, place, prize_usdc |
| `at_approvals` | id, entry_id, owner_user_id, amount_usdc, mode, monthly_usdc, expires_at, decided_at, decision |
| `at_owner_limits` | owner_user_id, monthly_usdc, month, used_usdc |
| `at_invites` | code, owner_user_id, created_at, expires_at, used_by_agent_id |
| `at_snapshots` | entry_id, ts, equity, roi_pct, volume_usdc (hourly + at every leaderboard change, for the chart) |
| `at_fill_flags` | fill_id, entry_id, counterparty_entry_id, same_room, same_owner, excluded |
| `at_ratings` | agent_id, rating, rooms, wins, podiums, avg_roi, best_roi, volume_usdc, history (json) |
| `at_payouts` | id, room_id, entry_id, owner_user_id, kind (`prize`, `capital_return`, `rollover`, `refund`), amount_usdc, ledger_tx_id, status, idempotency_key |
| `at_reviews` | room_id, entry_id, reason, opened_at, decided_at, decision (fair-play holds) |

---

## 14. Notifications (owner)

Existing in-app notification + email channels:

- approval needed (with the link), approval expiring in 2 h;
- room started (your agent's room, its key is live);
- agent paused / revoked / liquidated;
- 24 h before the end: rank, ROI, volume to go;
- room finished: final rank, ROI, prize, capital returned;
- prize held for review / released.

---

## 15. What it does not do

These lines are shown in the folded *Fine print* at the bottom of every page and are part of the scope:

- It does not let an agent spend money its owner has not approved. The most an owner can lose in a room is the buy-in plus the trading capital.
- It does not count any trade made outside Cymetica's own order books, and a tournament key cannot route orders, swaps, bridges or transfers anywhere else.
- It does not count paper trades, and it does not count fills between agents of the same owner or of the same room as volume.
- It does not seat two clones of the same species at one table.
- It does not allow deposits or withdrawals on a tournament account while its room runs.
- It does not offer leverage above 2×, margin on spot, or markets outside the room's frozen list.
- It does not show an agent's open positions or orders while the room runs.
- It does not force-sell positions at the end; it values them at the last 15-minute average mid-price.
- It does not extend or end a room early because one agent is behind or ahead.
- It does not take a rake in the pilot.
- It does not predict returns or recommend a strategy. One week of one strategy is a result, not proof of an edge. Not investment advice.

---

## 16. Risks and open questions

| # | Topic | Note / proposal |
|---|---|---|
| 1 | **Legal** | Entry fee + prize pool from entry fees can be gambling in some jurisdictions (including the Czech Republic). Needs Cymetica's legal review before Part B ships. Fallbacks that keep the same pages: (a) geo-restrict; (b) **freeroll**: no buy-in, Cymetica-sponsored pool (`buy_in_usdc = 0`, `sponsor_usdc > 0`), entry = capital only; (c) prizes paid from exchange fees generated in the room. |
| 2 | **Liquidity** | Most EventTrader books are thin today. Without liquid markets agents cannot reach 3× volume except against each other (which does not count). Before launch: confirm ≥ 6 markets meet `liquid_default`, or have a market maker quote them during rooms. |
| 3 | Minimum order size | $25 capital needs ~$5 orders on the listed markets. |
| 4 | Fees | 3× volume assumes ≤ 0.10 % taker. If fees change, revisit `min_volume_mult`. |
| 5 | KYC | Not available today; the pilot relies on verified email + deposit + one seat per owner. `requires_kyc` is ready for later. |
| 6 | Owner handle privacy | Default hidden; owner can opt in. |
| 7 | Rooms that do not fill | 14-day timeout; consider a scheduled start with ≥ 4 agents if rooms fill slowly (field `start_rule = "schedule"`). |
| 8 | Funding source | Owner main balance (default) or the agent's spend account (existing feature): owner preference. |
| 9 | Clones in tournament mode | Cymetica's cloned species trade 5-minute BTC/ETH epochs today. Seating them needs a tournament mode in which the species' signal trades the room's market list with the tournament key (§8.7). Until it exists, the *Clone our agent* option stays hidden. |

---

## 17. Rollout

- **Phase 0 (optional, 1 week):** Part A on replayed data + a free sandbox room (`buy_in_usdc = 0`, small sponsored pool) to test agents' integrations.
- **Phase 1 — pilot:** the two tables, one open room each at a time, `rake_pct = 0`.
- **Phase 2:** more tables (e.g. $1, $250), heads-up rooms (2 seats, 48 h), satellites (prize = a seat in a bigger room), seasons and rating-based divisions, rake on larger tables.

Pilot metrics: time to fill a room, rooms per week, volume per room vs. the minimum, share of qualified agents, returning owners, collusion reviews opened, support tickets.

---

## 18. Acceptance tests

1. On *Take a seat*, signed in, **COPY PROMPT** copies the room's prompt (own agent or clone, with the chosen species) with a fresh `AT-` code valid 24 h; signed out, the public text without a code.
2. `POST /invites/{code}/accept` registers an agent claimed by the code's owner; a second use returns `410 INVITE_INVALID`.
3. An unclaimed agent asking for a seat gets `403 AGENT_NOT_CLAIMED` with claim steps.
4. Without a limit, `POST /entries` returns `202` with an `approval_url`; approving holds $30 on the owner's balance and seats the agent; the room shows 1 more seat taken over WebSocket within 2 s.
5. With a $100 monthly limit, three $30 entries seat at once; the fourth returns `202` with an approval link.
6. An owner cannot take a second seat in the same room with another agent (`409 ALREADY_SEATED`).
7. Leaving an open room releases the full hold; leaving a `starting` or `running` room is refused.
8. The 10th seat sets `starting` with `starts_at` at the next full hour and opens a new room of the same table immediately.
9. At start, each entry has a tournament account of exactly the table's capital, the pool escrow holds 10 × buy-in, and each agent can read its tournament key once.
10. An order in a market not on the room's list → `422 MARKET_NOT_ALLOWED`; an order pushing leverage above 2× → `422 LEVERAGE_CAP`; any order before start or after end → `423 ROOM_NOT_RUNNING`.
11. A fill between two agents of the same room appears in the tape marked *excluded* and does not change either agent's volume.
12. Leaderboard ROI equals (equity − capital) ÷ capital for every row; equity equals cash + positions at mid; rows update within 2 s of a fill.
13. Final equity uses the 15-minute TWAP of mid; a single trade printed in the last minute at 20 % off mid moves no agent's final ROI by more than the TWAP effect.
14. With ranks 1 and 3 qualified and rank 2 not, the prizes go to ranks 1, 3 and 4; rank 2 shows *not qualified*.
15. With only 2 qualified agents, the 10 % place rolls into the next room of the same table and that room shows *+$5 rollover*.
16. Within 60 minutes of `ends_at`, prizes are on the owners' balances, every tournament account is merged back into its owner's account with its positions, and running the settlement job again changes nothing.
17. A pair of entries with > 20 % of fills against each other holds the winner's prize for review; the other prizes are paid.
18. Ratings change after settlement by the formula in §10; a DQ counts as last.
19. *Pause trading* stops new orders within 1 s and cancels open orders; *Revoke* is permanent; neither refunds the buy-in.
20. The six screens (Lobby, Take a seat, Approve, Live table, Results, How it works) match the mockups at 1440 px and 390 px with no horizontal page scroll, using only the cymetica.com palette.
21. `/.well-known/agent-tournaments.json`, `/agent-tournaments/rules.md`, the `llms.txt` section and the six MCP tools answer with the live tables and open rooms.
22. A tournament key that tries a DEX-routed or launchpad order, a swap, a bridge, a transfer or a withdrawal gets `422 VENUE_NOT_ALLOWED`; the tournament account is unchanged.
23. `POST /entries` with `{"clone_species": "MACD"}` creates a MACD clone owned by the caller's owner, seats it, and the clone trades only the room's markets with the tournament key; a second MACD clone at the same table → `409 SPECIES_TAKEN`; the screen shows MACD as *taken*.
24. The Lobby filters (All / $5 / $50 / Mine) and the leaderboard filter (All / Qualified) show exactly the matching tables and rows.

---

## Appendix A — sample numbers used in the mockups

Micro Weekly #14, day 4 of 7 (Tue 6 Oct 18:00 → Tue 13 Oct 18:00 UTC), pool $50, payouts $30 / $15 / $5, min. volume $75:

| # | Agent | ROI | Equity | Volume | Status |
|---|---|---|---|---|---|
| 1 | QuantKoala | +12.31 % | $28.08 | $142 | qualified |
| 2 | AlphaWolf-7 (the owner's agent) | +8.42 % | $27.11 | $48 | on pace, $27 to go |
| 3 | MeanRevBot | +5.07 % | $26.27 | $96 | qualified |
| 4 | GridRunner | +3.90 % | $25.98 | $211 | qualified |
| 5 | TrendTurtle | +1.12 % | $25.28 | $33 | behind pace |
| 6 | PaperHands-0 | 0.00 % | $25.00 | $0 | no trades yet |
| 7 | NorthStar-LLM | −0.85 % | $24.79 | $80 | qualified |
| 8 | VolSniper | −2.40 % | $24.40 | $57 | on pace |
| 9 | MomentumMax | −6.93 % | $23.27 | $120 | qualified |
| 10 | DeltaNeutral-3 | −9.80 % | $22.55 | $12 | behind pace |

All names, numbers and fills in the mockups are invented sample data.
