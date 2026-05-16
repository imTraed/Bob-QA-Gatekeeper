"""
Automatic Review Routes
Handles automatic code analysis and approval workflow
"""
from flask import Blueprint, request, jsonify, render_template
from models import db, AuditLog
from ai_integration.risk_analyzer import analyze_code
from ai_integration.ai_fixer import generate_fixes
from datetime import datetime

auto_review_bp = Blueprint('auto_review', __name__, url_prefix='/auto')


@auto_review_bp.route('/analyze', methods=['POST'])
def analyze_code_endpoint():
    """
    Automatic code analysis endpoint
    Analyzes code and returns risk assessment with auto-approval decision
    """
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({
            'success': False,
            'error': 'No code provided'
        }), 400
    
    code = data['code']
    context = data.get('context', {})
    
    # Analyze code automatically
    analysis = analyze_code(code, context)
    
    # Create audit log entry
    audit = AuditLog(
        code_snippet=code,
        ai_risk_score=analysis['risk_score'],
        human_approved=analysis['auto_approve'],  # Auto-approve if low risk
        reviewer_name=data.get('reviewer_name', 'Auto-Reviewer'),
        ai_model_name=data.get('ai_model', 'Bob-QA Auto-Analyzer'),
        project_name=data.get('project_name', 'Auto-Review'),
        comments=f"Análisis automático: {analysis['summary']}\n\nFactores: {len(analysis['risk_factors'])}",
        timestamp=datetime.utcnow()
    )
    
    db.session.add(audit)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'audit_id': audit.id,
        'analysis': analysis,
        'action': _get_action_message(analysis)
    })


@auto_review_bp.route('/quick-check', methods=['POST'])
def quick_check():
    """
    Quick code check without saving to database
    Returns immediate risk assessment
    """
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({
            'success': False,
            'error': 'No code provided'
        }), 400
    
    code = data['code']
    analysis = analyze_code(code)
    
    return jsonify({
        'success': True,
        'analysis': analysis,
        'action': _get_action_message(analysis)
    })


@auto_review_bp.route('/generate-fixes/<int:audit_id>', methods=['POST'])
def generate_fixes_endpoint(audit_id):
    """
    Generate 3 AI-powered solutions for a problematic audit
    """
    audit = AuditLog.query.get_or_404(audit_id)
    
    # Get API key from request or environment
    data = request.get_json() or {}
    api_key = data.get('api_key') or request.headers.get('X-API-Key')
    model = data.get('model', 'gpt-4')
    
    # Analyze current code
    analysis = analyze_code(audit.code_snippet)
    
    # Generate fixes
    fixes_result = generate_fixes(
        code=audit.code_snippet,
        risk_analysis=analysis,
        api_key=api_key
    )
    
    return jsonify({
        'success': True,
        'audit_id': audit_id,
        'fixes': fixes_result
    })


@auto_review_bp.route('/generate-fixes-inline', methods=['POST'])
def generate_fixes_inline():
    """
    Generate fixes for code without saving to database
    """
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({
            'success': False,
            'error': 'No code provided'
        }), 400
    
    code = data['code']
    api_key = data.get('api_key') or request.headers.get('X-API-Key')
    model = data.get('model', 'gpt-4')
    
    # Analyze code
    analysis = analyze_code(code)
    
    # Generate fixes
    fixes_result = generate_fixes(
        code=code,
        risk_analysis=analysis,
        api_key=api_key
    )
    
    return jsonify({
        'success': True,
        'fixes': fixes_result
    })


@auto_review_bp.route('/dashboard')
def auto_dashboard():
    """
    Dashboard for automatic review system
    Shows statistics and recent auto-reviews
    """
    # Get auto-review statistics
    total_auto = AuditLog.query.filter(
        AuditLog.ai_model_name.like('%Auto-Analyzer%')
    ).count()
    
    auto_approved = AuditLog.query.filter(
        AuditLog.ai_model_name.like('%Auto-Analyzer%'),
        AuditLog.human_approved == True
    ).count()
    
    auto_blocked = AuditLog.query.filter(
        AuditLog.ai_model_name.like('%Auto-Analyzer%'),
        AuditLog.ai_risk_score >= 0.7
    ).count()
    
    recent_auto = AuditLog.query.filter(
        AuditLog.ai_model_name.like('%Auto-Analyzer%')
    ).order_by(AuditLog.timestamp.desc()).limit(20).all()
    
    return render_template('auto_dashboard.html',
                         total_auto=total_auto,
                         auto_approved=auto_approved,
                         auto_blocked=auto_blocked,
                         recent_auto=recent_auto)


@auto_review_bp.route('/webhook', methods=['POST'])
def git_webhook():
    """
    Webhook endpoint for Git integration
    Automatically analyzes code from commits
    """
    data = request.get_json()
    
    # Extract code from commit (simplified)
    commits = data.get('commits', [])
    results = []
    
    for commit in commits:
        # In real implementation, would fetch actual code changes
        code = commit.get('message', '')  # Placeholder
        
        if code:
            analysis = analyze_code(code)
            
            # Create audit entry
            audit = AuditLog(
                code_snippet=code,
                ai_risk_score=analysis['risk_score'],
                human_approved=analysis['auto_approve'],
                reviewer_name='Git Webhook',
                ai_model_name='Bob-QA Auto-Analyzer',
                project_name=data.get('repository', {}).get('name', 'Unknown'),
                comments=f"Commit: {commit.get('id', 'unknown')}\n{analysis['summary']}",
                timestamp=datetime.utcnow()
            )
            
            db.session.add(audit)
            
            results.append({
                'commit_id': commit.get('id'),
                'analysis': analysis,
                'blocked': analysis['block_deployment']
            })
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'analyzed': len(results),
        'results': results
    })


def _get_action_message(analysis):
    """Generate action message based on analysis"""
    if analysis['block_deployment']:
        return {
            'status': 'BLOCKED',
            'icon': '🔴',
            'message': 'Despliegue bloqueado. Requiere revisión humana.',
            'can_proceed': False,
            'can_develop': False
        }
    elif analysis['require_review']:
        return {
            'status': 'REVIEW_REQUIRED',
            'icon': '🟡',
            'message': 'Desarrollo local permitido. Revisión requerida antes de push.',
            'can_proceed': False,
            'can_develop': True
        }
    else:
        return {
            'status': 'APPROVED',
            'icon': '🟢',
            'message': 'Aprobado automáticamente. Puede proceder.',
            'can_proceed': True,
            'can_develop': True
        }

# Made with Bob
