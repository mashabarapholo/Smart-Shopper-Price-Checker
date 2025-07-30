# In app.py (Final Version with Frontend)

from flask import Flask, request, jsonify, render_template # Added render_template
from flask_sqlalchemy import SQLAlchemy
import os

# --- APP & DATABASE CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# Add the templates folder to the app's context
app.template_folder = os.path.join(basedir, 'templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODEL DEFINITION ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(500), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    user_email = db.Column(db.String(120), nullable=False)

# --- API ENDPOINTS ---

# THIS IS THE UPDATED ROUTE
@app.route('/')
def home():
    """Renders the main HTML page for the user interface."""
    return render_template('index.html')

@app.route('/api/track', methods=['POST'])
def track_product():
    data = request.get_json()
    if not data or not all(key in data for key in ['product_url', 'target_price', 'user_email']):
        return jsonify({"error": "Missing required data."}), 400
    try:
        new_product = Product(
            product_url=data['product_url'],
            target_price=float(data['target_price']),
            user_email=data['user_email']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product is now being tracked successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add product."}), 500

# --- MAIN EXECUTION BLOCK ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)