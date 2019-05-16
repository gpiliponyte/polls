# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Question, Choice, Answer

from django.contrib import admin

# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
