# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b138-heroes-scene/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b138-heroes-scene/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up 23 November 2026 in a single
image — 31 stories, 6 regions. Three big drawn hero scenes lead the page:

- **AI rout hits Asia** — Kospi −3.3% to 4,708.54, sheds 161 pts
  (intraday −5.8%); Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — Bridgetown summit,
  Barbados; 150 delegates back a risk framework.
- **US lead over China at record low** — Asia Power Index 2026:
  US 78.9, China 73.6, gap 5.3, narrowest since 2018; India third at 40.5.

Below the heroes: a 10-story "More of the Day" grid, a world map with 13
numbered pins, an 18-item "Also on Monday" list, and a red DATE CHECK box
listing what is *not* 23 November (Dems reach 258, Sparta II fire,
El Chapo Isidro captured, EU–Indonesia pact, Nigeria boat, ICJ Myanmar
ruling) and what is not yet decided. Chips mark REPORTED (confirmed by
wires) vs CLAIM (one side's claim, independently unconfirmed).

## Build

`draw.py` (Pillow) renders `entry.png` (1024×1024). `main.py` (stdlib
only) validates the PNG and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`:

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=/tmp/out python3 -P -s main.py
```
