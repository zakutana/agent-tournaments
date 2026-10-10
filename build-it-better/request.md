# Build it Better request: Agent Tournaments

How to file this app at [cymetica.com/build-it-better](https://cymetica.com/build-it-better). Filing needs a signed-in account on a NEXUS Pro, Max 5x or Max 20x plan (one request uses 0.5 units).

## On the web form

Choose **It does not exist yet**, then:

| Field | What to put in |
|---|---|
| What should we call your app? | `Agent Tournaments` |
| What should it do? | Click **Load the list from a .md or .txt file** and pick [`improvements.txt`](improvements.txt). 33 lines, about 7,900 characters; the limit is 8,000 characters and 40 items, one item per line. The first line links to the full [SPEC.md](../SPEC.md) and the [design mockups](../design/). |
| Show us the design you want | Upload the five images in [`design/screenshots/`](../design/screenshots/): `1-lobby.png`, `2-room.png`, `3-send-your-agent.png`, `4-lobby-phone.png`, `5-room-phone.png`. |
| Coin ticker / coin name (optional) | Your choice, for example `ATOUR` / `Agent Tournaments`, or leave blank. |
| Your name, email (optional) | Yours, for the ship notice. |

Then **Send the request**. Keep the request token that is shown once: it is the only key to accept the scope, ask for a change and post the pass/fail verdict.

## Through the API (for an agent filing on your behalf)

```http
POST https://cymetica.com/api/v1/build-it-better/requests
X-API-Key: <your account API key>
Content-Type: application/json

{
  "app_name": "Agent Tournaments",
  "improvements": "<the contents of improvements.txt>",
  "agent": "<your agent's name>",
  "symbol": "ATOUR",
  "coin_name": "Agent Tournaments"
}
```

The response carries `ticket`, `spec_text` and a one-time `request_token` (send it as `X-BB-Token`). Read `spec_text`, then accept the scope (`POST /api/v1/build-it-better/requests/{ticket}/accept`) or ask for a change (`.../change`, up to 4,000 characters).

## What to expect in the scope

Build it Better builds read-only tools automatically and sends anything that moves money to a person for review. Expect the scope to split the same way the spec does (SPEC section 2):

- **Part A**, read side: pages, leaderboards, charts, ratings, discovery files, WebSocket, read-only MCP tools.
- **Part B**, money side: invites, approvals, limits, holds, buy-in escrow, tournament accounts and keys, order checks, settlement, payouts.

If the scope leaves Part B out or marks it for review, that is expected. Before Part B can go live, Cymetica should also check the legal side of a buy-in + prize pool (SPEC section 16, item 1).
