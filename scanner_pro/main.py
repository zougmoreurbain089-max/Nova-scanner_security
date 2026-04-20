# ============================================================
# SCANNER DE SECURITE - Fichier principal
# Auteur : Genere par Claude (Anthropic)
# Compatible : Kali Linux, Windows, Ubuntu, Mac
# ============================================================

import sys
import os

# Verifier que Python est bien en version 3
if sys.version_info[0] < 3:
    print("Erreur : Python 3 est requis !")
    sys.exit(1)

# Installer les dependances si necessaire
def installer_dependances():
    import subprocess
    packages = ["python-nmap", "requests", "reportlab", "colorama"]
    for package in packages:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

print("Demarrage du Scanner de Securite...")
print("Verification des dependances...")
installer_dependances()
print("Dependances OK !")

# Lancer l'interface graphique
from interface import LancerApplication

if __name__ == "__main__":
    LancerApplication()
