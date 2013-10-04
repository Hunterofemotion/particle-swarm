#-*- coding: utf-8 -*-
from random import randint
from random import randrange
import sys
class UEA(object):
    
    def __init__(self, clave, nombre, creditos, ueas_requeridas, creditos_requeridos):
        self.clave = clave
        self.nombre = nombre
        self.creditos = creditos
        self.ueas_requeridas = ueas_requeridas
        self.creditos_requeridos = creditos_requeridos

class Particula(object):
    __slots__ = ('posicion', 'velocidad', 'mejor_posicion', 'calidad_mejor_posicion', 'calidad',
        'calidad_EC', 'calidad_RC', 'calidad_SE', 'calidad_NT', 'ueas_violadas', 'trimestres', 'clip')
    def __init__(self, dimension):
        self.posicion = [randint(1, 18) for x in xrange(dimension)]
        self.velocidad = [randint(-3, 3) for x in xrange(dimension)]
        self.mejor_posicion = self.posicion[:]
        self.calidad_mejor_posicion = sys.maxint
        self.calidad = 0
        self.calidad_EC = 0
        self.calidad_RC = 0
        self.calidad_SE = 0
        self.calidad_NT = 0
        self.ueas_violadas = []
        self.trimestres = {}
        self.clip = lambda n, minn, maxn: max(min(maxn, n), minn)

    def actualizar_velocidad(self,P_global, ueas):
        f = 1 / 0.000001
        w = 0.7298
        for x in xrange(len(ueas)):
            alfa = randrange(0.7298*f, 1.49618*f)/f
            assert(0.7298 <= alfa < 1.49618)
            beta = randrange(0.7298*f, 1.49618*f)/f
            velocidad = w*self.velocidad[x] + \
            alfa*(self.mejor_posicion[x] - self.posicion[x]) + \
            beta*(P_global.posicion[x] - self.posicion[x])
            self.velocidad[x] = int(round(velocidad))
            self.velocidad[x] = self.clip(self.velocidad[x], -3, 3)

    def intercambiar_ueas(self):
        for q in self.ueas_violadas: 
            self.posicion[q[0]-1], self.posicion[q[1][0]-1] = self.posicion[q[1][0]-1], self.posicion[q[0]-1]

    def actualizar_posicion(self, ueas, limites_inferiores):
        for x in xrange(len(ueas)):
            self.posicion[x] += self.velocidad[x]
            self.posicion[x] = self.clip(self.posicion[x], 1, 18)
            if self.posicion[x] < limites_inferiores[x+1]:
                self.posicion[x] = limites_inferiores[x+1]


    def calcular_creditos_por_trimestre(self, ueas):
        for x in xrange(len(self.posicion)):
            uea_actual = ueas[x+1]
            self.trimestres[self.posicion[x]] = self.trimestres.get(self.posicion[x], 0) + uea_actual.creditos

    def calcular_calidad_EC(self):
        if self.trimestres.get(1, 0) == 0:
            self.calidad += 46
            self.calidad_EC += 46
        else:
            if self.trimestres.get(1, 0) > 46:
                diferencia = self.trimestres[1] - 46
                self.calidad += diferencia
                self.calidad_EC += diferencia

        for h in xrange(2, len(self.trimestres)+1):
            if self.trimestres.get(h, 0) > 60:
                diferencia = self.trimestres[h] - 60
                self.calidad += diferencia
                self.calidad_EC += diferencia

        for h in xrange(2,len(self.trimestres)):
            if self.trimestres.get(h, 0) == 0:
                if self.trimestres.get(h+1, 0) > 0:
                    self.calidad += 60
                    self.calidad_EC += 60

    def calcular_calidad_RC(self, ueas):
        for x in xrange(len(self.posicion)):
            uea_actual = ueas[x+1]
            if uea_actual.creditos_requeridos != 0:
                creditos_acumulados = 0
                for m in xrange(1,self.posicion[x-1]):
                    creditos_acumulados = creditos_acumulados + self.trimestres.get(m, 0)

                if creditos_acumulados < uea_actual.creditos_requeridos:
                    diferencia = uea_actual.creditos_requeridos - creditos_acumulados
                    self.calidad = self.calidad + diferencia
                    self.calidad_RC = self.calidad_RC + diferencia

    def calcular_calidad_NT(self):
        penalizacion = 0
        penalizacion = (max(self.posicion)-11)*2000
        self.calidad = self.calidad + penalizacion
        self.calidad_NT = self.calidad_NT + penalizacion

    def calcular_calidad_SE(self, ueas):
        for x in xrange(len(self.posicion)):
            uea_actual = ueas[x+1]
            if uea_actual.ueas_requeridas != [0]:
                ueas_relacionadas = [0, []]
                for clave_uea_seriada in uea_actual.ueas_requeridas:
                    if self.posicion[clave_uea_seriada-1] >= self.posicion[uea_actual.clave-1]:
                        if uea_actual.clave not in self.ueas_violadas:
                            ueas_relacionadas[0] = uea_actual.clave
                            self.calidad = self.calidad + 1
                            self.calidad_SE = self.calidad_SE + 1
                        ueas_relacionadas[1].append(clave_uea_seriada)
                if ueas_relacionadas[0] != 0:
                    self.ueas_violadas.append(ueas_relacionadas)

    def calcular_calidad(self, ueas):
        self.calidad = 0
        self.calidad_EC = 0
        self.calidad_RC = 0
        self.calidad_NT = 0
        self.calidad_SE = 0
        self.calcular_creditos_por_trimestre(ueas)
        self.calcular_calidad_EC()
        self.calcular_calidad_RC(ueas)
        self.calcular_calidad_NT()
        self.calcular_calidad_SE(ueas)
      

