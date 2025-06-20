import random as rnd

class Type():
    def __init__(self, tonnom):
        self._Nom = str(tonnom)
        self._Relations = dict() #Utiliser une liste de t-uple ou de listes était aussi bon
        
    def DefinirSensibilité(self, unautretype, taux):
        if isinstance(unautretype, Type) and unautretype not in self._Relations.keys() and float(taux) >= 0:
            # Ajout d'une nouvelle relation avec un autre type
            self._Relations[unautretype] = taux
    
    def RetournerSensibilité(self, unautretype):
        if isinstance(unautretype, Type) and unautretype in self._Relations.keys():
            return self._Relations[unautretype]
        # Cas par défaut, aucune sensibilité n'a été précisée
        return 1.0
    
    def __gt__(self, unautretype):
        if isinstance(unautretype, Type):
            return self.RetournerSensibilité(unautretype) > 1.0
        return False
    
    def __repr__(self): # Non demandé dans le test
        return "Type {}".format(self._Nom)
    
class Pokemon():
    def __init__(self, nom, hpmax, tontype):
        self._Nom = str(nom)
        self._VieMax = int()
        self._Vie = int()
        
        if hpmax > 0:
            self._VieMax = int(hpmax)
            self._Vie = int(hpmax)
        
        self._Type = None
        if isinstance(tontype, Type):
            self._Type = tontype
            
        self._Attaques = []
       
    def _Get_Vie(self):
        return self._Vie
    Vie = property(_Get_Vie)
    
    def _Get_Type(self):
        return self._Type
    Type = property(_Get_Type)
    
    def _Get_Nom(self):
        return self._Nom
    Nom = property(_Get_Nom)
    
    def AjouterAttaques(self, listeattaques): # Non demandé dans le test
        if isinstance(listeattaques, list):
            for element in listeattaques:
                self.AjouterAttaque(element)
    
    def AjouterAttaque(self, nouvelleattaque): # Non demandé dans le test
        # Vérification que c'est bien un objet de type Attaque
        if isinstance(nouvelleattaque, Attaque):
            # Vérification du type du pokemon est ok
            if nouvelleattaque.TypePokemonok(self):
                print("Ajout pour {} de '{}'".format(self._Nom, str(nouvelleattaque)))
                if len(self._Attaques) > 4:
                    # On en remplace une aléatoirement
                    self._Attaques[rnd.randint(0,len(self._Attaques) - 1)] = nouvelleattaque
                else:
                    self._Attaques.append(nouvelleattaque)
      
    def Attaquer(self, unpokemon):
        # Un pokemon attaque
        if isinstance(unpokemon, Pokemon):
            # S'il n'est pas KO, il peut attaquer
            if self._Vie > 0:
                if self._Attaques != []:
                    # Il choisit une attaque parmis celles disponibles
                    monattaque = rnd.choice(self._Attaques)
                    print("{} lance {} sur {}".format(self._Nom, monattaque.Nom, unpokemon.Nom))
                    #if unpokemon.Efficacité(monattaque) is not None: print(unpokemon.Efficacité(monattaque))
                    unpokemon.Defendre(self, monattaque)
                else:
                    print("{} n'a pas d'attaque de disponible".format(self._Nom))
            else:
                print("{} est KO, il ne peut plus attaquer".format(self._Nom))
    
    def Defendre(self, unpokemon, uneattaque):
        # Un pokemon se fait attaquer
        if isinstance(unpokemon, Pokemon) and isinstance(uneattaque, Attaque):
            
            # En fonction de la précision de l'attaque, celle-ci peut louper sa cible:
            if rnd.randint(0,100) > uneattaque.Precision:
                # Loupé !
                print("    Attaque a loupé sa cible")
            else:
                # Touché !, il prend des dégats
                if self.Efficacité(uneattaque) is not None: print(self.Efficacité(uneattaque))
                print("    {} prends {} points de dégats".format(self._Nom, self.CalculDegats(uneattaque)))
                self._Vie -= self.CalculDegats(uneattaque)
            
            # Et il répond s'il n'est pas KO
            self.Attaquer(unpokemon)
                        
    def CalculDegats(self, uneattaque):
         if isinstance(uneattaque, Attaque):
             return (uneattaque.Puissance * self._Type.RetournerSensibilité(uneattaque.Type))
         return 0.0

    def Efficacité(self, uneattaque): # Non demandé dans le test
         if isinstance(uneattaque, Attaque):
             Taux = self._Type.RetournerSensibilité(uneattaque.Type)
             if Taux >= 2: return "    C'est très efficace"
             if Taux > 1: return "    C'est efficace"
             if Taux <= 0.5: return "    Ce n'est pas très efficace"
             if Taux == 0: return "    Ce n'a aucun effet"  

    def __repr__(self): # Non demandé dans le test
        chaine = "{} est un pokemon de {}".format(self._Nom, str(self._Type))
        if len(self._Attaques) == 0:
            chaine += ", qui ne possède aucune attaque"
        else:
            chaine += "\n Dont les attaques sont:"
            for attaquetemp in self._Attaques:
                chaine += "\n -{}".format(str(attaquetemp))
        return chaine

