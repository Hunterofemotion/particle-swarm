#-*- coding: utf-8 -*-
from Utilerias import *
from ParticleSwarm import *
import unittest

class TestUtilerias(unittest.TestCase):

	def setUp(self):
		self.ueas = cargar_datos()
       
	def testFoo(self):
		self.assertTrue(True)

	def test_Uea(self):
		self.uea = UEA(1, "Introducción a la Física", 4, [], 0)
		self.assertEqual(self.uea.clave, 1)
		self.assertEqual(self.uea.nombre, "Introducción a la Física")
		self.assertEqual(self.uea.creditos, 4)
		self.assertEqual(self.uea.ueas_requeridas, [])
		self.assertEqual(self.uea.creditos_requeridos, 0)

	def test_cargar_datos(self):
		self.assertGreater(len(self.ueas), 0)
		creditos_totales = 0
		for x in self.ueas.values():
			creditos_totales += x.creditos
		for x in self.ueas.values():
			self.assertIsInstance(x, UEA)
			self.assertTrue(x.clave <= len(self.ueas))
			self.assertGreater(x.clave, 0)
			self.assertGreater(x.creditos, 0)
			self.assertGreaterEqual(x.creditos_requeridos, 0)
			self.assertIsInstance(x.clave, int)
			self.assertIsInstance(x.nombre, basestring)
			self.assertIsInstance(x.creditos, int)
			self.assertIsInstance(x.ueas_requeridas, list)
			self.assertIsInstance(x.creditos_requeridos, int)
			self.assertLess(x.creditos_requeridos, creditos_totales)
			self.assertEqual(x.clave, self.ueas[x.clave].clave)
			self.assertGreaterEqual(len(x.ueas_requeridas), 0)

	def test_seriacion(self):
		for x in self.ueas.values():
			for clave_uea_requerida in x.ueas_requeridas:
				self.assertGreater(x.clave, clave_uea_requerida)
		self.assertIn(self.ueas[1].clave, self.ueas[7].ueas_requeridas)
		self.assertIn(self.ueas[4].clave, self.ueas[7].ueas_requeridas)
		self.assertIn(self.ueas[7].clave, self.ueas[8].ueas_requeridas)
		self.assertNotIn(self.ueas[4].clave, self.ueas[8].ueas_requeridas)
		self.assertIn(self.ueas[11].clave, self.ueas[17].ueas_requeridas)
		self.assertIn(self.ueas[14].clave, self.ueas[17].ueas_requeridas)
		#TODO Agregar más casos de prueba en la seriación


	def test_seriacion_extendida(self):
		extender_seriacion(self.ueas)
		for x in self.ueas.values():
			for clave_uea_requerida in x.ueas_requeridas:
				self.assertGreater(x.clave, clave_uea_requerida)
		self.assertIn(self.ueas[1].clave, self.ueas[7].ueas_requeridas)
		self.assertIn(self.ueas[4].clave, self.ueas[7].ueas_requeridas)
		self.assertIn(self.ueas[7].clave, self.ueas[8].ueas_requeridas)
		self.assertIn(self.ueas[4].clave, self.ueas[8].ueas_requeridas)
		self.assertIn(self.ueas[1].clave, self.ueas[8].ueas_requeridas)
		#TODO Agregar más casos de prueba en la seriación

	def test_calcular_limites_inferiores(self):
		extender_seriacion(self.ueas)
		limites_inferiores = calcular_limites_inferiores(self.ueas)
		for limite_inferior in limites_inferiores.values():
			self.assertLessEqual(limite_inferior, 11)
			self.assertGreater(limite_inferior, 0)
		for x in self.ueas.values():
			if x.ueas_requeridas != []:
				self.assertGreater(limites_inferiores[x.clave], 1)
		self.assertEqual(limites_inferiores[1], 1)
		self.assertEqual(limites_inferiores[4], 1)
		self.assertEqual(limites_inferiores[1], 1)
		self.assertEqual(limites_inferiores[7], 2)
		self.assertEqual(limites_inferiores[8], 3)
		self.assertEqual(limites_inferiores[10], 3)
		self.assertEqual(limites_inferiores[11], 2)
		self.assertEqual(limites_inferiores[14], 3)
		self.assertEqual(limites_inferiores[62], 1)
		#TODO Agregar mas casos de prueba

	def test_Particula(self):
		extender_seriacion(self.ueas)
		particula = Particula(len(self.ueas))

		self.assertEqual(len(particula.posicion), len(self.ueas))
		self.assertEqual(len(particula.velocidad), len(self.ueas))
		for x in particula.posicion:
			self.assertTrue(1 <= x <= 18)
		for x in particula.velocidad:
			self.assertTrue(-3 <= x <= 3)

	def test_Particula_calcular_creditos_por_trimestre(self):
		extender_seriacion(self.ueas)
		particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		creditos_totales = 0
		for x in self.ueas.values():
			creditos_totales += x.creditos
		creditos_totales_por_trimestres = 0
		for x in particula.trimestres.values():
			self.assertGreaterEqual(x, 0)
			self.assertLessEqual(x, creditos_totales)
		for y in particula.trimestres:
			creditos_totales_por_trimestres += particula.trimestres[y]
		self.assertEqual(creditos_totales, creditos_totales_por_trimestres)
		#Revisar la integridad de las llaves del diccionario
		for x in xrange(len(particula.trimestres)):
			self.assertGreaterEqual(x, 0)
		

	def test_Particula_calcular_calidad_EC(self):
		extender_seriacion(self.ueas)
		particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad,0)
		self.assertEqual(particula.calidad_EC,0)
		self.assertEqual(particula.calidad_RC,0)
		self.assertEqual(particula.calidad_NT,0)
		self.assertEqual(particula.calidad_SE,0)
	 	particula.calcular_calidad_EC()
	 	self.assertGreaterEqual(particula.calidad_EC, 0)
	 	self.assertEqual(particula.calidad_EC, particula.calidad)
		self.assertEqual(particula.calidad_RC,0)
		self.assertEqual(particula.calidad_NT,0)
		self.assertEqual(particula.calidad_SE,0)

		#Prueba con una solución óptima.
		particula = Particula(len(self.ueas))
		particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
							5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10, 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
	 	particula.calcular_calidad_EC()
	 	self.assertGreaterEqual(particula.calidad_EC, 0)
	 	self.assertEqual(particula.calidad_EC, particula.calidad)
	 	self.assertEqual(particula.calidad_EC, 0)	 	

	def test_Particula_calcular_calidad_RC(self):
		extender_seriacion(self.ueas)
 		particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad,0)
		self.assertEqual(particula.calidad_EC,0)
		self.assertEqual(particula.calidad_RC,0)
		self.assertEqual(particula.calidad_NT,0)
		self.assertEqual(particula.calidad_SE,0)
		particula.calcular_calidad_RC(self.ueas)
		self.assertGreaterEqual(particula.calidad_RC, 0)
	 	self.assertEqual(particula.calidad_RC, particula.calidad)
		self.assertEqual(particula.calidad_EC,0)
		self.assertEqual(particula.calidad_NT,0)
		self.assertEqual(particula.calidad_SE,0)

		#Prueba con una solución que no incluye al 5 trimestre.
		particula = Particula(len(self.ueas))
	 	particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 1,
							1, 6, 1, 7, 6, 8, 1, 6, 1, 1, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10, 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.trimestres.get(5, 0), 0)
		self.assertNotEqual(particula.trimestres.get(6, 0), 0)

		#Prueba con una solución que no incluye al 5 y 6 trimestre.
		particula = Particula(len(self.ueas))
	 	particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 1,
							1, 7, 1, 7, 7, 8, 1, 7, 1, 1, 9,
							7, 7, 7, 7, 11, 10, 8, 8, 7, 7, 7,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10, 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.trimestres.get(5, 0), 0)
		self.assertEqual(particula.trimestres.get(6, 0), 0)

		#Prueba con una solución que solo incluye al trimestre 2.
		particula = Particula(len(self.ueas))
	 	particula.posicion = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
							2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
							2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
							2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
							2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
							2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
							2, 2]
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.trimestres.get(1, 0), 0)
		self.assertEqual(particula.trimestres.get(3, 0), 0)
		self.assertEqual(particula.trimestres.get(4, 0), 0)
		self.assertEqual(particula.trimestres.get(20, 0), 0)
		self.assertEqual(particula.trimestres.get(6, 0), 0)
		self.assertNotEqual(particula.trimestres.get(2, 0), 0)

		#Prueba con una solución óptima.
		particula = Particula(len(self.ueas))
	 	particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
							5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10, 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
		particula.calcular_calidad_RC(self.ueas)
		self.assertGreaterEqual(particula.calidad_RC, 0)
	 	self.assertEqual(particula.calidad_RC, particula.calidad)
	 	self.assertEqual(particula.calidad_RC, 0)

	def test_Particula_calcular_calidad_NT(self):
		extender_seriacion(self.ueas)
	 	particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad,0)
		self.assertEqual(particula.calidad_EC,0)
		self.assertEqual(particula.calidad_RC,0)
		self.assertEqual(particula.calidad_NT,0)
		self.assertEqual(particula.calidad_SE,0)
		particula.calcular_calidad_NT()
		self.assertGreaterEqual(particula.calidad_NT, 0)
	 	self.assertEqual(particula.calidad_NT, particula.calidad)
		self.assertEqual(particula.calidad_EC,0)
		self.assertEqual(particula.calidad_RC,0)
		self.assertEqual(particula.calidad_SE,0)

		#Prueba con una solución óptima.
		particula = Particula(len(self.ueas))
		particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
							5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10, 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
		particula.calcular_calidad_NT()
		self.assertGreaterEqual(particula.calidad_NT, 0)
	 	self.assertEqual(particula.calidad_NT, particula.calidad)
	 	self.assertEqual(particula.calidad_NT, 0)

	def test_Particula_calcular_calidad_SE(self):
		extender_seriacion(self.ueas)
		particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad,0)
		self.assertEqual(particula.calidad_EC,0)
		self.assertEqual(particula.calidad_RC,0)
		self.assertEqual(particula.calidad_NT,0)
		self.assertEqual(particula.calidad_SE,0)
		particula.calcular_calidad_SE(self.ueas)
		self.assertGreaterEqual(particula.calidad_SE, 0)
	 	self.assertEqual(particula.calidad_SE, particula.calidad)
		self.assertEqual(particula.calidad_EC,0)
		self.assertEqual(particula.calidad_RC,0)
		
		#Prueba con una solución óptima.
		particula = Particula(len(self.ueas))
		particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
							5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10, 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
		particula.calcular_calidad_SE(self.ueas)
		self.assertGreaterEqual(particula.calidad_SE, 0)
	 	self.assertEqual(particula.calidad_SE, particula.calidad)
	 	self.assertEqual(particula.calidad_SE, 0)
	 	self.assertEqual(particula.ueas_violadas, [])

	def test_Particular_calcular_calidad(self):
		extender_seriacion(self.ueas)
		particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad, 0)
		particula.calcular_calidad(self.ueas)
		self.assertGreaterEqual(particula.calidad, 0)
		self.assertLessEqual(particula.calidad_EC, particula.calidad)
		self.assertLessEqual(particula.calidad_RC, particula.calidad)
		self.assertLessEqual(particula.calidad_NT, particula.calidad)
		self.assertLessEqual(particula.calidad_SE, particula.calidad)
		suma_de_calidades = 0	
		suma_de_calidades += particula.calidad_EC
		suma_de_calidades += particula.calidad_RC
		suma_de_calidades += particula.calidad_NT
		suma_de_calidades += particula.calidad_SE
		self.assertEqual(suma_de_calidades, particula.calidad)

	def test_Particula_actualizar_velocidad(self):
		extender_seriacion(self.ueas)
		particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad, 0)
		particula.calcular_calidad(self.ueas)
		P_global = Particula(len(self.ueas))
		particula.actualizar_velocidad(P_global, self.ueas)

		particula = Particula(len(self.ueas))
		particula.velocidad = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
							0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1]

		particula.posicion = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
							5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
							5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
							5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
							5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
							5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
							5, 5]

		particula.mejor_posicion = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10]

		P_global.posicion = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
							10, 10]

		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad, 0)
		particula.calcular_calidad(self.ueas)
		particula.actualizar_velocidad(P_global, self.ueas)
		particula.actualizar_posicion(self.ueas)

	def test_Particula_actualizar_posicion(self):
		extender_seriacion(self.ueas)
		particula = Particula(len(self.ueas))
		particula.calcular_creditos_por_trimestre(self.ueas)
		self.assertEqual(particula.calidad, 0)
		particula.calcular_calidad(self.ueas)
		P_global = Particula(len(self.ueas))
		posicion_previa = particula.posicion[:]

		particula.actualizar_velocidad(P_global, self.ueas)
		self.assertEqual(particula.posicion,posicion_previa)
		particula.actualizar_posicion(self.ueas)
		for x in xrange(len(self.ueas)):
			self.assertGreaterEqual(particula.velocidad[x], -3)
			self.assertLessEqual(particula.velocidad[x], 3)

			self.assertGreaterEqual(particula.posicion[x], 1)
			self.assertLessEqual(particula.posicion[x], 18)
			if posicion_previa[x] <= 15 and posicion_previa[x] >= 4:
				self.assertEqual(posicion_previa[x] + particula.velocidad[x], particula.posicion[x])

	def test_Particula_intercambiar_ueas(self):
		pass


