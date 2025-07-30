# In checker.py (Final Automated Version)

import requests
from bs4 import BeautifulSoup
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Product # Import the Product model
import os
from dotenv import load_dotenv
import yagmail # For sending emails
import schedule # For scheduling

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# --- DATABASE CONNECTION ---
DATABASE_URI = 'sqlite:///products.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# --- WEB SCRAPING SETUP ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def send_alert_email(product, current_price):
    """Sends a price alert email to the user."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Email credentials not set. Cannot send alert.")
        return

    try:
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
        
        subject = f"Price Alert! Your tracked item is now ${current_price:.2f}"
        
        body = f"""
        <html>
        <body>
            <h2>Price Drop Notification</h2>
            <p>Good news! The price for the item you are tracking has dropped to or below your target price.</p>
            <p><strong>Current Price:</strong> <span style="color: green; font-weight: bold;">${current_price:.2f}</span></p>
            <p><strong>Your Target Price:</strong> ${product.target_price:.2f}</p>
            <p>You can purchase it here:</p>
            <a href="{product.product_url}">Buy Now</a>
            <p>This is an automated alert from the Smart Shopper Price Tracker.</p>
        </body>
        </html>
        """
        
        print(f"Sending email to {product.user_email}...")
        yag.send(to=product.user_email, subject=subject, contents=body)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {e}")

def scrape_amazon_price(url):
    """Scrapes the price of a product from an Amazon URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        price_span = soup.select_one('span.a-offscreen')
        if price_span:
            price_str = price_span.get_text().strip().replace('$', '').replace(',', '')
            return float(price_str)
        else:
            print(f"Could not find price element for URL: {url}")
            return None
    except Exception as e:
        print(f"An error occurred during scraping for {url}: {e}")
        return None

def check_prices():
    """Main job function to check all product prices."""
    print(f"\n--- Running Price Check Job at {time.ctime()} ---")
    
    products_to_check = session.query(Product).all()
    
    if not products_to_check:
        print("No products in the database to check.")
        return
        
    for product in products_to_check:
        current_price = scrape_amazon_price(product.product_url)
        time.sleep(5) # Increase delay to be safer
        
        if current_price and current_price <= product.target_price:
            print(f"PRICE ALERT! Product ID {product.id} price is ${current_price:.2f} (Target: ${product.target_price:.2f})")
            send_alert_email(product, current_price)
            
            # Remove the product from tracking after the alert is sent
            session.delete(product)
            session.commit()
            print(f"Product ID {product.id} has been removed from the tracking list.")
        elif current_price:
            print(f"Product ID {product.id} price is ${current_price:.2f} (Target: ${product.target_price:.2f}). No alert needed.")
        else:
            print(f"Could not retrieve price for Product ID {product.id}.")
    
    print("--- Price Check Job Finished ---")

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    print("--- Starting Smart Shopper Automation Service ---")
    
    # Define the schedule. Run the job every hour.
    schedule.every().hour.do(check_prices)
    
    # For testing, you can run it more frequently:
    # schedule.every(1).minutes.do(check_prices) 
    
    # Run the job once immediately on startup
    check_prices() 
    
    # Keep the script running forever to execute the schedule
    while True:
        schedule.run_pending()
        time.sleep(1)