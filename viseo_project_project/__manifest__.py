# -*- coding: utf-8 -*-
{
    'name': "viseo_project_project",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'viseo_internal_request', 'hr_expense'],

    # always loaded
    'data': [
        # 'security/project_security.xml',
        'views/groups.xml',
        'views/project_assets.xml',
        'security/ir.model.access.csv',
        # 'views/project.xml',
        'views/new_project_views.xml',
        'views/others_cost.xml',
        'views/others_models.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
