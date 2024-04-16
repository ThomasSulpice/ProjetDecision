import matplotlib.pyplot as plt

#1
class ConsoGES:
    def __init__(self, coutGES, utilite,description):
        self.coutGES = coutGES
        self.utilite = utilite
        self.description = description
        
    def equal(self, cons):
        return self.coutGES == cons.coutGES and self.utilite == cons.utilite \
            and self.description == cons.description

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
        
    def equal(self, sac):
        return self.alimentation.equal(sac.alimentation) and self.transport.equal(sac.transport) \
            and self.logement.equal(sac.logement) and self.consommation.equal(sac.consommation)

    #4
    def getCoutGES(self):
        # total_cout = 0
        # for objet_sac in self.alimentation + self.transport + self.logement + self.consommation:
        #     total_cout += objet_sac.coutGES
        # return total_cout
        return self.alimentation.coutGES + self.transport.coutGES \
            + self.logement.coutGES + self.consommation.coutGES

    def getUtilite(self):
        # total_utilite = 0
        # for objet_sac in self.alimentation + self.transport + self.logement + self.consommation:
        #     total_utilite += objet_sac.utilite
        # return total_utilite
        return self.alimentation.utilite + self.transport.utilite \
            + self.logement.utilite + self.consommation.utilite

    def est_valide(self,B):
        return self.getCoutGES() <= B

    #5
    def getSacsADos():
        sacs_a_dos = []
        for a in alimentation:
            for t in transport:
                for l in logement:
                    for c in consommation:
                        sac = SacADosGES(a, t, l, c)
                        sacs_a_dos.append(sac)
        return sacs_a_dos
    
    def filtre(L,B):
        sac_a_dos_filtre=[]
        for sac in L:
            if sac.est_valide(B)== True:
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
    
    #13
    def distance(self, SR):
        set_A = set(self.R)
        set_B = set(SR.R)
        pairs_diff = (set_A - set_B).union(set_B - set_A)
        return len(pairs_diff)*0.5

#8

A = SacADosGES.getSacsADos()

def getSR_PD():
    R = []
    for sac1 in A:
        for sac2 in A:
            if ( sac1.getCoutGES() < sac2.getCoutGES() and sac1.getUtilite() >= sac2.getUtilite() ) \
                or ( sac1.getCoutGES() <= sac2.getCoutGES() and sac1.getUtilite() > sac2.getUtilite() ):
                    R.append((sac1 , sac2))
    return SystemeRelationnel(A, R)

                    
#9

def front_Pareto():
    R = getSR_PD().R
    liste_faible = []
    for pair in R:
        liste_faible.append(pair[1])
    liste_forte = list(set(A) - set(liste_faible))
    x = [sac.getCoutGES() for sac in liste_forte]
    y = [sac.getUtilite() for sac in liste_forte]
    plt.scatter(x,y)
    plt.xlabel("coût GES du sac à dos")
    plt.ylabel("utilité du sac à dos")
    plt.title("Front de Pareto de A")
    plt.show()
        
front_Pareto()

        
#10

def getSR_LexU():
    R = []
    for sac1 in A:
        for sac2 in A:
            if ( sac1.getUtilite() > sac2.getUtilite() ) \
                or ( sac1.getUtilite() == sac2.getUtilite() and sac1.getCoutGES() < sac2.getCoutGES() ) :
                    R.append((sac1 , sac2))
    return SystemeRelationnel(A, R)

def getSR_LexC():
    R = []
    for sac1 in A:
        for sac2 in A:
            if ( sac1.getCoutGES() < sac2.getCoutGES() ) \
                or ( sac1.getCoutGES() == sac2.getCoutGES() and sac1.getUtilite() > sac2.getUtilite() ):
                    R.append((sac1 , sac2))
    return SystemeRelationnel(A, R)
        

#11

def getSR_Borne(B):
    R = []
    for sac1 in A:
        for sac2 in A:
            if ( sac1.getCoutGES() <= B and sac2.getCoutGES() > B ) \
                or ( sac1.getCoutGES() <= B and sac2.getCoutGES() <= B and sac1.getUtilite() > sac2.getUtilite()) :
                    R.append((sac1 , sac2))
    return SystemeRelationnel(A, R)

SR_PD = getSR_PD()
SR_LexU = getSR_LexU()
SR_LexC = getSR_LexU()
print("Distance entre Pareto et LexU :" + str(SR_PD.distance(SR_LexU)))
print("Distance entre Pareto et LexC :" + str(SR_PD.distance(SR_LexC)))
print("Distance entre LexU et LexC :" + str(SR_LexU.distance(SR_LexC)))
    


                    
                    



