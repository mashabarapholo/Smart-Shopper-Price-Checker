# Smart Shopper: Automated Price Tracker

## Project Overview

Smart Shopper is a full-stack web application designed to track product prices from e-commerce websites (initially Amazon) and notify users via email when a product's price drops below their desired target.

This project demonstrates a complete software development lifecycle, including building a backend API with Flask, managing a database with SQLAlchemy, creating a background worker for web scraping, and developing a user-friendly frontend with HTML and vanilla JavaScript.

## Core Features

- **Web-Based UI:** A simple and clean user interface for users to submit products they want to track.
- **Backend API:** A RESTful API built with Flask to handle requests for tracking new products.
- **Persistent Database:** Uses SQLite and SQLAlchemy to store information about tracked products, target prices, and user emails.
- **Automated Web Scraper:** A background "worker" script (`checker.py`) that periodically scrapes the current price of all tracked products.
- **Email Alert System:** Automatically sends a formatted HTML email to the user when a price drop is detected.
- **Secure Credential Management:** Keeps sensitive information like email passwords out of the source code using a `.env` file.

## Screenshot of the Frontend

*(Here you would add a screenshot of your web form)*

![Smart Shopper Frontend](<img width="1432" height="689" alt="smart_shopper_price" src="https://github.com/user-attachments/assets/b0940a15-e9ce-4190-ac51-d598cd9612b5" />
)

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **Web Scraping:** `requests`, `BeautifulSoup4`
- **Database:** SQLite
- **Automation:** `schedule` library
- **Emailing:** `yagmail`
- **Environment Management:** `python-dotenv`

## How to Run This Project

This project has two main components that need to be run separately: the **Web Server** and the **Checker Service**.

### 1. Initial Setup

1.  Clone this repository.
2.  Create a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file by copying `sample.env`.
4.  Fill in your email credentials in the `.env` file. You will need a [Google App Password](https://support.google.com/accounts/answer/185833).

### 2. Run the Web Server

This server handles the user interface and adding new products to the database.

```bash
python app.py
```
-   The web application will be available at `http://127.0.0.1:5000`.
-   The server will also automatically create the `products.db` database file on its first run.

### 3. Run the Automated Checker

This script runs in the background to check for price drops. **Open a second, separate terminal** to run this.

1.  Activate the virtual environment in the new terminal.
2.  Run the checker script:
    ```bash
    python checker.py
    ```
-   The checker will run once immediately and then continue to run in the background on its defined schedule (e.g., every hour).
-   Press `CTRL+C` to stop the checker service.