def extender_seriacion(ueas):
    for uea in ueas.values():
        revisar_seriacion(uea ,uea.ueas_requeridas , ueas)

def revisar_seriacion(uea, ueas_requeridas,ueas):
    if ueas_requeridas == []:
        return
    else:
        for x in ueas_requeridas:
            if x not in uea.ueas_requeridas:
                uea.ueas_requeridas.append(x)
            revisar_seriacion(uea, ueas[x].ueas_requeridas, ueas)

def cargar_datos():
    ueas = {}
    archivo = open("Seriacion_UEA_Creditos.txt", "r")
    datos = archivo.readlines()
    for registro in datos:
        linea = registro.split('-')
        clave = int(linea[0])
        nombre = linea[1]
        creditos = int(linea[2])
        ueas_requeridas = []
        for x in linea[3].split(';'):
            if int(x) != 0:
                ueas_requeridas.append(int(x))
        creditos_requeridos = int(linea[4])
        
        uea = UEA(clave, nombre, creditos, ueas_requeridas, creditos_requeridos)
        ueas[uea.clave] = uea
    return ueas

def calcular_limites_inferiores(ueas):
    limites_inferiores = {}
    for uea in ueas.values():
        if uea.ueas_requeridas == []:
            limites_inferiores[uea.clave] = 1
        else:
            limites_inferiores[uea.clave] = 2
    for n in xrange(2,19):
        calcular_limites(n, limites_inferiores, ueas)
    return limites_inferiores

def calcular_limites(n,limites_inferiores, ueas):
    for uea_actual in ueas.values():
        if uea_actual.ueas_requeridas !=[]:
            for clave_uea_seriada in uea_actual.ueas_requeridas:
                if uea_actual.creditos_requeridos < ueas[clave_uea_seriada].creditos_requeridos:
                    uea_actual.creditos_requeridos = ueas[clave_uea_seriada].creditos_requeridos
                if limites_inferiores[clave_uea_seriada] > n-1:
                    limites_inferiores[uea_actual.clave] = n+1