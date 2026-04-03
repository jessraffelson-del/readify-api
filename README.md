# Readify Bookstore API

A production-style RESTful API built for Readify Ltd., a fictional online bookstore modernizing its backend services. Built with Python and Flask-RESTX, this project demonstrates REST best practices, automated testing, and CI/CD deployment pipelines.

## What This Project Demonstrates

- RESTful API design with proper resource identification and HTTP verb usage
- Auto-generated OpenAPI/Swagger documentation via Flask-RESTX
- Automated Postman test collection covering full CRUD flows and validation errors
- CI/CD pipeline via GitHub Actions that runs tests automatically on every push
- Logging and monitoring hooks for API health and request tracking

## Tech Stack

- **Python 3** — core language
- **Flask-RESTX** — REST framework with built-in OpenAPI documentation generation
- **Postman** — API testing and automated test collection
- **Newman** — Postman CLI runner for CI/CD integration
- **GitHub Actions** — automated testing pipeline

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /books/ | List all books |
| POST | /books/ | Add a new book |
| GET | /books/{id} | Retrieve a book |
| PUT | /books/{id} | Replace a book entirely |
| PATCH | /books/{id} | Partially update a book |
| DELETE | /books/{id} | Delete a book |
| GET | /authors/ | List all authors |
| POST | /authors/ | Add a new author |

## Running Locally

**Clone the repo:**
```bash
git clone https://github.com/jessraffelson-del/readify-api.git
cd readify-api
```

**Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install flask flask-restx
```

**Start the server:**
```bash
python app.py
```

**Visit the interactive Swagger docs:**

http://127.0.0.1:5000/docs

## Automated Testing

Tests are written in Postman and cover:
- Create → Retrieve → Update → Delete book flow
- Validation error handling (missing required fields)
- 404 verification after deletion

**Run tests locally with Newman:**
```bash
npm install -g newman
newman run tests/readify-api-tests.json --env-var "baseUrl=http://127.0.0.1:5000"
```

## CI/CD Pipeline

Every push to the main branch automatically:
1. Spins up a clean Ubuntu environment
2. Installs Python and dependencies
3. Starts the Flask server
4. Runs the full Postman test collection via Newman
5. Reports pass/fail status

See the [Actions tab](https://github.com/jessraffelson-del/readify-api/actions) for live pipeline results.

## Project Context

Built as part of a coursework module on API design and deployment. Demonstrates production-ready patterns including proper HTTP status codes, OpenAPI documentation, automated regression testing, and continuous integration — the same workflow used by professional engineering teams.