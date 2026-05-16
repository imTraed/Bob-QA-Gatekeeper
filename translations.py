"""
Internationalization (i18n) for Bob-QA Gatekeeper
Supports English and Spanish
"""

TRANSLATIONS = {
    'en': {
        # Navigation
        'nav_dashboard': 'Dashboard',
        'nav_new_audit': 'New Audit',
        'nav_history': 'History',
        'nav_auto_review': 'Auto-Review',
        'nav_about': 'About',
        'nav_compliance': 'EU AI Act Compliant',
        
        # Dashboard
        'dashboard_title': 'Bob-QA Gatekeeper',
        'dashboard_subtitle': 'AI Code Audit Panel - EU AI Act Compliance',
        'dashboard_tagline': 'NO BREACHES, ONLY BOLD MOVES',
        'dashboard_description': 'We empower you to take bold actions that secure your digital world and eliminate threats.',
        
        # Statistics
        'stats_total': 'Total Audits',
        'stats_approved': 'Approved',
        'stats_pending': 'Pending Review',
        'stats_high_risk': 'High Risk Blocked',
        'stats_avg_risk': 'Average Risk Score',
        
        # Audit Detail
        'audit_title': 'Audit Log',
        'audit_code_snippet': 'Code Snippet',
        'audit_review_comments': 'Review Comments',
        'audit_status': 'Status',
        'audit_risk_assessment': 'Risk Assessment',
        'audit_details': 'Details',
        'audit_actions': 'Actions',
        
        # Risk Levels
        'risk_low': 'LOW',
        'risk_medium': 'MEDIUM',
        'risk_high': 'HIGH',
        'risk_critical': 'CRITICAL',
        
        # Status
        'status_approved': 'Approved',
        'status_pending': 'Pending',
        'status_rejected': 'Rejected',
        
        # AI Solutions
        'ai_solutions_title': 'AI Auto-Generated Solutions',
        'ai_solutions_subtitle': 'Automatic Analysis Complete',
        'ai_solutions_detected': 'The AI has detected',
        'ai_solutions_code': 'code and automatically generated',
        'ai_solutions_alternatives': 'alternative solutions',
        'ai_solutions_original_risk': 'Original risk',
        'ai_solutions_solution': 'Solution',
        'ai_solutions_improvement': 'Improvement',
        'ai_solutions_approach': 'Approach',
        'ai_solutions_explanation': 'Explanation',
        'ai_solutions_corrected_code': 'Corrected Code',
        'ai_solutions_original': 'Original Risk',
        'ai_solutions_new': 'New Risk',
        
        # Buttons
        'btn_apply': 'Apply This Solution',
        'btn_edit_apply': 'Edit & Apply',
        'btn_copy_code': 'Copy Code',
        'btn_edit_audit': 'Edit Audit',
        'btn_approve': 'Approve',
        'btn_reject': 'Reject',
        'btn_revoke': 'Revoke Approval',
        'btn_back': 'Back to History',
        'btn_boost_security': 'Boost Security',
        'btn_about_cipher': 'About Cipher',
        
        # Warnings
        'warning_high_risk': 'HIGH RISK - Auto-Solutions Generated',
        'warning_review_required': 'Review Required',
        'warning_review_text': 'Please review the AI-generated solutions and choose the most appropriate one for your use case. You can also edit any solution before applying it.',
        
        # Details
        'detail_reviewer': 'Reviewer',
        'detail_ai_model': 'AI Model',
        'detail_project': 'Project',
        'detail_timestamp': 'Timestamp',
        'detail_subtitle': 'Detailed audit information',
        'options': 'Options',
        'human_oversight_verified': 'Human oversight verified',
        
        # Messages
        'msg_solution_applied': 'Solution applied successfully!',
        'msg_code_copied': 'Code copied to clipboard!',
        'msg_confirm_apply': 'Apply this solution to the audit?\\n\\nThis will update the code snippet and mark as approved.',
        
        # Footer
        'footer_mission': 'MISSION',
        'footer_vision': 'VISION',
        'footer_mission_text': 'Our mission is to provide innovative cybersecurity solutions that empower businesses to thrive securely in a dynamic cyber landscape.',
        'footer_vision_text': 'Our vision is to be a global leader in cybersecurity, creating a secure digital future for businesses through innovation and resilience against cyber threats.',
    },
    'es': {
        # Navegación
        'nav_dashboard': 'Panel',
        'nav_new_audit': 'Nueva Auditoría',
        'nav_history': 'Historial',
        'nav_auto_review': 'Auto-Revisión',
        'nav_about': 'Acerca de',
        'nav_compliance': 'Cumple con EU AI Act',
        
        # Dashboard
        'dashboard_title': 'Bob-QA Gatekeeper',
        'dashboard_subtitle': 'Panel de Auditoría de Código IA - Cumplimiento EU AI Act',
        'dashboard_tagline': 'SIN BRECHAS, SOLO MOVIMIENTOS AUDACES',
        'dashboard_description': 'Te empoderamos para tomar acciones audaces que aseguran tu mundo digital y eliminan amenazas.',
        
        # Estadísticas
        'stats_total': 'Auditorías Totales',
        'stats_approved': 'Aprobadas',
        'stats_pending': 'Pendientes de Revisión',
        'stats_high_risk': 'Alto Riesgo Bloqueadas',
        'stats_avg_risk': 'Puntuación Promedio de Riesgo',
        
        # Detalle de Auditoría
        'audit_title': 'Registro de Auditoría',
        'audit_code_snippet': 'Fragmento de Código',
        'audit_review_comments': 'Comentarios de Revisión',
        'audit_status': 'Estado',
        'audit_risk_assessment': 'Evaluación de Riesgo',
        'audit_details': 'Detalles',
        'audit_actions': 'Acciones',
        
        # Niveles de Riesgo
        'risk_low': 'BAJO',
        'risk_medium': 'MEDIO',
        'risk_high': 'ALTO',
        'risk_critical': 'CRÍTICO',
        
        # Estado
        'status_approved': 'Aprobado',
        'status_pending': 'Pendiente',
        'status_rejected': 'Rechazado',
        
        # Soluciones IA
        'ai_solutions_title': 'Soluciones Auto-Generadas por IA',
        'ai_solutions_subtitle': 'Análisis Automático Completado',
        'ai_solutions_detected': 'La IA ha detectado código de',
        'ai_solutions_code': 'y ha generado automáticamente',
        'ai_solutions_alternatives': 'soluciones alternativas',
        'ai_solutions_original_risk': 'Riesgo original',
        'ai_solutions_solution': 'Solución',
        'ai_solutions_improvement': 'Mejora',
        'ai_solutions_approach': 'Enfoque',
        'ai_solutions_explanation': 'Explicación',
        'ai_solutions_corrected_code': 'Código Corregido',
        'ai_solutions_original': 'Riesgo Original',
        'ai_solutions_new': 'Nuevo Riesgo',
        
        # Botones
        'btn_apply': 'Aplicar Esta Solución',
        'btn_edit_apply': 'Editar y Aplicar',
        'btn_copy_code': 'Copiar Código',
        'btn_edit_audit': 'Editar Auditoría',
        'btn_approve': 'Aprobar',
        'btn_reject': 'Rechazar',
        'btn_revoke': 'Revocar Aprobación',
        'btn_back': 'Volver al Historial',
        'btn_boost_security': 'Aumentar Seguridad',
        'btn_about_cipher': 'Acerca de Cipher',
        
        # Advertencias
        'warning_high_risk': 'ALTO RIESGO - Soluciones Auto-Generadas',
        'warning_review_required': 'Revisión Requerida',
        'warning_review_text': 'Por favor revisa las soluciones generadas por IA y elige la más apropiada para tu caso de uso. También puedes editar cualquier solución antes de aplicarla.',
        
        # Detalles
        'detail_reviewer': 'Revisor',
        'detail_ai_model': 'Modelo IA',
        'detail_project': 'Proyecto',
        'detail_timestamp': 'Fecha y Hora',
        'detail_subtitle': 'Información detallada de la auditoría',
        'options': 'Opciones',
        'human_oversight_verified': 'Supervisión humana verificada',
        
        # Mensajes
        'msg_solution_applied': '¡Solución aplicada exitosamente!',
        'msg_code_copied': '¡Código copiado al portapapeles!',
        'msg_confirm_apply': '¿Aplicar esta solución a la auditoría?\\n\\nEsto actualizará el fragmento de código y lo marcará como aprobado.',
        
        # Footer
        'footer_mission': 'MISIÓN',
        'footer_vision': 'VISIÓN',
        'footer_mission_text': 'Nuestra misión es proporcionar soluciones innovadoras de ciberseguridad que empoderen a las empresas para prosperar de forma segura en un panorama cibernético dinámico.',
        'footer_vision_text': 'Nuestra visión es ser líderes globales en ciberseguridad, creando un futuro digital seguro para las empresas a través de la innovación y la resiliencia contra las amenazas cibernéticas.',
    }
}

