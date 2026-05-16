"""
Bob-QA Gatekeeper - Main Flask Application
EU AI Act Compliance Audit Panel for AI-Generated Code
"""
import os
from flask import Flask, render_template, session, request, redirect
from config import config
from models import db
from routes.main import main_bp
from routes.api import api_bp
from routes.auto_review import auto_review_bp
from translations import get_all_translations
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
    
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auto_review_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template filters
    register_template_filters(app)
    
    # Register context processors
    register_context_processors(app)
    
    # Register language routes
    register_language_routes(app)
    
    return app


def register_error_handlers(app):
    """Register custom error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return render_template('errors/500.html'), 500


def register_template_filters(app):
    """Register custom Jinja2 template filters"""
    
    @app.template_filter('risk_badge')
    def risk_badge_filter(risk_score):
        """Convert risk score to badge class"""
        if risk_score >= 0.7:
            return 'danger'
        elif risk_score >= 0.4:
            return 'warning'
        else:
            return 'success'
    
    @app.template_filter('risk_level')
    def risk_level_filter(risk_score):
        """Convert risk score to level text"""
        if risk_score >= 0.7:
            return 'HIGH'
        elif risk_score >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @app.template_filter('approval_badge')
    def approval_badge_filter(approved):
        """Convert approval status to badge class"""
        return 'success' if approved else 'secondary'
    
    @app.template_filter('approval_text')
    def approval_text_filter(approved):
        """Convert approval status to text"""
        return 'Approved' if approved else 'Pending'


def register_context_processors(app):
    """Register context processors for templates"""
    
    @app.context_processor
    def inject_language():
        """Inject current language and translations into all templates"""
        lang = session.get('language', 'en')
        translations = get_all_translations(lang)
        return {
            'current_lang': lang,
            't': translations
        }


def register_language_routes(app):
    """Register language switching routes"""
    
    @app.route('/set-language/<lang>')
    def set_language(lang):
        """Set user's preferred language"""
        if lang in ['en', 'es']:
            session['language'] = lang
        return redirect(request.referrer or '/')


if __name__ == '__main__':
    # Create application
    app = create_app()
    
    # Print startup information
    print("\n" + "="*80)
    print("Bob-QA Gatekeeper - EU AI Act Compliance Audit Panel with AI Auto-Correction")
    print("="*80)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"AI Integration: {'[ENABLED]' if os.getenv('OPENAI_API_KEY') else '[TEMPLATE MODE] (No API Key)'}")
    
    print("\n[ Web Interface ]")
    print("  Main Dashboard:")
    print("    http://localhost:5000/                    - Main Dashboard")
    print("    http://localhost:5000/audit/new           - Submit New Audit")
    print("    http://localhost:5000/audits              - Audit History")
    print("    http://localhost:5000/about               - About & Documentation")
    
    print("\n  [ AI Auto-Review System ]")
    print("    http://localhost:5000/auto/dashboard      - AI Auto-Review Dashboard")
    print("    Quick Test: Paste code and get instant analysis")
    print("    Generate 3 AI solutions for problematic code")
    print("    View auto-approval statistics")
    
    print("\n[ API Endpoints ]")
    print("  Standard Audit API:")
    print("    GET    /api/audits                           - List all audits")
    print("    POST   /api/audits                           - Create new audit")
    print("    GET    /api/audits/<id>                      - Get specific audit")
    print("    PUT    /api/audits/<id>                      - Update audit")
    print("    POST   /api/audits/<id>/approve              - Approve audit")
    print("    POST   /api/audits/<id>/reject               - Reject audit")
    print("    GET    /api/statistics                       - Get statistics")
    print("    GET    /api/health                           - Health check")
    
    print("\n  [ AI Auto-Review API ]")
    print("    POST   /auto/analyze                         - Analyze code & save to DB")
    print("    POST   /auto/quick-check                     - Quick analysis (no save)")
    print("    POST   /auto/generate-fixes/<id>             - Generate 3 AI solutions")
    print("    POST   /auto/generate-fixes-inline           - Generate fixes (no save)")
    print("    POST   /auto/webhook                         - Git webhook integration")
    print("    GET    /auto/dashboard                       - Auto-review dashboard")
    
    print("\n[ Risk Levels ]")
    print("    LOW    (0.0-0.4): Auto-approved, can proceed")
    print("    MEDIUM (0.4-0.7): Review required before push")
    print("    HIGH   (0.7-1.0): Blocked, requires human review")
    
    print("\n[ AI Features ]")
    print("    - Automatic risk detection (security, performance, maintainability)")
    print("    - Auto-approve/block based on risk score")
    print("    - Generate 3 alternative solutions with AI")
    print("    - Re-analyze each solution automatically")
    print("    - Show improvement percentage")
    print("    - Template mode (works without API key)")
    
    print("\n[ Quick Start ]")
    print("    1. Run 'python setup_db.py' if database doesn't exist")
    print("    2. (Optional) Set OPENAI_API_KEY for AI-powered solutions")
    print("    3. Visit http://localhost:5000/auto/dashboard")
    print("    4. Paste problematic code and click 'Analyze Code'")
    print("    5. If high risk, click 'Generate 3 AI Solutions'")
    print("    6. Choose the best solution or create your own")
    
    print("\n[ Documentation ]")
    print("    - README.md                 - General project documentation")
    
    print("\n[ Configuration ]")
    if os.getenv('OPENAI_API_KEY'):
        print("    [OK] OpenAI API Key: Configured")
        print(f"    [Model] {os.getenv('AI_MODEL', 'gpt-4')}")
    else:
        print("    [WARN] OpenAI API Key: Not configured (using template mode)")
        print("    Set OPENAI_API_KEY environment variable for AI-powered solutions")
        print("    Or create .env file with: OPENAI_API_KEY=sk-your-key-here")
    
    print("\nPress Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    # Run application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config.get('DEBUG', False)
    )

# Made with Bob - Production Ready Version with AI Auto-Correction
