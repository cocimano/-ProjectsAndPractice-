import random
from Implementacion.Utilidad import FechaYHora
from Implementacion.Entities.Encuesta import GeneradorEncuestas


class RespuestaDeCliente:
    def __init__(self, fechaEncuesta='', respuestaSeleccionada=None):
        self.fechaEncuesta = fechaEncuesta
        self.respuestaSeleccionada = respuestaSeleccionada

    def getValorRespuestaSeleccionada(self):
        return self.respuestaSeleccionada.getValorRta()

    def getDescripcionRespuestaSeleccionada(self):
        return self.respuestaSeleccionada.getDescripcionRta()

    def getRespuestaSeleccionada(self):
        return self.respuestaSeleccionada

    def getFechaEncuesta(self):
        return self.fechaEncuesta

    def __str__(self):
        r = ''
        r += '{:<50}'.format('Fecha de la Encuesta: ' + str(self.fechaEncuesta))
        r += '{:<30}'.format('Respuesta seleccionada: ' + str(self.respuestaSeleccionada))
        return r


class GeneradorRespuestasDeCliente:
    def generarRtasCliente(self, fechaEncuesta=FechaYHora.obtenerFechaHoraRandom(),
                           encuesta=GeneradorEncuestas().generarEncuestasAleatorias(1)[0]):
        rtasPosibles = []
        rtasGeneradas = []
        for pregunta in encuesta.getPreguntas():
            for rtaPosible in pregunta.getRespuestasPosibles():
                rtasPosibles.append(rtaPosible)
            rtasGeneradas.append(random.choice(rtasPosibles))
            rtasPosibles = []
        
        # Agrego al array las Respuestas del Cliente
        rtasDeCliente = []
        for rtaGenerada in rtasGeneradas:
            rtasDeCliente.append(RespuestaDeCliente(fechaEncuesta, rtaGenerada))

        return rtasDeCliente


def test():
    pass


if __name__ == '__main__':
    test()
