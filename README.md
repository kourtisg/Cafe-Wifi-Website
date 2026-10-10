# Cafe & Wifi Website

Day 88 of *100 Days of Code – The Complete Python Pro Bootcamp*.
A Flask website that lists laptop-friendly cafes in London from an SQLite database.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Then open http://127.0.0.1:5000

## Features

- Browse all cafes as cards: photo, location, seats, coffee price, and wifi / sockets / toilet / calls badges
- Filter cafes by location
- Add a new cafe with a validated form (required fields, valid URLs, unique name, price ≥ 0)
- Update the coffee price of a cafe
- Delete a cafe (with confirmation)
- CSRF protection on every form, flash messages for feedback, responsive Bootstrap 5 layout

## Files

| File | Purpose |
|---|---|
| `main.py` | Flask app, `Cafe` database model and routes |
| `forms.py` | `CafeForm` built with Flask-WTF / WTForms |
| `instance/cafes.db` | SQLite database with the cafe data |
| `templates/base.html` | Shared layout: navbar, flash messages, footer |
| `templates/index.html` | Cafe list, location filter, price update and delete |
| `templates/add.html` | Add-a-cafe form |
| `static/css/style.css` | Custom styles |
| `static/img/no-image.svg` | Fallback image for broken photo links |
