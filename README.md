# TrueTech

Django-based website for TrueTech (HTML, CSS, JavaScript, Python/Django, MySQL).

## Stack

- Python 3.14, Django 5.2 (LTS)
- MySQL (via mysqlclient)
- Jazzmin for a themed Django admin
- SMTP email via Gmail

## Project layout

- `truetech/` — Django project (settings, urls, wsgi/asgi)
- `core/` — single app holding the site's models, views, and admin
- `templates/` — project-level templates
- `static/` — project-level static files (CSS/JS/images), including the admin theme
- `media/` — uploaded files (served locally, no cloud storage)

## Setup

1. Create and activate the virtual environment:
   ```
   py -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a MySQL database (e.g. via MySQL Workbench):
   ```sql
   CREATE DATABASE truetech_db CHARACTER SET utf8mb4;
   ```
4. Copy `.env.example` to `.env` and fill in your values (DB credentials, SECRET_KEY, Gmail SMTP app password).
5. Run migrations and create a superuser:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. Start the dev server:
   ```
   python manage.py runserver
   ```
   Admin available at `http://127.0.0.1:8000/admin/`.

## Email (Gmail SMTP)

New enquiry submissions from the contact form are emailed as a branded HTML notification (see `templates/core/emails/new_enquiry.html`) to the address set in `EMAIL_HOST_USER`. To wire this up for a client:

1. Get the client's Gmail address and an [App Password](https://myaccount.google.com/apppasswords) for it (not their normal login password). This requires 2-Step Verification to be enabled on that Google account — the client (or whoever owns the inbox) generates this from their own Google Account settings.
2. Open `.env` in the project root (copy it from `.env.example` if it doesn't exist yet) and fill in:
   ```
   EMAIL_HOST_USER=client-email@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
   ```
   `EMAIL_HOST_USER` is both the sender and the inbox that receives new enquiry notifications. `EMAIL_HOST_PASSWORD` is the 16-character App Password from step 1 (spaces are fine).
3. Restart the dev server (or the production process) so the new `.env` values are picked up.
4. If email sending should use a non-Gmail provider, also override `EMAIL_HOST`, `EMAIL_PORT`, and `EMAIL_USE_TLS` in `.env` (see `truetech/settings.py` for the defaults).

`.env` is git-ignored, so these credentials never get committed — each environment (your machine, the client's, staging, production) keeps its own copy.

### Adding an email to the Django superuser account

The superuser login (`python manage.py createsuperuser`) doesn't require an email, but you can set/update one so Django can use it for password-reset links, etc.:

- **Via the admin UI**: log in at `/admin/`, go to **Home → Authentication and Authorization → Users**, open the superuser account, fill in the **Email address** field, and save.
- **Via the shell**:
  ```
  python manage.py shell -c "
  from django.contrib.auth.models import User
  u = User.objects.get(username='admin')
  u.email = 'client-admin@example.com'
  u.save()
  "
  ```
  (replace `'admin'` with the actual superuser username.)

## Adding social media links & the contact phone number

These live on the singleton **Footer** admin page — go to `/admin/` → **Core → Footer** (there's only one row; the admin redirects you straight to it):

- **Social icons**: fill in `Whatsapp number` (digits with country code, e.g. `971501234567` — or paste a full URL to link elsewhere instead), `Linkedin url`, `Twitter url`, and `Instagram url`. Leaving any of these blank hides that icon in the footer and in the floating action buttons (WhatsApp only) — no code changes needed.
- **Phone number**: set `Phone number` under the "Contact info" fieldset on the same Footer page (e.g. `+971 50 123 4567`). This powers both the footer contact info and the floating "Call" button.
- **Contact email**: set `Contact email` on the same page — this powers the footer's Email icon, the floating Email button, and is separate from the `EMAIL_HOST_USER` used for sending notifications above.

Changes save immediately and appear on the site on the next page load — no restart needed.

## Notes

- Media files are stored locally under `media/` (no third-party storage like Cloudinary).
- Brand colors: `#0B4EA2`, `#F58220`, `#F4F7FB`, `#E8F5FF`
- Fonts: Headings — Plus Jakarta Sans, Body text — Inter
