from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models import Note, User
from app import db
from flask_login import login_required, current_user
import requests
import os
import random
import datetime
from dotenv import load_dotenv

load_dotenv()

main_bp = Blueprint('main', __name__)

# Unsplash API integration
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_API_URL = "https://api.unsplash.com/photos/random"

def get_random_nature_image():
    """Get a random nature image from Unsplash collection"""
    # Using Unsplash Source API (no key required)
    # Collection IDs for nature images
    nature_collections = [
        '3330448',  # Nature
        '4642521',  # Beautiful Nature
        '3694365',  # Landscapes
        '1319040',  # Peaceful Nature
        '1976082',  # Forests
        '1254524',  # Mountains
        '784236',   # Water & Lakes
        '762960',   # Flowers
        '1118894',  # Autumn
        '3403106'   # Spring
    ]
    
    collection_id = random.choice(nature_collections)
    width = 1600
    height = 900
    
    # Using Unsplash Source API which doesn't require authentication
    return f"https://source.unsplash.com/collection/{collection_id}/{width}x{height}?t={random.randint(1, 10000)}"

def get_daily_inspiration():
    """Get a daily inspirational quote"""
    try:
        # Using free Zen Quotes API
        response = requests.get("https://zenquotes.io/api/today")
        data = response.json()
        if data and len(data) > 0:
            return {
                'quote': data[0]['q'],
                'author': data[0]['a']
            }
    except Exception as e:
        print(f"Error fetching inspirational quote: {e}")
    
    # Fallback quotes if API fails
    fallback_quotes = [
        {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
        {"quote": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
        {"quote": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair"},
        {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
        {"quote": "Hardships often prepare ordinary people for an extraordinary destiny.", "author": "C.S. Lewis"},
        {"quote": "Start where you are. Use what you have. Do what you can.", "author": "Arthur Ashe"}
    ]
    
    # Use today's date as seed for consistent quote throughout the day
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    random.seed(today)
    quote = random.choice(fallback_quotes)
    random.seed()
    return quote

@main_bp.route('/')
def index():
    """Home page with all notes"""
    # Get daily inspiration
    inspiration = get_daily_inspiration()
    
    # If user is logged in, show their notes
    if current_user.is_authenticated:
        # Get pinned notes first, then other notes sorted by updated_at
        pinned_notes = Note.query.filter_by(user_id=current_user.id, is_pinned=True).order_by(Note.updated_at.desc()).all()
        other_notes = Note.query.filter_by(user_id=current_user.id, is_pinned=False).order_by(Note.updated_at.desc()).all()
        notes = pinned_notes + other_notes
        return render_template('index.html', notes=notes, inspiration=inspiration)
    else:
        # Show welcome page for non-authenticated users
        return render_template('welcome.html', inspiration=inspiration)

@main_bp.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    """Create a new note"""
    if request.method == 'POST':
        title = request.form.get('title', 'Untitled')
        content = request.form.get('content', '')
        color = request.form.get('color', '#ffffff')
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Get a random nature image for the background
        background_image = get_random_nature_image() if request.form.get('use_background', False) else None
        
        note = Note(
            title=title,
            content=content,
            color=color,
            tags=tags,
            background_image=background_image,
            user_id=current_user.id
        )
        
        db.session.add(note)
        db.session.commit()
        
        flash('Note created successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('new_note.html')

@main_bp.route('/note/<int:note_id>', methods=['GET'])
@login_required
def view_note(note_id):
    """View a single note"""
    note = Note.query.get_or_404(note_id)
    
    # Check if user owns this note
    if note.user_id != current_user.id:
        flash('You do not have permission to view this note.', 'danger')
        return redirect(url_for('main.index'))
        
    return render_template('view_note.html', note=note)

@main_bp.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    """Edit an existing note"""
    note = Note.query.get_or_404(note_id)
    
    # Check if user owns this note
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note.', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        note.title = request.form.get('title', 'Untitled')
        note.content = request.form.get('content', '')
        note.color = request.form.get('color', '#ffffff')
        
        tags = request.form.get('tags', '').split(',')
        note.tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Update background image if requested
        if request.form.get('change_background', False):
            note.background_image = get_random_nature_image()
        
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('main.view_note', note_id=note.id))
    
    return render_template('edit_note.html', note=note)

@main_bp.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    """Delete a note"""
    note = Note.query.get_or_404(note_id)
    
    # Check if user owns this note
    if note.user_id != current_user.id:
        flash('You do not have permission to delete this note.', 'danger')
        return redirect(url_for('main.index'))
        
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/note/<int:note_id>/toggle-pin', methods=['POST'])
@login_required
def toggle_pin(note_id):
    """Toggle pin status of a note"""
    note = Note.query.get_or_404(note_id)
    
    # Check if user owns this note
    if note.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403
        
    note.is_pinned = not note.is_pinned
    db.session.commit()
    return jsonify({'success': True, 'is_pinned': note.is_pinned})

@main_bp.route('/api/notes', methods=['GET'])
@login_required
def api_get_notes():
    """API endpoint to get all notes"""
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@main_bp.route('/api/notes/search', methods=['GET'])
@login_required
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
    
    notes = Note.query.filter(
        Note.user_id == current_user.id,
        ((Note.title.ilike(f'%{query}%')) | 
        (Note.content.ilike(f'%{query}%')))
    ).order_by(Note.updated_at.desc()).all()
    
    return render_template('index.html', notes=notes, search_query=query)

@main_bp.route('/api/tags', methods=['GET'])
@login_required
def get_tags():
    """Get all unique tags"""
    notes = Note.query.filter_by(user_id=current_user.id).all()
    all_tags = []
    for note in notes:
        all_tags.extend(note.tags or [])
    
    unique_tags = list(set(all_tags))
    return jsonify(unique_tags)

@main_bp.route('/api/random-background', methods=['GET'])
def random_background():
    """Get a random nature background image"""
    image_url = get_random_nature_image()
    return jsonify({'url': image_url})

# Public sharing routes
@main_bp.route('/note/<int:note_id>/share', methods=['POST'])
@login_required
def share_note(note_id):
    """Toggle public sharing for a note"""
    note = Note.query.get_or_404(note_id)
    
    # Check if user owns this note
    if note.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403
    
    # Toggle public status
    note.is_public = not note.is_public
    
    # Generate share ID and slug if making public
    if note.is_public and not note.share_id:
        note.generate_share_id()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_public': note.is_public,
        'share_url': url_for('main.public_note', slug=note.slug, _external=True) if note.is_public else None
    })

@main_bp.route('/p/<slug>', methods=['GET'])
def public_note(slug):
    """View a publicly shared note"""
    note = Note.query.filter_by(slug=slug, is_public=True).first_or_404()
    
    # Increment view count
    note.increment_view()
    db.session.commit()
    
    # Get related public notes with similar tags
    related_notes = []
    if note.tags:
        # Get all public notes except the current one
        potential_related = Note.query.filter(
            Note.id != note.id,
            Note.is_public == True
        ).all()
        
        # Filter notes that have at least one tag in common
        related_with_score = []
        for related in potential_related:
            if related.tags:  # Make sure the note has tags
                # Count matching tags
                matching_tags = set(note.tags).intersection(set(related.tags))
                if matching_tags:  # If there's at least one matching tag
                    related_with_score.append((related, len(matching_tags), related.view_count or 0))
        
        # Sort by number of matching tags (desc) and view count (desc)
        related_with_score.sort(key=lambda x: (x[1], x[2]), reverse=True)
        related_notes = [note for note, _, _ in related_with_score[:3]]
    
    return render_template('public_note.html', note=note, related_notes=related_notes)

@main_bp.route('/shared', methods=['GET'])
def shared_notes():
    """View all publicly shared notes"""
    public_notes = Note.query.filter_by(is_public=True).order_by(Note.view_count.desc()).all()
    return render_template('shared_notes.html', notes=public_notes)

@main_bp.route('/api/notes/compact', methods=['GET'])
@login_required
def compact_notes_view():
    """Get a compact view of all notes"""
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template('compact_view.html', notes=notes)
