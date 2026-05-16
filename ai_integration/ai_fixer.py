"""
AI Code Fixer - Generates automatic solutions for detected issues
Uses OpenAI API or compatible models to suggest fixes
"""
import os
import json
from typing import Dict, List, Optional
import requests


class AICodeFixer:
    """
    Generates code fixes using AI models (OpenAI, Anthropic, etc.)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize AI Code Fixer
        
        Args:
            api_key: API key for the AI service (or from environment)
            model: Model to use (gpt-4, gpt-3.5-turbo, claude-3, etc.)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
    def generate_fixes(self, code: str, risk_analysis: Dict) -> Dict:
        """
        Generate 3 alternative solutions for problematic code
        
        Args:
            code: The original problematic code
            risk_analysis: Analysis result from risk_analyzer
        
        Returns:
            Dictionary with 3 solutions and their re-analysis
        """
        if not self.api_key:
            return self._generate_mock_fixes(code, risk_analysis)
        
        # Build prompt for AI
        prompt = self._build_fix_prompt(code, risk_analysis)
        
        try:
            # Call AI API
            solutions = self._call_ai_api(prompt)
            
            # Re-analyze each solution
            analyzed_solutions = self._analyze_solutions(solutions, risk_analysis)
            
            return {
                'success': True,
                'original_code': code,
                'original_risk': risk_analysis['risk_score'],
                'solutions': analyzed_solutions,
                'model_used': self.model
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback': self._generate_mock_fixes(code, risk_analysis)
            }
    
    def _build_fix_prompt(self, code: str, risk_analysis: Dict) -> str:
        """Build prompt for AI to generate fixes"""
        
        # Extract risk factors
        risk_factors = risk_analysis.get('risk_factors', [])
        risk_descriptions = [f"- {f['description']}" for f in risk_factors[:5]]
        
        prompt = f"""You are a code security expert. Analyze the following code that has security issues and generate EXACTLY 3 alternative solutions.

PROBLEMATIC CODE:
```
{code}
```

DETECTED ISSUES:
{chr(10).join(risk_descriptions)}

RISK SCORE: {risk_analysis['risk_score']} ({risk_analysis['risk_level']})

INSTRUCTIONS:
1. Generate EXACTLY 3 different solutions
2. Each solution must be COMPLETE and functional
3. Each solution must use a different approach
4. Clearly explain what changes in each solution
5. Order the solutions from simplest to most robust

RESPONSE FORMAT (JSON):
{{
  "solution_1": {{
    "title": "Descriptive title",
    "code": "complete code here",
    "explanation": "Detailed explanation of changes",
    "approach": "Approach used (e.g., parameterization, validation, etc.)"
  }},
  "solution_2": {{
    "title": "Descriptive title",
    "code": "complete code here",
    "explanation": "Detailed explanation of changes",
    "approach": "Approach used"
  }},
  "solution_3": {{
    "title": "Descriptive title",
    "code": "complete code here",
    "explanation": "Detailed explanation of changes",
    "approach": "Approach used"
  }}
}}