def get_translation(key, lang='en'):
    """Get translation for a key in specified language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def get_all_translations(lang='en'):
    """Get all translations for a language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en'])


# Add more translations for all pages
TRANSLATIONS['en'].update({
    # Index/Dashboard
    'welcome_title': 'Welcome to Bob-QA Gatekeeper',
    'welcome_subtitle': 'AI Code Audit Panel - EU AI Act Compliance',
    'recent_audits': 'Recent Audits',
    'view_all': 'View All',
    'no_audits': 'No audits found',
    
    # Audit Form
    'new_audit_title': 'Submit New Code Audit',
    'code_snippet_label': 'Code Snippet',
    'code_snippet_placeholder': 'Paste your code here...',
    'reviewer_name_label': 'Reviewer Name',
    'ai_model_label': 'AI Model Used',
    'project_name_label': 'Project Name',
    'risk_score_label': 'AI Risk Score',
    'comments_label': 'Comments',
    'approve_now': 'Approve Now',
    'submit_audit': 'Submit Audit',
    
    # Audit History
    'audit_history_title': 'Audit History',
    'filter_by': 'Filter by',
    'all_audits': 'All Audits',
    'approved_only': 'Approved Only',
    'pending_only': 'Pending Only',
    'high_risk_only': 'High Risk Only',
    
    # About Page
    'about_title': 'About Bob-QA Gatekeeper',
    'about_subtitle': 'EU AI Act Compliance Audit Panel',
    'overview': 'Overview',
    'compliance_features': 'Compliance Features',
    'risk_classification': 'Risk Classification',
    'key_features': 'Key Features',
    'system_info': 'System Info',
    'api_endpoints': 'API Endpoints',
    'resources': 'Resources',
    
    # Common
    'id': 'ID',
    'project': 'Project',
    'ai_model': 'AI Model',
    'risk_level': 'Risk Level',
    'status': 'Status',
    'reviewer': 'Reviewer',
    'timestamp': 'Timestamp',
    'actions': 'Actions',
    'view': 'View',
    'edit': 'Edit',
    'delete': 'Delete',
    'cancel': 'Cancel',
    'save': 'Save',
    'update': 'Update',
    'apply_filters': 'Apply Filters',
    'clear_filters': 'Clear Filters',
    'previous': 'Previous',
    'next': 'Next',
    'showing': 'Showing',
    'of': 'of',
    'no_results': 'No results found',
    'loading': 'Loading...',
    
    # Form Fields
    'required': 'Required',
    'optional': 'Optional',
    'paste_code': 'Paste the AI-generated code to be reviewed',
    'reviewer_help': 'Name of the human reviewer conducting the audit',
    'ai_model_help': 'Name and version of the AI model that generated the code',
    'project_help': 'Name of the project or module this code belongs to',
    'comments_help': 'Additional notes, concerns, or recommendations',
    'approve_help': 'Only approve code that meets all security, quality, and compliance requirements',
    
    # Risk Descriptions
    'risk_low_desc': 'Minimal oversight required',
    'risk_medium_desc': 'Standard review process',
    'risk_high_desc': 'Enhanced scrutiny required',
    
    # Quick Actions
    'quick_actions': 'Quick Actions',
    'submit_new_audit': 'Submit New Audit',
    'review_pending': 'Review Pending',
    'view_all_audits': 'View All Audits',
    
    # Table Headers
    'table_id': 'ID',
    'table_project': 'Project',
    'table_ai_model': 'AI Model',
    'table_risk': 'Risk Level',
    'table_status': 'Status',
    'table_reviewer': 'Reviewer',
    'table_timestamp': 'Timestamp',
    'table_actions': 'Actions',
    
    # Filters
    'filter_status': 'Status',
    'filter_risk': 'Risk Level',
    'filter_all': 'All',
    'filter_approved': 'Approved',
    'filter_pending': 'Pending',
    'filter_high': 'High (≥0.7)',
    'filter_medium': 'Medium (0.4-0.69)',
    'filter_low': 'Low (<0.4)',
    
    # Approval Rate
    'approval_rate': 'Approval Rate',
    
    # Audit Form Specific
    'audit_information': 'Audit Information',
    'code_snippet': 'Code Snippet',
    'ai_risk_score': 'AI Risk Score',
    'current': 'Current',
    'low_risk': 'Low Risk',
    'high_risk': 'High Risk',
    'risk_classification_help': 'Risk classification:',
    'approve_deployment': 'Approve this code for deployment',
    'approval_warning': 'Only approve code that meets all security, quality, and compliance requirements',
    
    # Messages
    'no_audits_found': 'No audit logs found',
    'create_first_audit': 'Create your first audit',
    'no_matching_filters': 'No audit logs found matching your filters',
    
    # About Page Content
    'overview_text': 'Bob-QA Gatekeeper is a comprehensive audit panel designed to ensure compliance with the European Union\'s AI Act by enforcing human oversight of AI-generated code before deployment.',
    'compliance_intro': 'This system addresses the critical need for transparency, accountability, and human-in-the-loop validation in AI-assisted software development, particularly for high-risk applications.',
    'key_compliance_features': 'Key Compliance Features:',
    'transparency': 'Transparency',
    'transparency_desc': 'All AI-generated code is logged with model information and timestamps',
    'human_oversight': 'Human Oversight',
    'human_oversight_desc': 'Mandatory human review and approval before deployment',
    'risk_assessment': 'Risk Assessment',
    'risk_assessment_desc': 'AI risk scoring for each code submission (0.0-1.0 scale)',
    'audit_trail': 'Audit Trail',
    'audit_trail_desc': 'Complete history of reviews, decisions, and justifications',
    'documentation': 'Documentation',
    'documentation_desc': 'Reviewer comments and compliance notes for each audit',
    'accountability': 'Accountability',
    'accountability_desc': 'Clear identification of reviewers and approval status',
    
    # System Info
    'version': 'Version',
    'framework': 'Framework',
    'database': 'Database',
    'license': 'License',
    'base_url': 'Base URL',
    'check_api_health': 'Check API Health',
    
    # IBM Badge
    'ibm_hackathon': 'IBM Hackathon Project',
    'built_for': 'Built for AI compliance and governance',
    
    # About Page - Features
    'dashboard_feature': 'Dashboard',
    'dashboard_feature_desc': 'Real-time statistics and recent audit overview',
    'audit_submission_feature': 'Audit Submission',
    'audit_submission_feature_desc': 'Easy-to-use form for submitting code reviews',
    'audit_history_feature': 'Audit History',
    'audit_history_feature_desc': 'Complete audit trail with filtering and search',
    'restful_api_feature': 'RESTful API',
    'restful_api_feature_desc': 'Programmatic access for CI/CD integration',
    'analytics_feature': 'Analytics',
    'analytics_feature_desc': 'Approval rates and risk distribution metrics',
    'export_feature': 'Export',
    'export_feature_desc': 'Generate compliance reports and documentation',
    
    # About Page - Links
    'eu_ai_act_site': 'EU AI Act Official Site',
    'flask_docs': 'Flask Documentation',
    'github_repo': 'GitHub Repository',
})

