from Implementacion.Entities.RespuestaPosible import GeneradoRrespuestasPosibles

import random
import copy


class Pregunta:
    def __init__(self, preg='', resp=None):
        self.pregunta = preg
        self.respuestasPosibles = resp

    def getDescripcion(self):
        return self.pregunta

    def listarRespuestasPosibles(self):
        respuestasPosibles = []
        for i in range(len(self.respuestasPosibles)):
            respuestasPosibles.append(str(self.respuestasPosibles[i].getValorRta()))
        return respuestasPosibles

    def getRespuestasPosibles(self):
        return self.respuestasPosibles

    def tieneRespuestaPosible(self, respuestaPosibleAVerificar):
        tieneRespuestaPosible = False
        for respuestaPosibleDeEstaPregunta in self.respuestasPosibles:
            if respuestaPosibleDeEstaPregunta == respuestaPosibleAVerificar:
                tieneRespuestaPosible = True
                break
        return tieneRespuestaPosible

    def __str__(self):
        r = ''
        r += '{:<50}\n'.format('Descripción de la pregunta: ' + self.pregunta)
        respuestasPosibles = self.listarRespuestasPosibles()
        r += 'Respuestas posibles: '
        for respuestaPosible in respuestasPosibles:
            r += '{} '.format(respuestaPosible)
        return r


class GeneradorPreguntas:
    # Preguntas que se responden con Si o No
    preguntasRandomBool = [
        '¿Le gustó la atención?',
        '¿Nos recomendaría a otras personas?',
        '¿Recibiste una respuesta o solución a tu consulta o problema?',
        '¿Experimentaste alguna dificultad técnica o de comunicación durante la interacción?',
        '¿El personal de atención al cliente demostró conocimiento y competencia en su respuesta?'
    ]
    # Preguntas que se responden con cantidad numérica
    preguntasRandomNros = [
        'Del 1 al 10, ¿en cuánto nos calificaría?',
        'Del 1 al 10, ¿qué tan fácil fue contactar a nuestro servicio de atención al cliente?',
        'Del 1 al 10, ¿qué tan bien resolvimos tu consulta o problema?',
        'Del 1 al 10, ¿qué tan rápido fue el tiempo de respuesta de nuestro equipo de atención al cliente?'
    ]

    def __init__(self, respuestasPosibles=GeneradoRrespuestasPosibles()):
        self.respuestasPosibles = respuestasPosibles
        self.preguntas = self.generarPreguntas()

    def generarPreguntas(self):
        preguntas = []
        for pregunta in self.preguntasRandomBool:
            respuestas = copy.deepcopy(self.respuestasPosibles.getRtasSiNo())
            preguntas.append(Pregunta(pregunta, respuestas))
        for pregunta in self.preguntasRandomNros:
            respuestas = copy.deepcopy(self.respuestasPosibles.getRtas1Al10())
            preguntas.append(Pregunta(pregunta, respuestas))

        return preguntas

    def obtenerPreguntasAleatorias(self, cantidadPreguntas):
        preguntas = cantidadPreguntas * [None]

        for i in range(cantidadPreguntas):
            preguntaRandom = random.choice(self.preguntas)
            while preguntaRandom in preguntas:
                preguntaRandom = random.choice(self.preguntas)
            preguntas[i] = preguntaRandom

        return preguntas


def test():
    n = int(input('Ingrese la cantidad de preguntas a generar (2 o 3): '))
    while n < 2 or n > 3:
        n = int(input('Ingrese la cantidad de preguntas a generar (2 o 3): '))

    preguntas = GeneradorPreguntas().obtenerPreguntasAleatorias(n)
    print('----Preguntas----')
    for i in range(n):
        print(preguntas[i])
        print('---------------------------------')


if __name__ == '__main__':
    test()
