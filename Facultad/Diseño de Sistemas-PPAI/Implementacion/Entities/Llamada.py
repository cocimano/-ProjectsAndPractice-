from Implementacion.Entities.Cliente import GeneradorClientes
from Implementacion.Entities.CambioEstado import GeneradorCambiosEstado
from Implementacion.Entities.RespuestaDeCliente import GeneradorRespuestasDeCliente
from Implementacion.Entities.Encuesta import GeneradorEncuestas

from Implementacion.Iterator.IAgregado import IAgregado
from Implementacion.Iterator.IteradorRespuestaCliente import IteradorRespuestaCliente

import random
from datetime import datetime


class Llamada(IAgregado):
    def __init__(
            self, descripcionOperador, detalleAccionRequerida, encuestaEnviada, observacionAuditor,
            respuestasDeEncuesta=None, cambiosEstado=[], cliente=None, duracion=-1):
        self.descripcionOperador = descripcionOperador
        self.detalleAccionRequerida = detalleAccionRequerida
        self.encuestaEnviada = encuestaEnviada
        self.observacionAuditor = observacionAuditor

        self.respuestasDeEncuesta = respuestasDeEncuesta
        self.cambiosEstado = cambiosEstado
        self.cliente = cliente

        if duracion == -1:
            self.duracion = self.calcularDuracion()
        else:
            self.duracion = duracion

    def getEncuestaEnviada(self):
        return self.encuestaEnviada

    # Cálculo de la duración de la llamada a través de Cambio de Estado
    def calcularDuracion(self):
        cambioEstadoIniciada = None
        cambioEstadoFinalizada = None

        for i in range(len(self.cambiosEstado)):
            if self.cambiosEstado[i].esEstadoInicial():
                cambioEstadoIniciada = self.cambiosEstado[i]
            elif self.cambiosEstado[i].esUltimoEstado():
                cambioEstadoFinalizada = self.cambiosEstado[i]

        if len(self.cambiosEstado) > 0:
            duracion = cambioEstadoFinalizada.getFechaHoraInicio() - cambioEstadoIniciada.getFechaHoraInicio()
        else:
            duracion = 0

        return duracion

    def esDePeriodo(self, fechaInicio, fechaFin):
        for cambioEstado in self.cambiosEstado:
            if cambioEstado.esEstadoInicial():
                fechaHoraInicio = cambioEstado.getFechaHoraInicio()

        if fechaInicio <= fechaHoraInicio <= fechaFin:
            return True
        return False

    def obtenerFechaHoraInicio(self):
        for cambioEstado in self.cambiosEstado:
            if cambioEstado.esEstadoInicial():
                return cambioEstado.getFechaHoraInicio()

    def getDuracion(self):
        return self.duracion

    def getNombreClienteDeLlamada(self):
        return self.cliente.getNombre()

    def getDniCliente(self):
        return self.cliente.getDni()

    def getRespuestas(self):
        return self.respuestasDeEncuesta

    def crearIterador(self, elementos, filtros):
        return IteradorRespuestaCliente(elementos, filtros)

    def getRespuestasSeleccionadas(self):
        respuestasSeleccionadas = []

        iteradorRespuestasCliente = self.crearIterador(self.respuestasDeEncuesta, None)
        iteradorRespuestasCliente.primero()
        while not iteradorRespuestasCliente.haTerminado():
            respuestaDeEncuesta = iteradorRespuestasCliente.actual()
            if respuestaDeEncuesta is not None:
                respuestasSeleccionadas.append(respuestaDeEncuesta.getRespuestaSeleccionada())
            iteradorRespuestasCliente.siguiente()

        # Implementacion anterior al rediseño con iterator
        # for i in range(len(self.respuestasDeEncuesta)):
        #     respuestaDeEncuesta = self.respuestasDeEncuesta[i]
        #     respuestasSeleccionadas.append(respuestaDeEncuesta.getRespuestaSeleccionada())

        return respuestasSeleccionadas

    def getValoresRespuestasSeleccionadas(self):
        valoresRespuestasSeleccionadas = []

        iteradorRespuestasCliente = self.crearIterador(self.respuestasDeEncuesta, None)
        iteradorRespuestasCliente.primero()
        while not iteradorRespuestasCliente.haTerminado():
            respuestaDeEncuesta = iteradorRespuestasCliente.actual()
            if respuestaDeEncuesta is not None:
                valoresRespuestasSeleccionadas.append(respuestaDeEncuesta.getValorRespuestaSeleccionada())
            iteradorRespuestasCliente.siguiente()

        # Implementacion anterior al rediseño con iterator
        # for i in range(len(self.respuestasDeEncuesta)):
        #     respuestaDeEncuesta = self.respuestasDeEncuesta[i]
        #     valoresRespuestasSeleccionadas.append(respuestaDeEncuesta.getValorRespuestaSeleccionada())

        return valoresRespuestasSeleccionadas

    # region Métodos no usados
    def setDescripcionOperador(self):
        pass

    def setDuracion(self):
        pass

    def setEstadoActual(self):
        pass

    def tieneRta(self):
        pass
    # endregion

    def getLlamada(self):
        return self

    def getEstadoActual(self):
        for i in range(len(self.cambiosEstado)):
            if self.cambiosEstado[i].esUltimoEstado():
                return self.cambiosEstado[i].getNombreEstado()

    def getCliente(self):
        return self.cliente

    def getCambiosEstado(self):
        return self.cambiosEstado

    def __str__(self):
        r = ''
        r += '{:<50}'.format('Descripción del operador: ' + self.descripcionOperador + '\n')
        r += '{:<50}'.format('Acción requerida: ' + self.detalleAccionRequerida)
        r += '{:<40}'.format('Duración de la llamada: ' + str(self.duracion))
        r += '{:<30}'.format('Encuesta Enviada: ' + str(self.encuestaEnviada))
        r += '{:<40}'.format('Observación del Auditor: ' + str(self.observacionAuditor) + '\n')
        r += '{:<40}'.format('Cliente: ' + str(self.cliente))
        r += '\nRespuestas de Encuesta: \n'
        for respuesta in self.respuestasDeEncuesta:
            r += '- {:<30}'.format(str(respuesta))
            r += '\n'
        r += 'Cambios de estado: \n'
        for cambioEstado in self.cambiosEstado:
            r += '- {:<30}'.format(str(cambioEstado))
            r += '\n'
        return r


