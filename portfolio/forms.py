from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # hidden "honeypot" field: real visitors never see it, spam bots fill it in
    website = forms.CharField(required=False)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
