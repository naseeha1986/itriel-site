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
ADV = [("Un accompagnement global", "Administratif, Comptable, paie/RH, finance et pilotage."), ("Une solution flexible", "Vous choisissez les services dont vous avez réellement besoin."), ("Un gain de temps", "Vous vous concentrez sur votre activité et vos clients."), ("Une meilleure visibilité", "Vous disposez d’outils pour suivre votre activité et votre trésorerie."), ("Une meilleure organisation", "Vos informations et documents sont structurés et facilement accessibles."), ("Un accompagnement dans la durée", "De la création de votre entreprise à son développement, votre accompagnement évolue avec vos besoins.")]
PLANS = [
 ("ESSENTIEL –", "Gestion administrative", "Pour les indépendants et petites TPE.", ["Gestion administrative", "Facturation", "Suivi clients/fournisseurs", "Classement et numérisation", "Téléprocedures", "Préparation et centralisation des éléments comptables", "Suivi administratif,"]),
 ("BUSINESS –", "Administratif + Finance + Paie/RH", "Pour les TPE/PME de quelques salariés.", ["Administratif", "Pré-comptabilité", "Suivi de trésorerie", "Facturation et relances", "Suivi fournisseurés", "Paie et administration RH", "Tableaux de bord financiers", "Suivi des principaux indicateurs"]),
 ("PILOTAGE –", "Direction financière externalisée", "Pour les PME qui veulent davantage de visibilité.", ["Budget prévisionnel", "Prévisionnel de trésorerie", "Suivi mensuel de trésorerie", "Analyse CA/marges/charges", "Tableaux de bord", "KPI, indicateur clé de performance.", "Analyse des écartes entre prévisionnel et réalisé ;", "Reporting mensuel;", "Préparation des éléments pour les rendez-vous avec l’expert-comptable ou le dirigeant;", "Aide à la décision."]),
]
ROWS = [("Pour qui ?", "Micro-entrepreneur / TPE", "TPE / PME", "PME / Dirigeant"), ("Administratif", "✓", "✓", "✓"), ("Pré-comptabilité", "✓", "✓", "✓"), ("Paie & RH", "Option", "✓", "✓"), ("Finance", "Option", "✓", "✓"), ("Suivi de trésorerie", "Option", "✓", "✓"), ("Tableau de bord", "—", "✓", "✓"), ("Reporting mensuel", "—", "—", "✓"), ("Analyse financière", "—", "—", "✓"), ("Aide au pilotage", "—", "—", "✓"), ("Tarif indicatif", "45–150 €/mois", "200–500 €/mois", "250–750 €+/mois")]
CARTE = [("Accompagnement création d'entreprise hors EI", "De 50 € à 120 €"), ("Accompagnement EI en Mico-entrepreneur ou autres régimes", "De 30 € à 75 €"), ("Diagnostic administratif & financier", "À partir de 75 €"), ("Collecte & organisation des pièces comptables-Préparation Bilan avec les experts comptables", "À partir de 250 €/année"), ("Suivi de trésorerie", "À partir de 25 €"), ("Tableau de bord financier", "À partir de 75 €"), ("Prévisionnel de trésorerie", "À partir de 50€"), ("Budget prévisionnel", "À partir de 100 €"), ("Mission administrative ponctuelle", "Sur devis"), ("Remise à niveau administrative", "Sur devis"), ("Accompagnement spécifique", "Sur devis")]
PAIE = [("Gestion complète de la paie", "19 € / bulletin", "Variables de paie, absences congés, maladie, IJSS, calcul et contrôle des bulletins"), ("DSN mensuelle", "Incluse", "Préparation, transmission et contrôle"), ("Contrôle DSN", "Inclus", "Vérification des retours et anomalies courantes"), ("DPAE", "10 € / salarié", "Réalisation et contrôle"), ("Entrée salarié complète", "20 € / salarié", "DPAE + dossier salarié + intégration en paie"), ("Contrat CDI/CDD simple", "30 €", "Rédaction du contrat"), ("Avenant simple", "15 €", "Rédaction et mise à jour du dossier"), ("Sortie salarié / STC", "35 €", "Solde de tout compte + documents de sortie"), ("Conseil RH", "20 € / heure", "Accompagnement RH courant"), ("Audit paie / RH", "À partir de 90 €", "Contrôle et analyse du dossier"), ("Reprise / mise en place d'un dossier paie", "À partir de 50 €", "Paramétrage et contrôle initial")]
DISC = "<strong>ITRIEL Consulting</strong> intervient en complément du cabinet d’expertise comptable et dans les limites des activités non réservées aux professionnels de l’expertise comptable."
ACCUEIL_LEFT = (
 "<h2>Une équipe engagée à vos côtés</h2>"
 "<p>ITRIEL Consulting accompagne les entrepreneurs, les indépendants, les TPE et les porteurs de projets dans leurs démarches professionnelles, leur organisation et le développement de leur activité.</p>"
 "<p>Forte de 15 ans d’expérience, notre équipe s’appuie sur ses compétences, sa connaissance du monde de l’entreprise et son engagement pour proposer un accompagnement personnalisé, adapté aux besoins et aux objectifs de chaque client.</p>"
 "<h2>Notre ambition : vous aider à avancer sereinement</h2>"
 "<p>De la réflexion initiale à la concrétisation de vos projets, nous vous accompagnons pour vous permettre d’aborder vos démarches avec davantage de clarté, de méthode et de sérénité.</p>"
 "<p>Nous souhaitons être un partenaire de confiance sur lequel vous pouvez compter pour structurer vos idées, faciliter votre parcours et contribuer au développement de votre activité.</p>")
