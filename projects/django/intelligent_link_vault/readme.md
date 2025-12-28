# Intelligent Link Vault

A modular Django-based URL shortener with a full REST API, automatic title scraping, and per-user click tracking.

## Features
- **Modular Apps**: Separate logic for `accounts` and `links`.
- **Auto-Metadata**: Title scraping via BeautifulSoup4.
- **Mobile Ready**: Token-based Authentication for React Native/API clients.
- **Race-Condition Safe**: Atomic click tracking using Django `F()` expressions.

## Tech Stack
- **Framework**: Django 6.x & Django REST Framework
- **Libraries**: Requests, BS4, DRF-Authtoken
- **Database**: SQLite

## API Endpoints
| Endpoint | Method | Auth | Description |
| :--- | :--- | :--- | :--- |
| `/api/accounts/register/` | POST | None | Create account + Get Token |
| `/api/accounts/login/` | POST | None | Exchange credentials for Token |
| `/api/accounts/me/` | GET | Token | View user profile & link count |
| `/api/links/vault/` | GET/POST | Token | Manage personal link collection |
| `/go/<short_code>/` | GET | None | Public redirect & click tracker |

## Quick Start
1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Database Setup**: `python manage.py migrate`
3. **Run Server**: `python manage.py runserver`

## Testing & Validation
The project includes a comprehensive test suite (Unit & Integration) covering authentication, privacy isolation, and scraping logic.
```powershell
# Run the integrated test suite
python manage.py test
```

---