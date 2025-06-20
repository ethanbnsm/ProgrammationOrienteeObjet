import random as rnd

class SuperHero():
    #Question 1
    def __init__(self, tonnom, tesdegats, tavie, tonpoidsmax, tonesquive, tonnomdesuperhero=None):
        self._Nom = str(tonnom)
        self._Surname = None
        if isinstance(tonnomdesuperhero,str) and len(str(tonnomdesuperhero)) > 0:
            self._Surname = str(tonnomdesuperhero)
        self._Degats = float(tesdegats)
        self._Vie = float(tavie)
        self._PoidsMax = float(tonpoidsmax)
        self._Esquive = int()
        if int(tonesquive) >= 0 and int(tonesquive) < 100:
            self._Esquive = int(tonesquive)
        self._Matos = []
    
    # Question 2
    def _Set_SurName(self, tonsurnom):
        if len(str(tonsurnom)) > 0:
            self._Surname = str(tonsurnom)
    def _GetSurName(self):
        return self._Surname
    Pseudo = property(_GetSurName, _Set_SurName)
    
    # Question 3
    def __repr__(self):
        if self._Surname is not None:
            return self._Surname
        else:
            return self._Nom
    # Question 8
    def Attaquer(self, cible):
        if isinstance(cible, SuperHero):
            # S'il n'est pas KO, il peut attaquer
            if self._Vie > 0:
               print("{} attaque {}".format(str(self), str(cible)))
               cible.Defendre(self, self._Degats + sum([i.Attaque for i in self._Matos]))
            else:
                print("{} n'est plus en etat d'attaquer".format(str(self)))
    
	# Question 9        
    def Defendre(self, attaquant, degatsenvoyés):
         if isinstance(attaquant, SuperHero):
            
            # En fonction de l'esquive de 
            if rnd.randint(0,100) > self._Esquive:
                # Esquivé !
                print("{} a esquivé l'attaque".format(str(self)))
            else:
                # Touché !, il prend des dégats dont une partie est absorbée par l'armure
                self._Vie -= abs(min([0, sum([i.Defense for i in self._Matos]) - degatsenvoyés]))
                if self._Vie > 0:
                    print("{} est touché, il lui reste {} points de vie".format(str(self), self._Vie))
            
            self.Attaquer(attaquant)
    # Question 7
    def AjouterMateriel(self, unobjet):
        if isinstance(unobjet, Objet):
            if sum([i.Masse for i in self._Matos]) + unobjet.Masse <= self._PoidsMax:
                if unobjet not in self._Matos:
                    self._Matos.append(unobjet)
            else:
                print("{} est trop chargé".format(str(self)))
        
class Objet():
    def __init__(self, tonnom, tamasse):
        self._Nom = str(tonnom)
        self._Masse = float(tamasse)
        self._Composants = []
    
    def _CalculerMasse(self):
        if self._Composants == []:
            return self._Masse
        else:
            return self._Masse + sum([i.Masse for i in self._Composants])
    
    def _CalculerDef(self):
        if self._Composants == []:
            return 0
        else:
            return sum([i.Defense for i in self._Composants])
      
    def _CalculerAtt(self):
         if self._Composants == []:
            return 0
         else:
            return sum([i.Attaque for i in self._Composants])
        
    def AjouterComposant(self, nouveaucomposant):
        if isinstance(nouveaucomposant, Objet):
            if nouveaucomposant not in self._Composants:
                self._Composants.append(nouveaucomposant)
    
    Defense = property(_CalculerDef)
    Attaque = property(_CalculerAtt)
    Masse = property(_CalculerMasse)
    
class Arme(Objet):
    def __init__(self, tonnom, tamasse, tesdegats):
        super().__init__(tonnom, tamasse)
        self._Degats = float(tesdegats)
        
    def _CalculerAtt(self):
        return super()._CalculerAtt() + self._Degats
    
    Attaque = property(_CalculerAtt)

class Armure(Objet):
    def __init__(self, tonnom, tamasse, tadefense):
        super().__init__(tonnom, tamasse)
        self._Defense = float(tadefense)
        
    def _CalculerDef(self):
        return super()._CalculerDef() + self._Defense

    Defense = property(_CalculerDef)

# instantiation des super héro
Strange = SuperHero("Stephen Strange", 10, 20, 20, 70)
IronMan= SuperHero("Tony STARK", 10, 50, 30, 60, "Iron Man")
Thanos = SuperHero("Thanos",15,100,80,40)
print(Strange)
Strange.Pseudo = "Docteur Strange"
print(Strange)


Strange.AjouterMateriel(Armure("Cape de Lévitation",2,15))

IronMan.AjouterMateriel(Armure("Hulkbuster",100,200))
Mark85 = Armure("Mark LXXXV",20,40)
Mark85.AjouterComposant(Arme("Rayon répulseur",2,10))
IronMan.AjouterMateriel(Mark85)

Gant = Armure("Gant de pouvoir",10,2)
Thanos.AjouterMateriel(Gant)
Gant.AjouterComposant(Arme("Pierre du Pouvoir",0.5,40))
Gant.AjouterComposant(Armure("Pierre du temps",0.5,20))

Strange.Attaquer(Thanos)
IronMan.Attaquer(Thanos)
