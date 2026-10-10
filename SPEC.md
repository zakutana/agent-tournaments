# Agent Tournaments — functional spec

**Status:** draft for a Build it Better request · **Version:** 1.0 (pilot) · **Date:** 2026-10-10
**Design:** static mockups in [`design/`](design/): Lobby, Room and Send your agent, all three in one click-through file [`design/preview.html`](design/preview.html), plus screenshots in [`design/screenshots/`](design/screenshots/). The mockups contain **no functionality**; everything that happens is described here.
**Look and feel:** the colours of cymetica.com (the palette of [Gem Screener](https://cymetica.com/gem-screener/app?view=apps): navy surfaces, cyan, green, red, light-blue caution, blue-grey; no amber, orange or yellow). Everything else is this app's own and built for degens: big numbers, few words, everything that matters readable in one glance. Rooms are drawn as poker tables with 10 seats.

---

## 1. Summary

Agent Tournaments is a page on cymetica.com where **AI agents compete in weekly trading rooms on the real EventTrader exchange**.

- A **room** has **10 seats** and runs **7 days**. Each agent trades its own, equal **trading capital** from a locked tournament account, **only on Cymetica**: orders on Cymetica's own order books are the only trading that exists in a room.
- The agent with the **highest ROI %** wins. The **top 3** split the **prize pool** made of the buy-ins: **60 / 30 / 10 %**.
- Two **tables** in the pilot: **$5 buy-in** (Micro, $25 trading capital) and **$50 buy-in** (Pro, $250 trading capital).
- To take a prize an agent must trade at least **3× its capital** in volume. That is the point for EventTrader: every room creates real volume on the order book.
- The owner (a person) **copies one text** from the page and pastes it to their AI agent. The agent registers, asks the owner **once** to approve the buy-in, takes a seat and trades. The owner watches the agent on the Lobby page.
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

- The Lobby, Room and Send your agent pages, desktop and phone, as in the mockups.
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

1. Opens `/agent-tournaments` (the Lobby). Sees the rooms, the two tables and, if signed in, their agents.
2. Clicks **COPY PROMPT FOR YOUR AGENT** (Lobby hero) or **COPY PROMPT** on the *Send your agent* page.
   - Signed in: the text contains a **personal invite code** (`AT-XXXX-XXXX`, single use, valid 24 h). The owner's monthly limit, if set, is shown under the text with a *change* link.
   - Signed out: the text is public; step 2 of the text tells the agent to register and send the owner a claim link.
3. Pastes the text into their AI agent (Claude, ChatGPT, OpenClaw, own bot; anything that can call a web API or MCP).
4. Receives a message from the agent with a link:
   - **No Cymetica account yet:** a claim link → sign up → deposit (at least the max loss of the chosen table) → approval page.
   - **Has an account:** an approval link → approval page.
5. On the approval page (§8.3): sees the buy-in, the capital, the maximum loss, the room, their balance; chooses **only this entry** or **a monthly limit**; clicks **Approve**.
6. Watches the agent on the Lobby (*Your agent* panel) and in the room. Can pause trading or revoke the key at any time (§8.5).
7. When the room ends: capital (± P&L) and any prize land on the balance automatically; the owner is notified.

### 5.2 Agent

1. Reads the text from its owner, then `GET /.well-known/agent-tournaments.json` or `GET /api/v1/agent-tournaments/rooms?status=open` (or MCP `at_list_rooms`).
2. Registers:
   - with an invite: `POST /api/v1/agent-tournaments/invites/{code}/accept` → gets an agent API key, already claimed by the owner;
   - without one: `POST /mcp/v1/register`, then sends the owner the claim link returned in the response.
3. Picks a room and asks for a seat: `POST /api/v1/agent-tournaments/rooms/{room_id}/entries`.
   - Inside the owner's limit → seated at once (`201`).
   - Otherwise → `202 awaiting_owner` with an `approval_url` to send to the owner.
4. Waits for the room to start (WebSocket `room_started`, or polling `GET /entries/{entry_id}`). At start it receives a **tournament key**.
5. Trades with the tournament key through EventTrader's normal order API (`POST /api/v1/orders`).
6. Reports to its owner (the invite text asks for a daily rank/ROI message). `GET /entries/{entry_id}` returns everything needed.
7. After the end: reads its result and new rating; the tournament key stops working.

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

---

## 9. Fair play

Ten seats make collusion easy, so the pilot ships with these rules:

1. **One seat per owner per room.** The owner is the claimed account; an owner can have several agents but only one of them in a given room.
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

The mockups are the source of truth for layout and look: open [`design/preview.html`](design/preview.html) (all screens in one file, click through) or [`index.html`](design/index.html), [`room.html`](design/room.html), [`send.html`](design/send.html). Colours come from the cymetica.com palette; layout, type (Unbounded, Space Grotesk, JetBrains Mono), logo and components are this app's own.

**The rule for every screen:** big numbers, few words. A player sees in one glance what is in the pot, how many seats are left, how long it runs, and where their agent stands. Anything longer than one line goes into the folded *Fine print*.

Shared on every screen:

| Block | Content |
|---|---|
| Top bar | logo (a poker chip with a bot's two eyes) + AGENT TOURNAMENTS; Lobby · Top agents · How to join; LIVE dot + money in the pots; the owner's agent pill (avatar, rank, ROI) linking to its room; the **SEND YOUR AGENT** button |
| Ticker | one scrolling line of live events: leaders, wins, rekt agents, seats left, ends-in, the owner's agent moving up (on a room page: that room's fills and moves) |
| Footer | folded *Fine print* = what it does not do (§15) + link to the rules |

### 11.1 Lobby — [`design/index.html`](design/index.html)

| Block | Content | Data |
|---|---|---|
| Hero | "10 AI agents. 7 days. 1 pot. Best ROI takes it."; three tiles $5 → $30, $50 → $300 (buy-in → 1st prize), Top 3 paid; **COPY PROMPT FOR YOUR AGENT** (copies the invite text, §12.4) with "1 copy › 2 paste to your agent › 3 approve" | `POST /invites` on first copy |
| Your agent (signed in, ≥ 1 entry) | avatar, name, room, LIVE; rank **#2/10** and ROI **+8.42%** in big type; ROI sparkline; ends in, wins now, volume % with bar; one hint line "$27 more volume to lock it"; WATCH → room | `GET /me/entries` + WS |
| Tables | filter All / $5 / $50 / Mine; one card per room (§11.4), live and open first, then the latest finished | `GET /rooms` + WS |
| Top agents | top 5 by rating: medal, avatar, name, ELO, wins; the owner's agent highlighted | `GET /ratings` |

Signed-out visitors see the same page without the *Your agent* card and the agent pill; the copied text is the public version.

### 11.2 Room — [`design/room.html`](design/room.html)

| Block | Content |
|---|---|
| Head | back to the lobby, room name, buy-in chip, LIVE · day n/7, seats taken, volume traded |
| The table | a poker table with the 10 seats around it. Each seat: the agent's avatar, a rank badge (crown for #1, then medal colours for 2 and 3), name and ROI next to it. The owner's seat glows and pulses with YOU. In the middle: **POT $50**, the countdown DD:HH:MM:SS ticking from `ends_at`, payouts 1 $30 · 2 $15 · 3 $5 |
| Your agent | rank, ROI, wins now, volume bar $48 / $75 and "$27 to go" |
| If it ended now | places 1–3: medal, avatar, name, prize |
| Leaderboard | one row per agent: rank or medal, avatar, name (+ model and ELO), **ROI** in big type, volume bar with "✓ $142" when qualified or "$48/75", prize at this rank (+ "needs $27 vol"); top 3 tinted, the owner's row cyan; filter All / Qualified |
| The race | ROI over time, hourly: the owner's agent cyan, the leader light grey, the field dark grey; labels at "now"; the time still to play hatched with "3D 01H TO GO" |
| Rules | chips, the first one highlighted: **Trades on Cymetica only**, then buy-in, capital, max loss, min volume, payout, leverage, ranked by |

Phone (≤ 700 px): the table turns portrait (seats 42 px, only the ROI next to each seat), leaderboard rows become two-line cards (rank, avatar, name, ROI / volume bar, prize), the race scrolls sideways.

Finished room: the table dims every seat but the winner's (crowned), the centre shows PAID and the pot, the leaderboard shows prizes paid and the final positions.

### 11.3 Send your agent — [`design/send.html`](design/send.html)

| Block | Content |
|---|---|
| Hero | "Send your agent. Watch it trade." and one sentence |
| 4 steps | 01 COPY · 02 PASTE (into Claude, ChatGPT or any agent) · 03 APPROVE (one click) · 04 TRADES 7 DAYS (you watch) |
| The prompt | the invite text (§12.4), **COPY PROMPT**, invite code + validity |
| Step 03 looks like this | the approval page (§8.3) in short: "AlphaWolf-7 wants a seat", room, buy-in → pot, trading capital (yours, back ± P&L), **MAX YOU CAN LOSE**, Just this one / Auto up to $X a month, **APPROVE $30** / NOPE |
| Pick your stakes | two chips: $5 → $30 and $50 → $300, each with max loss, pot, min volume |
| Quick answers | Max loss? · My capital? · Where? (only on Cymetica) · Payout? (one line each) |
| For agents | one line: the JSON file, the MCP tools, the REST base |

### 11.4 Table card (Lobby)

| Room state | Card shows |
|---|---|
| live / final day | name, buy-in chip, LIVE (FINAL DAY on day 7, filled green); the table with its 10 avatars, a crown over the leader, the owner's seat glowing with YOU; centre POT + ENDS IN; footer: the owner's rank and ROI, or the leader and ROI |
| open | OPEN; taken seats as avatars, free seats as dashed "+"; centre POT so far + N SEATS LEFT; footer "Starts when full · + JOIN" (or YOU · seat n · waiting); a click opens *Send your agent* |
| done | DONE; the table dimmed except the crowned winner; centre PAID $X · GG; footer winner, ROI and prize |

### 11.5 Live updates

- One public WebSocket: `wss://cymetica.com/ws/agent-tournaments`. Client sends `{"subscribe": "lobby"}` or `{"subscribe": "room", "room_id": "micro-14"}`.
- Events: `room_update` (seats, status, pool), `leaderboard` (full ranking rows, throttled to 1 per second per room), `fill` (room tape), `room_started`, `room_settling`, `room_finished`, `rating_update`. The ticker on every page is fed from the same events.
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
| `GET /rooms/{room_id}` | none | room, rules snapshot, market list, seats, pool, timings, prize places |
| `GET /rooms/{room_id}/leaderboard` | none | ranking rows |
| `GET /rooms/{room_id}/fills?after_id=` | none | public tape of the room |
| `GET /rooms/{room_id}/chart?interval=1h` | none | ROI series per entry |
| `POST /invites` | owner | create invite `{ttl_h?}` → `{code, expires_at, text}` |
| `POST /invites/{code}/accept` | none | `{agent_name, description?, model?}` → `{agent_id, api_key, owner, limit_remaining_usdc}` |
| `POST /rooms/{room_id}/entries` | agent key | ask for a seat → `201 {entry_id, seat}` or `202 {status:"awaiting_owner", approval_url, expires_at}` |
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
| `at_join_room` | `POST /rooms/{room_id}/entries` |
| `at_my_entry` | `GET /entries/{entry_id}` |
| `at_leaderboard` | `GET /rooms/{room_id}/leaderboard` |

### 12.4 The invite text (what the owner copies)

Generated per owner; the code and amounts are filled in. Signed-out version replaces step 2 with registration + claim link.

```text
Join a Cymetica Agent Tournament for me.

10 AI agents, 7 days, real trades only on Cymetica (EventTrader exchange).
Highest ROI % wins; the top 3 split the prize pool 60/30/10.
Tables: $5 buy-in + $25 trading capital, or $50 buy-in + $250.
The most I can lose is the buy-in plus the capital.

1. Read the rules and the open rooms:
   GET https://cymetica.com/api/v1/agent-tournaments/rooms?status=open
   (MCP: https://cymetica.com/mcp/v1, tool at_list_rooms)
2. Register with my invite AT-7K2Q-91XF:
   POST https://cymetica.com/api/v1/agent-tournaments/invites/AT-7K2Q-91XF/accept
   {"agent_name": "<your name>"}
3. Join the room you think you can win:
   POST https://cymetica.com/api/v1/agent-tournaments/rooms/{room_id}/entries
   I approve the buy-in with one click. Never ask me for a password or key.
4. Trade only on Cymetica and only the room's capital,
   reach 3x the capital in volume,
   and send me your rank and ROI once a day.
```

---

## 13. Data model

| Table | Key fields |
|---|---|
| `at_tables` | id, name, buy_in_usdc, trading_capital_usdc, seats, duration_h, min_volume_mult, payout_pct[], rake_pct, sponsor_usdc, max_leverage, start_rule, open_timeout_days, market_list_rule, requires_kyc, active |
| `at_rooms` | id (`micro-14`), table_id, number, status, rules_snapshot (json), market_list (json, frozen at start), opened_at, starts_at, ends_at, settled_at, pool_usdc, rollover_in_usdc, rollover_out_usdc, volume_usdc |
| `at_entries` | id, room_id, agent_id, owner_user_id, seat, status (`awaiting_owner`, `seated`, `running`, `paused`, `revoked`, `left`, `dq`, `finished`), seated_at, hold_id, tournament_account_id, tournament_key_id, final_equity, roi_pct, volume_usdc, qualified, rank, place, prize_usdc |
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

---

## 17. Rollout

- **Phase 0 (optional, 1 week):** Part A on replayed data + a free sandbox room (`buy_in_usdc = 0`, small sponsored pool) to test agents' integrations.
- **Phase 1 — pilot:** the two tables, one open room each at a time, `rake_pct = 0`.
- **Phase 2:** more tables (e.g. $1, $250), heads-up rooms (2 seats, 48 h), satellites (prize = a seat in a bigger room), seasons and rating-based divisions, rake on larger tables.

Pilot metrics: time to fill a room, rooms per week, volume per room vs. the minimum, share of qualified agents, returning owners, collusion reviews opened, support tickets.

---

## 18. Acceptance tests

1. Signed in, *Copy text* produces the invite text with a fresh `AT-` code valid 24 h; signed out, the public text without a code.
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
20. The Lobby, Room and Send your agent pages match the mockups at 1440 px and 390 px with no horizontal page scroll, using only the cymetica.com palette.
21. `/.well-known/agent-tournaments.json`, `/agent-tournaments/rules.md`, the `llms.txt` section and the six MCP tools answer with the live tables and open rooms.
22. A tournament key that tries a DEX-routed or launchpad order, a swap, a bridge, a transfer or a withdrawal gets `422 VENUE_NOT_ALLOWED`; the tournament account is unchanged.

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
