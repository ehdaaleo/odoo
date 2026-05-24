{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Hospital Management System',
    'depends': ['base'],

    'data': [
    'security/ir.model.access.csv',
    'views/patient_views.xml',
    'views/department_views.xml',
    'views/doctor_views.xml',
    'views/menu.xml',
],

    'application': True,
}