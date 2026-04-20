# ============================================================
# MODULE WEB - Analyse la securite d'un site web
# ============================================================

import socket
try:
    import requests
    REQUESTS_DISPONIBLE = True
except ImportError:
    REQUESTS_DISPONIBLE = False

# En-tetes de securite HTTP importants
ENTETES_SECURITE = {
    "Strict-Transport-Security": "Protection contre les attaques de downgrade HTTPS",
    "X-Content-Type-Options": "Protection contre le MIME sniffing",
    "X-Frame-Options": "Protection contre le clickjacking",
    "X-XSS-Protection": "Protection contre les attaques XSS",
    "Content-Security-Policy": "Controle les ressources chargees par le navigateur",
    "Referrer-Policy": "Controle les informations envoyees dans le referrer"
}

class ModuleWeb:
    def analyser(self, cible):
        resultats = {
            "https": False,
            "http_accessible": False,
            "entetes_ok": 0,
            "entetes_total": len(ENTETES_SECURITE),
            "entetes_manquants": [],
            "entetes_presents": [],
            "redirection_https": False,
            "score": 100,
            "failles": [],
            "recommandations": []
        }

        if not REQUESTS_DISPONIBLE:
            resultats["failles"].append("Module 'requests' non installe - scan web limite")
            resultats["score"] = 50
            return resultats

        # Construire les URLs
        if cible.startswith("http"):
            url_base = cible
        else:
            url_base = cible

        url_https = f"https://{url_base}"
        url_http = f"http://{url_base}"

        # Tester HTTPS
        try:
            reponse_https = requests.get(
                url_https,
                timeout=5,
                allow_redirects=True,
                verify=False
            )
            resultats["https"] = True
            headers = reponse_https.headers

            # Verifier les en-tetes de securite
            for entete, description in ENTETES_SECURITE.items():
                if entete in headers:
                    resultats["entetes_ok"] += 1
                    resultats["entetes_presents"].append(entete)
                else:
                    resultats["entetes_manquants"].append(entete)
                    resultats["failles"].append(
                        f"En-tete manquant : {entete} - {description}"
                    )
                    resultats["score"] -= 8

        except requests.exceptions.SSLError:
            resultats["failles"].append("Certificat SSL invalide ou expire")
            resultats["score"] -= 25
            resultats["recommandations"].append(
                "Renouveler le certificat SSL - utiliser Let's Encrypt (gratuit)"
            )
        except requests.exceptions.ConnectionError:
            resultats["https"] = False

        # Tester HTTP
        try:
            reponse_http = requests.get(url_http, timeout=5, allow_redirects=False)
            resultats["http_accessible"] = True

            # Verifier si HTTP redirige vers HTTPS
            if reponse_http.status_code in [301, 302, 307, 308]:
                location = reponse_http.headers.get("Location", "")
                if "https" in location.lower():
                    resultats["redirection_https"] = True
                else:
                    resultats["failles"].append(
                        "HTTP redirige mais pas vers HTTPS"
                    )
                    resultats["score"] -= 10
            else:
                resultats["failles"].append(
                    "Site accessible en HTTP sans redirection vers HTTPS"
                )
                resultats["score"] -= 20
                resultats["recommandations"].append(
                    "Forcer la redirection HTTP vers HTTPS sur le serveur web"
                )

        except Exception:
            pass

        # Si ni HTTP ni HTTPS ne fonctionne
        if not resultats["https"] and not resultats["http_accessible"]:
            resultats["failles"].append("Aucun serveur web detecte sur cette cible")
            resultats["score"] = 50

        # Recommandations si HTTPS absent
        if not resultats["https"]:
            resultats["failles"].append("HTTPS non configure - donnees transmises en clair")
            resultats["recommandations"].append(
                "Installer un certificat SSL/TLS - Let's Encrypt est gratuit"
            )
            resultats["score"] -= 30

        # Recommandations pour les en-tetes manquants
        if resultats["entetes_manquants"]:
            resultats["recommandations"].append(
                f"Ajouter les en-tetes de securite manquants dans la configuration du serveur web (nginx/apache)"
            )

        resultats["score"] = max(0, resultats["score"])
        return resultats
