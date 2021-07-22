This is Django project with one application called app.
Used database is SQLite. Structure: one table with 3 fields: id, question_text, right_answer.
Django-adminn is enabled, has one created superuser with login: admin, password: admin.
Template structure: app has base template called app_layout.html. Other templates are located in app_templates folder and they are based on app_layout.html.
app has separete module urls.py wich all application url pathes. This module is included in main url controller of the project.

Tests for views checks if view url loads properly.
Bonus features weren't done. 
