# Clash Royale Deck Helper

A lightweight Flask web application for building and sharing Clash Royale decks using seed-based card distribution. Deployed on PythonAnywhere.

## Features

- **Seed-based card distribution** — enter a 4-digit seed to deterministically deal 12 cards (8 public + 4 private) from a 120-card pool
- **Interactive card selection** — choose 8 cards from your pool; selected cards are numbered in pick order
- **Deep link export** — copy your deck directly to the Clash Royale mobile app via `clashroyale://copyDeck`
- **Tower type selection** — choose from Princess Tower, Dagger Duchess, Royal Chef, or Cannoneer
- **Bilingual UI** — full Chinese and English support, persisted per session
- **Poker table view** — optional Texas Hold'em seating display (toggled via `SHOW_POKER` flag)

## How It Works

1. Go to the home page and enter a 4-digit seed (0000–9999)
2. Select your side: **Blue King** or **Red King**
3. You'll see 8 shared public cards and 4 private cards unique to your color
4. Click cards to select exactly 8 for your deck (order matters — picks are numbered 1–8)
5. Pick a tower type and click **Copy Deck** to launch Clash Royale with your deck pre-loaded

Both players use the same seed, so the public pool is identical for both sides while each player's private cards differ.

## Project Structure

```
crtexas_pythonanywhere/
├── __init__.py          # Flask app factory
├── config.py            # App configuration and feature flags
├── routes.py            # Route handlers, game logic, i18n strings
├── data/
│   └── seating.json     # Player names for poker table
├── static/
│   ├── cards/           # 120 card PNGs (0.png – 119.png)
│   ├── css/main.css     # All styles
│   └── js/cardmap.js    # Card ID → Clash Royale deck key mapping
└── templates/
    ├── index.html        # Home page (seed input form)
    ├── game.html         # Card selection page
    └── poker.html        # Texas Hold'em table display
```

## Setup

**Requirements:** Python 3.6+, Flask

```bash
pip install flask
```

**Run locally:**

```bash
flask run
```

Or with the factory pattern:

```bash
python -m flask --app crtexas_pythonanywhere run
```

## Configuration

Edit [config.py](config.py) or set environment variables:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `"change-me-in-prod"` | Flask session secret — **change this in production** |
| `SHOW_POKER` | `True` | When `True`, the home page shows the poker table instead of the deck builder |

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page (deck builder or poker table depending on `SHOW_POKER`) |
| `/lang/<code>` | GET | Switch language (`zh` or `en`) |
| `/start` | POST | Validate seed and color, redirect to game |
| `/game/<color>` | GET | Render card selection page for `blue` or `red` |

## Deployment

This app is hosted on [PythonAnywhere](https://www.pythonanywhere.com). The repository name reflects this. No special deployment files are needed beyond a standard WSGI configuration pointing to the Flask app factory in `__init__.py`.

## License

[Apache License 2.0](LICENSE)