TRANSLATIONS['es'].update({
    # About Page - Features
    'dashboard_feature': 'Panel',
    'dashboard_feature_desc': 'Estadísticas en tiempo real y resumen de auditorías recientes',
    'audit_submission_feature': 'Envío de Auditoría',
    'audit_submission_feature_desc': 'Formulario fácil de usar para enviar revisiones de código',
    'audit_history_feature': 'Historial de Auditorías',
    'audit_history_feature_desc': 'Rastro de auditoría completo con filtrado y búsqueda',
    'restful_api_feature': 'API RESTful',
    'restful_api_feature_desc': 'Acceso programático para integración CI/CD',
    'analytics_feature': 'Analíticas',
    'analytics_feature_desc': 'Tasas de aprobación y métricas de distribución de riesgo',
    'export_feature': 'Exportar',
    'export_feature_desc': 'Generar informes de cumplimiento y documentación',
    
    # About Page - Links
    'eu_ai_act_site': 'Sitio Oficial EU AI Act',
    'flask_docs': 'Documentación de Flask',
    'github_repo': 'Repositorio GitHub',
})

TRANSLATIONS['es'].update({
    # Index/Dashboard
    'welcome_title': 'Bienvenido a Bob-QA Gatekeeper',
    'welcome_subtitle': 'Panel de Auditoría de Código IA - Cumplimiento EU AI Act',
    'recent_audits': 'Auditorías Recientes',
    'view_all': 'Ver Todas',
    'no_audits': 'No se encontraron auditorías',
    
    # Audit Form
    'new_audit_title': 'Enviar Nueva Auditoría de Código',
    'code_snippet_label': 'Fragmento de Código',
    'code_snippet_placeholder': 'Pega tu código aquí...',
    'reviewer_name_label': 'Nombre del Revisor',
    'ai_model_label': 'Modelo de IA Utilizado',
    'project_name_label': 'Nombre del Proyecto',
    'risk_score_label': 'Puntuación de Riesgo IA',
    'comments_label': 'Comentarios',
    'approve_now': 'Aprobar Ahora',
    'submit_audit': 'Enviar Auditoría',
    
    # Audit History
    'audit_history_title': 'Historial de Auditorías',
    'filter_by': 'Filtrar por',
    'all_audits': 'Todas las Auditorías',
    'approved_only': 'Solo Aprobadas',
    'pending_only': 'Solo Pendientes',
    'high_risk_only': 'Solo Alto Riesgo',
    
    # About Page
    'about_title': 'Acerca de Bob-QA Gatekeeper',
    'about_subtitle': 'Panel de Auditoría de Cumplimiento EU AI Act',
    'overview': 'Descripción General',
    'compliance_features': 'Características de Cumplimiento',
    'risk_classification': 'Clasificación de Riesgo',
    'key_features': 'Características Principales',
    'system_info': 'Información del Sistema',
    'api_endpoints': 'Endpoints de API',
    'resources': 'Recursos',
    
    # Common
    'id': 'ID',
    'project': 'Proyecto',
    'ai_model': 'Modelo IA',
    'risk_level': 'Nivel de Riesgo',
    'status': 'Estado',
    'reviewer': 'Revisor',
    'timestamp': 'Fecha y Hora',
    'actions': 'Acciones',
    'view': 'Ver',
    'edit': 'Editar',
    'delete': 'Eliminar',
    'cancel': 'Cancelar',
    'save': 'Guardar',
    'update': 'Actualizar',
    'apply_filters': 'Aplicar Filtros',
    'clear_filters': 'Limpiar Filtros',
    'previous': 'Anterior',
    'next': 'Siguiente',
    'showing': 'Mostrando',
    'of': 'de',
    'no_results': 'No se encontraron resultados',
    'loading': 'Cargando...',
    
    # Form Fields
    'required': 'Requerido',
    'optional': 'Opcional',
    'paste_code': 'Pega el código generado por IA para ser revisado',
    'reviewer_help': 'Nombre del revisor humano que realiza la auditoría',
    'ai_model_help': 'Nombre y versión del modelo de IA que generó el código',
    'project_help': 'Nombre del proyecto o módulo al que pertenece este código',
    'comments_help': 'Notas adicionales, preocupaciones o recomendaciones',
    'approve_help': 'Solo aprueba código que cumpla con todos los requisitos de seguridad, calidad y cumplimiento',
    
    # Risk Descriptions
    'risk_low_desc': 'Supervisión mínima requerida',
    'risk_medium_desc': 'Proceso de revisión estándar',
    'risk_high_desc': 'Escrutinio mejorado requerido',
    
    # Quick Actions
    'quick_actions': 'Acciones Rápidas',
    'submit_new_audit': 'Enviar Nueva Auditoría',
    'review_pending': 'Revisar Pendientes',
    'view_all_audits': 'Ver Todas las Auditorías',
    
    # Table Headers
    'table_id': 'ID',
    'table_project': 'Proyecto',
    'table_ai_model': 'Modelo IA',
    'table_risk': 'Nivel de Riesgo',
    'table_status': 'Estado',
    'table_reviewer': 'Revisor',
    'table_timestamp': 'Fecha y Hora',
    'table_actions': 'Acciones',
    
    # Filters
    'filter_status': 'Estado',
    'filter_risk': 'Nivel de Riesgo',
    'filter_all': 'Todos',
    'filter_approved': 'Aprobados',
    'filter_pending': 'Pendientes',
    'filter_high': 'Alto (≥0.7)',
    'filter_medium': 'Medio (0.4-0.69)',
    'filter_low': 'Bajo (<0.4)',
    
    # Approval Rate
    'approval_rate': 'Tasa de Aprobación',
    
    # Audit Form Specific
    'audit_information': 'Información de Auditoría',
    'code_snippet': 'Fragmento de Código',
    'ai_risk_score': 'Puntuación de Riesgo IA',
    'current': 'Actual',
    'low_risk': 'Riesgo Bajo',
    'high_risk': 'Riesgo Alto',
    'risk_classification_help': 'Clasificación de riesgo:',
    'approve_deployment': 'Aprobar este código para despliegue',
    'approval_warning': 'Solo aprueba código que cumpla con todos los requisitos de seguridad, calidad y cumplimiento',
    
    # Messages
    'no_audits_found': 'No se encontraron registros de auditoría',
    'create_first_audit': 'Crea tu primera auditoría',
    'no_matching_filters': 'No se encontraron registros de auditoría que coincidan con tus filtros',
    
    # About Page Content
    'overview_text': 'Bob-QA Gatekeeper es un panel de auditoría integral diseñado para garantizar el cumplimiento con la Ley de IA de la Unión Europea mediante la aplicación de supervisión humana del código generado por IA antes del despliegue.',
    'compliance_intro': 'Este sistema aborda la necesidad crítica de transparencia, responsabilidad y validación humana en el desarrollo de software asistido por IA, particularmente para aplicaciones de alto riesgo.',
    'key_compliance_features': 'Características Clave de Cumplimiento:',
    'transparency': 'Transparencia',
    'transparency_desc': 'Todo el código generado por IA se registra con información del modelo y marcas de tiempo',
    'human_oversight': 'Supervisión Humana',
    'human_oversight_desc': 'Revisión y aprobación humana obligatoria antes del despliegue',
    'risk_assessment': 'Evaluación de Riesgo',
    'risk_assessment_desc': 'Puntuación de riesgo IA para cada envío de código (escala 0.0-1.0)',
    'audit_trail': 'Rastro de Auditoría',
    'audit_trail_desc': 'Historial completo de revisiones, decisiones y justificaciones',
    'documentation': 'Documentación',
    'documentation_desc': 'Comentarios del revisor y notas de cumplimiento para cada auditoría',
    'accountability': 'Responsabilidad',
    'accountability_desc': 'Identificación clara de revisores y estado de aprobación',
    
    # System Info
    'version': 'Versión',
    'framework': 'Framework',
    'database': 'Base de Datos',
    'license': 'Licencia',
    'base_url': 'URL Base',
    'check_api_health': 'Verificar Salud de API',
    
    # IBM Badge
    'ibm_hackathon': 'Proyecto Hackathon IBM',
    'built_for': 'Construido para cumplimiento y gobernanza de IA',
    'audit_history_title': 'Historial de Auditorías',
    'filter_by': 'Filtrar por',
    'all_audits': 'Todas las Auditorías',
    'approved_only': 'Solo Aprobadas',
    'pending_only': 'Solo Pendientes',
    'high_risk_only': 'Solo Alto Riesgo',
})

# Made with Bob