class Attaque():
    def __init__(self, nom, tapuissance, tontype, typepokemon, taprecision = 100):
        self._Nom = str(nom)
        self._Puissance = int(tapuissance)
        self._Type = None
        self._TypeCompatibles = []
        self._Precision = int(taprecision)
        
        if isinstance(tontype, Type):
            self._Type = tontype
        if isinstance(typepokemon, list):
            for element in typepokemon:
                if isinstance(element, Type) and element not in self._TypeCompatibles:
                    self._TypeCompatibles.append(element)        
        
    def _Get_Puissance(self):
        return self._Puissance
    Puissance = property(_Get_Puissance)
    
    def _Get_Type(self):
        return self._Type
    Type = property(_Get_Type)
    
    def _Get_Nom(self):
        return self._Nom
    Nom = property(_Get_Nom)
        
    def _Get_Precision(self):
        return self._Precision
    Precision = property(_Get_Precision)
    
    def TypePokemonok(self, unpokemon):
        if isinstance(unpokemon, Pokemon):
            if self._TypeCompatibles == []:
                return True
            else:
                return unpokemon.Type in self._TypeCompatibles
        return False
    
    def __repr__(self): # Non demandé dans le test
        return "Attaque {}".format (self._Nom)
    
class Biclasse(Pokemon):
    def __init__(self, nom, hpmax, tonpremiertype, tonsecondtype):
        super().__init__(nom, hpmax, tonpremiertype)
        self._SecondType = None
        if isinstance(tonsecondtype, Type):
            self._SecondType = tonsecondtype
        
    def CalculDegats(self, uneattaque):
        if isinstance(uneattaque, Attaque):
            return (uneattaque.Puissance * self._Type.RetournerSensibilité(uneattaque.Type)) * self._SecondType.RetournerSensibilité(uneattaque.Type)
        
    def AjouterAttaque(self, nouvelleattaque):
        # Vérification que c'est bien un objet de type Attaque
        if isinstance(nouvelleattaque, Attaque):
            # Vérification du type du pokemon est ok
            if nouvelleattaque.TypePokemonok(self._Type) or nouvelleattaque.TypePokemonok(self._SecondType):
                if len(self._Attaques) > 4:
                    # On en remplace une aléatoirement
                    self._Attaques[rnd.randint(0,len(self._Attaques) - 1)] = nouvelleattaque
                else:
                    self._Attaques.append(nouvelleattaque)
        
# Définition des types et de leurs sensibilités       
TypesDispos = {"Normal":Type("Normal"), "Feu":Type("Feu"), "Eau":Type("Eau"), "Electrik":Type("Electrik")}
TypesDispos["Eau"].DefinirSensibilité(TypesDispos["Electrik"],2)
TypesDispos["Eau"].DefinirSensibilité(TypesDispos["Eau"],0.5)
TypesDispos["Eau"].DefinirSensibilité(TypesDispos["Feu"],0.5)
TypesDispos["Feu"].DefinirSensibilité(TypesDispos["Eau"],2)
TypesDispos["Feu"].DefinirSensibilité(TypesDispos["Feu"],0.5)
TypesDispos["Electrik"].DefinirSensibilité(TypesDispos["Electrik"],0.5)

print("Feu plus fort que l'eau ?", str(TypesDispos["Feu"]>TypesDispos["Eau"]))

# Définitions des attaques
Attaques = []
Attaques.append(Attaque("Eclair",16,TypesDispos["Electrik"],[TypesDispos["Electrik"]],75))
Attaques.append(Attaque("Flammèche",16,TypesDispos["Feu"],[TypesDispos["Feu"]],75))
Attaques.append(Attaque("Pistolet A O",16,TypesDispos["Eau"],[TypesDispos["Eau"]],50))
Attaques.append(Attaque("Charge",6,None,None,100))

# Créations des pokemon et de leur attaques
Pokemons = [Pokemon("Pikachu",35,TypesDispos["Electrik"]), Pokemon("Salamèche",39,TypesDispos["Feu"]), Pokemon("Carapuce",44,TypesDispos["Eau"])]
print("\nAjout des attaques aux pokemons + vérifications que leur type est compatible :")
for eachpokemon in Pokemons:
    eachpokemon.AjouterAttaques(Attaques)

print("\nInformations retournées par le premier Pokemon de la liste :")
print(Pokemons[0])

print("\nQue le combat commence !")
Pokemons[1].Attaquer(Pokemons[2])
