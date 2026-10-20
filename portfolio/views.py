from django.shortcuts import render
from .models import (
    Profile, SectionText, Service, MethodStep, Advantage, Plan, ComparisonRow, PriceItem,
)

# (view id, menu label). Each menu item opens one "page" (a group of sections) of the single-page site.
NAV = [
    ("accueil",    "Accueil"),
    ("equipe",     "Notre équipe"),
    ("methode",    "Notre méthode"),
    ("solutions",  "Nos solutions"),
    ("engagement", "Notre engagement"),
    ("formules",   "Nos formules"),
    ("tarifs",     "Nos tarifs"),
]


def index(request):
    """The whole site is rendered by this one view (single-page layout)."""
    p = Profile.objects.first()
    plans = list(Plan.objects.all())
    for plan, dot in zip(plans, ("dot-grey.png", "dot-navy.png", "dot-gold.png")):
        plan.dot = dot
    advantages = list(Advantage.objects.all())
    context = {
        "nav": NAV,
        "p": p,
        "descriptors": [s.strip() for s in (p.hero_services if p else "").split("|") if s.strip()],
        "t": {s.key: s for s in SectionText.objects.all()},
        "services": Service.objects.all(),
        "steps": MethodStep.objects.all(),
        "adv_left": advantages[:3],
        "adv_right": advantages[3:],
        "plans": plans,
        "rows": ComparisonRow.objects.all(),
        "carte": PriceItem.objects.filter(group="carte"),
        "paie": PriceItem.objects.filter(group="paie"),
    }
    return render(request, "portfolio/index.html", context)

