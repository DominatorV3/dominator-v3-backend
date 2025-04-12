import random

def get_token_score(token_address):
    """
    Simule un score IA entre 0.01 et 0.99 pour un token donné.
    Plus tard, on pourra remplacer ça par une vraie API IA.
    """
    score = round(random.uniform(0.01, 0.99), 2)
    return score

def is_token_clean(score, threshold=0.70):
    """
    Détermine si un token est "clean" selon un seuil de score.
    """
    return score < threshold

def display_token_score(token, score):
    """
    Affiche joliment le score IA du token dans la console.
    """
    if is_token_clean(score):
        print(f"✅ Analyse IA : le token {token} a un score sécurisé ({score})")
    else:
        print(f"❌ Analyse IA : le token {token} a un score de risque élevé ({score})")