class TestParticleSwarm(unittest.TestCase):

	def setUp(self):
		self.ueas = cargar_datos()
		extender_seriacion(self.ueas)

	def testBar(self):
		self.assertTrue(True)

	def test_PSO(self):
		limites_inferiores = calcular_limites_inferiores(self.ueas)
		numero_de_particulas = 50
		pso = PSO(self.ueas, numero_de_particulas, limites_inferiores)
		pso.inicializar_particulas()
		self.assertEqual(len(pso.particulas), numero_de_particulas)
		#Verificar que las partículas cumplan los límites inferiores
		for particula in pso.particulas:
			self.assertGreaterEqual(particula.posicion[1-1], 1)
			self.assertGreaterEqual(particula.posicion[4-1], 1)
			self.assertGreaterEqual(particula.posicion[1-1], 1)
			self.assertGreaterEqual(particula.posicion[7-1], 2)
			self.assertGreaterEqual(particula.posicion[8-1], 3)
			self.assertGreaterEqual(particula.posicion[10-1], 3)
			self.assertGreaterEqual(particula.posicion[11-1], 2)
			self.assertGreaterEqual(particula.posicion[14-1], 3)
			self.assertGreaterEqual(particula.posicion[62-1], 1)
		#Verificar que la mejor partícula del enjambre (global),
		#cumpla los límites inferiores
		self.assertGreaterEqual(pso.P_global.posicion[1-1], 1)
		self.assertGreaterEqual(pso.P_global.posicion[4-1], 1)
		self.assertGreaterEqual(pso.P_global.posicion[1-1], 1)
		self.assertGreaterEqual(pso.P_global.posicion[7-1], 2)
		self.assertGreaterEqual(pso.P_global.posicion[8-1], 3)
		self.assertGreaterEqual(pso.P_global.posicion[10-1], 3)
		self.assertGreaterEqual(pso.P_global.posicion[11-1], 2)
		self.assertGreaterEqual(pso.P_global.posicion[14-1], 3)
		self.assertGreaterEqual(pso.P_global.posicion[62-1], 1)
		#TODO Agregar más casos de prueba





def main():
	unittest.main()

if __name__ == '__main__':
    main()