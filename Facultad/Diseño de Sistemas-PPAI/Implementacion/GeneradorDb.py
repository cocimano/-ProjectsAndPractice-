from Implementacion.Persistencia.PersistenciaEncuesta import PersistenciaEncuesta
from Implementacion.Persistencia.PersistenciaLlamada import PersistenciaLlamada
from Implementacion.Persistencia.PersistenciaCliente import PersistenciaCliente
from Implementacion.Persistencia.PersistenciaEstado import PersistenciaEstado

from Implementacion.Entities.RespuestaPosible import GeneradoRrespuestasPosibles
from Implementacion.Entities.Pregunta import GeneradorPreguntas
from Implementacion.Entities.Encuesta import GeneradorEncuestas
from Implementacion.Entities.Llamada import GeneradorLlamadas


def generarDb():
    CANTIDAD_LLAMADAS = 100

    # Obtener generadores
    generadorRtasPosibles = GeneradoRrespuestasPosibles()
    generadorPreguntas = GeneradorPreguntas(generadorRtasPosibles)
    generadorEncuestas = GeneradorEncuestas(generadorPreguntas)
    generadorLlamadas = GeneradorLlamadas()

    # Generar encuestas y llamadas
    encuestasRandom = generadorEncuestas.generarEncuestasAleatorias(CANTIDAD_LLAMADAS)
    for i in range(CANTIDAD_LLAMADAS):
        llamadaRandom = generadorLlamadas.generarLlamadaRandom(encuestasRandom[i], persistir=True)


def borrarDb():
    PersistenciaEncuesta().deleteAll()
    PersistenciaLlamada().deleteAll()
    PersistenciaCliente().deleteAll()
    PersistenciaEstado().deleteAll()


if __name__ == "__main__":
    generarDb()
    # borrarDb()
