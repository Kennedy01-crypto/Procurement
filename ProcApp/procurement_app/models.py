# procurement_app/models.py
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(80), nullable=False, default='ADA') # e.g., 'ADA', 'Chief Officer', etc.
    name = db.Column(db.String(100)) # To satisfy {{ current_user.name }} in dashboard
    aies = db.relationship('AIE', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    aies = db.relationship('AIE', backref='department_ref', lazy=True)

    def __repr__(self):
        return self.name

class AIE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aie_number = db.Column(db.String(20), unique=True, nullable=False)
    procurement_plan_id = db.Column(db.String(50))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    justification = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='draft')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    
    line_items = db.relationship('AIELineItem', backref='aie', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<AIE {self.aie_number}>'

class AIELineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    aie_id = db.Column(db.Integer, db.ForeignKey('aie.id'), nullable=False)

    def __repr__(self):
        return f'<AIELineItem {self.description}>'
