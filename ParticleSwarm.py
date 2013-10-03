#-*- coding: utf-8 -*-
from Utilerias import *
class PSO(object):

    def __init__(self, ueas, numero_de_particulas, limites_inferiores):
        self.ueas = ueas
        self.numero_de_particulas = numero_de_particulas
        self.limites_inferiores = limites_inferiores
        self.particulas = []
        self.P_global = Particula(len(ueas))
        self.clip = lambda n, minn, maxn: max(min(maxn, n), minn)

    def inicializar_particulas(self):
    	for x in xrange(len(self.ueas)):
            if self.P_global.posicion[x] < self.limites_inferiores[x+1]:
                self.P_global.posicion[x] = self.limites_inferiores[x+1]
        
        for y in xrange(self.numero_de_particulas):
            particula = Particula(len(self.ueas))
            #Preprocesar partículas
            for x in xrange(len(self.ueas)):
                if particula.posicion[x] < self.limites_inferiores[x+1]:
                    particula.posicion[x] = self.limites_inferiores[x+1]
            self.particulas.append(particula)