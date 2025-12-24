from flask import Flask, request
from models import db, FertilizerBag, CarbonAuditLog
import os
from datetime import datetime

app = Flask(__name__)

# I configure my app here (I will use Environment Variables in Production)
# I am currently using SQLite for my local prototype, but I will use PostgreSQL for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///olkaria.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    """
    I handle the USSD logic loop from Africa's Talking here.
    My Flow: Welcome -> Enter Code -> Verify -> Result
    """
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    response = ""

    if text == '':
        # I handle Level 0: Main Menu
        response  = "CON Welcome to Olkaria Green-Verify \n"
        response += "1. Verify Fertilizer Bag \n"
        response += "2. Report Issue"

    elif text == '1':
        # I handle Level 1: Prompt for Code
        response = "CON Enter the 5-digit code found on the seal:"

    elif text.startswith('1*'):
        # I handle Level 2: Verification Logic
        user_code = text.split('*')[1]
        
        # --- I START MY LOGIC HERE ---
        # 1. I search the DB for the code provided by the user
        bag = FertilizerBag.query.filter_by(serial_code=user_code).first()

        if bag:
            if bag.is_verified:
                 # My Case: Double Scan (Possible Reuse/Fraud)
                 response = f"END WARNING: Code {user_code} was ALREADY used on {bag.verified_at}. \nPotential Counterfeit."
            else:
                 # My Case: Success - I record the "Burn Event" for Carbon Credits
                 bag.is_verified = True
                 bag.verified_at = datetime.utcnow()
                 
                 # In production, I would hash the phone number here
                 bag.farmer_phone_hash = "HASHED_PHONE_NUMBER" 
                 
                 db.session.commit()
                 
                 response = f"END CONFIRMED: Genuine KenGen Green Urea. \nBatch: {bag.batch_number}. \nSafe to plant. Usage recorded."
        else:
            # My Case: Invalid Code
            response = "END FAKE PRODUCT DETECTED. \nThis code does not exist in the Olkaria Registry."
        # --- I END MY LOGIC HERE ---

    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # I initialize the DB for testing
    app.run(debug=True)