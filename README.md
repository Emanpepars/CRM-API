# Simple CRM API

A small CRM (Customer Relationship Management) backend built with **Python**, **Flask**, and **SQLAlchemy**.

It manages **Customers**, **Leads**, and **Notes**, with simple filtering, searching, and a basic reporting endpoint.


---

## Features

- CRUD for **Customers**
- CRUD for **Leads** (with optional link to a Customer)
- CRUD for **Notes** (each note belongs to a Lead)
- Filter leads by **status**
- Search leads by **name or email**
- Basic **report endpoint** (totals + conversion rate)

### Lead Statuses
`new`, `contacted`, `qualified`, `won`, `lost`

---

## Project Structure

```
Simple CRM API/
├── app.py             # Flask app entry point
├── config.py          # Configuration (DB URI, etc.)
├── models.py          # SQLAlchemy models
├── routes.py          # All API endpoints
├── requirements.txt   # Python dependencies
└── README.md
```

---

## How to Run

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate     # macOS / Linux
# venv\Scripts\activate      # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

The API will start at **http://127.0.0.1:5000**.
A SQLite database file `crm.db` is created automatically on first run.

---

## API Endpoints

All requests/responses are JSON.

### Health check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/`      | Confirms the API is running |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/customers`             | List all customers |
| GET    | `/customers/<id>`        | Get one customer |
| POST   | `/customers`             | Create a customer |
| PUT    | `/customers/<id>`        | Update a customer |
| DELETE | `/customers/<id>`        | Delete a customer |

**Create customer body**
```json
{
  "name": "Alice",
  "email": "alice@example.com",
  "phone": "0123456789"
}
```

### Leads
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/leads`                 | List leads (supports filters below) |
| GET    | `/leads/<id>`            | Get one lead |
| POST   | `/leads`                 | Create a lead |
| PUT    | `/leads/<id>`            | Update a lead |
| DELETE | `/leads/<id>`            | Delete a lead |

**Filters / search**
- `GET /leads?status=new` — filter by status
- `GET /leads?search=ali` — search by name or email (partial match)
- They can be combined: `GET /leads?status=new&search=ali`

**Create lead body**
```json
{
  "name": "Bob",
  "email": "bob@example.com",
  "phone": "0100000000",
  "status": "new",
  "customer_id": 1
}
```
> `status` and `customer_id` are optional. Default status is `"new"`.

### Notes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/leads/<lead_id>/notes` | List notes for a lead |
| POST   | `/leads/<lead_id>/notes` | Create a note for a lead |
| GET    | `/notes/<id>`            | Get one note |
| PUT    | `/notes/<id>`            | Update a note |
| DELETE | `/notes/<id>`            | Delete a note |

**Create note body**
```json
{ "content": "Called the customer, will follow up next week." }
```

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/reports/leads` | Total / won / lost leads + conversion rate (%) |

**Example response**
```json
{
  "total_leads": 10,
  "won_leads": 3,
  "lost_leads": 2,
  "conversion_rate": 30.0
}
```

---

## Error Format

Errors are returned as JSON with a clear message:

```json
{ "error": "Fields 'name' and 'email' are required" }
```

Common status codes:
- `400` — bad request / validation error
- `404` — resource not found
- `405` — method not allowed
- `409` — conflict (e.g. duplicate email)

---

## Notes

- Database: **SQLite** (file: `crm.db`)
- No authentication is included by design.
- Built for learning and clarity, not production deployment.
