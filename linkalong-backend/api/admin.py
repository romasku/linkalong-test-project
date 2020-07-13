from django.contrib import admin

from api import models

admin.site.register(models.Text)
admin.site.register(models.Sentence)
admin.site.register(models.Paragraph)
