class Profil():
    def __init__(self,nom):
        self._Nom = str(nom)
        self._ProfilRecherche = None
        self._Parametres = {} # Dictionnaire des paramètres : clef = paramètre, valeurs = valeurs
        
    def _Get_Parametres(self):
        return self._Parametres
    Parametres = property(_Get_Parametres)
        
    def Definir_Recherche(self, profilrecherche):
        if isinstance(profilrecherche, Profil) and profilrecherche != self:
            self._ProfilRecherche = profilrecherche
    
    def Matching(self,unautreprofil):
        if isinstance(unautreprofil, Profil) is True and unautreprofil != self:
            sommepondérations = float()
            sommepondérée = float()
            
            for unparametre,savaleur in self._Parametres.items():
                sommepondérations += unparametre.Ponderation
                
                if unparametre in unautreprofil.Parametres.keys():
                    sommepondérée += unparametre.Ponderation * unparametre.CalculerSimilarité(unautreprofil.Parametres[unparametre], savaleur)
                    
            if sommepondérations > 0:
                return sommepondérée / sommepondérations
        return 0.0
        
    def Add_Parametre(self, unparametre, valeur):
        if unparametre not in self._Parametres.keys() and isinstance(unparametre, Parametre):
            self._Parametres[unparametre] = valeur
            
class Parametre():
    def __init__(self, nom, poids):
        self._Weight = float(poids)
        self._Name = str(nom)
        
    def _Get_Ponderation(self):
        return self._Weight
    Ponderation = property(_Get_Ponderation)
    
    def CalculerSimilarité(self, valeur1, valeur2):
        return None

class Numerique(Parametre):
    def CalculerSimilarité(self, valeur1, valeur2):
        return 1 / (1 + abs(valeur1 - valeur2))

class Independant(Parametre):
    def CalculerSimilarité(self, valeur1, valeur2):
        return float(valeur1 == valeur2)
    
class Dependant(Parametre):
    def __init__(self, nom, poids):
        super().__init__(nom, poids)
        self._Valeurs = {}
        
    def CalculerSimilarité(self, valeur1, valeur2):
        if valeur1 == valeur2:
            return 1.0
        elif (valeur1,valeur2) in self._Valeurs.keys():
            return self._Valeurs[(valeur1,valeur2)]
        elif (valeur2,valeur1) in self._Valeurs.keys():
            return self._Valeurs[(valeur2,valeur1)]
        return 0.0
    
    def Add_Relation(self,valeur1,valeur2, similarité):
        if (valeur1,valeur2) not in self._Valeurs.keys():
            self._Valeurs[(valeur1,valeur2)] = similarité
            

# Utilisation des classes
# Préapation des paramètrs descriptifs
Parametres = [Numerique("age", 2), Independant("couleur yeux", 1), Dependant("musique", 3)]
Parametres[2].Add_Relation("pop", "soul", 0.2)
Parametres[2].Add_Relation("rock", "pop", 0.3)
Parametres[2].Add_Relation("hardrock", "pop", 0.3)

# Test du fonctionnement des comparaison entre parametres
print("Calcul similarité paramètre numérique : ", Parametres[0].CalculerSimilarité(25, 27))
print("Calcul similarité paramètre indépendant : ", Parametres[1].CalculerSimilarité("bleu", "marron"))
print("Calcul similarité paramètre dépendant : ", Parametres[2].CalculerSimilarité("pop", "rock"))
print("Calcul similarité paramètre dépendant (dans l'autre sens) : ", Parametres[2].CalculerSimilarité("rock", "pop"))
print("Calcul similarité pondéré : ", (2 * Parametres[0].CalculerSimilarité(25, 27) + 1 * 0 + 3 * Parametres[2].CalculerSimilarité("rock", "pop")) / (1 + 2 + 3))

# Déclaration de deux profils
PremierProfil = Profil("profil1")
PremierProfil.Add_Parametre(Parametres[0], 25)
PremierProfil.Add_Parametre(Parametres[1], "bleu")
PremierProfil.Add_Parametre(Parametres[2], "pop")

SecondProfil = Profil("profil2")
SecondProfil.Add_Parametre(Parametres[0], 27)
SecondProfil.Add_Parametre(Parametres[2], "rock")

# Comparaison des deux profils
print("Similarité des deux profils : ", PremierProfil.Matching(SecondProfil))
