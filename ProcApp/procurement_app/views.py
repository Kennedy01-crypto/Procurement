
# procurement_app/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import AIEForm
from .models import AIE, AIELineItem, Department
from .extensions import db
from sqlalchemy.exc import IntegrityError
import datetime

aie_bp = Blueprint('aie', __name__, url_prefix='/aie')

def generate_aie_number():
    """Generates a unique AIE number based on the current date and sequence."""
    today = datetime.date.today()
    # Find the last AIE for today to determine the sequence number
    last_aie_today = AIE.query.filter(AIE.aie_number.like(f"AIE-{today.strftime('%Y%m%d')}-%")).order_by(AIE.id.desc()).first()
    
    if last_aie_today:
        last_seq = int(last_aie_today.aie_number.split('-')[-1])
        new_seq = last_seq + 1
    else:
        new_seq = 1
        
    return f"AIE-{today.strftime('%Y%m%d')}-{new_seq:04d}"

@aie_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_aie():
    form = AIEForm()
    if form.validate_on_submit():
        # Calculate total amount from line items to ensure data integrity
        total_amount = sum(item.quantity.data * item.unit_price.data for item in form.line_items)
        
        try:
            new_aie = AIE(
                aie_number=generate_aie_number(),
                procurement_plan_id=form.procurement_plan_id.data,
                department_id=form.department.data.id,
                amount=total_amount,
                justification=form.justification.data,
                author=current_user
            )
            db.session.add(new_aie)

            for item_form in form.line_items:
                line_item = AIELineItem(
                    description=item_form.description.data,
                    quantity=item_form.quantity.data,
                    unit_price=item_form.unit_price.data,
                    aie=new_aie
                )
                db.session.add(line_item)
            
            db.session.commit()
            flash('AIE has been created successfully!', 'success')
            return redirect(url_for('aie.list_aie'))
        except IntegrityError:
            db.session.rollback()
            flash('A server error occurred while generating the AIE number. Please try submitting again.', 'error')
        
    return render_template('aie/create_aie.html', form=form)

# Route to list all AIE requests
@aie_bp.route('/list')
@login_required
def list_aie():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status')

    query = AIE.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    # Use Flask-SQLAlchemy's paginate for efficient pagination
    pagination = query.order_by(AIE.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    aies = pagination.items
    return render_template('aie/aie_list.html', aies=aies, pagination=pagination)

# Route to show details for a specific AIE request
@aie_bp.route('/detail/<int:aie_id>')
@login_required
def aie_detail(aie_id):
    aie = AIE.query.get_or_404(aie_id)
    return render_template('aie/aie_detail.html', aie=aie)

# Placeholder route for reviewing an AIE to prevent BuildError
@aie_bp.route('/review/<int:aie_id>')
@login_required
def review_aie(aie_id):
    # In a real app, you would have a form or logic here
    flash(f'Review page for AIE ID {aie_id} is under construction.', 'info')
    return redirect(url_for('aie.list_aie'))

# Other routes for your application phases go here
@aie_bp.route('/approvals', methods=['GET'])
def approve_aie():
    return "Chief Officer AIE Approvals Page (under construction)"