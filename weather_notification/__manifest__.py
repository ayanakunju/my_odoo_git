# -*- coding: utf-8 -*-
{
    'name': "Weather Notification",
    'version': '17.0.3.0.0',
    'depends': ['base', 'sale'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module add a new icon near systray icons, and it shows the current weather.
    """,

    'assets': {
        'web.assets_backend': [
            '/weather_notification/static/src/js/weather_notification.js',
            '/weather_notification/static/src/xml/weather_notification_template.xml',
        ],
    },
    'application': True,

}
