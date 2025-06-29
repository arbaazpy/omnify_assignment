# Event Management API

A Django REST Framework (DRF) based API to manage events and attendees, implementing features such as event creation, registration, attendee listing, and authentication. Built with DRF and drf-spectacular for modern API-first projects.

---

## Features

### Authentication
- User registration with name, email, and password
- JWT-based login and logout
- Secure user profile endpoint (`/me`)

### Event Management
- Create events with name, location, start/end time, and capacity
- Creator is automatically assigned
- Cannot create events with invalid time range

### Attendee Registration
- Users can register other users to events
- Prevents:
  - Event creator registering as an attendee
  - Duplicate attendee registration
  - Exceeding event capacity
- List of attendees returned in flat user list

### API Endpoints
- `POST /events/`: Create event
- `GET /events/`: List all events
- `POST /events/{id}/register/`: Register a user as attendee
- `GET /events/{id}/attendees/`: Get event with attendees
- `POST /register/`: Create user
- `POST /login/`: Get access/refresh token pair
- `POST /logout/`: Blacklist refresh token
- `GET /me/`: Get current user

---

## Installation

1. **Clone the repository**
```bash
git clone git@github.com:arbaazpy/omnify_assignment.git
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

- **Event tags & filtering**
- **CSV export of attendee list**
- **Public/private event visibility**

---

**Note:** This project was developed as part of a technical assignment for Omnify, demonstrating practical skills in Django REST Framework, clean architecture, and API design best practices.