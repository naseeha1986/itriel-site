from django.contrib import admin
from .models import *
for m in (Profile, SectionText, Service, MethodStep, Advantage, Plan, ComparisonRow, PriceItem):
    admin.site.register(m)
