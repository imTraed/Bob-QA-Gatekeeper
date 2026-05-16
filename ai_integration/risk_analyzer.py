"""
Automatic Risk Analyzer for AI-Generated Code
Analyzes code and assigns risk scores automatically
"""
import re
from typing import Dict, List, Tuple


class RiskAnalyzer:
    """
    Analyzes code and calculates risk score based on patterns and keywords
    """
    
    # High-risk patterns (0.7-1.0)
    HIGH_RISK_PATTERNS = {
        'sql_injection': r'(SELECT|INSERT|UPDATE|DELETE).*\+.*["\']',
        'hardcoded_credentials': r'(password|api_key|secret|token)\s*=\s*["\'][^"\']+["\']',
        'eval_exec': r'\b(eval|exec)\s*\(',
        'unsafe_deserialization': r'\b(pickle\.loads|yaml\.load|marshal\.load)\s*\(',
        'command_injection': r'\b(os\.system|subprocess\.call|subprocess\.run).*\+',
        'xss_vulnerability': r'innerHTML\s*=|document\.write\(',
        'crypto_weak': r'\b(md5|sha1)\s*\(',
        'file_operations': r'\b(open|read|write)\s*\(.*user',
    }
    
    # Medium-risk patterns (0.4-0.6)
    MEDIUM_RISK_PATTERNS = {
        'database_query': r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\b',
        'network_request': r'\b(requests\.get|requests\.post|fetch|axios)\b',
        'file_handling': r'\b(open|read|write|close)\s*\(',
        'authentication': r'\b(login|authenticate|authorize|session)\b',
        'payment': r'\b(payment|charge|transaction|billing)\b',
        'user_input': r'\b(input|request\.|params\.|query\.)\b',
        'encryption': r'\b(encrypt|decrypt|cipher|hash)\b',
    }
    
    # Low-risk patterns (0.0-0.3)
    LOW_RISK_PATTERNS = {
        'formatting': r'\b(format|strip|lower|upper|replace)\b',
        'logging': r'\b(log|print|console\.log|debug)\b',
        'comments': r'(#|//|/\*|\*/)',
        'constants': r'\b[A-Z_]{2,}\s*=',
        'simple_math': r'[\+\-\*/]\s*\d+',
    }
    
    # Critical keywords that increase risk
    CRITICAL_KEYWORDS = [
        'password', 'secret', 'token', 'api_key', 'private_key',
        'credit_card', 'ssn', 'admin', 'root', 'sudo',
        'DROP TABLE', 'DELETE FROM', 'TRUNCATE', 'ALTER TABLE'
    ]
    
    def __init__(self):
        self.risk_score = 0.0
        self.risk_factors = []
        self.recommendations = []
    
    def analyze(self, code: str, context: Dict = None) -> Dict:
        """
        Analyze code and return risk assessment
        
        Args:
            code: The code snippet to analyze
            context: Optional context (language, project_type, etc.)
        
        Returns:
            Dictionary with risk_score, risk_level, factors, and recommendations
        """
        self.risk_score = 0.0
        self.risk_factors = []
        self.recommendations = []
        
        if not code or not code.strip():
            return self._build_result(0.0, "No code provided")
        
        # Analyze high-risk patterns
        high_risk_count = self._check_patterns(code, self.HIGH_RISK_PATTERNS, 'HIGH')
        
        # Analyze medium-risk patterns
        medium_risk_count = self._check_patterns(code, self.MEDIUM_RISK_PATTERNS, 'MEDIUM')
        
        # Analyze low-risk patterns
        low_risk_count = self._check_patterns(code, self.LOW_RISK_PATTERNS, 'LOW')
        
        # Check for critical keywords
        critical_count = self._check_critical_keywords(code)
        
        # Calculate base risk score
        base_score = self._calculate_base_score(
            high_risk_count, 
            medium_risk_count, 
            low_risk_count,
            critical_count
        )
        
        # Adjust based on code complexity
        complexity_factor = self._analyze_complexity(code)
        
        # Final risk score
        self.risk_score = min(1.0, base_score + complexity_factor)
        
        # Generate recommendations
        self._generate_recommendations()
        
        return self._build_result(self.risk_score)
    
    def _check_patterns(self, code: str, patterns: Dict, risk_level: str) -> int:
        """Check code against pattern dictionary"""
        count = 0
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                count += len(matches)
                self.risk_factors.append({
                    'level': risk_level,
                    'pattern': pattern_name,
                    'matches': len(matches),
                    'description': self._get_pattern_description(pattern_name)
                })
        return count
    
    def _check_critical_keywords(self, code: str) -> int:
        """Check for critical security keywords"""
        count = 0
        for keyword in self.CRITICAL_KEYWORDS:
            if keyword.lower() in code.lower():
                count += 1
                self.risk_factors.append({
                    'level': 'CRITICAL',
                    'pattern': 'critical_keyword',
                    'keyword': keyword,
                    'description': f'Critical keyword detected: {keyword}'
                })
        return count
    
    def _calculate_base_score(self, high: int, medium: int, low: int, critical: int) -> float:
        """Calculate base risk score from pattern counts"""
        score = 0.0
        
        # Critical keywords have highest impact
        score += critical * 0.25
        
        # High-risk patterns
        score += high * 0.15
        
        # Medium-risk patterns
        score += medium * 0.08
        
        # Low-risk patterns slightly increase score
        score += low * 0.02
        
        return min(1.0, score)
    
    def _analyze_complexity(self, code: str) -> float:
        """Analyze code complexity and return adjustment factor"""
        lines = code.split('\n')
        line_count = len([l for l in lines if l.strip()])
        
        # More lines = slightly higher risk
        if line_count > 100:
            return 0.1
        elif line_count > 50:
            return 0.05
        elif line_count > 20:
            return 0.02
        
        return 0.0
    
    def _generate_recommendations(self):
        """Generate recommendations based on risk factors"""
        if self.risk_score >= 0.7:
            self.recommendations.append("[HIGH RISK] Mandatory human review required")
            self.recommendations.append("[BLOCK] Deployment blocked until approval")
            self.recommendations.append("[ACTION] Assign to senior reviewer")
        elif self.risk_score >= 0.4:
            self.recommendations.append("[MEDIUM RISK] Review recommended before production")
            self.recommendations.append("[WARN] Allow local dev, block cloud push")
            self.recommendations.append("[ACTION] Document changes carefully")
        else:
            self.recommendations.append("[LOW RISK] Can proceed with auto-approval")
            self.recommendations.append("[OK] Allow direct deployment")
            self.recommendations.append("[OK] Automatic audit logging")
        
        # Specific recommendations based on patterns
        for factor in self.risk_factors:
            if factor['level'] == 'CRITICAL' or factor['level'] == 'HIGH':
                pattern = factor.get('pattern', '')
                if 'sql' in pattern:
                    self.recommendations.append("[SUGGEST] Use parameterized queries to prevent SQL injection")
                elif 'credential' in pattern:
                    self.recommendations.append("[SUGGEST] Move credentials to environment variables")
                elif 'eval' in pattern or 'exec' in pattern:
                    self.recommendations.append("[SUGGEST] Avoid eval/exec, use safe alternatives")
                elif 'command' in pattern:
                    self.recommendations.append("[SUGGEST] Validate and sanitize input before executing commands")
    
    def _get_pattern_description(self, pattern_name: str) -> str:
        """Get human-readable description for pattern"""
        descriptions = {
            'sql_injection': 'Potential SQL injection vulnerability',
            'hardcoded_credentials': 'Hardcoded credentials in code',
            'eval_exec': 'Use of eval/exec (very dangerous)',
            'unsafe_deserialization': 'Unsafe deserialization',
            'command_injection': 'Potential command injection',
            'xss_vulnerability': 'Potential XSS vulnerability',
            'crypto_weak': 'Weak cryptographic algorithm',
            'file_operations': 'File operations with user input',
            'database_query': 'Database query',
            'network_request': 'Network request',
            'file_handling': 'File handling',
            'authentication': 'Authentication code',
            'payment': 'Payment processing',
            'user_input': 'User input handling',
            'encryption': 'Encryption operations',
            'formatting': 'Data formatting',
            'logging': 'Logging',
            'comments': 'Code comments',
            'constants': 'Constants definition',
            'simple_math': 'Simple math operations',
        }
        return descriptions.get(pattern_name, 'Pattern detected')
    
    def _build_result(self, score: float, message: str = None) -> Dict:
        """Build final result dictionary"""
        risk_level = self._get_risk_level(score)
        
        return {
            'risk_score': round(score, 2),
            'risk_level': risk_level,
            'risk_factors': self.risk_factors,
            'recommendations': self.recommendations,
            'auto_approve': score < 0.4,  # Auto-approve if low risk
            'block_deployment': score >= 0.7,  # Block if high risk
            'require_review': score >= 0.4,  # Require review if medium or high
            'message': message or f'Análisis completado: {risk_level}',
            'summary': self._generate_summary(score)
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Convert score to risk level"""
        if score >= 0.7:
            return 'HIGH'
        elif score >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_summary(self, score: float) -> str:
        """Generate human-readable summary"""
        if score >= 0.7:
            return f"[HIGH RISK] ({score:.2f}): Code blocked. Human review required before proceeding."
        elif score >= 0.4:
            return f"[MEDIUM RISK] ({score:.2f}): Local dev allowed. Review required before push."
        else:
            return f"[LOW RISK] ({score:.2f}): Auto-approval. Can proceed with deployment."


# Singleton instance
_analyzer = None

def get_analyzer() -> RiskAnalyzer:
    """Get or create analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = RiskAnalyzer()
    return _analyzer


def analyze_code(code: str, context: Dict = None) -> Dict:
    """
    Convenience function to analyze code
    
    Args:
        code: Code snippet to analyze
        context: Optional context information
    
    Returns:
        Risk analysis result
    """
    analyzer = get_analyzer()
    return analyzer.analyze(code, context)

# Made with Bob
