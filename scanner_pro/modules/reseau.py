# ============================================================
# MODULE RESEAU - Analyse le reseau et detecte l'OS
# ============================================================

import socket
import subprocess
import platform

class ModuleReseau:
    def analyser(self, cible):
        resultats = {
            "actif": False,
            "os": "Inconnu",
            "adresse_ip": "",
            "nom_hote": "",
            "score": 100,
            "failles": [],
            "recommandations": []
        }

        # Resoudre le nom de domaine en IP
        try:
            ip = socket.gethostbyname(cible)
            resultats["adresse_ip"] = ip
            resultats["nom_hote"] = cible
        except socket.gaierror:
            resultats["failles"].append(f"Impossible de resoudre l'adresse : {cible}")
            resultats["score"] = 0
            return resultats

        # Verifier si l'hote est actif (ping)
        try:
            systeme = platform.system().lower()
            if systeme == "windows":
                commande = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                commande = ["ping", "-c", "1", "-W", "1", ip]

            resultat = subprocess.run(
                commande,
                capture_output=True,
                text=True,
                timeout=5
            )
            resultats["actif"] = resultat.returncode == 0
        except Exception:
            resultats["actif"] = False

        if not resultats["actif"]:
            resultats["failles"].append("Hote injoignable ou filtre par un pare-feu")
            resultats["recommandations"].append("Verifier que la cible est bien accessible sur le reseau")
            resultats["score"] = 50
            return resultats

        # Detection basique de l'OS via TTL
        try:
            if systeme == "windows":
                commande_ttl = ["ping", "-n", "1", ip]
            else:
                commande_ttl = ["ping", "-c", "1", ip]

            sortie = subprocess.run(commande_ttl, capture_output=True, text=True, timeout=5)
            sortie_texte = sortie.stdout.lower()

            if "ttl=64" in sortie_texte or "ttl=63" in sortie_texte:
                resultats["os"] = "Linux / Unix / Android"
            elif "ttl=128" in sortie_texte or "ttl=127" in sortie_texte:
                resultats["os"] = "Windows"
            elif "ttl=254" in sortie_texte or "ttl=255" in sortie_texte:
                resultats["os"] = "Cisco / Routeur reseau"
            else:
                resultats["os"] = "OS inconnu"
        except Exception:
            resultats["os"] = "Detection OS echouee"

        # Verifications de securite reseau
        # Verifier si le ping ICMP est autorise (peut etre une faille)
        if resultats["actif"]:
            resultats["failles"].append("Le ping ICMP est autorise - peut reveler la presence de l'hote")
            resultats["recommandations"].append("Bloquer les requetes ICMP entrantes sur le pare-feu en production")
            resultats["score"] -= 10

        return resultats
