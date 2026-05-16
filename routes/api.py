"""
API routes for Bob-QA Gatekeeper
RESTful endpoints for programmatic access
"""
from flask import Blueprint, jsonify, request
from models import db, AuditLog
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/audits', methods=['GET'])
def get_audits():
    """
    Get all audit logs with optional filtering
    Query parameters:
    - status: 'approved', 'pending', or 'all' (default: 'all')
    - risk: 'high', 'medium', 'low', or 'all' (default: 'all')
    - limit: number of results (default: 50)
    """
    status = request.args.get('status', 'all')
    risk = request.args.get('risk', 'all')
    limit = request.args.get('limit', 50, type=int)
    
    # Build query
    query = AuditLog.query
    
    # Apply filters
    if status == 'approved':
        query = query.filter_by(human_approved=True)
    elif status == 'pending':
        query = query.filter_by(human_approved=False)
    
    if risk == 'high':
        query = query.filter(AuditLog.ai_risk_score >= 0.7)
    elif risk == 'medium':
        query = query.filter(AuditLog.ai_risk_score >= 0.4, AuditLog.ai_risk_score < 0.7)
    elif risk == 'low':
        query = query.filter(AuditLog.ai_risk_score < 0.4)
    
    # Get results
    audits = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'count': len(audits),
        'audits': [audit.to_dict() for audit in audits]
    })


@api_bp.route('/audits/<int:audit_id>', methods=['GET'])
def get_audit(audit_id):
    """
    Get a specific audit log by ID
    """
    audit = AuditLog.query.get(audit_id)
    
    if not audit:
        return jsonify({
            'success': False,
            'error': 'Audit log not found'
        }), 404
    
    return jsonify({
        'success': True,
        'audit': audit.to_dict()
    })


@api_bp.route('/audits', methods=['POST'])
def create_audit():
    """
    Create a new audit log
    Required fields: code_snippet, ai_risk_score, reviewer_name
    Optional fields: ai_model_name, project_name, comments, human_approved
    """
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    required_fields = ['code_snippet', 'ai_risk_score', 'reviewer_name']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
    
    # Validate ai_risk_score
    try:
        risk_score = float(data['ai_risk_score'])
        if not 0.0 <= risk_score <= 1.0:
            return jsonify({
                'success': False,
                'error': 'ai_risk_score must be between 0.0 and 1.0'
            }), 400
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'error': 'ai_risk_score must be a number'
        }), 400
    
    # Create audit log
    audit = AuditLog(
        code_snippet=data['code_snippet'],
        ai_risk_score=risk_score,
        reviewer_name=data['reviewer_name'],
        ai_model_name=data.get('ai_model_name', ''),
        project_name=data.get('project_name', ''),
        comments=data.get('comments', ''),
        human_approved=data.get('human_approved', False),
        timestamp=datetime.utcnow()
    )
    
    db.session.add(audit)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Audit log created successfully',
        'audit': audit.to_dict()
    }), 201


@api_bp.route('/audits/<int:audit_id>', methods=['PUT'])
def update_audit(audit_id):
    """
    Update an existing audit log
    """
    audit = AuditLog.query.get(audit_id)
    
    if not audit:
        return jsonify({
            'success': False,
            'error': 'Audit log not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update fields if provided
    if 'code_snippet' in data:
        audit.code_snippet = data['code_snippet']
    
    if 'ai_risk_score' in data:
        try:
            risk_score = float(data['ai_risk_score'])
            if not 0.0 <= risk_score <= 1.0:
                return jsonify({
                    'success': False,
                    'error': 'ai_risk_score must be between 0.0 and 1.0'
                }), 400
            audit.ai_risk_score = risk_score
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'ai_risk_score must be a number'
            }), 400
    
    if 'reviewer_name' in data:
        audit.reviewer_name = data['reviewer_name']
    
    if 'ai_model_name' in data:
        audit.ai_model_name = data['ai_model_name']
    
    if 'project_name' in data:
        audit.project_name = data['project_name']
    
    if 'comments' in data:
        audit.comments = data['comments']
    
    if 'human_approved' in data:
        audit.human_approved = bool(data['human_approved'])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Audit log updated successfully',
        'audit': audit.to_dict()
    })


@api_bp.route('/audits/<int:audit_id>/approve', methods=['POST'])
def approve_audit_api(audit_id):
    """
    Approve an audit log
    """
    audit = AuditLog.query.get(audit_id)
    
    if not audit:
        return jsonify({
            'success': False,
            'error': 'Audit log not found'
        }), 404
    
    audit.human_approved = True
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Audit log #{audit_id} approved',
        'audit': audit.to_dict()
    })


@api_bp.route('/audits/<int:audit_id>/reject', methods=['POST'])
def reject_audit_api(audit_id):
    """
    Reject an audit log
    """
    audit = AuditLog.query.get(audit_id)
    
    if not audit:
        return jsonify({
            'success': False,
            'error': 'Audit log not found'
        }), 404
    
    data = request.get_json() or {}
    rejection_comment = data.get('comment', '')
    
    audit.human_approved = False
    
    if rejection_comment:
        audit.comments = f"{audit.comments}\n\nREJECTION: {rejection_comment}" if audit.comments else f"REJECTION: {rejection_comment}"
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Audit log #{audit_id} rejected',
        'audit': audit.to_dict()
    })


@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get audit statistics
    """
    stats = AuditLog.get_statistics()
    
    return jsonify({
        'success': True,
        'statistics': stats
    })


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'Bob-QA Gatekeeper API'
    })

# Made with Bob