Reply ONLY with the JSON, no additional text."""

        return prompt
    
    def _call_ai_api(self, prompt: str) -> List[Dict]:
        """Call AI API to generate solutions"""
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': 'Eres un experto en seguridad de código que genera soluciones seguras y bien explicadas.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(
            f'{self.api_base}/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Parse AI response
        content = result['choices'][0]['message']['content']
        
        # Extract JSON from response
        try:
            # Try to parse as JSON
            solutions_data = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                solutions_data = json.loads(json_match.group(1))
            else:
                # Try to find JSON object
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    solutions_data = json.loads(json_match.group(0))
                else:
                    raise ValueError("No se pudo extraer JSON de la respuesta")
        
        # Convert to list format
        solutions = []
        for i in range(1, 4):
            key = f'solution_{i}'
            if key in solutions_data:
                solutions.append(solutions_data[key])
        
        return solutions
    
    def _analyze_solutions(self, solutions: List[Dict], original_analysis: Dict) -> List[Dict]:
        """Re-analyze each solution to verify it's better"""
        from ai_integration.risk_analyzer import analyze_code
        
        analyzed = []
        
        for i, solution in enumerate(solutions, 1):
            # Analyze the fixed code
            new_analysis = analyze_code(solution['code'])
            
            # Calculate improvement
            improvement = original_analysis['risk_score'] - new_analysis['risk_score']
            improvement_percent = (improvement / original_analysis['risk_score'] * 100) if original_analysis['risk_score'] > 0 else 0
            
            analyzed.append({
                'solution_number': i,
                'title': solution.get('title', f'Solución {i}'),
                'code': solution['code'],
                'explanation': solution.get('explanation', ''),
                'approach': solution.get('approach', ''),
                'original_risk': original_analysis['risk_score'],
                'new_risk': new_analysis['risk_score'],
                'improvement': round(improvement, 2),
                'improvement_percent': round(improvement_percent, 1),
                'new_risk_level': new_analysis['risk_level'],
                'auto_approve': new_analysis['auto_approve'],
                'still_blocked': new_analysis['block_deployment'],
                'risk_factors_remaining': len(new_analysis['risk_factors']),
                'recommendations': new_analysis['recommendations'][:3]
            })
        
        # Sort by improvement (best first)
        analyzed.sort(key=lambda x: x['improvement'], reverse=True)
        
        return analyzed
    
    def _generate_mock_fixes(self, code: str, risk_analysis: Dict) -> Dict:
        """
        Generate mock fixes when API is not available
        Provides template-based solutions
        """
        from ai_integration.risk_analyzer import analyze_code
        
        solutions = []
        
        # Solution 1: Basic fix (parametrization)
        solution_1_code = self._apply_basic_fix(code, risk_analysis)
        analysis_1 = analyze_code(solution_1_code)
        
        solutions.append({
            'solution_number': 1,
            'title': 'Basic Solution: Parameterization',
            'code': solution_1_code,
            'explanation': 'Replaces string concatenation with parameterized queries to prevent injection.',
            'approach': 'Query parameterization',
            'original_risk': risk_analysis['risk_score'],
            'new_risk': analysis_1['risk_score'],
            'improvement': round(risk_analysis['risk_score'] - analysis_1['risk_score'], 2),
            'improvement_percent': round((risk_analysis['risk_score'] - analysis_1['risk_score']) / risk_analysis['risk_score'] * 100, 1) if risk_analysis['risk_score'] > 0 else 0,
            'new_risk_level': analysis_1['risk_level'],
            'auto_approve': analysis_1['auto_approve'],
            'still_blocked': analysis_1['block_deployment']
        })
        
        # Solution 2: Intermediate fix (validation + parametrization)
        solution_2_code = self._apply_intermediate_fix(code, risk_analysis)
        analysis_2 = analyze_code(solution_2_code)
        
        solutions.append({
            'solution_number': 2,
            'title': 'Intermediate Solution: Validation + Parameterization',
            'code': solution_2_code,
            'explanation': 'Adds input validation in addition to parameterization for greater security.',
            'approach': 'Input Validation + Parameterization',
            'original_risk': risk_analysis['risk_score'],
            'new_risk': analysis_2['risk_score'],
            'improvement': round(risk_analysis['risk_score'] - analysis_2['risk_score'], 2),
            'improvement_percent': round((risk_analysis['risk_score'] - analysis_2['risk_score']) / risk_analysis['risk_score'] * 100, 1) if risk_analysis['risk_score'] > 0 else 0,
            'new_risk_level': analysis_2['risk_level'],
            'auto_approve': analysis_2['auto_approve'],
            'still_blocked': analysis_2['block_deployment']
        })
        
        # Solution 3: Advanced fix (ORM + validation)
        solution_3_code = self._apply_advanced_fix(code, risk_analysis)
        analysis_3 = analyze_code(solution_3_code)
        
        solutions.append({
            'solution_number': 3,
            'title': 'Advanced Solution: ORM + Full Validation',
            'code': solution_3_code,
            'explanation': 'Uses ORM (SQLAlchemy) for complete database abstraction with robust validation.',
            'approach': 'ORM + Full Validation + Error Handling',
            'original_risk': risk_analysis['risk_score'],
            'new_risk': analysis_3['risk_score'],
            'improvement': round(risk_analysis['risk_score'] - analysis_3['risk_score'], 2),
            'improvement_percent': round((risk_analysis['risk_score'] - analysis_3['risk_score']) / risk_analysis['risk_score'] * 100, 1) if risk_analysis['risk_score'] > 0 else 0,
            'new_risk_level': analysis_3['risk_level'],
            'auto_approve': analysis_3['auto_approve'],
            'still_blocked': analysis_3['block_deployment']
        })
        
        return {
            'success': True,
            'original_code': code,
            'original_risk': risk_analysis['risk_score'],
            'solutions': solutions,
            'model_used': 'Template-based (No API key)',
            'note': 'Soluciones generadas por plantillas. Configura OPENAI_API_KEY para soluciones personalizadas con IA.'
        }
    
    def _apply_basic_fix(self, code: str, risk_analysis: Dict) -> str:
        """Apply basic template fix"""
        # Simple string replacement for common patterns
        fixed = code
        
        # Fix SQL injection
        if 'sql' in code.lower() or 'select' in code.lower():
            fixed = fixed.replace('f"', '"')
            fixed = fixed.replace("f'", "'")
            fixed = fixed.replace('{', '?').replace('}', '')
            if 'execute' in fixed:
                fixed += '\n# Nota: Usar parámetros: db.execute(query, (param1, param2))'
        
        # Fix hardcoded credentials
        if 'password' in code.lower() or 'api_key' in code.lower():
            fixed = '# Usar variables de entorno\nimport os\n' + fixed
            fixed = fixed.replace('= "', '= os.getenv("').replace('"', '")')
        
        return fixed
    
    def _apply_intermediate_fix(self, code: str, risk_analysis: Dict) -> str:
        """Apply intermediate template fix"""
        fixed = self._apply_basic_fix(code, risk_analysis)
        
        # Add input validation
        validation = """
# Validación de entrada
def validate_input(value):
    if not value or not isinstance(value, str):
        raise ValueError("Entrada inválida")
    # Sanitizar entrada
    return value.strip()

"""
        return validation + fixed
    
    def _apply_advanced_fix(self, code: str, risk_analysis: Dict) -> str:
        """Apply advanced template fix"""
        # Suggest ORM usage
        orm_code = """
# Solución con ORM (SQLAlchemy)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    
# Uso seguro con ORM
def get_user_safe(user_id):
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
"""
        return orm_code


# Singleton instance
_fixer = None

def get_fixer(api_key: Optional[str] = None, model: str = "gpt-4") -> AICodeFixer:
    """Get or create fixer instance"""
    global _fixer
    if _fixer is None or api_key:
        _fixer = AICodeFixer(api_key, model)
    return _fixer


def generate_fixes(code: str, risk_analysis: Dict, api_key: Optional[str] = None) -> Dict:
    """
    Convenience function to generate fixes
    
    Args:
        code: Problematic code
        risk_analysis: Risk analysis result
        api_key: Optional API key
    
    Returns:
        Dictionary with 3 solutions
    """
    fixer = get_fixer(api_key)
    return fixer.generate_fixes(code, risk_analysis)

# Made with Bob
