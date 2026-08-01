from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    gifts = db.relationship(
        "Gift",
        backref="user",
        cascade="all, delete-orphan",
        order_by="Gift.position",
        lazy=True,
    )
    assigned_to = db.relationship(
        "User",
        remote_side=[id],
        foreign_keys=[assigned_to_id],
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "address": self.address}


class Gift(db.Model):
    __tablename__ = "gifts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    position = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "url": self.url,
            "notes": self.notes,
            "position": self.position,
        }
