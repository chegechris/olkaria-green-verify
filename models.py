from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FertilizerBag(db.Model):
    """
    I define this model to be the Digital Twin of a physical fertilizer bag.
    """
    __tablename__ = 'fertilizer_bags'

    id = db.Column(db.Integer, primary_key=True)
    serial_code = db.Column(db.String(12), unique=True, nullable=False, index=True)
    
    # I store my Traceability Data here
    batch_number = db.Column(db.String(50), nullable=False) # e.g., 'KEN-OLK-2025-BATCH1'
    production_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # I track the Verification Status with these fields
    is_verified = db.Column(db.Boolean, default=False)
    verification_count = db.Column(db.Integer, default=0)
    
    # I maintain this Audit Trail for Carbon Credits
    verified_at = db.Column(db.DateTime, nullable=True)
    farmer_phone_hash = db.Column(db.String(255), nullable=True) # I anonymize this for Privacy
    
    def __repr__(self):
        return f'<Bag {self.serial_code} | Batch {self.batch_number}>'

class CarbonAuditLog(db.Model):
    """
    I use this immutable log for Carbon Credit Auditors (Verra/Gold Standard).
    """
    id = db.Column(db.Integer, primary_key=True)
    bag_id = db.Column(db.Integer, db.ForeignKey('fertilizer_bags.id'))
    event_type = db.Column(db.String(20)) # I track types like 'VERIFICATION', 'FRAUD_ATTEMPT'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    origin_plant = db.Column(db.String(50), default='Olkaria-Naivasha')