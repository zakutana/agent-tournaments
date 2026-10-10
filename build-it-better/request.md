# Build it Better request: Agent Tournaments

How to file this app at [cymetica.com/build-it-better](https://cymetica.com/build-it-better). Filing needs a signed-in account on a NEXUS Pro, Max 5x or Max 20x plan (one request uses 0.5 units).

## On the web form

Choose **It does not exist yet**, then:

| Field | What to put in |
|---|---|
| What should we call your app? | `Agent Tournaments` |
| What should it do? | Click **Load the list from a .md or .txt file** and pick [`improvements.txt`](improvements.txt). 32 lines, about 7,600 characters; the limit is 8,000 characters and 40 items, one item per line. The first line links to the design brief [SPEC.md](../SPEC.md) and the [design mockups](../design/) (open `design/preview.html` to click through). The text asks for the design, the copy and the two prompts, adds paper mode, manual setup, your trades and the many-agents Lobby, and leaves the implementation to Cymetica. |
| Show us the design you want | Upload the 10 images in [`design/screenshots/`](../design/screenshots/): `1-lobby.png`, `2-lobby-10-agents.png`, `3-take-a-seat.png`, `4-manual-setup.png`, `5-live-table.png`, `6-results.png`, `7-how-it-works.png`, `8-lobby-10-agents-phone.png`, `9-take-a-seat-phone.png`, `10-live-table-phone.png`. |
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

The request gives Cymetica the design, the copy, the prompts and the rules, and leaves the implementation to them (brief section 8). Build it Better builds read-only parts automatically and sends anything that moves money (buy-ins, approvals, payouts) to a person for review, so expect the scope to split that way. Before real-money tables go live, Cymetica should check the legal side of a buy-in + prize pool (brief section 8).
