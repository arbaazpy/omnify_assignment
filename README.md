# Event Management API

A Django REST Framework (DRF) based API to manage events and attendees. It supports features like event creation, attendee registration, user authentication, and timezone-aware scheduling. Built using Django, DRF, and drf-spectacular with clean, modular architecture.

---

## Features

### Authentication
- User registration with name, email, and password
- JWT-based login and logout
- Secure user profile endpoint (`/me`)

### Event Management
- Create events with name, location, start/end time, and max capacity
- Creator is automatically assigned
- Validates that end time is after start time
- **Timezone-aware output**: Convert slots to user-specified timezone via `?tz=ZoneName` param

### Attendee Registration
- Users can register other users to events
- Prevents:
  - Event creator registering as an attendee
  - Duplicate attendee registration
  - Exceeding event capacity
- List of attendees returned in flat user list

### API Endpoints

| Method | Endpoint                         | Description                       |
|--------|----------------------------------|-----------------------------------|
| POST   | `/events/`                       | Create an event                   |
| GET    | `/events/`                       | List all events (supports `?tz=`) |
| POST   | `/events/{id}/register/`         | Register a user for an event      |
| GET    | `/events/{id}/attendees/`        | List all attendees for the event  |
| POST   | `/register/`                     | Create a user account             |
| POST   | `/login/`                        | Get access/refresh token pair     |
| POST   | `/logout/`                       | Blacklist refresh token           |
| GET    | `/me/`                           | Get current user profile          |
---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/arbaazpy/omnify_assignment.git
cd omnify_assignment
```

2. **Set up a virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Apply migrations**
```bash
python manage.py migrate
```

5. **Create a superuser (optional)**
```bash
pip install -r requirements.txt
```

5. **Run development server**
```bash
pip install -r requirements.txt
```
---

## API Documentation

**Swagger UI available at:**
```bash
http://localhost:8000/api/docs/
```

**OpenAPI schema available at:**
```bash
http://localhost:8000/api/schema/
```
---

## Running Tests

Tests use Django's `TestCase` and DRF's `APITestCase`. Faker and Factory Boy are used for data generation.
```bash
python manage.py test
```

**Swagger UI available at:**
```bash
http://localhost:8000/api/schema/
```


## Technologies Used

- **Django 5.0+**
- **Django REST Framework**
- **drf-spectacular (OpenAPI 3 documentation)**
- **SimpleJWT for auth**
- **Factory Boy + Faker for testing**
- **PostgreSQL**


## Future Improvements

- **Filtering events by tags, location, or date**
- **CSV export of attendee list**
- **Public/private event visibility toggle**
- **Webhooks or email reminders for events**
- **Role-based access control (RBAC)**

---

## Note

This project was developed as part of a technical assignment for Omnify, showcasing:

- **Clean Django architecture**
- **Django ORM optimization (e.g., select_related, prefetch_related)**
- **Timezone-aware event management**
- **API documentation via OpenAPI/Swagger**
