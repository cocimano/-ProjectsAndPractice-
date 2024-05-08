from Implementacion.Utilidad import FechaYHora
from Implementacion.Entities.Pregunta import GeneradorPreguntas

from Implementacion.Iterator.IAgregado import IAgregado
from Implementacion.Iterator.IteradorPregunta import IteradorPregunta

import random
from datetime import datetime
import copy


class Encuesta(IAgregado):
    def __init__(self, descripcion='', fechaFinVigencia='', preguntas=None):
        self.descripcion = descripcion
        self.fechaFinVigencia = fechaFinVigencia
        self.preguntas = preguntas

    def armarEncuesta(self):
        pass

    def esEncuestaDeCliente(self):
        pass

    # Encuesta es Vigente si aún no superó la fechaHora actual
    def esVigente(self):
        if self.fechaFinVigencia > datetime.now():
            return True
        return False

    def getDescripcionEncuesta(self):
        return self.descripcion

    def __str__(self):
        r = ''
        r += '{:<50}\n'.format('Descripción de la encuesta: ' + self.descripcion)
        r += '{:<30}\n'.format(
            'Fecha de fin de vigencia: ' + datetime.strftime(self.fechaFinVigencia, "%d/%m/%Y %H:%M:%S"))
        r += 'Preguntas: \n'
        for pregunta in self.preguntas:
            r += '- {:<30}'.format(str(pregunta))
            r += '\n'
        return r

    def getPreguntas(self):
        return self.preguntas

    def crearIterador(self, preguntas, filtros):
        return IteradorPregunta(preguntas, filtros)

    def obtenerDescripcionesPreguntasDeRespuestasPosibles(self, respuestasPosibles):
        descripcionesPeguntas = []

        # Aplicacion patron iterator
        for i in range(len(respuestasPosibles)):
            respuestaPosible = respuestasPosibles[i]
            iteradorPreguntas = self.crearIterador(self.preguntas, respuestaPosible)
            iteradorPreguntas.primero()
            while not iteradorPreguntas.haTerminado():
                pregunta = iteradorPreguntas.actual()
                if pregunta is not None:
                    descripcionesPeguntas.append(pregunta.getDescripcion())
                    break
                iteradorPreguntas.siguiente()

        # Implementacion anterior a la aplicacion del patron iterator
        # for i in range(len(respuestasPosibles)):
        #     respuestaPosible = respuestasPosibles[i]
        #     for pregunta in self.preguntas:
        #         if pregunta.tieneRespuestaPosible(respuestaPosible):
        #             descripcionesPeguntas.append(pregunta.getDescripcion())
        #             break

        return descripcionesPeguntas


class GeneradorEncuestas:
    descrip = ['Encuesta de satisfaccion', 'Encuesta de calidad', 'Encuesta de servicio',
               'Encuesta de producto', 'Encuesta de atencion al cliente', 'Encuesta de atencion al publico']

    def __init__(self, adhocPreguntas=GeneradorPreguntas()):
        self.adhocPreguntas = adhocPreguntas

    def generarEncuestasAleatorias(self, cantidadEncuestas, adhocPreguntas=None):
        # Crear array de Encuestas 
        encuestas = cantidadEncuestas * [None]

        if adhocPreguntas is None:
            adhocPreguntas = GeneradorPreguntas()

        for i in range(cantidadEncuestas):
            descripcion = random.choice(self.descrip)
            randomDate = FechaYHora.obtenerFechaHoraRandom(endDate=datetime(2030, 12, 31))
            # Se debe generar 2 o 3 preguntas aleatorias para cada encuesta
            preguntasRandom = copy.deepcopy(adhocPreguntas.obtenerPreguntasAleatorias(random.randint(2, 3)))
            encuestas[i] = Encuesta(descripcion, randomDate, preguntasRandom)
        return encuestas

    # Mostrar las encuestas generadas
    def mostrar(self, vector):
        print('----Encuestas----')
        for i in range(len(vector)):
            print(vector[i])
            print('---------------------------------')


def main():
    n = int(input('Ingrese la cantidad de encuestas a generar: '))

    encuestasAdhoc = GeneradorEncuestas()
    encuestas = encuestasAdhoc.generarEncuestasAleatorias(n)
    encuestasAdhoc.mostrar(encuestas)


if __name__ == '__main__':
    main()
