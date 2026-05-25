{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Hospital Management System',
    'depends': ['base', 'crm'],

    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/res_partner_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/menu.xml',
        'reports/patient_report.xml',
    ],

    'application': True,
}
