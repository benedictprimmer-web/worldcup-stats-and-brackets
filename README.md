# James vs Fran — World Cup 2026 Sweepstake Tracker

A single self-contained web app tracking a 48-team World Cup sweepstake
between James and Fran (24 teams each, snake draft). Live scoreboard,
fixtures, per-owner team pages, group tables, knockout bracket, plus a
lead-over-time chart and head-to-head stats.

**Live site:** https://benedictprimmer-web.github.io/worldcup-stats-and-brackets/

Everything is in `index.html` — no server, no build step, no dependencies.
Open it on any phone; add to home screen for an app-like icon.

## Going live (one-time)

GitHub Pages serves the site from `main`:

1. Open **Settings → Pages**
   (https://github.com/benedictprimmer-web/worldcup-stats-and-brackets/settings/pages)
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**
3. Branch: **main**, folder: **/ (root)** → **Save**
4. Wait ~1 minute, then the URL above is live. Send it to Fran once — she
   never needs a new link; she just refreshes after an update.

## Updating scores

All match data lives in the `RESULTS` array inside `index.html`. To record
a played match:

1. Find the match by team names (e.g. `"Turkey"` vs `"United States"`).
2. Set `"status"` from `"SCHEDULED"` to `"FINISHED"`.
3. Fill in the `score` block:
   ```json
   "score": {
     "winner": "HOME_TEAM",        // or "AWAY_TEAM" or "DRAW"
     "fullTime": { "home": 2, "away": 1 }
   }
   ```
4. Commit to `main`. Pages redeploys automatically in ~1 minute; Fran's
   refresh shows the new scores. The scoreboard, tables, bracket, and
   stats all recompute themselves.

For knockout matches, add a new entry to `RESULTS` with the right `"stage"`:
`LAST_32`, `LAST_16`, `QUARTER_FINALS`, `SEMI_FINALS`, `THIRD_PLACE`, or
`FINAL`. A penalty-shootout win is recorded by setting `winner` to the team
that advanced (optionally add `"penalties": { "home": 4, "away": 3 }`).

## Scoring

| Event | Points |
|---|---|
| Group win | 2 |
| Group draw | 1 each |
| Knockout win (pens count as a win) | 3 |
| Reach Round of 16 / QF / SF / Final / win it | +1 / +2 / +3 / +4 / +5 (cumulative) |

A team is marked eliminated automatically once the knockout draw is
populated and it isn't in it.
