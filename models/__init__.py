"""
Database models package for Bob-QA Gatekeeper
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to make them available
from models.audit_log import AuditLog

__all__ = ['db', 'AuditLog']

# Made with Bob
