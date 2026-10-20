import re
import time
from django.core import signing
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import ContactForm
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
    ("contact",    "Contact"),
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
        "sent": request.GET.get("sent") == "1",
        "form_ts": signing.dumps(time.time(), salt="contact-form"),
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


def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR", "")) or "?"


def _hit(key, limit, window):
    """Count one event under `key`; True while it is still within `limit` per `window` seconds."""
    cache.add(key, 0, window)
    try:
        return cache.incr(key) <= limit
    except ValueError:
        cache.set(key, 1, window)
        return True


@require_POST
def contact(request):
    """Receives the contact form. Saves the message in the database (visible in /admin)
    and, if CONTACT_EMAIL + EMAIL_HOST are configured, also e-mails it to the client.
    Spam protection: honeypot, form timer, per-visitor and global rate limits, link limit, duplicates."""
    ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    def reply(ok, text, status=200):
        if ajax:
            return JsonResponse({"ok": ok, "message": text}, status=status)
        return redirect("/?sent=1#contact" if ok else "/#contact")

    thanks = "Merci, votre message a bien été envoyé."
    # 1. honeypot: bots fill the hidden field -> pretend success, store nothing
    if request.POST.get("website"):
        return reply(True, thanks)
    # 2. timer: a human needs a few seconds; a bot posts instantly or replays a very old form
    try:
        age = time.time() - signing.loads(request.POST.get("ts", ""), salt="contact-form", max_age=7200)
    except signing.BadSignature:
        return reply(False, "Le formulaire a expiré. Merci de recharger la page puis de réessayer.", 400)
    if age < 4:
        return reply(True, thanks)
    # 3. rate limits: per visitor (3 per hour, 8 per day) and for the whole site (40 per hour)
    ip = _client_ip(request)
    if not (_hit(f"c:h:{ip}", 3, 3600) and _hit(f"c:d:{ip}", 8, 86400) and _hit("c:all", 40, 3600)):
        return reply(False, "Trop de messages envoyés. Merci de réessayer plus tard.", 429)
    form = ContactForm(request.POST)
    if not form.is_valid():
        return reply(False, "Veuillez vérifier les champs du formulaire.", 400)
    d = form.cleaned_data
    # 4. content checks: too long, too many links, repeated text
    if len(d["message"]) > 3000 or len(re.findall(r"https?://|www\.", d["message"], re.I)) > 2:
        return reply(True, thanks)
    if not _hit("c:dup:" + str(hash((d["email"].lower(), d["message"][:200]))), 1, 86400):
        return reply(True, thanks)
    msg = form.save()
    # 5. e-mail the client (optional), at most 30 e-mails a day
    to = getattr(settings, "CONTACT_EMAIL", "")
    if to and getattr(settings, "EMAIL_HOST", "") and _hit("c:mail", 30, 86400):
        try:
            send_mail(
                subject=f"[ITRIEL CONSULTING] {msg.subject}",
                message=f"De : {msg.name} <{msg.email}>\n\n{msg.message}",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or to,
                recipient_list=[to], fail_silently=True,
            )
        except Exception:
            pass
    return reply(True, thanks)
