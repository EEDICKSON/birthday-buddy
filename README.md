### 🎂 Birthday Buddy

Video Demo: https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE

## 📌 Description

Birthday Buddy is a full-stack web application developed as a final project for CS50. It allows users to privately store, manage, and track birthdays with a clean interface and intelligent date-based sorting.

Inspired by the CS50 “Birthdays” lab, this project expands the idea into a multi-user system with authentication, persistent storage, and dynamic countdown logic.

The application focuses on simplicity and privacy—providing a lightweight alternative to storing personal dates across social media platforms.

## 🎯 Project Motivation

Modern platforms often mix personal data with unnecessary complexity. Birthday Buddy was designed as a utility-first application where users can:

Store important dates privately

View upcoming birthdays clearly

Avoid clutter from social platforms

A key goal was ensuring:

Strict data isolation per user

Accurate and meaningful date calculations

## ⚙️ Core Features

🔐 1. Secure User Authentication

Passwords are securely hashed using werkzeug.security (pbkdf2:sha256)

No plain-text password storage

Session-based authentication using user_id

Enhancements:

Usernames are normalized (lowercase + trimmed)

Prevents duplicate accounts and login inconsistencies

## 📅 2. Advanced Date Logic

A custom helper function calculates the number of days until the next birthday.

Handled Cases:

Future birthdays in the current year

Past birthdays → automatically shifted to next year

Leap year support (Feb 29)

Invalid dates rejected via datetime validation

This ensures:

Accurate countdowns

No application crashes from invalid input

### 🧾 3. Full CRUD Functionality

Users can fully manage their data:

Create: Add new birthdays

Read: View all birthdays sorted by upcoming date

Update: Edit existing entries

Delete: Remove entries securely

All operations enforce user ownership checks, ensuring data privacy.

## 🏗️ Technical Architecture

🔧 Backend

Python with Flask

Flask-SQLAlchemy ORM

Session-based authentication

🗄️ Database

SQLite (file-based, lightweight, portable)

🎨 Frontend

HTML5 + Bootstrap 5

Jinja2 templating engine

🧠 Design Pattern

The application follows the Model-View-Controller (MVC) pattern:

Model: SQLAlchemy classes (User, Birthday)

View: Jinja2 templates

Controller: Flask routes (app.py)

This separation improves:

Code organization

Maintainability

Scalability

## ⚠️ Development Challenges

1. Template Logic Errors

A TemplateSyntaxError occurred due to incorrect use of Jinja2 expressions.
This was resolved by simplifying template logic and separating validation into backend routes.

2. Data Integrity & Edge Cases

Handling invalid dates and leap years required careful validation.
A fallback mechanism ensures corrupted data does not break the application.

## 📁 File Structure

/project-root
│── app.py # Main Flask application (routes, logic, authentication)
│── birthdays.db # SQLite database (auto-generated)
│── birthdays.sqbpro # Database management file (SQLite Browser)
│── README.md # Project documentation
│
├── templates/ # Jinja2 HTML templates
│ │── layout.html # Base layout (shared structure)
│ │── index.html # Dashboard (list of birthdays)
│ │── login.html # Login page
│ │── register.html # Registration page
│ │── update.html # Update page for birthdays
│
├── static/ # Static files (CSS, images, JS if added)
│
└── **pycache**/ # Python cache (auto-generated)

In accordance with CS50 Academic Honesty policy:

AI tools (e.g., Gemini) were used as learning aids for debugging and understanding concepts

All final implementation decisions, architecture, and design are original work
