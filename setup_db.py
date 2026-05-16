"""
Database initialization script for Bob-QA Gatekeeper
Creates the SQLite database and audit_logs table with massive enterprise sample data
"""
import os
import sys
import random
from datetime import datetime, timedelta

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import config
from models import db, AuditLog

def create_app():
    """Create Flask application for database setup"""
    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app

def init_database(app, add_sample_data=True):
    """Initialize the database with tables and optional sample data"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully!")
        
        if add_sample_data:
            print("\nAdding enterprise sample audit logs...")
            add_sample_audits()
            print("✓ Sample data added successfully!")
        
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE")
        print("="*50)
        stats = AuditLog.get_statistics()
        print(f"\nTotal audit logs: {stats['total']}")
        print(f"Approved: {stats['approved']}")
        print(f"Pending: {stats['pending']}")
        print(f"High risk: {stats['high_risk']}")
        print(f"Approval rate: {stats['approval_rate']}%")

def add_sample_audits():
    """Add massive sample audit log entries for enterprise testing"""
    
    # 20 Corporate-level audits
    projects = ["Core Banking API", "Healthcare Patient Data", "Payment Gateway", "User Auth Service", "Trading Algorithm", "Government Cloud Connector", "HR Payroll System", "Logistics Optimizer"]
    reviewers = ["Alice Johnson", "Bob Smith", "Carol Martinez", "David Lee", "Elena Rostova", "Marcus Chen"]
    models = ["GPT-4o", "Claude-3.5-Sonnet", "Gemini 1.5 Pro", "Llama-3", "Mistral Large", "GitHub Copilot", "IBM Granite"]
    
    sample_audits = [
        # 1. High Risk SQL Injection
        {
            'code_snippet': '''def authenticate_admin(username, password):\n    query = "SELECT * FROM admins WHERE user = '" + username + "' AND pass = '" + password + "'"\n    db.execute(query)\n    return db.fetchone()''',
            'ai_risk_score': 0.95,
            'human_approved': False,
            'reviewer_name': 'David Lee',
            'timestamp': datetime.utcnow() - timedelta(minutes=15),
            'ai_model_name': 'IBM Granite',
            'project_name': 'Core Banking API',
            'comments': 'CRITICAL: Severe SQL Injection detected. Cannot be deployed under EU AI Act without fixing.'
        },
        # 2. Medium Risk Logging
        {
            'code_snippet': '''def log_transaction(amount, account_id, cc_number):\n    print(f"Transaction: {amount} from {account_id}")\n    # TODO: remove cc_number from logs\n    logger.info(f"Payment processed: {cc_number}")''',
            'ai_risk_score': 0.65,
            'human_approved': False,
            'reviewer_name': 'Alice Johnson',
            'timestamp': datetime.utcnow() - timedelta(minutes=45),
            'ai_model_name': 'Claude-3',
            'project_name': 'Payment Gateway',
            'comments': 'MEDIUM RISK: Logging PII (Credit Card). Pending revision.'
        },
        # 3. Low Risk formatting
        {
            'code_snippet': '''def format_currency(amount, currency="USD"):\n    if currency == "USD":\n        return f"${amount:,.2f}"\n    return f"{amount:,.2f} {currency}"''',
            'ai_risk_score': 0.12,
            'human_approved': True,
            'reviewer_name': 'Elena Rostova',
            'timestamp': datetime.utcnow() - timedelta(hours=2),
            'ai_model_name': 'IBM Watsonx',
            'project_name': 'Payment Gateway',
            'comments': 'Approved: Safe string formatting operation.'
        },
        # 4. High Risk Eval
        {
            'code_snippet': '''def execute_dynamic_rules(rule_string, context):\n    # Evaluates business rules dynamically\n    result = eval(rule_string, {}, context)\n    return result''',
            'ai_risk_score': 0.88,
            'human_approved': True,
            'reviewer_name': 'Carol Martinez',
            'timestamp': datetime.utcnow() - timedelta(hours=5),
            'ai_model_name': 'GPT-4',
            'project_name': 'Trading Algorithm',
            'comments': 'Approved after AI Auto-Correction applied AST parsing instead of eval().'
        },
        # 5. Low Risk DTO
        {
            'code_snippet': '''class PatientDTO:\n    def __init__(self, id, name, age):\n        self.id = id\n        self.name = name\n        self.age = age''',
            'ai_risk_score': 0.05,
            'human_approved': True,
            'reviewer_name': 'Bob Smith',
            'timestamp': datetime.utcnow() - timedelta(hours=6),
            'ai_model_name': 'IBM Granite',
            'project_name': 'Healthcare Patient Data',
            'comments': 'Auto-approved.'
        }
    ]
    
    # Generate 35 more random audits to bulk up the DB (bias toward Pending)
    for i in range(35):
        risk = random.random()
        
        if risk >= 0.7:
            approved = False # High risk is always pending human review
        elif risk >= 0.4:
            approved = random.choice([True, False, False, False]) # Medium is mostly pending
        else:
            approved = random.choice([True, False]) # Low is 50/50
            
        sample_audits.append({
            'code_snippet': f'''# Auto-generated module part {i}\ndef process_data_chunk_{i}(data):\n    """Processing telemetry"""\n    results = []\n    for item in data:\n        results.append(item * {random.randint(1,10)})\n    return results''',
            'ai_risk_score': risk,
            'human_approved': approved,
            'reviewer_name': random.choice(reviewers),
            'timestamp': datetime.utcnow() - timedelta(hours=random.randint(7, 72)),
            'ai_model_name': random.choice(models),
            'project_name': random.choice(projects),
            'comments': 'Auto-approved.' if approved else 'Pending manual review by QA team.'
        })
        
    for audit_data in sample_audits:
        audit = AuditLog(**audit_data)
        db.session.add(audit)
    
    db.session.commit()

def reset_database(app):
    with app.app_context():
        print("\nDropping all tables...")
        db.drop_all()
        print("Recreating tables...")
        db.create_all()
        print("\nAdding sample data...")
        add_sample_audits()
        print("\n[OK] Database reset complete!")

if __name__ == '__main__':
    app = create_app()
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database(app)
    else:
        init_database(app, add_sample_data=True)
