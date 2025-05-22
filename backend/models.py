from datetime import datetime

from sqlalchemy import func

from extensions import db

class URLMapping(db.Model):
    """
    URLMapping model to store shortened URLs
    """
    __tablename__ = 'url_mappings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    long_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        """
        Returns a string representation of the URLMapping object
        """
        return f"<URLMapping {self.short_code} -> {self.long_url}>"

    def to_dict(self):
        """
        Returns a dictionary representation of the URLMapping object
        """
        return {
            'id': self.id,
            'short_code': self.short_code,
            'long_url': self.long_url,
            'created_at': self.created_at.isoformat()
        }