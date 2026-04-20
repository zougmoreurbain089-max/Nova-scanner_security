============================================================
   SCANNER DE SECURITE v1.0
   Outil d'audit de securite informatique
============================================================

⚠️  AVERTISSEMENT LEGAL ⚠️
Utilisez cet outil UNIQUEMENT sur des systemes que vous
possedez ou pour lesquels vous avez une autorisation ecrite.
Toute utilisation non autorisee est illegale.

============================================================
 INSTALLATION - KALI LINUX
============================================================

1. Ouvrir un terminal dans le dossier scanner_securite/

2. Installer les dependances :
   pip install python-nmap requests reportlab colorama

3. Lancer l'application :
   python3 main.py

============================================================
 INSTALLATION - WINDOWS
============================================================

1. Installer Python 3 depuis : https://www.python.org/downloads/
   ⚠️  Cocher "Add Python to PATH" pendant l'installation !

2. Installer Nmap depuis : https://nmap.org/download.html

3. Ouvrir l'invite de commandes (cmd) dans le dossier

4. Installer les dependances :
   pip install python-nmap requests reportlab colorama

5. Lancer l'application :
   python main.py

============================================================
 STRUCTURE DU PROJET
============================================================

scanner_securite/
│
├── main.py              ← LANCER L'APPLICATION ICI
├── interface.py         ← Interface graphique (Tkinter)
├── moteur.py            ← Cerveau du scanner
├── README.txt           ← Ce fichier
│
├── modules/
│   ├── reseau.py        ← Analyse reseau et detection OS
│   ├── ports.py         ← Scan des ports TCP
│   ├── web.py           ← Analyse securite web
│   └── mots_de_passe.py ← Verification authentification
│
└── rapports/
    └── generateur.py    ← Generation rapports PDF

============================================================
 FONCTIONNALITES
============================================================

✅ Scan reseau (ping, detection OS)
✅ Scan des 21 ports les plus importants
✅ Analyse securite des sites web (HTTPS, en-tetes)
✅ Detection des services d'authentification
✅ Score global de securite /100
✅ Generation de rapport PDF
✅ Interface graphique moderne
✅ Compatible Kali Linux et Windows

============================================================
 UTILISATION
============================================================

1. Entrer l'IP ou le domaine cible
   Exemples : 192.168.1.1 | 10.0.0.1 | exemple.com

2. Cocher les modules a activer

3. Cliquer sur "LANCER LE SCAN"

4. Apres le scan, cliquer sur "GENERER RAPPORT" pour PDF

============================================================
 SUPPORT
============================================================

En cas de probleme :
- Verifier que Python 3 est bien installe
- Verifier la connexion reseau
- Lancer en tant qu'administrateur si necessaire

============================================================
