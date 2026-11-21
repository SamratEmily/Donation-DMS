# Donation Management System (DMS)

A Django web app that connects **donors**, **volunteers** and **admins** to manage charitable donations from submission to delivery. Donors list what they want to give, admins review it and assign it to an area, volunteers in that area collect it, and a delivery photo closes the loop.

## Features

- **Three roles, three dashboards**: Admin, Donor and Volunteer, each with its own workspace.
- **Donation lifecycle**: New → Accepted → Collected → Delivered (or Rejected), with a visual timeline.
- **Donation types**: Food, Clothes, Money, Books, Toys, Medicine and Other.
- **Area-based assignment**: volunteers only see pickups in their assigned area.
- **Volunteer approval**: new volunteers stay *Pending* until an admin accepts them.
- **Delivery gallery**: volunteers and admins upload proof-of-delivery photos.
- **Admin tools**: searchable tables with Copy/CSV/Excel/Print export, area management and a status pipeline.
- **Modern, responsive UI** built on Bootstrap 5.
- **One-command demo data**: `seed_data` loads sample areas, users, donations and photos.

## Tech stack

Python 3.10+ · Django 5.1 · SQLite · Bootstrap 5 · DataTables · Font Awesome · Pillow

## Getting started

**Requirements:** Python 3.10 or newer.

```bash
git clone https://github.com/SamratEmily/Donation-DMS.git
cd Donation-DMS
```

Run these **one line at a time**.

**Windows** (PowerShell or Git Bash)

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py seed_data
.venv/Scripts/python manage.py runserver 8000
```

**macOS / Linux**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_data
.venv/bin/python manage.py runserver 8000
```

Then open <http://127.0.0.1:8000>. Next time you only need the last (`runserver`) line.

A step-by-step guide for running the project in Visual Studio Code is included as [HOW_TO_RUN.pdf](HOW_TO_RUN.pdf).

## Demo accounts

Created by `seed_data`. You sign in with an **email**, not a username.

| Role | Email | Password |
|---|---|---|
| Admin | `admin@example.com` | `admin123` |
| Donor | `donor@example.com` | `donor123` |
| Volunteer (Mirpur) | `volunteer@example.com` | `volunteer123` |

More demo users: `rahim.donor@`, `nusrat.donor@` and `karim.donor@example.com` (password `donor123`), plus `tania.vol@`, `sakib.vol@`, `mitu.vol@`, `pending.vol@` and `rejected.vol@example.com` (password `volunteer123`).

- Login page: <http://127.0.0.1:8000/login/>
- Django admin panel: <http://127.0.0.1:8000/admin/>

`seed_data` is safe to run more than once. It only adds what is missing and never deletes anything.

## Project structure

```
accounts/     Custom email-based user model, login/sign-up, seed_data command
dashboard/    Role-specific dashboards
donations/    Donations and volunteer collection requests
donors/       Donor profiles
volunteers/   Volunteer profiles and approval
areas/        Donation areas
gallery/      Delivery photos
templates/    Base layouts and shared snippets
static/       CSS (app.css, landing.css) and JS
```

## Note

This project is configured for **local development** (`DEBUG = True`, a development secret key and demo passwords). Change these before deploying it anywhere public.
