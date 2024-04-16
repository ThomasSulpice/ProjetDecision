#1
class ConsoGES:
  def __init__(self, coutGES, utilite,description):
        self.coutGES = coutGES
        self.utilite = utilite
        self.description = description
        
#2       
alimentation = [
    ConsoGES(2.2, 5, "Alimentation très carnée"),
    ConsoGES(1.2, 7, "Alimentation modérément carnée"),
    ConsoGES(0.9, 6, "Alimentation végétarienne"),
    ConsoGES(0.4, 4, "Alimentation végétalienne")
]

transport = [
    ConsoGES(3, 4, "Utilisation d'une grosse voiture thermique pour 5000km à l'année par personne"),
    ConsoGES(2.1, 6, "Utilisation d'une petite voiture thermique pour 10000km àl'année par personne"),
    ConsoGES(1.6, 5, "Utilisation d'une voiture électrique de taille moyenne pour 5000km à l'année par personne"),
    ConsoGES(0.3, 3, "Utilisation de la mobilité douce")
]

logement = [
    ConsoGES(3, 7, "Occupation d'une maison mal isolée thermiquement 60m2 par personne)"),
    ConsoGES(0.2, 6, "Occupation d'un appartement très bien isolé thermiquement 40m2 par personne)")
]
consommation = [
    ConsoGES(2.5, 10, "Consommation importante de biens et services"),
    ConsoGES(1.3, 6, "Consommation sobre de biens et services")
]
#3
class SacADosGES:
      def __init__(self, alimentation, transport, logement, consommation):
        self.alimentation = alimentation
        self.transport = transport
        self.logement = logement
        self.consommation = consommation
        
        #4
        def getCoutGES(self):
          total_cout = 0
          for objet_sac in self.alimentation + self.transport + self.logement + self.consommation:
            total_cout += objet_sac.coutGES
          return total_cout
        
        def getUtilite(self):
          total_utilite = 0
          for objet_sac in self.alimentation + self.transport + self.logement + self.consommation:
            total_utilite += objet_sac.utilite
          return total_utilite
        
        def est_valide(self,B):
          return self.getCoutGES() <= B
        
        
       #5  
        def getSacsADos(alimentation, transport, logement, consommation):
          sacs_a_dos = []
          for a in alimentation:
            for t in transport:
                for l in logement:
                    for c in consommation:
                        sac = SacADosGES([a], [t], [l], [c])
                        sacs_a_dos.append(sac)
          return sacs_a_dos
        
        def filtre(self,sac_a_dos,B):
          sac_a_dos_filtre=[]
          for sac in sac_a_dos:
            if est_valide(sac,B)== True:
              sac_a_dos_filtre.append(sac)
          return sac_a_dos_filtre
 #6  

class SystemeRelationnel:
    def __init__(self, A, R):
        self.A = A  # Ensemble des éléments
        self.R = R  # Ensemble des paires constituant la relation binaire
        
    #7
    def est_reflexive(self):
        for element in self.A:
            if (element, element) not in self.R:
                return False
        return True

    def est_symetrique(self):
        for (a, b) in self.R:
            if (b, a) not in self.R:
                return False
        return True

    def est_transitive(self):
        for (a, b) in self.R:
            for (c, d) in self.R:
                if b == c and (a, d) not in self.R:
                    return False
        return True


 
