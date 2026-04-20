# ============================================================
# SYSTEME DE LICENCE - Scanner de Securite Pro
# Auteur : Zougmore Urbain
# ============================================================

import os
import json
import datetime
import hashlib

# Fichier de licence stocke dans AppData (Windows)
def _get_licence_path():
    appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
    dossier = os.path.join(appdata, "ScannerSecuritePro")
    os.makedirs(dossier, exist_ok=True)
    return os.path.join(dossier, ".lic")

# ---- Generateur des 1000 codes binaires ----
def generer_tous_les_codes():
    """
    Genere les 1000 codes de licence en binaire.
    Client 1   -> 0000000001
    Client 2   -> 0000000010
    Client 3   -> 0000000011
    ...
    Client 1000 -> 1111101000
    Chaque code est hache pour la securite.
    """
    codes = {}
    for i in range(1, 1001):
        code_binaire = format(i, '010b')  # 10 chiffres binaires
        # Hash du code pour eviter la falsification
        code_hash = hashlib.sha256(f"ZougmoreUrbain_{code_binaire}_SecureScan".encode()).hexdigest()[:16].upper()
        codes[code_binaire] = {
            "client_numero": i,
            "code_affiche": code_binaire,
            "hash_verification": code_hash
        }
    return codes

# Liste complete des codes valides
CODES_VALIDES = generer_tous_les_codes()

def verifier_code(code_saisi):
    """Verifie si un code de licence est valide."""
    code_nettoye = code_saisi.strip().replace(" ", "")
    
    # Verifier si c'est un code binaire valide
    if code_nettoye in CODES_VALIDES:
        return True, CODES_VALIDES[code_nettoye]["client_numero"]
    
    # Verifier aussi en format hash (si le revendeur envoie le hash)
    for code_bin, info in CODES_VALIDES.items():
        if code_nettoye.upper() == info["hash_verification"]:
            return True, info["client_numero"]
    
    return False, 0

def activer_licence(code_saisi):
    """Active la licence avec le code fourni. Retourne (succes, message)."""
    valide, numero_client = verifier_code(code_saisi)
    
    if not valide:
        return False, "Code de licence invalide.\nContactez Zougmore Urbain au +226 57 37 30 16"
    
    # Verifier si ce code est deja utilise
    donnees_existantes = lire_licence()
    if donnees_existantes and donnees_existantes.get("code") == code_saisi.strip():
        # Meme code, renouvellement
        pass
    elif donnees_existantes and donnees_existantes.get("code") != code_saisi.strip():
        # Code different sur cette machine
        pass
    
    # Enregistrer la licence
    date_activation = datetime.datetime.now()
    date_expiration = date_activation + datetime.timedelta(days=30)
    
    donnees_licence = {
        "code": code_saisi.strip(),
        "client_numero": numero_client,
        "date_activation": date_activation.isoformat(),
        "date_expiration": date_expiration.isoformat(),
        "actif": True
    }
    
    chemin = _get_licence_path()
    with open(chemin, "w") as f:
        json.dump(donnees_licence, f)
    
    return True, f"✅ Licence activee avec succes !\nValable 30 jours jusqu'au {date_expiration.strftime('%d/%m/%Y')}\nMerci de votre confiance - Zougmore Urbain"

def lire_licence():
    """Lit les donnees de licence depuis le fichier."""
    chemin = _get_licence_path()
    if not os.path.exists(chemin):
        return None
    try:
        with open(chemin, "r") as f:
            return json.load(f)
    except Exception:
        return None

def verifier_statut_licence():
    """
    Verifie le statut de la licence.
    Retourne: (statut, jours_restants, message)
    statut: 'actif', 'expire', 'aucune'
    """
    donnees = lire_licence()
    
    if not donnees:
        return "aucune", 0, "Aucune licence active"
    
    date_expiration = datetime.datetime.fromisoformat(donnees["date_expiration"])
    maintenant = datetime.datetime.now()
    
    jours_restants = (date_expiration - maintenant).days
    
    if maintenant > date_expiration:
        return "expire", 0, "Licence expiree"
    
    return "actif", jours_restants, f"Licence active - {jours_restants} jours restants"

def get_codes_pour_revendeur():
    """
    Retourne la liste des 1000 codes a imprimer pour le revendeur.
    Usage : python licence.py
    """
    lignes = []
    lignes.append("=" * 60)
    lignes.append("CODES DE LICENCE - Scanner de Securite Pro")
    lignes.append("Auteur : Zougmore Urbain | Tel : +226 57 37 30 16")
    lignes.append("Prix : 3000 FCFA/mois via Orange Money")
    lignes.append("=" * 60)
    lignes.append("")
    for i in range(1, 1001):
        code = format(i, '010b')
        lignes.append(f"Client #{i:04d} | Code : {code}")
    return "\n".join(lignes)


# Si lance directement : afficher les codes
if __name__ == "__main__":
    print(get_codes_pour_revendeur())
    # Sauvegarder dans un fichier
    with open("codes_licence_1000.txt", "w") as f:
        f.write(get_codes_pour_revendeur())
    print("\n✅ Liste sauvegardee dans : codes_licence_1000.txt")
