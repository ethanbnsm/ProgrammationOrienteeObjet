import random as rnd

class Test():
    def __init__(self, Name, Designer):
        self._Name = str(Name)
        self._Designer = str(Designer)
        self._MyQuestions = list()
    
    def __add__(self,OneQuestion):
        if isinstance(OneQuestion, tuple) and isinstance(OneQuestion[0], Question):
            self._MyQuestions.append(OneQuestion)
    
    def AddQuestions(self, SeveralQuestions):
        if isinstance(SeveralQuestions, list):
            for OneQuestion in SeveralQuestions:
                self + OneQuestion
    
    def GenerateStatment(self):
        Result = str()
        
        for i in range(len(self._MyQuestions)):
            Result += "Question {} - {} points: \n".format(i+1, self._MyQuestions[i][1])
            Result += self._MyQuestions[i][0].GenerateQuestion() +"\n"
        
        return Result

class Question():
     def __init__(self, Topic, Label, Difficulty, Author):
         self._Topic = str(Topic)
         self._Label = str(Label)
         self._Difficulty = float(Difficulty)
         if self._Difficulty > 5:
             self._Difficulty = 5
         if self._Difficulty < 0:
             self._Difficulty = 0
         self._Author = str(Author)
         
     def GenerateQuestion(self):
         return self._Label + "\n"

class QCM(Question):
    def __init__(self,Topic, Label, Difficulty, Author, Propositions=[]):
        super().__init__(Topic, Label, Difficulty, Author)
        self._GoodPropositions = list()
        self._BadPropositions = list()
        if isinstance(Propositions, list) and len(Propositions) == 2 and isinstance(Propositions[0], list) and isinstance(Propositions[1], list):
            self._GoodPropositions = Propositions[0]
            self._BadPropositions = Propositions[1]

    def AddProposition(self,OneProposition,Type):
        if isinstance(Type,bool) and isinstance(OneProposition, str):
            if Type is True:
                self._GoodPropositions.append(OneProposition)
            else:
                self._BadPropositions.append(OneProposition)        

    def GenerateQuestion(self):
        Result = super().GenerateQuestion()
        # Sélection de la bonne valeur
        GoodAnswer = rnd.sample(self._GoodPropositions,1)
       
        # Sélection de deux mauvaises valeurs
        Propositions = GoodAnswer + rnd.sample(self._BadPropositions,2)
        rnd.shuffle(Propositions)
        
        # Fusion et mise en forme
        for Proposition in Propositions:
            Result += "     -> " + Proposition + "\n"

        return Result

class Libre(Question):
     def __init__(self,Topic, Label, Difficulty, Author, Length):
        super().__init__(Topic, Label, Difficulty, Author)
        self._Length = int(Length)
    
     def GenerateQuestion(self):
        Result = super().GenerateQuestion()
        Result += "_"*self._Length
        
        return Result
