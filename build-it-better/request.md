# Build it Better request: Agent Tournaments

How to file this app at [cymetica.com/build-it-better](https://cymetica.com/build-it-better). Filing needs a signed-in account on a NEXUS Pro, Max 5x or Max 20x plan (one request uses 0.5 units).

## On the web form

Choose **It does not exist yet**, then:

| Field | What to put in |
|---|---|
| What should we call your app? | `Agent Tournaments` |
| What should it do? | Click **Load the list from a .md or .txt file** and pick [`improvements.txt`](improvements.txt). 32 lines, 7,907 characters (7,939 with CRLF line breaks); the limit is 8,000 characters and 40 items, one item per line. The first line links to the design brief [SPEC.md](../SPEC.md) and the [design mockups](../design/) (open `design/preview.html` to click through). The text asks for the design, the copy and what the two prompts must do, adds paper mode, manual setup, your trades, the many-agents Lobby and agents that find Cymetica on their own, and leaves the prompt words and the implementation to Cymetica. |
| Show us the design you want | Leave it empty. Everything is on GitHub: the brief links the clickable mockup and every screenshot (the form would take at most 6 pictures anyway). |
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

The request gives Cymetica the design, the copy, what the prompts must do and the rules, and leaves the prompt words and the implementation to them (brief section 9). Build it Better builds read-only parts automatically and sends anything that moves money (buy-ins, approvals, payouts) to a person for review, so expect the scope to split that way. Before real-money tables go live, Cymetica should check the legal side of a buy-in + prize pool (brief section 9).
