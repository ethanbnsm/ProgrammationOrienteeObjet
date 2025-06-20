class Polynome():
    def __init__(self, valeurs = None):
        self._Monomes=[]
        if isinstance(valeurs, list):
            for element in valeurs:
                if isinstance(element,tuple) and len(element) == 2:
                    # instantie un monome de dégré donné
                    newmonome = Monome(element[0], element[1])
                    self._Monomes.append(newmonome)                   

    def Add_Monome(self, newmonome):
        if isinstance(newmonome, Monome):
            degrés = [element.Degré for element in self._Monomes]
            if newmonome.Degré in degrés:
                # Cas où le degré est déjà existant
                pos = degrés.index(newmonome.Degré)
                nouvelelement = self._Monomes.pop(pos)
                self._Monomes.append(nouvelelement + newmonome)
            else:
                # Le degré n'existe pas, on peut l'ajouter
                self._Monomes.append(newmonome)

    def Derivee(self):
        PolyDerive = Polynome()
        for element in self._Monomes:
            resultat = element.Derivee()
            if resultat is not None:
                PolyDerive.Add_Monome(resultat)
        
        return PolyDerive
        
    def Evaluer(self,x):
        resultat = float()
        for element in self._Monomes:
            resultat += element.Evaluer(x)
        return resultat
        
    def __str__(self):
        resultat = ""
        for element in self._Monomes[:-1]:
            resultat += str(element) + " + "
        resultat += str(self._Monomes[-1])
        return resultat

    def __mul__(self,element):
        return "coucou"
        

class Monome():
    def __init__(self, degré, coef):
        if coef >= 0:
            self._Degré = int(degré)
        else:
            self._Degré = 0
        self._Coef = float(coef)
        
    def Derivee(self):
        if self._Degré > 0:
            return Monome(self.Degré-1, self._Coef * self._Degré)
        else:
            return Monome(0,0)
    
    def _Get_Coef(self):
        return self._Coef
    def _Set_Coef(self, nouvellevaleur):
        if isinstance(nouvellevaleur, int):
            self._Coef = nouvellevaleur
    Coef = property(_Get_Coef, _Set_Coef)
    
    def _Get_Degré(self):
        return self._Degré
    def _Set_Degré(self, nouvellevaleur):
        if isinstance(nouvellevaleur, int):
            self._Degré = nouvellevaleur
    Degré = property(_Get_Degré, _Set_Degré)
    
    def Evaluer(self,x):
        return self._Coef * x ** self._Degré
    
    def __str__(self):
        if self._Degré == 0:
            return str(self._Coef)
        elif self._Degré == 1:
            return "{}.x".format(self._Coef)
        elif self._Degré > 1:
            return "{}.x^{}".format(self._Coef, self._Degré)
        
        return "0"
    
    def __add__(self, autreelement):
        if isinstance(autreelement, Monome):
            if self._Degré != autreelement.Degré:
                Poly = Polynome()
                Poly.Add_Monome(self)
                Poly.Add_Monome(autreelement)
                return Poly
            elif isinstance(autreelement, MonomeRationnel) == False:
                # Cas monome classique
                return Monome(self._Degré, self._Coef + autreelement.Coef)
            else:
                # On appelle l'addition de la classe Monome Rationnel
                return autreelement + self
    
    
class MonomeRationnel(Monome):
     def __init__(self, degré, coefrationnel):
        self._Degré = int(degré)
        self._CoefDenominateur = 1
        self._CoefNumerateur = 1
        
        if isinstance(coefrationnel, tuple) and len(coefrationnel)==2:
            self._CoefNumerateur = coefrationnel[0]
            self._CoefDenominateur = coefrationnel[1]

     def _Get_Denominateur(self):
         return self._CoefDenominateur
     def _Get_Numerateur(self):
         return self._CoefNumerateur
     Numerateur = property(_Get_Numerateur)
     Denominateur = property(_Get_Denominateur)

     def Evaluer(self,x):
        return float(self._CoefNumerateur / self._CoefDenominateur) * x ** self._Degré

     def __str__(self):
        if self._Degré == 0:
            return "{}/{}".format(self._CoefNumerateur, self._CoefDenominateur)
        elif self._Degré == 1:
            return "{}/{}.x".format(self._CoefNumerateur, self._CoefDenominateur)
        elif self._Degré > 1:
            return "{}/{}.x^{}".format(self._CoefNumerateur, self._CoefDenominateur, self._Degré)
        
        return ""
    
     def __add__(self, autreelement):
         if isinstance(autreelement, Monome):
            if self._Degré != autreelement.Degré:
                Poly = Polynome()
                Poly.Add_Monome(self)
                Poly.Add_Monome(autreelement)
                return Poly
            elif isinstance(autreelement, MonomeRationnel):
                # Cas de somme de deux monomes rationnels
                if self._CoefDenominateur == autreelement.Denominateur:
                    return MonomeRationnel(self._Degré, (self._CoefNumerateur + autreelement.Numerateur, self._CoefDenominateur))
                else:
                    return MonomeRationnel(self._Degré, (self.Numerateur*autreelement.Denominateur + autreelement.Numerateur*self._CoefDenominateur, self._CoefDenominateur*autreelement.Denominateur))
            else:
                # cas de somme de monome rationnel avec un monome classique
                return MonomeRationnel(self._Degré, (self._CoefNumerateur + autreelement.Coef*self._CoefDenominateur, self._CoefDenominateur))

     def Derivee(self):
        if self._Degré > 0:
            return MonomeRationnel(self.Degré-1, (self._CoefNumerateur * self._Degré, self._CoefDenominateur))
        else:
            return None


Poly = Polynome([(0,5),(2,6)])
Poly.Add_Monome(MonomeRationnel(1,(2,3)))
Poly.Add_Monome(MonomeRationnel(2,(1,4)))
print("Expression du polynôme : ", Poly)
print("Evaluation en 0 : ", Poly.Evaluer(0))
DPoly = Poly.Derivee()
print("Derivée : ",DPoly)
print("Evaluation en 1 : ",DPoly.Evaluer(1))

print(MonomeRationnel(1,(1,4)) + MonomeRationnel(1,(1,2)))
