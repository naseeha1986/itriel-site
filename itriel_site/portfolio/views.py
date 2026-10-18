import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import *


NAV=[("accueil","Accueil"),("presentation","Présentation"),("solutions","Solutions"),("methode","Méthode"),("engagement","Engagement"),("offres","Offres"),("formules","Formules"),("tarifs","Tarifs"),("paie","Paie & RH"),("contact","Contact")]


def index(request):
    services = list(Service.objects.all())
    ctx = {
        "p": Profile.objects.first(),
        "t": {s.key: s for s in SectionText.objects.all()},
        "groups": [
            {"id": "solutions", "services": services[:3], "first": True},
            {"id": "solutions-2", "services": services[3:], "first": False},
        ],
        "nav": NAV,
        "steps": MethodStep.objects.all(),
        "advantages": Advantage.objects.all(),
        "plans": Plan.objects.all(),
        "rows": ComparisonRow.objects.all(),
        "carte": PriceItem.objects.filter(group="carte"),
        "paie": PriceItem.objects.filter(group="paie"),
    }
    return render(request, "portfolio/index.html", ctx)


@require_POST
def contact_submit(request):
    try:
        data = json.loads(request.body or "{}")
    except ValueError:
        data = request.POST
    name, email = (data.get("name") or "").strip(), (data.get("email") or "").strip()
    subject, message = (data.get("subject") or "").strip(), (data.get("message") or "").strip()
    errors = {}
    if not name: errors["name"] = "Champ requis."
    if not subject: errors["subject"] = "Champ requis."
    if not message: errors["message"] = "Champ requis."
    try: validate_email(email)
    except ValidationError: errors["email"] = "E-mail invalide."
    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)
    ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
    return JsonResponse({"ok": True})
