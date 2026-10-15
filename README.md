# URL Shortener API

A simple RESTful API that shortens long URLs, built with **Python**, **FastAPI** and **SQLite**.
It supports creating, retrieving, updating and deleting short URLs, and it tracks how many times each short URL has been accessed.

## Features

- Create a short URL with a randomly generated, unique code
- Retrieve the original URL from a short code
- Update the URL behind an existing short code
- Delete a short URL
- View access statistics for a short URL
- Request validation (`400`) and not-found handling (`404`)
- Visiting `/<shortCode>` redirects the browser to the original URL
- Interactive API docs at `/docs`

## Tech stack

| Part | Tool |
|---|---|
| Language | Python 3 |
| Framework | FastAPI |
| Server | Uvicorn |
| Database | SQLite (built-in `sqlite3` module) |
| Validation | Pydantic |

## Project structure

```
URL-Shortener/
├── app/
│   ├── __init__.py
│   ├── main.py         # creates the app, startup, error handler, redirect route
│   ├── database.py     # init_db() and get_db() (SQLite connection per request)
│   ├── schemas.py      # Pydantic request model (UrlBody)
│   ├── utils.py        # now_iso(), is_valid_url(), generate_code()
│   ├── crud.py         # all SQL: create, get, update, delete, increment
│   └── routes.py       # the /shorten endpoints
├── requirements.txt
├── .gitignore
└── README.md
```

Request flow:

```
request -> routes.py -> crud.py -> database.py (SQLite)
                |
         utils.py / schemas.py (validation, code generation)
```

## Getting started

### 1. Clone and enter the project

```bash
git clone https://github.com/shahariarpo/URL-Shortener
cd URL-Shortener
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # bash/zsh
source .venv/bin/activate.fish   # fish
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

Run this from the project root (the folder that contains `app/`):

```bash
uvicorn app.main:app --reload
```

The database file `urls.db` and its table are created automatically on first start.

Open the interactive docs at <http://127.0.0.1:8000/docs>.

## API endpoints

| Method | Endpoint | Description | Success | Errors |
|---|---|---|---|---|
| `POST` | `/shorten` | Create a short URL | `201` | `400` |
| `GET` | `/shorten/{shortCode}` | Retrieve the original URL (counts as an access) | `200` | `404` |
| `PUT` | `/shorten/{shortCode}` | Update the URL | `200` | `400`, `404` |
| `DELETE` | `/shorten/{shortCode}` | Delete the short URL | `204` | `404` |
| `GET` | `/shorten/{shortCode}/stats` | Get URL statistics | `200` | `404` |
| `GET` | `/{shortCode}` | Redirect to the original URL | `307` | `404` |

### Create a short URL

```bash
curl -i -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/some/long/url"}'
```

Response `201 Created`:

```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123",
  "createdAt": "2026-10-15T12:00:00Z",
  "updatedAt": "2026-10-15T12:00:00Z"
}
```

### Retrieve the original URL

```bash
curl -i http://127.0.0.1:8000/shorten/abc123
```

Returns `200 OK` with the same shape as above, or `404 Not Found`.

### Update a short URL

```bash
curl -i -X PUT http://127.0.0.1:8000/shorten/abc123 \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/some/updated/url"}'
```

Returns `200 OK` with the updated record. `updatedAt` changes; `createdAt` does not.

### Delete a short URL

```bash
curl -i -X DELETE http://127.0.0.1:8000/shorten/abc123
```

Returns `204 No Content` with an empty body.

### Get statistics

```bash
curl -i http://127.0.0.1:8000/shorten/abc123/stats
```

Response `200 OK`:

```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123",
  "createdAt": "2026-10-15T12:00:00Z",
  "updatedAt": "2026-10-15T12:00:00Z",
  "accessCount": 10
}
```

### Redirect

Open `http://127.0.0.1:8000/abc123` in a browser to be redirected to the original URL.

## Validation rules

A request is rejected with `400 Bad Request` when:

- the JSON body has no `url` field, or `url` is not a string
- the URL does not start with `http://` or `https://`, has no host, or contains spaces

## How it works

- Each short code is 6 random characters (letters and digits) generated with Python's `secrets` module. The code is checked against the database and regenerated if it is already taken, and the `short_code` column also has a `UNIQUE` constraint.
- The `urls` table stores `id`, `url`, `short_code`, `created_at`, `updated_at` and `access_count`.
- `access_count` goes up each time a short URL is retrieved (`GET /shorten/{shortCode}`) or visited through the redirect. The stats endpoint only reads it.
- `get_db()` is a FastAPI dependency that opens one SQLite connection per request and closes it afterwards.
- The redirect uses a temporary redirect (`307`) so browsers do not cache it and every visit is counted.

## Notes

- `urls.db` is a local data file and is ignored by git. Delete it to reset all data; it is recreated on the next start.
- No authentication or authorization is implemented.

## Possible improvements

- A small HTML frontend that calls the API
- Automated tests with `pytest` and FastAPI's `TestClient`
- Custom short codes and expiry dates
- A migration to PostgreSQL or MySQL for production use