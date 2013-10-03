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
		particula = Particula(len(self.ueas))
		# particula.posicion = posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
		# 								2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
		# 								5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
		# 								7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
		# 								9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
		# 								10, 1, 1, 4, 8, 9, 10 , 10, 11, 11,
		# 								7, 11]
		self.assertEqual(len(particula.posicion), len(self.ueas))
		self.assertEqual(len(particula.velocidad), len(self.ueas))
		for x in particula.posicion:
			self.assertTrue(1 <= x <= 18)
		for x in particula.velocidad:
			self.assertTrue(-3 <= x <= 3)

	def test_Particula_calcular_creditos_por_trimestre(self):
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
		particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
							5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10 , 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
	 	particula.calcular_calidad_EC()
	 	self.assertGreaterEqual(particula.calidad_EC, 0)
	 	self.assertEqual(particula.calidad_EC, particula.calidad)
	 	self.assertEqual(particula.calidad_EC, 0)	 	

	def test_Particula_calcular_calidad_RC(self):
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
	 	particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
							5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10 , 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
		particula.calcular_calidad_RC(self.ueas)
		self.assertGreaterEqual(particula.calidad_RC, 0)
	 	self.assertEqual(particula.calidad_RC, particula.calidad)
	 	self.assertEqual(particula.calidad_RC, 0)

	def test_Particula_calcular_calidad_NT(self):
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
		particula.posicion = [1, 1, 2, 1, 7, 1, 2, 4, 2, 8, 2,
							2, 3, 3, 11, 3, 4, 4, 4, 8, 8, 5,
							5, 6, 5, 7, 6, 8, 5, 6, 5, 5, 9,
							7, 7, 6, 6, 11, 10, 8, 8, 7, 7, 6,
							9, 11, 9, 9, 10, 9, 2, 9, 8, 10,
							10, 1, 1, 4, 8, 9, 10 , 10, 11, 11,
							7, 11]
		particula.calcular_creditos_por_trimestre(self.ueas)
		particula.calcular_calidad_NT()
		self.assertGreaterEqual(particula.calidad_NT, 0)
	 	self.assertEqual(particula.calidad_NT, particula.calidad)
	 	self.assertEqual(particula.calidad_NT, 0)







def main():
	unittest.main()

if __name__ == '__main__':
    main()