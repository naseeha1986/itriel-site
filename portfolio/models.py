from django.db import models


class Profile(models.Model):
    """Page 1 (cover/contact) + page 2 (introduction)."""
    tagline = models.CharField(max_length=200)
    hero_question = models.CharField(max_length=200)
    hero_cta = models.CharField(max_length=200)
    hero_brand = models.CharField(max_length=100)
    hero_subtitle = models.CharField(max_length=250)
    hero_services = models.CharField(max_length=250)
    call_title = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    linkedin = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logo/", blank=True)
    expertise = models.JSONField(default=list, help_text="[{label, icon}]")
    intro = models.JSONField(default=list, help_text="4 paragraphs (HTML allowed)")
    disclaimer = models.TextField()
    def __str__(self): return "Profile"


class SectionText(models.Model):
    key = models.SlugField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=250, blank=True)
    body = models.TextField(blank=True)
    extra = models.TextField(blank=True)
    def __str__(self): return self.key


class Service(models.Model):
    number = models.CharField(max_length=2)
    title = models.CharField(max_length=100)
    items = models.JSONField(default=list)
    objective = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["order"]
    def __str__(self): return f"{self.number} {self.title}"


class MethodStep(models.Model):
    number = models.CharField(max_length=2)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    class Meta: ordering = ["number"]
    def __str__(self): return self.title


class Advantage(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=250)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["order"]
    def __str__(self): return self.title


class Plan(models.Model):
    name = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    audience = models.CharField(max_length=150)
    services = models.JSONField(default=list)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["order"]
    def __str__(self): return self.name


class ComparisonRow(models.Model):
    label = models.CharField(max_length=100)
    essentiel = models.CharField(max_length=60)
    business = models.CharField(max_length=60)
    pilotage = models.CharField(max_length=60)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["order"]
    def __str__(self): return self.label


class PriceItem(models.Model):
    GROUPS = [("carte", "Tarifs à la carte"), ("paie", "Gestion Paie & RH")]
    group = models.CharField(max_length=10, choices=GROUPS)
    label = models.CharField(max_length=200)
    price = models.CharField(max_length=60)
    included = models.CharField(max_length=250, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["group", "order"]
    def __str__(self): return self.label


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.name} – {self.subject}"
