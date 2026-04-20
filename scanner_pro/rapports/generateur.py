# ============================================================
# GENERATEUR DE RAPPORT PDF
# ============================================================

import os
import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

class GenerateurRapport:
    def __init__(self):
        self.dossier_rapports = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "rapports"
        )
        os.makedirs(self.dossier_rapports, exist_ok=True)

    def generer(self, resultats):
        horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        cible_propre = resultats["cible"].replace(".", "_").replace("/", "_")
        nom_fichier = f"rapport_{cible_propre}_{horodatage}.pdf"
        chemin = os.path.join(self.dossier_rapports, nom_fichier)

        if REPORTLAB_OK:
            return self._generer_pdf(resultats, chemin)
        else:
            return self._generer_txt(resultats, chemin.replace(".pdf", ".txt"))

    def _generer_pdf(self, resultats, chemin):
        doc = SimpleDocTemplate(chemin, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        contenu = []

        # Style personnalise
        style_titre = ParagraphStyle(
            "Titre", parent=styles["Title"],
            fontSize=20, textColor=colors.HexColor("#1a1a2e"),
            spaceAfter=6, alignment=TA_CENTER
        )
        style_h2 = ParagraphStyle(
            "H2", parent=styles["Heading2"],
            fontSize=13, textColor=colors.HexColor("#16213e"),
            spaceBefore=12, spaceAfter=4
        )
        style_normal = ParagraphStyle(
            "Normal2", parent=styles["Normal"],
            fontSize=10, spaceAfter=3
        )
        style_danger = ParagraphStyle(
            "Danger", parent=styles["Normal"],
            fontSize=10, textColor=colors.HexColor("#c0392b"),
            spaceAfter=3
        )
        style_ok = ParagraphStyle(
            "OK", parent=styles["Normal"],
            fontSize=10, textColor=colors.HexColor("#27ae60"),
            spaceAfter=3
        )

        # En-tete
        contenu.append(Paragraph("RAPPORT D'AUDIT DE SECURITE", style_titre))
        contenu.append(Paragraph("Scanner de Securite - Usage ethique uniquement", styles["Normal"]))
        contenu.append(Spacer(1, 0.5*cm))
        contenu.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e")))
        contenu.append(Spacer(1, 0.3*cm))

        # Informations generales
        contenu.append(Paragraph("INFORMATIONS GENERALES", style_h2))
        donnees_info = [
            ["Cible analysee", resultats["cible"]],
            ["Date du scan", resultats["date"]],
            ["Modules utilises", str(len(resultats.get("modules", {})))],
            ["Total failles detectees", str(len(resultats.get("failles", [])))],
        ]
        tableau_info = Table(donnees_info, colWidths=[5*cm, 12*cm])
        tableau_info.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf1fb")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("ROWBACKGROUNDS", (1, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        contenu.append(tableau_info)
        contenu.append(Spacer(1, 0.4*cm))

        # Score global
        score = resultats.get("score_global", 0)
        couleur_score = "#27ae60" if score >= 80 else "#f39c12" if score >= 60 else "#e74c3c"
        style_score = ParagraphStyle(
            "Score", parent=styles["Normal"],
            fontSize=18, textColor=colors.HexColor(couleur_score),
            alignment=TA_CENTER, spaceBefore=6, spaceAfter=6
        )
        contenu.append(Paragraph(f"SCORE GLOBAL DE SECURITE : {score}/100", style_score))

        if score >= 80:
            appreciation = "BONNE SECURITE"
        elif score >= 60:
            appreciation = "SECURITE MOYENNE"
        elif score >= 40:
            appreciation = "SECURITE FAIBLE"
        else:
            appreciation = "SECURITE CRITIQUE"
        contenu.append(Paragraph(f"Appreciation : {appreciation}", styles["Normal"]))
        contenu.append(Spacer(1, 0.4*cm))
        contenu.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))

        # Failles detectees
        contenu.append(Paragraph("FAILLES DETECTEES", style_h2))
        failles = resultats.get("failles", [])
        if failles:
            for faille in failles:
                contenu.append(Paragraph(f"⚠  {faille}", style_danger))
        else:
            contenu.append(Paragraph("✓ Aucune faille critique detectee", style_ok))
        contenu.append(Spacer(1, 0.4*cm))

        # Recommandations
        contenu.append(Paragraph("RECOMMANDATIONS", style_h2))
        recommandations = resultats.get("recommandations", [])
        if recommandations:
            for i, rec in enumerate(recommandations, 1):
                contenu.append(Paragraph(f"{i}. {rec}", style_normal))
        else:
            contenu.append(Paragraph("Aucune recommandation supplementaire.", style_normal))
        contenu.append(Spacer(1, 0.4*cm))

        # Details par module
        contenu.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
        contenu.append(Paragraph("DETAILS PAR MODULE", style_h2))

        modules = resultats.get("modules", {})
        noms_modules = {
            "reseau": "Module Reseau",
            "ports": "Module Ports",
            "web": "Module Web",
            "mots_de_passe": "Module Mots de Passe"
        }

        for cle, nom in noms_modules.items():
            if cle in modules:
                mod = modules[cle]
                contenu.append(Paragraph(
                    f"{nom} - Score : {mod.get('score', 'N/A')}/100",
                    style_h2
                ))
                if cle == "ports" and mod.get("ports_ouverts"):
                    donnees_ports = [["Port", "Service", "Etat"]]
                    for p in mod["ports_ouverts"]:
                        donnees_ports.append([
                            str(p["numero"]),
                            p["service"],
                            p["etat"]
                        ])
                    t = Table(donnees_ports, colWidths=[3*cm, 7*cm, 4*cm])
                    t.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
                        ("FONTSIZE", (0, 0), (-1, -1), 9),
                        ("PADDING", (0, 0), (-1, -1), 5),
                    ]))
                    contenu.append(t)
                contenu.append(Spacer(1, 0.3*cm))

        # Pied de page
        contenu.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
        contenu.append(Spacer(1, 0.2*cm))
        contenu.append(Paragraph(
            "Ce rapport a ete genere automatiquement par le Scanner de Securite. "
            "Utilisez ces informations de maniere ethique et legale uniquement.",
            ParagraphStyle("Footer", parent=styles["Normal"],
                          fontSize=8, textColor=colors.HexColor("#888888"), alignment=TA_CENTER)
        ))

        doc.build(contenu)
        return chemin

    def _generer_txt(self, resultats, chemin):
        """Version texte si reportlab n'est pas installe"""
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("RAPPORT D'AUDIT DE SECURITE\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Cible : {resultats['cible']}\n")
            f.write(f"Date  : {resultats['date']}\n")
            f.write(f"Score : {resultats.get('score_global', 0)}/100\n\n")
            f.write("FAILLES DETECTEES :\n")
            for faille in resultats.get("failles", []):
                f.write(f"  - {faille}\n")
            f.write("\nRECOMMANDATIONS :\n")
            for rec in resultats.get("recommandations", []):
                f.write(f"  - {rec}\n")
        return chemin
