"""
Main routes for Bob-QA Gatekeeper web interface
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, AuditLog
from datetime import datetime

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Dashboard/home page showing audit statistics and recent audits
    """
    # Get statistics
    stats = AuditLog.get_statistics()
    
    # Get recent audits
    recent_audits = AuditLog.get_recent_audits(limit=10)
    
    # Get pending audits count
    pending_count = AuditLog.query.filter_by(human_approved=False).count()
    
    return render_template('index.html', 
                         stats=stats, 
                         recent_audits=recent_audits,
                         pending_count=pending_count)


@main_bp.route('/audit/new', methods=['GET', 'POST'])
def new_audit():
    """
    Form for submitting new code audit
    """
    if request.method == 'POST':
        # Get form data
        code_snippet = request.form.get('code_snippet')
        ai_risk_score = float(request.form.get('ai_risk_score', 0.5))
        reviewer_name = request.form.get('reviewer_name')
        ai_model_name = request.form.get('ai_model_name', '')
        project_name = request.form.get('project_name', '')
        comments = request.form.get('comments', '')
        human_approved = request.form.get('human_approved') == 'on'
        
        # Validate required fields
        if not code_snippet or not reviewer_name:
            flash('Code snippet and reviewer name are required!', 'error')
            return redirect(url_for('main.new_audit'))
        
        # Create new audit log
        audit = AuditLog(
            code_snippet=code_snippet,
            ai_risk_score=ai_risk_score,
            human_approved=human_approved,
            reviewer_name=reviewer_name,
            ai_model_name=ai_model_name,
            project_name=project_name,
            comments=comments,
            timestamp=datetime.utcnow()
        )
        
        # Save to database
        db.session.add(audit)
        db.session.commit()
        
        flash(f'Audit log #{audit.id} created successfully!', 'success')
        return redirect(url_for('main.audit_detail', audit_id=audit.id))
    
    return render_template('audit_form.html')


@main_bp.route('/audit/<int:audit_id>')
def audit_detail(audit_id):
    """
    View details of a specific audit log with automatic AI solution generation
    """
    from ai_integration.risk_analyzer import analyze_code
    from ai_integration.ai_fixer import generate_fixes
    import os
    
    audit = AuditLog.query.get_or_404(audit_id)
    
    # Automatically generate AI solutions for all risk levels
    ai_solutions = None
    if True:
        # Analyze the code
        analysis = analyze_code(audit.code_snippet)
        
        # Override the analyzed risk score with the actual DB score so calculations make sense
        analysis['risk_score'] = audit.ai_risk_score
        
        # Generate 3 solutions automatically
        api_key = os.getenv('OPENAI_API_KEY')
        fixes_result = generate_fixes(
            code=audit.code_snippet,
            risk_analysis=analysis,
            api_key=api_key
        )
        
        ai_solutions = fixes_result
    
    return render_template('audit_detail.html', audit=audit, ai_solutions=ai_solutions)


@main_bp.route('/audit/<int:audit_id>/edit', methods=['GET', 'POST'])
def edit_audit(audit_id):
    """
    Edit an existing audit log
    """
    audit = AuditLog.query.get_or_404(audit_id)
    
    if request.method == 'POST':
        # Update audit fields
        audit.code_snippet = request.form.get('code_snippet', audit.code_snippet)
        audit.ai_risk_score = float(request.form.get('ai_risk_score', audit.ai_risk_score))
        audit.reviewer_name = request.form.get('reviewer_name', audit.reviewer_name)
        audit.ai_model_name = request.form.get('ai_model_name', audit.ai_model_name)
        audit.project_name = request.form.get('project_name', audit.project_name)
        audit.comments = request.form.get('comments', audit.comments)
        audit.human_approved = request.form.get('human_approved') == 'on'
        
        # Save changes
        db.session.commit()
        
        flash(f'Audit log #{audit.id} updated successfully!', 'success')
        return redirect(url_for('main.audit_detail', audit_id=audit.id))
    
    return render_template('audit_form.html', audit=audit, edit_mode=True)


@main_bp.route('/audit/<int:audit_id>/approve', methods=['POST'])
def approve_audit(audit_id):
    """
    Approve an audit log
    """
    audit = AuditLog.query.get_or_404(audit_id)
    audit.human_approved = True
    db.session.commit()
    
    flash(f'Audit log #{audit.id} approved!', 'success')
    return redirect(url_for('main.audit_detail', audit_id=audit.id))


@main_bp.route('/audit/<int:audit_id>/reject', methods=['POST'])
def reject_audit(audit_id):
    """
    Reject an audit log
    """
    audit = AuditLog.query.get_or_404(audit_id)
    audit.human_approved = False
    
    # Add rejection comment if provided
    rejection_comment = request.form.get('rejection_comment', '')
    if rejection_comment:
        audit.comments = f"{audit.comments}\n\nREJECTION: {rejection_comment}" if audit.comments else f"REJECTION: {rejection_comment}"
    
    db.session.commit()
    
    flash(f'Audit log #{audit.id} rejected!', 'warning')
    return redirect(url_for('main.audit_detail', audit_id=audit.id))


@main_bp.route('/audit/<int:audit_id>/export')
def export_audit(audit_id):
    """
    Export an approved audit log as a formal PDF report (Print View)
    """
    audit = AuditLog.query.get_or_404(audit_id)
    if not audit.human_approved:
        flash('Only approved audits can be exported.', 'warning')
        return redirect(url_for('main.audit_detail', audit_id=audit.id))
        
    return render_template('audit_report.html', audit=audit)


@main_bp.route('/audits')
def audit_history():
    """
    View all audit logs with filtering options
    """
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    risk_filter = request.args.get('risk', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Build query
    query = AuditLog.query
    
    # Apply status filter
    if status_filter == 'approved':
        query = query.filter_by(human_approved=True)
    elif status_filter == 'pending':
        query = query.filter_by(human_approved=False)
    
    # Apply risk filter
    if risk_filter == 'high':
        query = query.filter(AuditLog.ai_risk_score >= 0.7)
    elif risk_filter == 'medium':
        query = query.filter(AuditLog.ai_risk_score >= 0.4, AuditLog.ai_risk_score < 0.7)
    elif risk_filter == 'low':
        query = query.filter(AuditLog.ai_risk_score < 0.4)
    
    # Order by risk descending first, then by timestamp
    query = query.order_by(AuditLog.ai_risk_score.desc(), AuditLog.timestamp.desc())
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    audits = pagination.items
    
    return render_template('audit_history.html', 
                         audits=audits,
                         pagination=pagination,
                         status_filter=status_filter,
                         risk_filter=risk_filter)


@main_bp.route('/about')
def about():
    """
    About page with EU AI Act compliance information
    """
    return render_template('about.html')

# Made with Bob
