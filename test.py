import matplotlib.pyplot as plt
import numpy as np
from mip import Model, xsum, minimize, CONTINUOUS
import time


# 1
class ConsoGES:
    def __init__(self, coutGES, utilite, description):
        self.coutGES = coutGES
        self.utilite = utilite
        self.description = description

    def equal(self, cons):
        return self.coutGES == cons.coutGES and self.utilite == cons.utilite \
            and self.description == cons.description


# 2
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


# 3
class SacADosGES:
    def __init__(self, alimentation, transport, logement, consommation):
        self.alimentation = alimentation
        self.transport = transport
        self.logement = logement
        self.consommation = consommation

    def equal(self, sac):
        return self.alimentation.equal(sac.alimentation) and self.transport.equal(sac.transport) \
            and self.logement.equal(sac.logement) and self.consommation.equal(sac.consommation)

    # 4
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

    def est_valide(self, B):
        return self.getCoutGES() <= B

    # 5
    def getSacsADos():
        sacs_a_dos = []
        for a in alimentation:
            for t in transport:
                for l in logement:
                    for c in consommation:
                        sac = SacADosGES(a, t, l, c)
                        sacs_a_dos.append(sac)
        return sacs_a_dos

    def filtre(L, B):
        sac_a_dos_filtre = []
        for sac in L:
            if sac.est_valide(B) == True:
                sac_a_dos_filtre.append(sac)
        return sac_a_dos_filtre

    def binary_list(self):
        liste = [0 for i in range(12)]
        for k in range(4):
            if self.alimentation.equal(alimentation[k]):
                liste[k] = 1
                break
        for k in range(4):
            if self.transport.equal(transport[k]):
                liste[4 + k] = 1
                break
        if self.logement.equal(logement[0]):
            liste[8] = 1
        else:
            liste[9] = 1
        if self.consommation.equal(consommation[0]):
            liste[10] = 1
        else:
            liste[11] = 1
        return liste


# 6

class SystemeRelationnel:
    def __init__(self, A, R):
        self.A = A  # Ensemble des éléments
        self.R = R  # Ensemble des paires constituant la relation binaire

    # 7
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

    # 13
    def distance(self, SR):
        set_A = set(self.R)
        set_B = set(SR.R)
        pairs_diff = (set_A - set_B).union(set_B - set_A)
        return len(pairs_diff) * 0.5


# 8

A = SacADosGES.getSacsADos()


def getSR_PD():
    R = []
    for sac1 in A:
        for sac2 in A:
            if (sac1.getCoutGES() < sac2.getCoutGES() and sac1.getUtilite() >= sac2.getUtilite()) \
                    or (sac1.getCoutGES() <= sac2.getCoutGES() and sac1.getUtilite() > sac2.getUtilite()):
                R.append((sac1, sac2))
    return SystemeRelationnel(A, R)


# 9

def front_Pareto():
    R = getSR_PD().R
    liste_faible = []
    for pair in R:
        liste_faible.append(pair[1])
    liste_forte = list(set(A) - set(liste_faible))
    x = [sac.getCoutGES() for sac in liste_forte]
    y = [sac.getUtilite() for sac in liste_forte]
    plt.figure(1)
    plt.scatter(x, y)
    plt.xlabel("coût GES du sac à dos")
    plt.ylabel("utilité du sac à dos")
    plt.title("Front de Pareto de A")
    plt.show()


front_Pareto()


# 10

def getSR_LexU():
    R = []
    for sac1 in A:
        for sac2 in A:
            if (sac1.getUtilite() > sac2.getUtilite()) \
                    or (sac1.getUtilite() == sac2.getUtilite() and sac1.getCoutGES() < sac2.getCoutGES()):
                R.append((sac1, sac2))
    return SystemeRelationnel(A, R)


def getSR_LexC():
    R = []
    for sac1 in A:
        for sac2 in A:
            if (sac1.getCoutGES() < sac2.getCoutGES()) \
                    or (sac1.getCoutGES() == sac2.getCoutGES() and sac1.getUtilite() > sac2.getUtilite()):
                R.append((sac1, sac2))
    return SystemeRelationnel(A, R)


# 11

def getSR_Borne(B):
    R = []
    for sac1 in A:
        for sac2 in A:
            if (sac1.getCoutGES() <= B and sac2.getCoutGES() > B) \
                    or (sac1.getCoutGES() <= B and sac2.getCoutGES() <= B and sac1.getUtilite() > sac2.getUtilite()):
                R.append((sac1, sac2))
    return SystemeRelationnel(A, R)


# 14

SR_PD = getSR_PD()
SR_LexU = getSR_LexU()
SR_LexC = getSR_LexC()
SR_Borne2 = getSR_Borne(2)
SR_Borne3 = getSR_Borne(3)
SR_Borne5 = getSR_Borne(5)

