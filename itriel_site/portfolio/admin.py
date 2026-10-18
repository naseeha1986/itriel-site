from django.contrib import admin
from .models import *
for m in (Profile, SectionText, Service, MethodStep, Advantage, Plan, ComparisonRow, PriceItem):
    admin.site.register(m)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    readonly_fields = ("created_at",)
