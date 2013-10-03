#-*- coding: utf-8 -*-
from random import randint
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
        'calidad_EC', 'calidad_RC', 'calidad_S', 'calidad_NT', 'ueas_violadas', 'trimestres')
    def __init__(self, dimension):
        self.posicion = [randint(1, 18) for x in xrange(dimension)]
        self.velocidad = [randint(-3, 3) for x in xrange(dimension)]
        self.mejor_posicion = self.posicion[:]
        self.calidad_mejor_posicion = sys.maxint
        self.calidad = 0
        self.calidad_EC = 0
        self.calidad_RC = 0
        self.calidad_S = 0
        self.calidad_NT = 0
        self.ueas_violadas = []
        self.trimestres = {}

    def calcular_creditos_por_trimestre(self, ueas):
        for i in xrange(1, 19):
            self.trimestres[i] = 0
        for x in xrange(len(self.posicion)):
            uea_actual = ueas[x+1]
            self.trimestres[self.posicion[x]] = self.trimestres[self.posicion[x]] + uea_actual.creditos

    def calcular_calidad_EC(self):
        self.calidad_EC = 0
        self.calidad = 0
        if self.trimestres[1] == 0:
            self.calidad = self.calidad + 46
            self.calidad_EC = self.calidad_EC + 46
        else:
            if self.trimestres[1] > 46:
                diferencia = self.trimestres[1] - 46
                self.calidad = self.calidad + diferencia
                self.calidad_EC = self.calidad_EC + diferencia
            # if trimestres[1] < 21 and trimestres[1] != 0:
            #     diferencia = 21 - trimestres[1]
            #     self.calidad = self.calidad + diferencia
            #     self.calidad_EC = self.calidad_EC + diferencia
        for h in xrange(2, len(self.trimestres)+1):
            if self.trimestres[h] > 60:
                diferencia = self.trimestres[h] - 60
                self.calidad = self.calidad + diferencia
                self.calidad_EC = self.calidad_EC + diferencia
            # if trimestres[h] < 21 and trimestres[h] != 0:
            #     diferencia = 21 - trimestres[h]
            #     self.calidad = self.calidad + diferencia
            #     self.calidad_EC = self.calidad_EC + diferencia

        for h in xrange(2,len(self.trimestres)):
            if self.trimestres[h] == 0:
                if self.trimestres[h+1] > 0:
                    self.calidad = self.calidad + 60
                    self.calidad_EC = self.calidad_EC + 60

    def calcular_calidad_RC(self, ueas):
        self.calidad_RC = 0
        self.calidad = 0
        for x in xrange(len(self.posicion)):
            uea_actual = ueas[x+1]
            if uea_actual.creditos_requeridos != 0:
                creditos_acumulados = 0
                for m in xrange(1,self.posicion[x-1]):
                    creditos_acumulados = creditos_acumulados + self.trimestres[m]

                if creditos_acumulados < uea_actual.creditos_requeridos:
                    diferencia = uea_actual.creditos_requeridos - creditos_acumulados
                    self.calidad = self.calidad + diferencia
                    self.calidad_RC = self.calidad_RC + diferencia
      

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