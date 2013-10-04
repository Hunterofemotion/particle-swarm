#-*- coding: utf-8 -*-
from Utilerias import *
from copy import deepcopy
class PSO(object):

    def __init__(self, ueas, numero_de_particulas, limites_inferiores):
        self.ueas = ueas
        self.numero_de_particulas = numero_de_particulas
        self.limites_inferiores = limites_inferiores
        self.particulas = []
        self.P_global = Particula(len(ueas))

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

    def iterar(self):
        for particula in self.particulas:
            particula.calcular_calidad(self.ueas)
            

            if particula.calidad < particula.calidad_mejor_posicion:
                particula.mejor_posicion = particula.posicion[:]
                particula.calidad_mejor_posicion = particula.calidad

            if particula.calidad <= self.P_global.calidad_mejor_posicion:
                print 'cum'
                self.P_global = deepcopy(particula)

            particula.actualizar_velocidad(self.P_global, self.ueas)
            particula.actualizar_posicion(self.ueas, self.limites_inferiores)

            self.P_global.intercambiar_ueas()

        print self.P_global.calidad

def main():
    ueas = cargar_datos()
    extender_seriacion(ueas)
    limites_inferiores = calcular_limites_inferiores(ueas)
    pso = PSO(ueas, 50, limites_inferiores)
    pso.inicializar_particulas()
    for x in xrange(1000):
        pso.iterar()

if __name__ == '__main__':
    main()

