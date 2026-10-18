from django.core.management.base import BaseCommand
from portfolio.models import *

SERVICES = [
 ("01", "ADMINISTRATIF", ["Gestion administrative courante", "Gestion et organisation documentaire", "Classement et numérisation", "Facturation", "Suivi des réglements", "Suivi clients et fournisseurs", "Relances", "Téléprocédures", "Démarches administratives", "Organisation et suivi des dossiers"], "vous permettre de vous concentrer sur votre cœur de métier."),
 ("02", "COMPTABILITÉ", ["Collecte des pièces comptables", "Tri et classement", "Numérisation", "Organisation des justificatifs", "Centralisation des documents", "Suivi des factures clients et fournisseurs", "Préparation des éléments nécessaires à la comptabilité", "Intervention cabinet comptable pour la partie Réglementée."], "vous faire gagner du temps et faciliter le travail des experts-comptables."),
 ("03", "PAIE & RH", ["Collecte des variables de paie", "Gestion administrative de la paie", "Bulletins de salaire", "Déclarations sociales", "Administration du personnel", "Suivi des congés et absences", "Dossiers salariés", "Organisation documentaire RH", "Suivi administratif des entrées et sorties"], "simplifier la gestion de vos collaborateurs et vous faire gagner du temps."),
 ("04", "FINANCE", ["Suivi de trésorerie", "Prévisionnel de trésorerie", "Budget prévisionnel", "Suivi du chiffre d'affaires", "Suivi des charges", "Suivi des créances clients", "Suivi des dettes fournisseurs", "Analyse des écarts", "Tableaux de bord financiers", "Indicateurs de performance"], "vous donner une vision claire de votre situation financiére pour vous permettre d’anticiper."),
 ("05", "PILOTAGE", ["Tableaux de bord", "Reporting mensuel", "Suivi des objectifs", "Indicateurs de performance", "Analyse du chiffre d'affaires", "Analyse des écarts entre prévisionnel et réalisé", "Aide à la décision", "Accompagnement dans le pilotage de l’activité"], ""),
 ("06", "CRÉATION ENTREPRISES", ["Orientation dans les démarches de création", "Aide à la constitution des dossiers", "Préparation des documents administratifs", "Accompagnement dans les formalités", "Organisation administrative de votre activité", "Mise en place de vos premiers outils de gestion", "Aide à la mise en place de votre facturation", "Organisation et classement de vos documents", "Orientation vers les organismes et professionnels compétents"], "vous permettre de démarrer sur de bonnes bases et de construire progressivement une organisation adaptée à votre activité."),
]
STEPS = [("01", "ÉCOUTER :", "Nous commençons par vous."), ("02", "DIAGNOSTIQUER :", "Nous identifions ce qui doit être amélioré."), ("03", "STRUCTURER :", "Nous mettons de l'ordre dans votre gestion."), ("04", "PRENDRE EN CHARGE :", "Nous vous libérons du quotidien."), ("05", "COORDONNER :", "Itriel + vos partenaires."), ("06", "SUIVRE & PILOTER :", "Nous ne nous arrêtons pas à la prestation.")]
ADV = [("UN ACCOMPAIGNEMENT GLOBAL", "Administratif, pré-comptabilité, paie/RH, finance et pilotage."), ("UNE SOLUTION FLEXIBLE", "Vous choisissez les services dont vous avez réellement besoin."), ("UN GAIN DE TEMPS", "Vous vous concentrez sur votre activité et vos clients."), ("UNE MEILLEURE ORGANISATION", "Vos informations et documents sont structurés et facilement accessibles."), ("UNE MEILLEURE VISIBILITÉ", "Vous disposez d’outils pour suivre votre activité et votre trésorerie."), ("UN ACCOMPAIGNEMENT DANS LA DURÉE", "De la création de votre entreprise à son développement, votre accompagnement évolue avec vos besoins.")]
PLANS = [
 ("ESSENTIEL –", "Gestion administrative", "Pour les indépendants et petites TPE.", ["Gestion administrative", "Facturation", "Suivi clients/fournisseurs", "Classement et numérisation", "Téléprocedures", "Préparation et centralisation des éléments comptables", "Suivi administratif,"]),
 ("BUSINESS –", "Administratif + Finance + Paie/RH", "Pour les TPE/PME de quelques salariés.", ["Administratif", "Pré-comptabilité", "Suivi de trésorerie", "Facturation et relances", "Suivi fournisseurés", "Paie et administration RH", "Tableaux de bord financiers", "Suivi des principaux indicateurs"]),
 ("PILOTAGE –", "Direction financière externalisée", "Pour les PME qui veulent davantage de visibilité.", ["Budget prévisionnel", "Prévisionnel de trésorerie", "Suivi mensuel de trésorerie", "Analyse CA/marges/charges", "Tableaux de bord", "KPI, indicateur clé de performance.", "Analyse des écartes entre prévisionnel et réalisé ;", "Reporting mensuel;", "Préparation des éléments pour les rendez-vous avec l’expert-comptable ou le dirigeant;", "Aide à la décision."]),
]
ROWS = [("Pour qui ?", "Micro-entrepreneur / TPE", "TPE / PME", "PME / Dirigeant"), ("Administratif", "✓", "✓", "✓"), ("Pré-comptabilité", "✓", "✓", "✓"), ("Paie & RH", "Option", "✓", "✓"), ("Finance", "Option", "✓", "✓"), ("Suivi de trésorerie", "Option", "✓", "✓"), ("Tableau de bord", "—", "✓", "✓"), ("Reporting mensuel", "—", "—", "✓"), ("Analyse financière", "—", "—", "✓"), ("Aide au pilotage", "—", "—", "✓"), ("Tarif indicatif", "45–150 €/mois", "200–500 €/mois", "250–750 €+/mois")]
CARTE = [("Accompagnement création d'entreprise hors EI", "De 50 € à 120 €"), ("Accompagnement EI en Mico-entrepreneur ou autres régimes", "De 30 € à 75 €"), ("Diagnostic administratif & financier", "À partir de 75 €"), ("Collecte & organisation des pièces comptables-Préparation Bilan avec les experts comptables", "À partir de 250 €/année"), ("Suivi de trésorerie", "À partir de 25 €"), ("Tableau de bord financier", "À partir de 75 €"), ("Prévisionnel de trésorerie", "À partir de 50€"), ("Budget prévisionnel", "À partir de 100 €"), ("Mission administrative ponctuelle", "Sur devis"), ("Remise à niveau administrative", "Sur devis"), ("Accompagnement spécifique", "Sur devis")]
PAIE = [("Gestion complète de la paie", "19 € / bulletin", "Variables de paie, absences congés, maladie, IJSS, calcul et contrôle des bulletins"), ("DSN mensuelle", "Incluse", "Préparation, transmission et contrôle"), ("Contrôle DSN", "Inclus", "Vérification des retours et anomalies courantes"), ("DPAE", "10 € / salarié", "Réalisation et contrôle"), ("Entrée salarié complète", "20 € / salarié", "DPAE + dossier salarié + intégration en paie"), ("Contrat CDI/CDD simple", "30 €", "Rédaction du contrat"), ("Avenant simple", "15 €", "Rédaction et mise à jour du dossier"), ("Sortie salarié / STC", "35 €", "Solde de tout compte + documents de sortie"), ("Conseil RH", "20 € / heure", "Accompagnement RH courant"), ("Audit paie / RH", "À partir de 90 €", "Contrôle et analyse du dossier"), ("Reprise / mise en place d'un dossier paie", "À partir de 50 €", "Paramétrage et contrôle initial")]
DISC = "<strong>ITRIEL Consulting</strong> intervient en complément du cabinet d’expertise comptable et dans les limites des activités non réservées aux professionnels de l’expertise comptable."
TEXTS = {
 "solutions": ("VOTRE ENTREPRISE,", "NOS SOLUTIONS", "Chaque entreprise a des besoins différents. Que vous soyez en phase de création, de développement ou de croissance, <strong>Itriel Consulting</strong> vous accompagne avec des prestations modulables et adaptées à votre organisation.", ""),
 "method": ("NOTRE MÉTHODE", "UNE MÉTHODE SIMPLE, STRUCTURÉE ET PERSONNALISÉE", "Chez <strong>ITRIEL Consulting</strong>, nous ne nous contentons pas d'exécuter des tâches. Nous commençons par comprendre votre entreprise, nous organisons votre gestion, nous prenons en charge les missions définies ensemble et nous assurons un suivi régulier.", ""),
 "engagement": ("NOTRE ENGAGEMENT", "DE LA GESTION QUOTIDIENNE AU PILOTAGE DE VOTRE ENTREPRISE", "POURQUOI CHOISIR ITRIEL CONSULTING ?", ""),
 "offers": ("NOS OFFRES & TARIFS", "Des solutions adaptés à vos besoins", "On structure l'activité autour de 3 niveaux.", "Nos Formules"),
 "formules": ("NOS FORMULES", "DES SOLUTIONS QUI S’ADAPTENT À VOTRE ENTREPRISE", "★ BUSINESS — NOTRE FORMULE RECOMMANDÉE", "Un accompagnement complet pour les TPE/PME qui souhaitent externaliser leur back-office sans recruter."),
 "carte": ("NOS TARIFS À LA CARTE", "", "Les tarifs sont indicatifs et sont établis selon le volume, la complexité et le périmètre de la mission.", ""),
 "paie": ("GESTION PAIE & RH", "", "", ""),
}