class GeneradorLlamadas:
    def __init__(self):
        pass

    def generarLlamadaRandom(self, encuesta=GeneradorEncuestas().generarEncuestasAleatorias(1)[0], persistir=False):
        desc = ['Ofrecimiento de reembolso o crédito para compensar cualquier cargo adicional.',
                'Asistencia técnica para resolver problemas de velocidad de conexión.',
                'Aclaración de las políticas de cancelación', 'Aclaración de las políticas de cambio de servicio.',
                'Actualización de servicios.']
        accionreq = ['Comunicar saldo.', 'Dar de baja tarjeta.', 'Denunciar un robo.']
        observAudi = ['Ninguna.', 'Incorrecto trato del operador al cliente.', 'Voz poco clara del operador.',
                      'El operador se demoró.',
                      'La respuesta que el operador brindó no resolvió el problema del cliente.']

        descripcionOperadorRandom = random.choice(desc)
        detalleAccionRequeridaRandom = random.choice(accionreq)
        encuestaEnviada = True
        observacionAuditor = random.choice(observAudi)
        clienteRandom = GeneradorClientes().obtenerClienteRandom()

        # Generar llamadas que sólo pasan por los estados de Iniciada -> Finalizada o
        # Iniciada ->  En Curso -> Finalizada
        cambiosEstadoRandom = GeneradorCambiosEstado().obtenerCambiosEstado(index=random.randint(0, 1))

        fechaHoraFin = datetime.now()
        for cambioEstado in cambiosEstadoRandom:
            if cambioEstado.esUltimoEstado():
                fechaHoraFin = cambioEstado.getFechaHoraInicio()
        rtasDeCliente = GeneradorRespuestasDeCliente().generarRtasCliente(fechaHoraFin, encuesta)

        # Creo el objeto Llamada 
        llamadaRandom = Llamada(
            descripcionOperadorRandom, detalleAccionRequeridaRandom, encuestaEnviada, observacionAuditor,
            respuestasDeEncuesta=rtasDeCliente, cliente=clienteRandom, cambiosEstado=cambiosEstadoRandom)
        if persistir:
            from Implementacion.Persistencia.PersistenciaEncuesta import PersistenciaEncuesta
            idsPreguntas = PersistenciaEncuesta().desmaterializarUna(encuesta)
            from Implementacion.Persistencia.PersistenciaLlamada import PersistenciaLlamada
            idLlamada = PersistenciaLlamada().desmaterializarUna(llamadaRandom, idsPreguntas)

        return llamadaRandom


def test():
    adhocLlamadas = GeneradorLlamadas()
    for i in range(5):
        print()
        llamadaRandom = adhocLlamadas.generarLlamadaRandom()
        print(llamadaRandom)


if __name__ == '__main__':
    test()