ACCUEIL_RIGHT = (
 "<p>Chez ITRIEL Consulting, nous sommes convaincus que chaque projet mérite une attention particulière. Nous privilégions l’écoute, la proximité et la confiance afin de comprendre vos besoins et de vous orienter vers des solutions concrètes et adaptées.</p>"
 "<p>Notre approche repose sur la complémentarité des compétences, le sérieux du suivi et la volonté de construire des relations professionnelles durables.</p>"
 "<h2>ITRIEL Consulting, votre partenaire pour construire l’avenir de vos projets.</h2>"
 "<p>Vous avez une idée, un projet de création ou une activité à développer ? Échangeons ensemble sur vos besoins.</p>")
EQUIPE_BODY = (
 "<p class=\"exp\">15 ans d’expérience au service de la performance des entreprises</p>"
 "<h3 class=\"who\">BELAID NASSIMA</h3>"
 "<p class=\"role\">Présidente — ITRIEL</p>"
 "<p>J’accompagne les entrepreneurs, indépendants, TPE et PME dans la gestion quotidienne de leur activité et le développement de leurs projets. Une approche rigoureuse, personnalisée et orientée vers des solutions concrètes.</p>")
EQUIPE_EXTRA = (
 "<h3>MES DOMAINES D’INTERVENTION</h3>"
 "<ul>"
 "<li><u>COMPTABILITÉ &amp; GESTION</u> — suivi comptable, organisation administrative et pilotage de l’activité</li>"
 "<li><u>GESTION SOCIALE &amp; PAIE</u> — préparation des bulletins et démarches sociales</li>"
 "<li><u>GESTION ADMINISTRATIVE</u> — assistance dans les formalités et obligations de l’entreprise</li>"
 "<li><u>ACCOMPAGNEMENT ENTREPRENEURIAL</u> — création, structuration et suivi des projets</li>"
 "<li><u>CONSEIL &amp; ORGANISATION</u> — optimisation des méthodes et solutions adaptées</li>"
 "</ul>"
 "<h3>MA VISION</h3>"
 "<p>Une gestion rigoureuse, une organisation efficace et un accompagnement de confiance pour vous permettre de vous concentrer sur votre cœur de métier.</p>")
