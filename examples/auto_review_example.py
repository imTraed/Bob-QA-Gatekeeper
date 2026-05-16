"""
Ejemplo de uso del sistema de Auto-Review de Bob-QA Gatekeeper
Muestra cómo integrar el análisis automático en tu flujo de trabajo
"""
import requests
import json


# Configuración
API_BASE_URL = "http://localhost:5000"


def analyze_code_example():
    """
    Ejemplo 1: Analizar código y guardar en base de datos
    """
    print("=" * 60)
    print("EJEMPLO 1: Análisis Completo con Guardado")
    print("=" * 60)
    
    # Código de ejemplo (con vulnerabilidad SQL injection)
    code = """
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
"""
    
    # Enviar a análisis
    response = requests.post(
        f"{API_BASE_URL}/auto/analyze",
        json={
            "code": code,
            "reviewer_name": "Juan Pérez",
            "project_name": "Sistema de Usuarios",
            "ai_model": "GPT-4"
        }
    )
    
    result = response.json()
    
    if result['success']:
        print(f"\n✅ Análisis completado")
        print(f"📝 Audit ID: {result['audit_id']}")
        print(f"\n📊 Análisis:")
        print(f"   Puntuación de Riesgo: {result['analysis']['risk_score']}")
        print(f"   Nivel: {result['analysis']['risk_level']}")
        print(f"   Resumen: {result['analysis']['summary']}")
        
        print(f"\n🎯 Acción:")
        print(f"   Estado: {result['action']['status']}")
        print(f"   {result['action']['icon']} {result['action']['message']}")
        print(f"   Puede desarrollar: {'✅' if result['action']['can_develop'] else '❌'}")
        print(f"   Puede hacer push: {'✅' if result['action']['can_proceed'] else '❌'}")
        
        if result['analysis']['risk_factors']:
            print(f"\n⚠️ Factores de Riesgo ({len(result['analysis']['risk_factors'])}):")
            for factor in result['analysis']['risk_factors']:
                print(f"   - [{factor['level']}] {factor['description']}")
        
        if result['analysis']['recommendations']:
            print(f"\n💡 Recomendaciones:")
            for rec in result['analysis']['recommendations']:
                print(f"   {rec}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print("\n")


def quick_check_example():
    """
    Ejemplo 2: Verificación rápida sin guardar
    """
    print("=" * 60)
    print("EJEMPLO 2: Verificación Rápida (Sin Guardar)")
    print("=" * 60)
    
    # Código seguro de ejemplo
    code = """
def format_date(date_string):
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return None
"""
    
    response = requests.post(
        f"{API_BASE_URL}/auto/quick-check",
        json={"code": code}
    )
    
    result = response.json()
    
    if result['success']:
        analysis = result['analysis']
        action = result['action']
        
        print(f"\n{action['icon']} {action['status']}")
        print(f"Puntuación: {analysis['risk_score']} ({analysis['risk_level']})")
        print(f"Mensaje: {action['message']}")
        
        if analysis['auto_approve']:
            print("\n✅ Este código puede ser aprobado automáticamente")
        elif analysis['block_deployment']:
            print("\n🛑 Este código está BLOQUEADO - requiere revisión humana")
        else:
            print("\n⏸️ Este código requiere revisión antes de push")
    
    print("\n")


def compare_codes_example():
    """
    Ejemplo 3: Comparar código inseguro vs seguro
    """
    print("=" * 60)
    print("EJEMPLO 3: Comparación de Código Inseguro vs Seguro")
    print("=" * 60)
    
    # Código INSEGURO
    unsafe_code = """
def process_payment(card_number, amount):
    # ❌ INSEGURO: SQL injection + credenciales hardcodeadas
    api_key = "sk-1234567890abcdef"
    query = f"INSERT INTO payments VALUES ('{card_number}', {amount})"
    db.execute(query)
"""
    
    # Código SEGURO
    safe_code = """
def process_payment(card_number, amount):
    # ✅ SEGURO: Consulta parametrizada + variables de entorno
    import os
    api_key = os.getenv('PAYMENT_API_KEY')
    query = "INSERT INTO payments VALUES (?, ?)"
    db.execute(query, (card_number, amount))
"""
    
    print("\n🔴 Analizando código INSEGURO...")
    unsafe_result = requests.post(
        f"{API_BASE_URL}/auto/quick-check",
        json={"code": unsafe_code}
    ).json()
    
    print(f"   Riesgo: {unsafe_result['analysis']['risk_score']} - {unsafe_result['analysis']['risk_level']}")
    print(f"   Estado: {unsafe_result['action']['status']}")
    
    print("\n🟢 Analizando código SEGURO...")
    safe_result = requests.post(
        f"{API_BASE_URL}/auto/quick-check",
        json={"code": safe_code}
    ).json()
    
    print(f"   Riesgo: {safe_result['analysis']['risk_score']} - {safe_result['analysis']['risk_level']}")
    print(f"   Estado: {safe_result['action']['status']}")
    
    print("\n📊 Comparación:")
    print(f"   Reducción de riesgo: {unsafe_result['analysis']['risk_score'] - safe_result['analysis']['risk_score']:.2f}")
    print(f"   Código inseguro: {'BLOQUEADO' if unsafe_result['analysis']['block_deployment'] else 'PERMITIDO'}")
    print(f"   Código seguro: {'BLOQUEADO' if safe_result['analysis']['block_deployment'] else 'PERMITIDO'}")
    
    print("\n")


def batch_analysis_example():
    """
    Ejemplo 4: Análisis en lote de múltiples archivos
    """
    print("=" * 60)
    print("EJEMPLO 4: Análisis en Lote")
    print("=" * 60)
    
    code_samples = [
        {
            "name": "utils.py",
            "code": "def add(a, b): return a + b"
        },
        {
            "name": "auth.py",
            "code": "password = 'admin123'  # Hardcoded password"
        },
        {
            "name": "db.py",
            "code": "query = f'DELETE FROM users WHERE id = {user_id}'"
        }
    ]
    
    results = []
    
    for sample in code_samples:
        response = requests.post(
            f"{API_BASE_URL}/auto/quick-check",
            json={"code": sample["code"]}
        )
        
        if response.status_code == 200:
            result = response.json()
            results.append({
                "file": sample["name"],
                "risk": result['analysis']['risk_score'],
                "level": result['analysis']['risk_level'],
                "blocked": result['analysis']['block_deployment']
            })
    
    print("\n📋 Resultados del Análisis en Lote:\n")
    print(f"{'Archivo':<15} {'Riesgo':<10} {'Nivel':<10} {'Estado'}")
    print("-" * 50)
    
    for r in results:
        status = "🔴 BLOQUEADO" if r['blocked'] else "🟢 OK"
        print(f"{r['file']:<15} {r['risk']:<10.2f} {r['level']:<10} {status}")
    
    blocked_count = sum(1 for r in results if r['blocked'])
    print(f"\n⚠️ Archivos bloqueados: {blocked_count}/{len(results)}")
    
    print("\n")


def integration_workflow_example():
    """
    Ejemplo 5: Flujo de trabajo completo de integración
    """
    print("=" * 60)
    print("EJEMPLO 5: Flujo de Trabajo de Integración")
    print("=" * 60)
    
    print("\n📝 Simulando flujo de desarrollo con IA...\n")
    
    # Paso 1: IA genera código
    print("1️⃣ IA genera código para función de login")
    ai_generated_code = """
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = db.execute(query).fetchone()
    return user is not None
"""
    
    # Paso 2: Análisis automático
    print("2️⃣ Sistema analiza automáticamente...")
    response = requests.post(
        f"{API_BASE_URL}/auto/quick-check",
        json={"code": ai_generated_code}
    )
    
    result = response.json()
    analysis = result['analysis']
    
    print(f"   Riesgo detectado: {analysis['risk_score']} ({analysis['risk_level']})")
    
    # Paso 3: Decisión basada en riesgo
    if analysis['block_deployment']:
        print("3️⃣ 🛑 CÓDIGO BLOQUEADO - Alto riesgo detectado")
        print("   Razón: SQL Injection vulnerability")
        print("   Acción: Solicitar revisión humana")
        
        # Paso 4: Mostrar recomendaciones
        print("\n4️⃣ 💡 Recomendaciones del sistema:")
        for rec in analysis['recommendations'][:3]:
            print(f"   {rec}")
        
        # Paso 5: Código corregido
        print("\n5️⃣ Desarrollador corrige el código:")
        fixed_code = """
def login(username, password):
    query = "SELECT * FROM users WHERE username=? AND password=?"
    user = db.execute(query, (username, password)).fetchone()
    return user is not None
"""
        
        # Paso 6: Re-análisis
        print("6️⃣ Re-análisis del código corregido...")
        fixed_response = requests.post(
            f"{API_BASE_URL}/auto/quick-check",
            json={"code": fixed_code}
        )
        
        fixed_result = fixed_response.json()
        fixed_analysis = fixed_result['analysis']
        
        print(f"   Nuevo riesgo: {fixed_analysis['risk_score']} ({fixed_analysis['risk_level']})")
        
        if not fixed_analysis['block_deployment']:
            print("7️⃣ ✅ Código aprobado - Puede proceder con el despliegue")
        else:
            print("7️⃣ ⚠️ Aún requiere revisión adicional")
    
    print("\n")


def main():
    """
    Ejecutar todos los ejemplos
    """
    print("\n" + "=" * 60)
    print("🤖 BOB-QA GATEKEEPER - EJEMPLOS DE AUTO-REVIEW")
    print("=" * 60 + "\n")
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code != 200:
            print("❌ Error: El servidor no está respondiendo")
            print("   Asegúrate de que Flask esté corriendo: python app.py")
            return
        
        # Ejecutar ejemplos
        analyze_code_example()
        quick_check_example()
        compare_codes_example()
        batch_analysis_example()
        integration_workflow_example()
        
        print("=" * 60)
        print("✅ Todos los ejemplos completados")
        print("=" * 60)
        print("\n💡 Próximos pasos:")
        print("   1. Visita el dashboard: http://localhost:5000/auto/dashboard")
        print("   2. Lee la guía completa: AUTO_REVIEW_GUIDE.md")
        print("   3. Integra con tu flujo de trabajo")
        print("\n")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que Flask esté corriendo: python app.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()

# Made with Bob
