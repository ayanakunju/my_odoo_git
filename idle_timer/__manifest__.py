# -*- coding: utf-8 -*-

{
    'name': "Idle Timer",
    'version': '17.0.3.0.0',
    'depends': ['base','survey'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
        This module gives an idle timer for the quiz, and accessible from the survey module.
    """,

    'data': [
            'views/config_settings.xml',
            'views/survey_timer.xml',
        ],
    'assets': {
        'survey.survey_assets': [
            'idle_timer/static/src/js/survey_timer.js'
        ],
    },
    'application': True,

}
