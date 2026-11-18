[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Plowester1/news-image-20261118-poler-v1/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Plowester1/news-image-20261118-poler-v1/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World in One Day — 18 November 2026

An entry in make.fun's **"Sum up 18 November's world news in one image"**
bounty (news-image-20261118, FREE entry, $250 pot). The program copies a
single 1024×1024 infographic to `/output/entry.png`: a dark neon cyber
front page summing up Wednesday 18 November 2026's world news in eight
stories, each verified against multiple news sources for that day.

## The eight stories

1. **Tech / Nvidia (hero)** — Nvidia board rejects Huang's return, record
   $115.8B quarter: the board turns down Jensen Huang's offer to return as
   CEO as the chipmaker posts a record $115.8B quarter.
2. **Tech / OpenAI** — OpenAI launches GPT-6.2 Astra and Sol, cuts prices:
   new models Astra and Sol, with lower API prices.
3. **Cyber** — Cyberattack hits Zoom, CNN, HSBC, IKEA and more: a major
   incident hits sites linked to Zoom, CNN, HSBC and IKEA.
4. **Diplomacy** — Xi greets Trump in Shenzhen as APEC opens: Xi meets
   Trump at Air Force One in Shenzhen.
5. **Middle East** — US strikes Iran's Qeshm Island as Iran hits back: US
   jets hit a Guard site; Iran hits back.
6. **Europe** — Ukraine hits Crimean Bridge for a second day: the road span
   collapses into the strait.
7. **US Politics** — Peltola wins Alaska, Democrats take Senate 56–44:
   Peltola beats Sullivan; the Senate goes 56–44.
8. **Russia** — Russia plans 20 million drones for Ukraine next year:
   Moscow plans to launch 20 million drones at Ukraine in 2027.

## How it is built

`entry.png` is composed programmatically with Python PIL (`build_image.py`):
crisp vector text, a near-black page with cyan/magenta neon accents, a
glowing hero card and neon-bordered cards with drawn icon motifs, no
AI-generated imagery, so every headline is legible and correct. `main.py`
is a pure file copy — no network, no randomness — so both runs write
identical bytes, verified with a SHA-256 check.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, identical on every run
```