class Command(BaseCommand):
    help = "Load the Itriel Consulting brochure content (verbatim from the PDF)."
    def handle(self, *a, **k):
        for m in (Profile, SectionText, Service, MethodStep, Advantage, Plan, ComparisonRow, PriceItem):
            m.objects.all().delete()
        Profile.objects.create(
            tagline="Votre gestion, Notre engagement", hero_question="VOUS ÊTES ENTREPRENEUR OU DIRIGEANT DE TPE/PEME ?",
            hero_cta="PARLONS DE VOTRE PROJET.", hero_brand="ITRIEL CONSULTING",
            hero_subtitle="Votre partenaire administratif et financier, à chaque étape de votre entreprise.",
            hero_services="Administratif • Comptabilité • Paie & RH • Finance • Création & Orientation • Pilotage",
            call_title="Premier échange — 30 minutes", phone="07 68 47 64 08", email="itriel.consul@gmail.com",
            linkedin="www.linkedin.com/in/itriel-consulting-878196438",
            expertise=[{"label": l, "icon": i} for l, i in [("Administratif", "folder-open"), ("Comptabilité Réglementé", "calculator"), ("Paie & RH", "users"), ("Finance", "chart-pie"), ("Création Orientation", "compass"), ("Pilotage", "chart-line")]],
            intro=["<strong>Itriel Consulting accompagne les Micos entrepreneurs, entrepreneurs, TPE et PME dans la gestion et le développement de leur activité.</strong>",
                   "Nous vous aidons à organiser votre entreprise, simplifier votre gestion au quotidien et piloter votre activité grâce à un accompagnement personnalisé.",
                   "Vous gagnez du temps. Vous êtes mieux organisé. Vous pilotez votre activité avec plus de visibilité.",
                   "Sans recruter. Sans créer un service administratif ou financier.<br>Une solution externalisée, flexible et adaptée à votre entreprise."],
            disclaimer=DISC)
        for k, (t, s, b, e) in TEXTS.items():
            SectionText.objects.create(key=k, title=t, subtitle=s, body=b, extra=e)
        for i, (n, t, it, o) in enumerate(SERVICES): Service.objects.create(number=n, title=t, items=it, objective=o, order=i)
        for n, t, x in STEPS: MethodStep.objects.create(number=n, title=t, text=x)
        for i, (t, x) in enumerate(ADV): Advantage.objects.create(title=t, text=x, order=i)
        for i, (n, s, a, sv) in enumerate(PLANS): Plan.objects.create(name=n, subtitle=s, audience=a, services=sv, order=i)
        for i, r in enumerate(ROWS): ComparisonRow.objects.create(label=r[0], essentiel=r[1], business=r[2], pilotage=r[3], order=i)
        for i, (l, p) in enumerate(CARTE): PriceItem.objects.create(group="carte", label=l, price=p, order=i)
        for i, (l, p, c) in enumerate(PAIE): PriceItem.objects.create(group="paie", label=l, price=p, included=c, order=i)
        self.stdout.write(self.style.SUCCESS("Contenu chargé."))
