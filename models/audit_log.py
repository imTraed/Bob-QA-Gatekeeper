"""
AuditLog model for tracking AI-generated code reviews
"""
from datetime import datetime
from models import db


class AuditLog(db.Model):
    """
    Model for storing audit logs of AI-generated code reviews.
    Complies with EU AI Act requirements for transparency and human oversight.
    """
    __tablename__ = 'audit_logs'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Core audit fields
    code_snippet = db.Column(db.Text, nullable=False)
    ai_risk_score = db.Column(db.Float, nullable=False)
    human_approved = db.Column(db.Boolean, default=False, nullable=False)
    reviewer_name = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # EU AI Act compliance fields
    ai_model_name = db.Column(db.String(200), nullable=True)
    project_name = db.Column(db.String(200), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        """String representation of AuditLog"""
        return f'<AuditLog {self.id}: {self.project_name} - {"Approved" if self.human_approved else "Pending"}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'code_snippet': self.code_snippet,
            'ai_risk_score': self.ai_risk_score,
            'human_approved': self.human_approved,
            'reviewer_name': self.reviewer_name,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'ai_model_name': self.ai_model_name,
            'project_name': self.project_name,
            'comments': self.comments,
            'risk_level': self.get_risk_level()
        }
    
    def get_risk_level(self):
        """
        Determine risk level based on AI risk score.
        Aligns with EU AI Act risk classification.
        """
        if self.ai_risk_score >= 0.7:
            return 'HIGH'
        elif self.ai_risk_score >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def get_recent_audits(limit=10):
        """Get most recent audit logs"""
        return AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def get_pending_audits():
        """Get all pending (not approved) audit logs"""
        return AuditLog.query.filter_by(human_approved=False).order_by(AuditLog.timestamp.desc()).all()
    
    @staticmethod
    def get_approved_audits():
        """Get all approved audit logs"""
        return AuditLog.query.filter_by(human_approved=True).order_by(AuditLog.timestamp.desc()).all()
    
    @staticmethod
    def get_high_risk_audits():
        """Get all high-risk audit logs (score >= 0.7)"""
        return AuditLog.query.filter(AuditLog.ai_risk_score >= 0.7).order_by(AuditLog.timestamp.desc()).all()
    
    @staticmethod
    def get_statistics():
        """Get audit statistics for dashboard"""
        total = AuditLog.query.count()
        approved = AuditLog.query.filter_by(human_approved=True).count()
        pending = AuditLog.query.filter_by(human_approved=False).count()
        high_risk = AuditLog.query.filter(AuditLog.ai_risk_score >= 0.7).count()
        
        return {
            'total': total,
            'approved': approved,
            'pending': pending,
            'high_risk': high_risk,
            'approval_rate': round((approved / total * 100) if total > 0 else 0, 2)
        }

# Made with Bob
