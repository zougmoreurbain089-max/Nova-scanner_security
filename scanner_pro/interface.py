# ============================================================
# INTERFACE GRAPHIQUE ULTRA DESIGN - Scanner de Securite Pro
# Auteur : Zougmore Urbain
# Copyright (c) 2026 - Tous droits reserves
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import datetime
from moteur import MoteurScan
from licence import verifier_statut_licence, activer_licence

COULEURS = {
    "fond_principal":   "#050A18",
    "fond_secondaire":  "#0A1628",
    "fond_carte":       "#0D1F3C",
    "accent_cyan":      "#00F5FF",
    "accent_vert":      "#00FF88",
    "accent_rouge":     "#FF2D55",
    "accent_orange":    "#FF8C00",
    "accent_violet":    "#7B2FFF",
    "texte_blanc":      "#FFFFFF",
    "texte_gris":       "#8899AA",
    "texte_dim":        "#445566",
    "bordure":          "#1A3050",
    "scan_bg":          "#020810",
}


class FenetreActivation(tk.Toplevel):
    def __init__(self, parent, callback_succes):
        super().__init__(parent)
        self.callback_succes = callback_succes
        self.title("Activation Licence")
        self.geometry("520x430")
        self.configure(bg=COULEURS["fond_principal"])
        self.resizable(False, False)
        self.grab_set()
        self._centrer()
        self._construire()

    def _centrer(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 260
        y = (self.winfo_screenheight() // 2) - 215
        self.geometry(f"+{x}+{y}")

    def _construire(self):
        cadre_haut = tk.Frame(self, bg="#0A1628", pady=18)
        cadre_haut.pack(fill="x")
        tk.Label(cadre_haut, text="🔐", font=("Segoe UI", 32),
                 bg="#0A1628", fg=COULEURS["accent_cyan"]).pack()
        tk.Label(cadre_haut, text="ACTIVATION DE LICENCE",
                 font=("Courier New", 14, "bold"),
                 bg="#0A1628", fg=COULEURS["accent_cyan"]).pack()
        tk.Label(cadre_haut, text="Scanner de Securite Pro — by Zougmore Urbain",
                 font=("Courier New", 9), bg="#0A1628", fg=COULEURS["texte_gris"]).pack()

        corps = tk.Frame(self, bg=COULEURS["fond_principal"], padx=35, pady=20)
        corps.pack(fill="both", expand=True)

        tk.Label(corps, text="CODE DE LICENCE (format binaire) :",
                 font=("Courier New", 10, "bold"),
                 bg=COULEURS["fond_principal"], fg=COULEURS["texte_blanc"]).pack(anchor="w")
        tk.Label(corps, text="Ex: 0000000001  |  0000000010  |  0000001111",
                 font=("Courier New", 9),
                 bg=COULEURS["fond_principal"], fg=COULEURS["texte_gris"]).pack(anchor="w", pady=(2, 8))

        self.champ_code = tk.Entry(
            corps, font=("Courier New", 18, "bold"), width=18,
            bg=COULEURS["fond_carte"], fg=COULEURS["accent_cyan"],
            insertbackground=COULEURS["accent_cyan"],
            relief="flat", bd=8, justify="center"
        )
        self.champ_code.pack(pady=5, ipady=8, fill="x")
        self.champ_code.focus()
        self.champ_code.bind("<Return>", lambda e: self._activer())

        cadre_pay = tk.Frame(corps, bg="#0D1F3C", pady=14, padx=18)
        cadre_pay.pack(fill="x", pady=12)
        tk.Label(cadre_pay, text="💳  OBTENIR UNE LICENCE",
                 font=("Courier New", 10, "bold"),
                 bg="#0D1F3C", fg=COULEURS["accent_orange"]).pack()
        tk.Label(cadre_pay, text="3 000 FCFA / mois",
                 font=("Courier New", 14, "bold"),
                 bg="#0D1F3C", fg=COULEURS["accent_vert"]).pack(pady=4)
        tk.Label(cadre_pay, text="📱 Orange Money : +226 57 37 30 16",
                 font=("Courier New", 11), bg="#0D1F3C", fg=COULEURS["texte_blanc"]).pack()
        tk.Label(cadre_pay, text="Zougmore Urbain",
                 font=("Courier New", 9), bg="#0D1F3C", fg=COULEURS["texte_gris"]).pack()

        tk.Button(corps, text="✅  ACTIVER MA LICENCE",
                  font=("Courier New", 11, "bold"),
                  bg=COULEURS["accent_cyan"], fg=COULEURS["fond_principal"],
                  relief="flat", padx=20, pady=10, cursor="hand2",
                  command=self._activer).pack(fill="x")

    def _activer(self):
        code = self.champ_code.get().strip()
        if not code:
            messagebox.showerror("Erreur", "Entrez un code de licence !", parent=self)
            return
        succes, message = activer_licence(code)
        if succes:
            messagebox.showinfo("✅ Activee !", message, parent=self)
            self.destroy()
            self.callback_succes()
        else:
            messagebox.showerror("❌ Code invalide", message, parent=self)


class FenetreExpiration(tk.Toplevel):
    def __init__(self, parent, callback_activation):
        super().__init__(parent)
        self.callback_activation = callback_activation
        self.title("Licence Expiree")
        self.geometry("480x360")
        self.configure(bg=COULEURS["fond_principal"])
        self.resizable(False, False)
        self.grab_set()
        self._centrer()
        self._construire()
        self.protocol("WM_DELETE_WINDOW", self._bloquer)

    def _centrer(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 240
        y = (self.winfo_screenheight() // 2) - 180
        self.geometry(f"+{x}+{y}")

    def _bloquer(self):
        messagebox.showwarning("Licence requise",
            "Activez votre licence pour utiliser ce logiciel.\n\n"
            "Orange Money : +226 57 37 30 16\nZougmore Urbain", parent=self)

    def _construire(self):
        cadre_haut = tk.Frame(self, bg="#1A0505", pady=20)
        cadre_haut.pack(fill="x")
        tk.Label(cadre_haut, text="⛔", font=("Segoe UI", 36),
                 bg="#1A0505", fg=COULEURS["accent_rouge"]).pack()
        tk.Label(cadre_haut, text="LICENCE EXPIREE",
                 font=("Courier New", 16, "bold"),
                 bg="#1A0505", fg=COULEURS["accent_rouge"]).pack()

        corps = tk.Frame(self, bg=COULEURS["fond_principal"], padx=30, pady=20)
        corps.pack(fill="both", expand=True)

        tk.Label(corps,
                 text="Votre licence de 30 jours a expire.\nRenouvelez pour continuer.",
                 font=("Courier New", 11), bg=COULEURS["fond_principal"],
                 fg=COULEURS["texte_blanc"], justify="center").pack(pady=8)

        cadre_pay = tk.Frame(corps, bg="#0D1F3C", pady=14, padx=20)
        cadre_pay.pack(fill="x", pady=8)
        tk.Label(cadre_pay, text="3 000 FCFA / mois",
                 font=("Courier New", 14, "bold"),
                 bg="#0D1F3C", fg=COULEURS["accent_vert"]).pack()
        tk.Label(cadre_pay, text="📱 Orange Money : +226 57 37 30 16\n👤 Zougmore Urbain",
                 font=("Courier New", 11), bg="#0D1F3C",
                 fg=COULEURS["texte_blanc"], justify="center").pack(pady=5)

        tk.Button(corps, text="🔑  ENTRER MON NOUVEAU CODE",
                  font=("Courier New", 11, "bold"),
                  bg=COULEURS["accent_vert"], fg=COULEURS["fond_principal"],
                  relief="flat", padx=20, pady=10, cursor="hand2",
                  command=lambda: (self.destroy(), self.callback_activation())
                  ).pack(fill="x")


class InterfacePrincipale:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Scanner de Securite Pro — Zougmore Urbain")
        self.fenetre.geometry("1000x700")
        self.fenetre.configure(bg=COULEURS["fond_principal"])
        self.fenetre.resizable(True, True)
        self.moteur = MoteurScan()
        self.scan_en_cours = False
        self.resultats_actuels = None
        self._construire_interface()
        self._verifier_licence_demarrage()

    def _verifier_licence_demarrage(self):
        statut, jours, _ = verifier_statut_licence()
        if statut == "aucune":
            self.fenetre.after(300, self._premiere_activation)
        elif statut == "expire":
            self.fenetre.after(300, lambda: FenetreExpiration(self.fenetre, self._ouvrir_activation))
        elif jours <= 5:
            self.fenetre.after(500, lambda: messagebox.showwarning(
                "⚠️ Expiration proche",
                f"Votre licence expire dans {jours} jour(s) !\n\n"
                f"Renouvelez via Orange Money :\n3 000 FCFA au +226 57 37 30 16\nZougmore Urbain",
                parent=self.fenetre))

    def _premiere_activation(self):
        messagebox.showinfo("Bienvenue !",
            "Bienvenue dans Scanner de Securite Pro !\n\n"
            "Entrez votre code de licence pour commencer.\n\n"
            "📱 Orange Money : +226 57 37 30 16\n"
            "👤 Zougmore Urbain\n"
            "💰 3 000 FCFA / mois", parent=self.fenetre)
        self._ouvrir_activation()

    def _ouvrir_activation(self):
        FenetreActivation(self.fenetre, self._on_activation_reussie)

    def _on_activation_reussie(self):
        statut, jours, _ = verifier_statut_licence()
        self.label_licence.configure(
            text=f"✅ Licence active — {jours} jours restants",
            fg=COULEURS["accent_vert"])

    def _construire_interface(self):
        # ── BARRE DU HAUT ──
        cadre_top = tk.Frame(self.fenetre, bg="#060E1F")
        cadre_top.pack(fill="x")

        barre_couleur = tk.Canvas(cadre_top, height=3, bg="#060E1F", highlightthickness=0)
        barre_couleur.pack(fill="x")

        def dessiner_barre(e):
            barre_couleur.delete("all")
            w = e.width
            barre_couleur.create_rectangle(0, 0, w//3, 3, fill=COULEURS["accent_cyan"], outline="")
            barre_couleur.create_rectangle(w//3, 0, 2*w//3, 3, fill=COULEURS["accent_violet"], outline="")
            barre_couleur.create_rectangle(2*w//3, 0, w, 3, fill=COULEURS["accent_vert"], outline="")

        barre_couleur.bind("<Configure>", dessiner_barre)

        cadre_titre = tk.Frame(cadre_top, bg="#060E1F", pady=12, padx=20)
        cadre_titre.pack(fill="x")

        cadre_gauche_titre = tk.Frame(cadre_titre, bg="#060E1F")
        cadre_gauche_titre.pack(side="left")
        tk.Label(cadre_gauche_titre, text="⬡", font=("Segoe UI", 26),
                 bg="#060E1F", fg=COULEURS["accent_cyan"]).pack(side="left", padx=(0, 10))
        cadre_txt = tk.Frame(cadre_gauche_titre, bg="#060E1F")
        cadre_txt.pack(side="left")
        tk.Label(cadre_txt, text="SCANNER DE SECURITE PRO",
                 font=("Courier New", 17, "bold"),
                 bg="#060E1F", fg=COULEURS["accent_cyan"]).pack(anchor="w")
        tk.Label(cadre_txt, text="by Zougmore Urbain  •  Outil d'audit de securite informatique  •  v1.0",
                 font=("Courier New", 8), bg="#060E1F", fg=COULEURS["texte_gris"]).pack(anchor="w")

        cadre_droite_titre = tk.Frame(cadre_titre, bg="#060E1F")
        cadre_droite_titre.pack(side="right")

        statut, jours, _ = verifier_statut_licence()
        if statut == "actif":
            txt_lic, col_lic = f"✅ Licence active — {jours} jours", COULEURS["accent_vert"]
        elif statut == "expire":
            txt_lic, col_lic = "⛔ Licence expiree", COULEURS["accent_rouge"]
        else:
            txt_lic, col_lic = "⚠️ Aucune licence", COULEURS["accent_orange"]

        self.label_licence = tk.Label(cadre_droite_titre, text=txt_lic,
                                      font=("Courier New", 9, "bold"),
                                      bg="#060E1F", fg=col_lic)
        self.label_licence.pack(anchor="e")

        tk.Button(cadre_droite_titre, text="🔑 Renouveler",
                  font=("Courier New", 8), bg=COULEURS["fond_carte"],
                  fg=COULEURS["accent_orange"], relief="flat", padx=8, pady=3,
                  cursor="hand2", command=self._ouvrir_activation).pack(anchor="e", pady=2)

        # ── ZONE CENTRALE ──
        central = tk.Frame(self.fenetre, bg=COULEURS["fond_principal"])
        central.pack(fill="both", expand=True, padx=12, pady=10)

        # Panneau gauche
        pg = tk.Frame(central, bg=COULEURS["fond_carte"], width=275, padx=14, pady=14)
        pg.pack(side="left", fill="y", padx=(0, 8))
        pg.pack_propagate(False)

        tk.Label(pg, text="◈  CONFIGURATION", font=("Courier New", 10, "bold"),
                 bg=COULEURS["fond_carte"], fg=COULEURS["accent_cyan"]).pack(anchor="w")
        tk.Frame(pg, bg=COULEURS["bordure"], height=1).pack(fill="x", pady=6)

        tk.Label(pg, text="CIBLE (IP / DOMAINE)", font=("Courier New", 8, "bold"),
                 bg=COULEURS["fond_carte"], fg=COULEURS["texte_gris"]).pack(anchor="w", pady=(6, 2))

        self.champ_cible = tk.Entry(pg, font=("Courier New", 12),
                                    bg=COULEURS["fond_secondaire"],
                                    fg=COULEURS["accent_cyan"],
                                    insertbackground=COULEURS["accent_cyan"],
                                    relief="flat", bd=6)
        self.champ_cible.insert(0, "192.168.1.1")
        self.champ_cible.pack(fill="x", pady=3, ipady=6)

        tk.Frame(pg, bg=COULEURS["bordure"], height=1).pack(fill="x", pady=8)
        tk.Label(pg, text="MODULES D'ANALYSE", font=("Courier New", 8, "bold"),
                 bg=COULEURS["fond_carte"], fg=COULEURS["texte_gris"]).pack(anchor="w", pady=(0, 6))

        self.opt_reseau = tk.BooleanVar(value=True)
        self.opt_ports  = tk.BooleanVar(value=True)
        self.opt_web    = tk.BooleanVar(value=True)
        self.opt_mdp    = tk.BooleanVar(value=True)

        for txt, var, col in [
            ("🌐  Reseau & OS",    self.opt_reseau, COULEURS["accent_cyan"]),
            ("🔌  Scan de Ports",  self.opt_ports,  COULEURS["accent_violet"]),
            ("🌍  Securite Web",   self.opt_web,    COULEURS["accent_vert"]),
            ("🔑  Mots de Passe",  self.opt_mdp,    COULEURS["accent_orange"]),
        ]:
            f = tk.Frame(pg, bg=COULEURS["fond_secondaire"], pady=4, padx=8)
            f.pack(fill="x", pady=2)
            tk.Checkbutton(f, text=txt, variable=var, font=("Courier New", 10),
                           fg=col, bg=COULEURS["fond_secondaire"],
                           selectcolor=COULEURS["fond_carte"],
                           activebackground=COULEURS["fond_secondaire"],
                           activeforeground=col).pack(anchor="w")

        tk.Frame(pg, bg=COULEURS["bordure"], height=1).pack(fill="x", pady=10)

        self.bouton_scan = tk.Button(pg, text="▶  LANCER LE SCAN",
                                     font=("Courier New", 11, "bold"),
                                     bg=COULEURS["accent_cyan"], fg=COULEURS["fond_principal"],
                                     relief="flat", pady=10, cursor="hand2",
                                     command=self.lancer_scan)
        self.bouton_scan.pack(fill="x", pady=2)

        self.bouton_rapport = tk.Button(pg, text="📄  RAPPORT PDF",
                                        font=("Courier New", 11, "bold"),
                                        bg=COULEURS["accent_vert"], fg=COULEURS["fond_principal"],
                                        relief="flat", pady=10, cursor="hand2",
                                        state="disabled", command=self.generer_rapport)
        self.bouton_rapport.pack(fill="x", pady=2)

        tk.Button(pg, text="🗑  EFFACER", font=("Courier New", 10),
                  bg=COULEURS["fond_secondaire"], fg=COULEURS["accent_rouge"],
                  relief="flat", pady=7, cursor="hand2",
                  command=self.effacer).pack(fill="x", pady=2)

        tk.Frame(pg, bg=COULEURS["bordure"], height=1).pack(fill="x", pady=10)
        tk.Label(pg, text="SCORE DE SECURITE", font=("Courier New", 8, "bold"),
                 bg=COULEURS["fond_carte"], fg=COULEURS["texte_gris"]).pack(anchor="w")

        self.label_score = tk.Label(pg, text="--/100", font=("Courier New", 28, "bold"),
                                    bg=COULEURS["fond_carte"], fg=COULEURS["texte_dim"])
        self.label_score.pack(pady=4)

        self.label_appr = tk.Label(pg, text="En attente...", font=("Courier New", 9),
                                   bg=COULEURS["fond_carte"], fg=COULEURS["texte_gris"],
                                   wraplength=240)
        self.label_appr.pack()

        tk.Label(pg, text="© 2026 Zougmore Urbain\nScanner de Securite Pro v1.0",
                 font=("Courier New", 7), bg=COULEURS["fond_carte"],
                 fg=COULEURS["texte_dim"], justify="center").pack(side="bottom", pady=5)

        # Panneau droit
        pd = tk.Frame(central, bg=COULEURS["fond_secondaire"])
        pd.pack(side="left", fill="both", expand=True)

        cadre_res_top = tk.Frame(pd, bg=COULEURS["fond_carte"], padx=15, pady=8)
        cadre_res_top.pack(fill="x")
        tk.Label(cadre_res_top, text="◈  RESULTATS EN TEMPS REEL",
                 font=("Courier New", 10, "bold"),
                 bg=COULEURS["fond_carte"], fg=COULEURS["accent_vert"]).pack(side="left")
        self.label_statut = tk.Label(cadre_res_top, text="● PRET",
                                     font=("Courier New", 9, "bold"),
                                     bg=COULEURS["fond_carte"], fg=COULEURS["accent_vert"])
        self.label_statut.pack(side="right")

        self.zone_resultats = scrolledtext.ScrolledText(
            pd, font=("Courier New", 10),
            bg=COULEURS["scan_bg"], fg=COULEURS["accent_vert"],
            insertbackground=COULEURS["accent_vert"],
            relief="flat", padx=15, pady=10, state="disabled")
        self.zone_resultats.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Cyber.Horizontal.TProgressbar",
                        troughcolor=COULEURS["fond_carte"],
                        background=COULEURS["accent_cyan"], thickness=4)
        self.barre_progression = ttk.Progressbar(pd, mode="indeterminate",
                                                  style="Cyber.Horizontal.TProgressbar")
        self.barre_progression.pack(fill="x")

        self._message_bienvenue()

    def _message_bienvenue(self):
        statut, jours, _ = verifier_statut_licence()
        msgs = [
            "╔══════════════════════════════════════════════════════╗",
            "║     SCANNER DE SECURITE PRO  v1.0                   ║",
            "║     by Zougmore Urbain  —  © 2026                   ║",
            "╚══════════════════════════════════════════════════════╝",
            "",
        ]
        if statut == "actif":
            msgs.append(f"  ✅ Licence active — {jours} jours restants")
        msgs += ["  ⚠️  Usage autorise uniquement sur vos propres systemes", "",
                 "  Entrez une cible et cliquez LANCER LE SCAN", "─" * 56]
        for m in msgs:
            self.afficher_message(m)

    def afficher_message(self, message):
        self.zone_resultats.configure(state="normal")
        self.zone_resultats.insert("end", message + "\n")
        self.zone_resultats.see("end")
        self.zone_resultats.configure(state="disabled")

    def lancer_scan(self):
        statut, _, _ = verifier_statut_licence()
        if statut == "expire":
            FenetreExpiration(self.fenetre, self._ouvrir_activation)
            return
        if statut == "aucune":
            self._ouvrir_activation()
            return
        if self.scan_en_cours:
            messagebox.showwarning("Scan en cours", "Un scan est deja en cours !", parent=self.fenetre)
            return
        cible = self.champ_cible.get().strip()
        if not cible:
            messagebox.showerror("Erreur", "Veuillez entrer une cible !", parent=self.fenetre)
            return

        modules = {"reseau": self.opt_reseau.get(), "ports": self.opt_ports.get(),
                   "web": self.opt_web.get(), "mots_de_passe": self.opt_mdp.get()}

        self.scan_en_cours = True
        self.bouton_scan.configure(state="disabled", text="⏳  SCAN EN COURS...")
        self.bouton_rapport.configure(state="disabled")
        self.barre_progression.start(10)
        self.label_statut.configure(text="● SCAN EN COURS", fg=COULEURS["accent_orange"])
        self.label_score.configure(text="--/100", fg=COULEURS["texte_dim"])

        self.afficher_message(f"\n{'─'*56}")
        self.afficher_message(f"  SCAN — {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.afficher_message(f"  Cible : {cible}\n{'─'*56}\n")

        threading.Thread(target=self._executer_scan, args=(cible, modules), daemon=True).start()

    def _executer_scan(self, cible, modules):
        try:
            resultats = self.moteur.lancer_scan_complet(cible, modules, self.afficher_message)
            self.fenetre.after(0, self._scan_termine, resultats)
        except Exception as e:
            self.fenetre.after(0, self._scan_erreur, str(e))

    def _scan_termine(self, resultats):
        self.scan_en_cours = False
        self.barre_progression.stop()
        self.bouton_scan.configure(state="normal", text="▶  LANCER LE SCAN")
        self.bouton_rapport.configure(state="normal")
        self.label_statut.configure(text="● TERMINE", fg=COULEURS["accent_vert"])
        self.resultats_actuels = resultats
        score = resultats.get("score_global", 0)
        col = COULEURS["accent_vert"] if score >= 80 else COULEURS["accent_orange"] if score >= 60 else COULEURS["accent_rouge"]
        self.label_score.configure(text=f"{score}/100", fg=col)
        appr = "✅ Bonne securite" if score >= 80 else "⚠️ Securite moyenne" if score >= 60 else "🔴 Securite faible" if score >= 40 else "❌ Critique"
        self.label_appr.configure(text=appr)
        self.afficher_message("\n  ✅ Scan termine ! Cliquez RAPPORT PDF pour exporter.\n")

    def _scan_erreur(self, erreur):
        self.scan_en_cours = False
        self.barre_progression.stop()
        self.bouton_scan.configure(state="normal", text="▶  LANCER LE SCAN")
        self.label_statut.configure(text="● ERREUR", fg=COULEURS["accent_rouge"])
        self.afficher_message(f"\n  ❌ Erreur : {erreur}\n")

    def generer_rapport(self):
        if self.resultats_actuels:
            from rapports.generateur import GenerateurRapport
            gen = GenerateurRapport()
            chemin = gen.generer(self.resultats_actuels)
            messagebox.showinfo("✅ Rapport PDF", f"Rapport sauvegarde :\n{chemin}", parent=self.fenetre)
        else:
            messagebox.showwarning("Aucun resultat", "Lancez d'abord un scan !", parent=self.fenetre)

    def effacer(self):
        self.zone_resultats.configure(state="normal")
        self.zone_resultats.delete("1.0", "end")
        self.zone_resultats.configure(state="disabled")
        self._message_bienvenue()


def LancerApplication():
    fenetre = tk.Tk()
    InterfacePrincipale(fenetre)
    fenetre.mainloop()
