from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

LEAD_STATUSES = ["new", "contacted", "qualified", "won", "lost"]


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    leads = db.relationship("Lead", backref="customer", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    status = db.Column(db.String(20), nullable=False, default="new")
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship(
        "Note", backref="lead", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "customer_id": self.customer_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "lead_id": self.lead_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