print("Distance entre Pareto et LexU :" + str(SR_PD.distance(SR_LexU)))
print("Distance entre Pareto et LexC :" + str(SR_PD.distance(SR_LexC)))
print("Distance entre Pareto et Borne2 :" + str(SR_PD.distance(SR_Borne2)))
print("Distance entre Pareto et Borne3 :" + str(SR_PD.distance(SR_Borne3)))
print("Distance entre Pareto et Borne5 :" + str(SR_PD.distance(SR_Borne5)))
print("Distance entre LexU et LexC :" + str(SR_LexU.distance(SR_LexC)))
print("Distance entre LexU et Borne2 :" + str(SR_LexU.distance(SR_Borne2)))
print("Distance entre LexU et Borne3 :" + str(SR_LexU.distance(SR_Borne3)))
print("Distance entre LexU et Borne5 :" + str(SR_LexU.distance(SR_Borne5)))
print("Distance entre LexC et Borne2 :" + str(SR_LexC.distance(SR_Borne2)))
print("Distance entre LexC et Borne3 :" + str(SR_LexC.distance(SR_Borne3)))
print("Distance entre LexC et Borne5 :" + str(SR_LexC.distance(SR_Borne5)))


# 15

def utiliteMax(B):
    items = alimentation + transport + logement + consommation
    M = np.zeros((13, int(np.floor(10 * B) + 1)))

    for i in range(1, 13):
        for c in range(1, int(np.floor(10 * B) + 1)):
            if items[i - 1].coutGES <= c / 10:
                if i <= 4:
                    M[i, c] = max(M[i - 1, c], items[i - 1].utilite)
                elif i <= 8:
                    if M[4, c - int(np.floor(items[i - 1].coutGES * 10))] == 0:
                        M[i, c] = M[i - 1, c]
                    else:
                        M[i, c] = max(M[i - 1, c],
                                      M[4, c - int(np.floor(items[i - 1].coutGES * 10))] + items[i - 1].utilite)
                elif i <= 10:
                    if M[8, c - int(np.floor(items[i - 1].coutGES * 10))] == M[
                        4, c - int(np.floor(items[i - 1].coutGES * 10))]:
                        M[i, c] = M[i - 1, c]
                    else:
                        M[i, c] = max(M[i - 1, c],
                                      M[8, c - int(np.floor(items[i - 1].coutGES * 10))] + items[i - 1].utilite)
                else:
                    if M[8, c - int(np.floor(items[i - 1].coutGES * 10))] == M[
                        4, c - int(np.floor(items[i - 1].coutGES * 10))] \
                            or M[10, c - int(np.floor(items[i - 1].coutGES * 10))] == M[
                        8, c - int(np.floor(items[i - 1].coutGES * 10))]:
                        M[i, c] = M[i - 1, c]
                    else:
                        M[i, c] = max(M[i - 1, c],
                                      M[10, c - int(np.floor(items[i - 1].coutGES * 10))] + items[i - 1].utilite)
            else:
                M[i, c] = M[i - 1, c]
    return max(M[:, -1])


# 16

B = [i / 10 for i in range(22, 108)]
maxU = [utiliteMax(b) for b in B]
plt.figure(2)
plt.plot(B, maxU)
plt.xlabel("borne de coût GES")
plt.ylabel("niveau d\'utilité optimale")
plt.title("Graphique du niveau d\'utilité optimale en fonction de la borne de coût GES")
plt.grid()
plt.show()


# 17
def estOrdMin(P, k1, k2):
    m = Model()
    u = [m.add_var(var_type=CONTINUOUS, lb=0, ub=100) for i in range(12)]

    for pair in P:
        list1 = pair[0].binary_list()
        list2 = pair[1].binary_list()
        m += xsum(u[i] * (list1[i] - list2[i]) for i in range(12)) >= 10 ** (-6)

    k1_list = k1.binary_list()
    k2_list = k2.binary_list()
    m.objective = minimize(xsum(u[i] * (k1_list[i] - k2_list[i]) for i in range(12)))

    m.verbose = 0

    m.optimize()
    # m.write('PL.pl')

    if m.objective_value <= 0:
        return False
    else:
        return True


# testsum = 0
# for i in range(63):
#     if estOrdMin([SR_LexU.R[0],SR_LexU.R[1]] , A[0] , A[i+1]):
#         testsum+=1
# print("testsum:" + str(testsum))

def nonOrdDomines(P, B):
    listeSacs = []
    sacsBornes = SacADosGES.filtre(A, B)

    for sac in A:
        nonDomine = True
        for sacB in sacsBornes:
            if estOrdMin(P, sacB, sac):
                nonDomine = False
                break
        if nonDomine:
            listeSacs.append(sac)

    return listeSacs


# print(len(SR_PD.R))
# -> 763

start = time.time()

x_B = [i / 10 for i in range(22, 50)]
x_R = [i for i in range(20)]

y_B = [len(nonOrdDomines(SR_PD.R[:50], b)) for b in x_B]
y_R = [len(nonOrdDomines(SR_PD.R[:i + 1], 5)) for i in x_R]

plt.figure(3)
plt.plot(x_B, y_B)
plt.xlabel("coût GES B")
plt.ylabel("nombre de sac à dos")
plt.title("Graphique du nombre de sacs à dos non ordinalement dominés par ceux de coût <B")
plt.grid()
plt.show()

plt.figure(4)
plt.plot(x_R, y_R)
plt.xlabel("|R|")
plt.ylabel("nombre de sacs à dos")
plt.title("Graphique du nombre de sacs à dos non ordinalement dominés en fonction du nombre de pairs de P (B=5)")
plt.grid()
plt.show()

end = time.time()
print("temps d'exécution question 18 :" + str(end - start))