TEXTS = {
 "equipe": ("PROFIL EQUIPE ITRIEL", "Comptable & Gestionnaire d’entreprise", EQUIPE_BODY, EQUIPE_EXTRA),
 "accueil": ("", "", ACCUEIL_LEFT, ACCUEIL_RIGHT),
 "method": ("NOTRE MÉTHODE", "UNE MÉTHODE SIMPLE, STRUCTURÉE ET PERSONNALISÉE", "Chez <strong>ITRIEL Consulting</strong>, nous ne nous contentons pas d'exécuter des tâches. Nous commençons par comprendre votre entreprise, nous organisons votre gestion, nous prenons en charge les missions définies ensemble et nous assurons un suivi régulier.", ""),
 "solutions": ("VOTRE ENTREPRISE,", "NOS SOLUTIONS", "Chaque entreprise a des besoins différents. Que vous soyez en phase de création, de développement ou de croissance, <strong>Itriel Consulting</strong> vous accompagne avec des prestations modulables et adaptées à votre organisation.", ""),
 "engagement": ("NOTRE ENGAGEMENT", "DE LA GESTION QUOTIDIENNE AU PILOTAGE DE VOTRE ENTREPRISE", "POURQUOI CHOISIR ITRIEL CONSULTING ?", ""),
 "offers": ("Nos Formules", "", "On structure l'activité autour de 3 niveaux.", ""),
 "formules": ("DES SOLUTIONS QUI S’ADAPTENT À VOTRE ENTREPRISE", "", "★ BUSINESS — NOTRE FORMULE RECOMMANDÉE", "Un accompagnement complet pour les TPE/PME qui souhaitent externaliser leur back-office sans recruter."),
 "carte": ("NOS TARIFS À LA CARTE", "", "Les tarifs sont indicatifs et sont établis selon le volume, la complexité et le périmètre de la mission.", ""),
 "paie": ("GESTION PAIE & RH", "", "", ""),
}

class Command(BaseCommand):
    help = "Load the ITRIEL CONSULTING content (verbatim from the 9-page PDF)."
    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="replace existing content")
    def handle(self, *a, **k):
        if Profile.objects.exists() and not k["force"]:
            self.stdout.write("Contenu déjà présent, ignoré (utilisez --force pour remplacer).")
            return
        for m in (Profile, SectionText, Service, MethodStep, Advantage, Plan, ComparisonRow, PriceItem):
            m.objects.all().delete()
        Profile.objects.create(
            tagline="Votre gestion, notre engagement", hero_question="ITRIEL CONSULTING",
            hero_cta="À vos côtés pour entreprendre et développer vos projets", hero_brand="ITRIEL CONSULTING",
            hero_subtitle="Un accompagnement professionnel, une approche humaine et des solutions adaptées à vos ambitions.",
            hero_services="Comptabilité/Finance|Paie/RH|Démarches administratives",
            call_title="30 minutes d’entretien gratuites pour faire le point sur votre projet.",
            phone="07 68 47 64 08", email="itriel.consul@gmail.com", linkedin="",
            expertise=[{"label": l, "icon": i} for l, i in [("Administratif", "ic-folder.png"), ("Comptabilité Réglementée", "ic-calc.png"), ("Paie & RH", "ic-people.png"), ("Finance", "ic-pie.png"), ("Création Orientation", "ic-compass.png"), ("Pilotage", "ic-chart.png")]],
            intro=[], disclaimer=DISC)
        for key, (t, s, b, e) in TEXTS.items():
            SectionText.objects.create(key=key, title=t, subtitle=s, body=b, extra=e)
        for i, (n, t, it, o) in enumerate(SERVICES): Service.objects.create(number=n, title=t, items=it, objective=o, order=i)
        for n, t, x in STEPS: MethodStep.objects.create(number=n, title=t, text=x)
        for i, (t, x) in enumerate(ADV): Advantage.objects.create(title=t, text=x, order=i)
        for i, (n, s, a, sv) in enumerate(PLANS): Plan.objects.create(name=n, subtitle=s, audience=a, services=sv, order=i)
        for i, r in enumerate(ROWS): ComparisonRow.objects.create(label=r[0], essentiel=r[1], business=r[2], pilotage=r[3], order=i)
        for i, (l, p) in enumerate(CARTE): PriceItem.objects.create(group="carte", label=l, price=p, order=i)
        for i, (l, p, c) in enumerate(PAIE): PriceItem.objects.create(group="paie", label=l, price=p, included=c, order=i)
        self.stdout.write(self.style.SUCCESS("Contenu chargé."))
