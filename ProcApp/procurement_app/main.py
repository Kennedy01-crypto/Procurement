# procurement_app/main.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('home.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/account')
@login_required
def account():
    return render_template('account.html', title="My Account")

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # This is placeholder data. You will need to fetch real data
    # for the logged-in user from your database.
    stats = {
        'aies_created': 15, 'aies_pending': 3, 'aies_approved_month': 8,
        'aies_rejected': 1, 'rlpos_received': 12, 'specs_pending': 2,
        'tenders_in_progress': 4, 'upcoming_deadlines': 1, 'active_tenders': 5,
        'submitted_bids': 20, 'pending_feedback': 4
    }
    # Placeholder for recent activities to avoid template errors
    recent_activities = []
    return render_template('dashboard.html', stats=stats, recent_activities=recent_activities)
