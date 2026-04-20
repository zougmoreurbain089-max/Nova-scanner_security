# ============================================================
# MOTEUR DE SCAN - Orchestre tous les modules
# ============================================================

import datetime
from modules.reseau import ModuleReseau
from modules.ports import ModulePorts
from modules.web import ModuleWeb
from modules.mots_de_passe import ModuleMotsDePasse

class MoteurScan:
    def __init__(self):
        self.module_reseau = ModuleReseau()
        self.module_ports = ModulePorts()
        self.module_web = ModuleWeb()
        self.module_mdp = ModuleMotsDePasse()

    def lancer_scan_complet(self, cible, modules, callback_affichage):
        """
        Lance tous les modules actives et retourne les resultats complets.
        cible : IP ou domaine a scanner
        modules : dict des modules a activer
        callback_affichage : fonction pour afficher les messages en temps reel
        """
        resultats = {
            "cible": cible,
            "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "modules": {},
            "score_global": 0,
            "failles": [],
            "recommandations": []
        }

        score_total = 0
        nb_modules = 0

        # ---- MODULE RESEAU ----
        if modules.get("reseau"):
            callback_affichage("🌐 [RESEAU] Analyse du reseau en cours...")
            res = self.module_reseau.analyser(cible)
            resultats["modules"]["reseau"] = res
            score_total += res.get("score", 0)
            nb_modules += 1
            resultats["failles"].extend(res.get("failles", []))
            resultats["recommandations"].extend(res.get("recommandations", []))

            callback_affichage(f"   → Hote actif : {'OUI' if res.get('actif') else 'NON'}")
            callback_affichage(f"   → OS detecte : {res.get('os', 'Inconnu')}")
            callback_affichage(f"   → Score securite reseau : {res.get('score', 0)}/100")
            for faille in res.get("failles", []):
                callback_affichage(f"   ⚠️  {faille}")

        # ---- MODULE PORTS ----
        if modules.get("ports"):
            callback_affichage("\n🔌 [PORTS] Scan des ports en cours...")
            res = self.module_ports.analyser(cible)
            resultats["modules"]["ports"] = res
            score_total += res.get("score", 0)
            nb_modules += 1
            resultats["failles"].extend(res.get("failles", []))
            resultats["recommandations"].extend(res.get("recommandations", []))

            ports_ouverts = res.get("ports_ouverts", [])
            callback_affichage(f"   → Ports ouverts trouves : {len(ports_ouverts)}")
            for port in ports_ouverts:
                callback_affichage(f"   → Port {port['numero']}/TCP - {port['service']} - {port['etat']}")
            callback_affichage(f"   → Score securite ports : {res.get('score', 0)}/100")
            for faille in res.get("failles", []):
                callback_affichage(f"   ⚠️  {faille}")

        # ---- MODULE WEB ----
        if modules.get("web"):
            callback_affichage("\n🌍 [WEB] Analyse du site web en cours...")
            res = self.module_web.analyser(cible)
            resultats["modules"]["web"] = res
            score_total += res.get("score", 0)
            nb_modules += 1
            resultats["failles"].extend(res.get("failles", []))
            resultats["recommandations"].extend(res.get("recommandations", []))

            callback_affichage(f"   → HTTPS actif : {'OUI' if res.get('https') else 'NON'}")
            callback_affichage(f"   → En-tetes securite : {res.get('entetes_ok', 0)}/{res.get('entetes_total', 0)}")
            callback_affichage(f"   → Score securite web : {res.get('score', 0)}/100")
            for faille in res.get("failles", []):
                callback_affichage(f"   ⚠️  {faille}")

        # ---- MODULE MOTS DE PASSE ----
        if modules.get("mots_de_passe"):
            callback_affichage("\n🔑 [MOTS DE PASSE] Verification des politiques...")
            res = self.module_mdp.analyser(cible)
            resultats["modules"]["mots_de_passe"] = res
            score_total += res.get("score", 0)
            nb_modules += 1
            resultats["failles"].extend(res.get("failles", []))
            resultats["recommandations"].extend(res.get("recommandations", []))

            callback_affichage(f"   → Services avec auth detectes : {res.get('services_auth', 0)}")
            callback_affichage(f"   → Score securite mots de passe : {res.get('score', 0)}/100")
            for faille in res.get("failles", []):
                callback_affichage(f"   ⚠️  {faille}")

        # ---- CALCUL SCORE GLOBAL ----
        if nb_modules > 0:
            resultats["score_global"] = round(score_total / nb_modules)

        callback_affichage(f"\n{'='*60}")
        callback_affichage(f"SCORE GLOBAL DE SECURITE : {resultats['score_global']}/100")
        callback_affichage(self._appreciation(resultats["score_global"]))
        callback_affichage(f"Total failles detectees : {len(resultats['failles'])}")
        callback_affichage(f"{'='*60}")

        return resultats

    def _appreciation(self, score):
        if score >= 80:
            return "✅ Appreciation : BONNE SECURITE"
        elif score >= 60:
            return "⚠️  Appreciation : SECURITE MOYENNE - Ameliorations recommandees"
        elif score >= 40:
            return "🔴 Appreciation : SECURITE FAIBLE - Actions urgentes requises"
        else:
            return "❌ Appreciation : SECURITE CRITIQUE - Systeme tres vulnerable"
