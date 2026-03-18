Here’s a **clean, polished README.md** version of your CS50 Birthday Buddy project, formatted properly for GitHub and ready to copy-paste. I’ve kept all your content, added proper Markdown spacing, headings, and bullet points, and made it easy to read.

---

```markdown
# 🎂 Birthday Buddy
**CS50x Final Project | 2026**  
**GitHub:** EEDICKSON  
**edX username:** ED_2505_KSIR  
**Author:** Eric E. Dickson  

**Video Demo:** https://youtu.be/t3i8usHy3nM

---

## 📌 Project Overview
Birthday Buddy is a robust, full-stack web application designed to help users track and manage personal birthdays in a secure, private environment. While the initial inspiration came from the CS50 "Birthdays" lab, this project is a complete architectural overhaul.  

It moves from a simple single-table display into a sophisticated multi-user system featuring:

- Encrypted authentication  
- A relational database via SQLAlchemy ORM  
- A custom-built proximity sorting algorithm  

In an age where social media platforms often clutter birthday notifications with advertisements and data tracking, Birthday Buddy offers a "utility-first" alternative. It focuses on **data sovereignty**, allowing users to store sensitive dates privately.

---

## 🎯 Design Philosophy & Motivation
The core philosophy behind Birthday Buddy is **simplicity and relevance**. Traditional calendar applications sort birthdays chronologically from January to December, which can be unintuitive if a birthday in January is coming up while it’s December.  

The app automatically calculates **“distance in time”** so the most immediate celebrations are at the top of the dashboard. This required moving beyond basic SQL `ORDER BY` clauses, implementing backend Python logic to handle **rolling year calculations**.

---

## ⚙️ Technical Features & Architecture

### 1. Model-View-Controller (MVC) Pattern
The app strictly follows MVC to ensure maintainability:

- **Model:**  
  - Defined using Flask-SQLAlchemy (`User` and `Birthday` tables)  
  - Pythonic ORM interactions reduce syntax errors compared to raw SQL  

- **View:**  
  - Jinja2 templates with inheritance (`layout.html`)  
  - Ensures DRY (Don’t Repeat Yourself) principles for navbar and footer  

- **Controller:**  
  - `app.py` handles route logic and data flow between browser and database  

---

### 2. Secure Authentication System
Security is a top priority:

- **Password Hashing:** Using `werkzeug.security` with PBKDF2-SHA256; no plain-text storage.  
- **Session Management:** Tracks `user_id` per logged-in session, preventing horizontal privilege escalation.  
- **Username Normalization:** Usernames are stripped of whitespace and lowercased to prevent duplicates (e.g., "Alice" vs "alice ").  

---

### 3. Advanced Proximity Sorting Algorithm
Implemented via the `get_days_until` helper function:

1. Capture current date with `datetime.date.today()`.  
2. Create a date object for the birthday in the current year.  
3. If the date has passed, increment the year by 1.  
4. Return the difference in days.  

The `/` route sorts birthday objects by this dynamic `days_until` value, ensuring upcoming birthdays appear first.

---

### 4. Defensive Programming & Validation
Multi-layered validation ensures the app is crash-proof:

- **Frontend:** HTML5 input types with `required` attributes.  
- **Backend:** Try-except blocks in `/add` and `/edit` routes catch invalid dates (e.g., February 31 or Month 13), flash an error message, and redirect safely.

---

## 🏗️ Detailed File Structure
```

app.py              # Core Flask app with routes and database configs
birthdays.db        # SQLite relational database
helpers.py          # @login_required decorator & date calculations

templates/          # Jinja2 HTML templates
layout.html       # Base template with navbar/footer
index.html        # Main dashboard
login.html        # Login page
register.html     # Registration page
update.html       # Update birthday entries

static/             # CSS and other static assets

````

---

## ⚠️ Challenges & Lessons Learned

- **Leap Year Edge Case:**  
  Handling February 29th required careful validation. Non-leap years are gracefully managed so countdown logic remains accurate.

- **CRUD and Ownership:**  
  Every `/edit/<id>` or `/delete` request verifies that `birthday.user_id` matches `session["user_id"]` to prevent unauthorized data manipulation.

---

## 📜 Academic Honesty Note
This project was developed as the CS50x Final Project.  

- AI tools (Gemini) were used **only for debugging and brainstorming documentation structure**.  
- All final decisions regarding code, architecture, and features were made independently.

---

## 🚀 Getting Started

1. **Install dependencies:**
   ```bash
   pip install flask flask-sqlalchemy
````

2. **Set Flask app environment variable:**

   * macOS/Linux:

     ```bash
     export FLASK_APP=app.py
     ```
   * Windows:

     ```cmd
     set FLASK_APP=app.py
     ```
3. **Run the server:**

   ```bash
   flask run
   ```
4. The database (`birthdays.db`) will initialize automatically on first run.

---

```
