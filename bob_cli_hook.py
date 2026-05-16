import sys
import subprocess
import json
import urllib.request
import urllib.error

# Bob-QA Gatekeeper Configuration
GATEKEEPER_URL = "http://localhost:5000/api/audits"
PROJECT_NAME = "IBM Hackathon Project"
REVIEWER_NAME = "Automated CI/CD Git Hook"
AI_MODEL = "Bob-QA Risk Analyzer (Local)"

def get_staged_changes():
    """Gets the diff of the files that are about to be committed."""
    try:
        result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error running git diff: {e}")
        return ""

def calculate_local_risk(code):
    """
    Simulates a fast risk evaluation using local heuristics.
    In production, this could call a small LLM or IBM Watson.
    """
    risk_score = 0.1 # Base risk
    
    # Dangerous keywords
    dangerous_keywords = [
        "password", "secret", "token", "API_KEY", 
        "eval(", "exec(", "SELECT *", "DROP TABLE",
        "os.system", "subprocess.Popen"
    ]
    
    code_lower = code.lower()
    found_risks = []
    
    for kw in dangerous_keywords:
        if kw.lower() in code_lower:
            risk_score += 0.4
            found_risks.append(kw)
    
    # Cap at 1.0 maximum
    return min(risk_score, 1.0), found_risks

def send_to_gatekeeper(code, risk_score):
    """Sends the code to the Bob-QA Gatekeeper panel via REST API."""
    data = {
        "code_snippet": code,
        "ai_risk_score": risk_score,
        "reviewer_name": REVIEWER_NAME,
        "ai_model_name": AI_MODEL,
        "project_name": PROJECT_NAME,
        "human_approved": False # Always requires human approval if high risk
    }
    
    req = urllib.request.Request(
        GATEKEEPER_URL, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return True, result.get('audit', {}).get('id')
    except Exception as e:
        print(f"\n[!] Warning: Could not connect to Bob-QA Gatekeeper at {GATEKEEPER_URL}")
        print(f"[!] Ensure Flask is running. Error: {e}")
        return False, None

def main():
    print("[INFO] Bob-QA Gatekeeper: Analyzing code before commit...")
    
    code = get_staged_changes()
    if not code:
        print("[OK] No code changes to analyze. Continuing...")
        sys.exit(0)
    
    # Calculate risk
    risk_score, risks_found = calculate_local_risk(code)
    
    print(f"[STAT] Calculated Risk Level: {risk_score:.2f}")
    if risks_found:
        print(f"[WARN] Dangerous patterns detected: {', '.join(risks_found)}")
    
    # Send to panel
    print("[NET]  Sending report to Bob-QA Gatekeeper...")
    success, audit_id = send_to_gatekeeper(code, risk_score)
    
    if success:
        print(f"[OK]   Audit registered successfully (ID: #{audit_id})")
    
    # Gatekeeper Logic (Middleware)
    if risk_score >= 0.7:
        print("\n" + "="*50)
        print("[ERROR] HIGH RISK DETECTED - COMMIT BLOCKED")
        print("="*50)
        print("The EU AI Act requires human oversight for this risk level.")
        print(f"Please open http://localhost:5000/audit/{audit_id} and approve the code.")
        print("Once approved, try committing again.")
        print("="*50 + "\n")
        sys.exit(1) # Block the commit
        
    elif risk_score >= 0.4:
        print("[WARN] Medium risk. Commit allowed, but code is pending review.")
        sys.exit(0) # Allow the commit
        
    else:
        print("[OK]   Low risk. Commit authorized automatically.")
        sys.exit(0) # Allow the commit

if __name__ == "__main__":
    main()
