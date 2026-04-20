# ============================================================
# MODULE MOTS DE PASSE - Verifie les services d'authentification
# ============================================================

import socket

# Services qui utilisent une authentification
SERVICES_AUTH = {
    22: "SSH",
    21: "FTP",
    23: "Telnet",
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    3306: "MySQL",
    5432: "PostgreSQL",
    3389: "RDP",
    5900: "VNC",
    6379: "Redis",
    27017: "MongoDB"
}

# Bannieres qui indiquent des configurations par defaut dangereuses
BANNIERES_DANGEREUSES = [
    "default",
    "admin",
    "test",
    "demo",
    "anonymous"
]

class ModuleMotsDePasse:
    def analyser(self, cible):
        resultats = {
            "services_auth": 0,
            "services_detectes": [],
            "services_sans_auth": [],
            "score": 100,
            "failles": [],
            "recommandations": []
        }

        # Resoudre l'IP
        try:
            ip = socket.gethostbyname(cible)
        except Exception:
            resultats["failles"].append("Impossible de resoudre l'adresse")
            resultats["score"] = 0
            return resultats

        # Verifier quels services d'auth sont actifs
        for port, service in SERVICES_AUTH.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                resultat = sock.connect_ex((ip, port))

                if resultat == 0:
                    resultats["services_auth"] += 1
                    service_info = {"port": port, "service": service, "banniere": ""}

                    # Tenter de recuperer la banniere
                    try:
                        banniere = sock.recv(1024).decode("utf-8", errors="ignore").strip()
                        service_info["banniere"] = banniere[:100]

                        # Verifier si banniere contient des infos dangereuses
                        for mot in BANNIERES_DANGEREUSES:
                            if mot.lower() in banniere.lower():
                                resultats["failles"].append(
                                    f"Port {port} ({service}) : banniere revelatrice d'une config par defaut"
                                )
                                resultats["score"] -= 15
                    except Exception:
                        pass

                    resultats["services_detectes"].append(service_info)

                    # Verifications specifiques par service
                    if port == 6379:  # Redis
                        self._verifier_redis(ip, resultats)
                    elif port == 27017:  # MongoDB
                        self._verifier_mongodb(ip, resultats)
                    elif port == 23:  # Telnet
                        resultats["failles"].append(
                            "Telnet actif : protocole non chiffre, mots de passe visibles"
                        )
                        resultats["recommandations"].append(
                            "Remplacer Telnet par SSH immediatement"
                        )
                        resultats["score"] -= 25

                sock.close()
            except Exception:
                pass

        # Recommandations generales
        if resultats["services_auth"] > 0:
            resultats["recommandations"].append(
                "Utiliser des mots de passe forts (min. 12 caracteres, majuscules, chiffres, symboles)"
            )
            resultats["recommandations"].append(
                "Activer l'authentification a deux facteurs (2FA) sur tous les services"
            )
            resultats["recommandations"].append(
                "Mettre en place une limite de tentatives de connexion (fail2ban)"
            )

        if resultats["services_auth"] > 5:
            resultats["failles"].append(
                f"{resultats['services_auth']} services avec authentification exposes - surface d'attaque importante"
            )
            resultats["score"] -= 10

        resultats["score"] = max(0, resultats["score"])
        return resultats

    def _verifier_redis(self, ip, resultats):
        """Verifier si Redis est accessible sans authentification"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, 6379))
            sock.send(b"PING\r\n")
            reponse = sock.recv(100).decode("utf-8", errors="ignore")
            sock.close()

            if "+PONG" in reponse:
                resultats["failles"].append(
                    "Redis accessible SANS authentification - base de donnees exposee !"
                )
                resultats["recommandations"].append(
                    "Configurer un mot de passe Redis dans redis.conf : requirepass VotreMotDePasse"
                )
                resultats["score"] -= 30
        except Exception:
            pass

    def _verifier_mongodb(self, ip, resultats):
        """Verifier si MongoDB est accessible sans authentification"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            resultat = sock.connect_ex((ip, 27017))
            sock.close()

            if resultat == 0:
                resultats["failles"].append(
                    "MongoDB potentiellement accessible sans authentification"
                )
                resultats["recommandations"].append(
                    "Activer l'authentification MongoDB et limiter l'acces par IP"
                )
                resultats["score"] -= 20
        except Exception:
            pass
