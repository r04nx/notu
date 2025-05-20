from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
import uuid
from slugify import slugify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.relationship('Note', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    color = db.Column(db.String(20), default='#ffffff')
    is_pinned = db.Column(db.Boolean, default=False)
    tags = db.Column(JSON, default=list)
    background_image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Public sharing fields
    is_public = db.Column(db.Boolean, default=False)
    share_id = db.Column(db.String(36), unique=True, nullable=True)
    slug = db.Column(db.String(255), unique=True, nullable=True)
    view_count = db.Column(db.Integer, default=0)
    allow_comments = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Note {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'color': self.color,
            'is_pinned': self.is_pinned,
            'tags': self.tags,
            'background_image': self.background_image,
            'is_public': self.is_public,
            'share_id': self.share_id,
            'slug': self.slug,
            'view_count': self.view_count,
            'allow_comments': self.allow_comments,
            'user_id': self.user_id,
            'author_username': self.author.username if self.author else None
        }
        
    def generate_share_id(self):
        """Generate a unique share ID and slug for public sharing"""
        if not self.share_id:
            self.share_id = str(uuid.uuid4())
        
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{self.share_id[:8]}"
        
        return self.share_id
        
    def increment_view(self):
        """Increment the view count for this note"""
        if self.view_count is None:
            self.view_count = 1
        else:
            self.view_count += 1
