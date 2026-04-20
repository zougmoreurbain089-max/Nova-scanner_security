# ============================================================
# MODULE PORTS - Scan des ports ouverts
# ============================================================

import socket
import concurrent.futures

# Ports courants et leurs services associes
PORTS_COURANTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB"
}

# Ports consideres comme dangereux si ouverts
PORTS_DANGEREUX = {
    21: "FTP transmet les mots de passe en clair",
    23: "Telnet est non chiffre - utiliser SSH a la place",
    135: "RPC peut etre exploite par des malwares",
    139: "NetBIOS expose des informations systeme",
    445: "SMB - vulnerable a des attaques comme EternalBlue",
    1433: "SQL Server expose directement sur le reseau",
    3389: "RDP accessible directement - risque de brute force",
    5900: "VNC - souvent mal configure et sans chiffrement",
    6379: "Redis sans authentification par defaut",
    27017: "MongoDB sans authentification par defaut"
}

class ModulePorts:
    def __init__(self, timeout=1):
        self.timeout = timeout

    def _scanner_port(self, ip, port):
        """Tester si un port est ouvert"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            resultat = sock.connect_ex((ip, port))
            sock.close()
            if resultat == 0:
                return {
                    "numero": port,
                    "service": PORTS_COURANTS.get(port, "Inconnu"),
                    "etat": "OUVERT"
                }
        except Exception:
            pass
        return None

    def analyser(self, cible):
        resultats = {
            "ports_ouverts": [],
            "ports_fermes": 0,
            "score": 100,
            "failles": [],
            "recommandations": []
        }

        # Resoudre l'IP
        try:
            ip = socket.gethostbyname(cible)
        except Exception:
            resultats["failles"].append("Impossible de resoudre l'adresse pour le scan de ports")
            resultats["score"] = 0
            return resultats

        # Scanner tous les ports courants en parallele
        ports_a_scanner = list(PORTS_COURANTS.keys())

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = {
                executor.submit(self._scanner_port, ip, port): port
                for port in ports_a_scanner
            }
            for future in concurrent.futures.as_completed(futures):
                resultat = future.result()
                if resultat:
                    resultats["ports_ouverts"].append(resultat)
                else:
                    resultats["ports_fermes"] += 1

        # Trier par numero de port
        resultats["ports_ouverts"].sort(key=lambda x: x["numero"])

        # Analyser les risques
        for port_info in resultats["ports_ouverts"]:
            numero = port_info["numero"]
            if numero in PORTS_DANGEREUX:
                faille = f"Port {numero} ({port_info['service']}) ouvert : {PORTS_DANGEREUX[numero]}"
                resultats["failles"].append(faille)
                resultats["score"] -= 15

        # Recommandations generales
        nb_ports = len(resultats["ports_ouverts"])
        if nb_ports > 10:
            resultats["recommandations"].append(
                f"{nb_ports} ports ouverts detectes - Fermer les ports inutiles"
            )
            resultats["score"] -= 10

        if 23 in [p["numero"] for p in resultats["ports_ouverts"]]:
            resultats["recommandations"].append(
                "Telnet detecte - Migrer vers SSH immediatement"
            )

        if 21 in [p["numero"] for p in resultats["ports_ouverts"]]:
            resultats["recommandations"].append(
                "FTP detecte - Utiliser SFTP ou FTPS a la place"
            )

        if 3389 in [p["numero"] for p in resultats["ports_ouverts"]]:
            resultats["recommandations"].append(
                "RDP ouvert - Limiter l'acces par IP ou utiliser un VPN"
            )

        # Score minimum de 0
        resultats["score"] = max(0, resultats["score"])

        return resultats
