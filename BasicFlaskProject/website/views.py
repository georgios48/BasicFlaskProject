from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import JSON

from . import db
from website.models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# Creating note after login
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)
# Deleting note
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = JSON.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

        return jsonify({})