import os
import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, UserMixin
from sqlalchemy import text
from .forms import QuestionForm, LoginForm, UploadForm, EditForm, ContactForm
from .models import Note, Contact, db

# Import Google Gemini client
from google import genai

main = Blueprint('main', __name__)

# Initialize Gemini client
gemini_client = genai.Client(api_key=os.environ.get("GOOGLE_GEMINI_API_KEY"))

# Dummy Admin User for Flask-Login
class AdminUser(UserMixin):
    id = 1

# Home Page
@main.route("/")
def index():
    # Get the 4 most recent uploads
    latest_notes = Note.query.order_by(Note.created_at.desc()).limit(4).all()
    return render_template("index.html", latest_notes=latest_notes)

# Admin Login
@main.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'souravsj' and form.password.data == 'Sourav@123':
            login_user(AdminUser())
            session['admin'] = True
            flash('Login successful!', 'success')
            return redirect(request.args.get('next') or url_for('main.admin_dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('admin_login.html', form=form)

# Admin Logout
@main.route('/logout')
def logout():
    session.pop('admin', None)
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.index'))

# Admin Dashboard
@main.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('main.admin_login'))
    form = UploadForm()
    notes = Note.query.all()
    return render_template('admin_dashboard.html', notes=notes, form=form)

# Upload Note (Cloudinary)
@main.route('/upload-note', methods=['POST'])
def upload_note():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.pdf_file.data
        if file:
            result = cloudinary.uploader.upload(
                file,
                resource_type="raw",
                folder="noteopedia_pdfs"
            )
            # Force direct download link for PDFs
            file_url = result.get("secure_url").replace(
    "/upload/",
    f"/upload/fl_attachment:{form.title.data.replace(' ', '_')}.pdf/"
)
            new_note = Note(
                title=form.title.data,
                subject=form.subject.data,
                level=form.level.data,
                type=form.type.data,
                file_url=file_url
            )
            db.session.add(new_note)
            db.session.commit()
            flash('✅ Note uploaded successfully!')
            return redirect(url_for('main.admin_dashboard'))

    flash('❌ Failed to upload note.', 'danger')
    return redirect(url_for('main.admin_dashboard'))

# Edit Note
@main.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = EditForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.subject = form.subject.data
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('edit_note.html', form=form)

# Delete Note
@main.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', 'success')
    return redirect(url_for('main.admin_dashboard'))

# About Page
@main.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(new_contact)
        db.session.commit()
        flash("✅ Message sent successfully!", "success")
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)

# Category View
@main.route('/category/<category_name>')
def category_view(category_name):
    level_map = {
        'class10_notes': 'Class 10',
        'puc_materials': 'PUC',
        'degree_notes': 'Degree',
        'competitive': 'Competitive'
    }
    level = level_map.get(category_name)
    if not level:
        return "Category not found", 404
    notes = Note.query.filter_by(level=level).order_by(Note.created_at.desc()).all()
    return render_template(f'{category_name}.html', notes=notes, category=level)

# Browse/Search Notes
@main.route('/browse')
def browse_notes():
    search = request.args.get('search', '')
    selected_type = request.args.get('type', '')
    selected_level = request.args.get('level', '')

    query = "SELECT title, subject, type, file_url, id FROM note WHERE 1=1"
    filters = {}

    if search:
        query += " AND (title LIKE :search OR subject LIKE :search)"
        filters["search"] = f"%{search}%"

    if selected_type:
        query += " AND type = :type"
        filters["type"] = selected_type

    if selected_level:
        query += " AND level = :level"
        filters["level"] = selected_level

    notes = db.session.execute(text(query), filters).fetchall()
    return render_template('search.html', notes=notes, search=search, selected_type=selected_type, selected_level=selected_level)

# Ask Question (Google Gemini)
@main.route('/ask', methods=['GET', 'POST'])
def ask_question():
    form = QuestionForm()
    answer = None
    if form.validate_on_submit():
        user_question = form.question.data
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_question
            )
            answer = response.text
        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template("ask.html", form=form, answer=answer)
