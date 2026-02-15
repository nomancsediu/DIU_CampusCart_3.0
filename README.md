<div align="center">

# 🛒 DIU Campus Cart  
### 🚀 A Secure Real-Time Campus Marketplace for DIU Students  

<p>
  <img src="https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Django%20Channels-4.x-0C4B33?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-Channel%20Layer-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-Production%20Ready-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-Interactive-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/WebSockets-RealTime-000000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Google%20OAuth-Authentication-4285F4?style=for-the-badge&logo=google&logoColor=white" />
</p>

</div>

---

# 🎯 Project Overview

**DIU Campus Cart** is a full-stack Django-based campus marketplace platform built exclusively for the DIU (Daffodil International University) community.
It enables verified students to buy and sell products securely within the campus ecosystem while communicating in real-time using WebSockets.
This project demonstrates real-world backend architecture, authentication systems, database modeling, and scalable real-time communication.

---

# ✨ Core Functionalities

## 👤 User Authentication & Profiles

- Email-based registration with OTP verification (10-minute expiration)
- Google OAuth login integration
- Secure session-based authentication
- Custom user profile system:
  - Profile photo upload
  - Bio / Description
  - Phone number
  - Department & Batch info
- Password hashing using Django's secure authentication system

---

## 🛍 Product Management System

- Create, edit, and delete product listings
- Category-based organization (slug routing)
- Decimal-based price handling (max_digits=10, decimal_places=2)
- Product condition (New / Used)
- Multiple product images with custom ordering
- Availability toggle system
- Automatic timestamps (created_at / updated_at)

---

## 💬 Real-Time Messaging System

- WebSocket-based instant messaging (Django Channels)
- Redis-powered channel layer
- Unique conversation per (product, buyer, seller)
- Persistent conversation history
- Email notification on first message
- No page refresh required for chat updates

---

## 🔍 Product Discovery

- Category-based browsing
- Product detail page with image gallery
- Structured listing system
- Organized and scalable database design

---

# 🏗 Architecture Highlights

- ASGI-based Django application
- Channel layers for scalable real-time routing
- Modular app separation:
  - `accounts`
  - `products`
  - `chat`
- Environment variable management using `.env`
- Production-ready deployment (Daphne / Gunicorn)
- Database upgrade path to PostgreSQL

---

# 🛠 Technology Stack

## Backend
- Django 6.x
- Django Channels
- Django REST Framework (optional)
- Daphne (ASGI server)

## Real-Time Layer
- WebSockets
- Redis (Channel Layer)

## Frontend
- HTML5
- CSS3
- JavaScript

## Database
- SQLite (Development)
- PostgreSQL (Production-ready)

## Authentication
- Django Allauth
- Google OAuth 2.0
- OTP Email Verification

## Image Handling
- Pillow

---

# 🔐 Security Features

- OTP-based email verification
- Secure password hashing
- Environment variable protection
- Unique database constraints
- Session-based authentication control

---

# 🚀 Installation & Setup

```bash
git clone <repository-url>
cd campuscart
python -m venv env

# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````
Application runs at:
```
http://localhost:8000
```
---

# 📂 Project Structure

```
campuscart/
│
├── accounts/     # Authentication & profile system
├── products/     # Product management
├── chat/         # Real-time messaging
├── templates/    # Global templates
├── media/        # Uploaded files
└── campuscart/   # Core project settings
```

---

# 🧠 What This Project Demonstrates

* Full-stack Django development
* Real-time system architecture
* Redis integration
* Secure authentication flow
* Clean database design
* Production-aware backend engineering

---

# 👨‍💻 Developed By Abdullah Al Noman

CSE Student
Aspiring Software Engineer
Focused on Backend Systems, Real-Time Architecture & Clean Code Design

---

<div align="center">
⭐ If you find this project valuable, consider giving it a star.
</div>

