from Implementacion.Iterator.IAgregado import IAgregado
from Implementacion.Iterator.IteradorLlamada import IteradorLlamada
from Implementacion.Iterator.IteradorEncuesta import IteradorEncuesta

from datetime import datetime
import csv

# Librerias para impresion
# pip install win32printing
import win32print
# pip install pywin32
import win32api
from glob import glob


class GestorConsultarEncuesta():
    def __init__(self,
                 pantalla=None,
                 llamadas=[],
                 encuestas=[],
                 fechaInicioPeriodo=datetime.now(),
                 fechaFinPeriodo=datetime.now(),
                 llamadasDePeriodo=[],
                 nombreClienteDeLlamada='',
                 estadoLlamada=None,
                 duracionLlamada=0,
                 preguntasYRtasSeleccionadas=[],
                 descripcionEncuesta=''
                 ):
        self.pantalla = pantalla
        self.llamadas = llamadas
        self.encuestas = encuestas

        self.fechaInicioPeriodo = fechaInicioPeriodo
        self.fechaFinPeriodo = fechaFinPeriodo
        self.llamadasDePeriodo = llamadasDePeriodo
        self.nombreClienteDeLlamada = nombreClienteDeLlamada
        self.estadoLlamada = estadoLlamada
        self.duracionLlamada = duracionLlamada
        self.preguntasYRtasSeleccionadas = preguntasYRtasSeleccionadas
        self.descripcionEncuesta = descripcionEncuesta

    def setPantalla(self, pantallaConsultarEncuesta):
        self.pantalla = pantallaConsultarEncuesta

    def nuevaConsultaEncuesta(self):
        self.pantalla.pedirPeriodo()

    def tomarPeriodo(self, fechaInicio, fechaFin):
        self.fechaInicioPeriodo = fechaInicio
        self.fechaFinPeriodo = fechaFin
        self.buscarLlamadas()

    def crearIteradorLlamada(self, elem, filtros):
        return IteradorLlamada(elem, filtros)

    def crearIteradorEncuesta(self, elem, filtros):
        return IteradorEncuesta(elem, filtros)

    # Busco las Llamadas para el Período seleccionado y las almaceno
    def buscarLlamadas(self):
        self.llamadasDePeriodo = []

        # Aplicacion patron iterator
        iteradorLlamadas = self.crearIteradorLlamada(self.llamadas, [self.fechaInicioPeriodo, self.fechaFinPeriodo])
        iteradorLlamadas.primero()
        while not iteradorLlamadas.haTerminado():
            llamadaActual = iteradorLlamadas.actual()
            if llamadaActual is not None:
                self.llamadasDePeriodo.append(llamadaActual)
            iteradorLlamadas.siguiente()

        # Implementacion anterior al rediseño con iterator
        # for llamada in self.llamadas:
        #     if llamada.esDePeriodo(self.fechaInicioPeriodo, self.fechaFinPeriodo) and llamada.getEncuestaEnviada():
        #         self.llamadasDePeriodo.append(llamada)

        # Ordeno a través de la función 'lambda' por fechaHoraInicio
        # (tomando como parámetro cada llamada) y guardo en array las fechas
        self.llamadasDePeriodo.sort(key=lambda x: x.obtenerFechaHoraInicio())
        fechasLlamadas = []
        for llamada in self.llamadasDePeriodo:
            fechasLlamadas.append(datetime.strftime(llamada.obtenerFechaHoraInicio(), '%d/%m/%Y %H:%M:%S'))

        if len(fechasLlamadas) > 0:
            self.pantalla.pedirSeleccionLlamada(fechasLlamadas)
        else:
            self.pantalla.mostrarNoHayLlamadas()

    def buscarDatosLlamada(self, indexLlamada):
        self.nombreClienteDeLlamada = self.llamadasDePeriodo[indexLlamada].getNombreClienteDeLlamada()
        self.estadoLlamada = self.llamadasDePeriodo[indexLlamada].getEstadoActual()
        self.duracionLlamada = self.llamadasDePeriodo[indexLlamada].getDuracion()

    def buscarDatosRtas(self, indexLlamada):
        respuestasSeleccionadas = self.llamadasDePeriodo[indexLlamada].getRespuestasSeleccionadas()
        valoresRespuestasSeleccionadas = self.llamadasDePeriodo[indexLlamada].getValoresRespuestasSeleccionadas()
        return respuestasSeleccionadas, valoresRespuestasSeleccionadas

    # Busco datos de la llamada seleccionada
    def tomarSeleccionLlamada(self, indexLlamada):
        self.buscarDatosLlamada(indexLlamada)
        respuestasSeleccionadas, valoresRespuestasSeleccionadas = self.buscarDatosRtas(indexLlamada)
        self.preguntasYRtasSeleccionadas = []

        # Para saber qué Pregunta Respondió el Cliente:
        descripcionesPreguntas = []
        self.descripcionEncuesta = ''

        # Aplicacion patron iterator
        iteradorEncuestas = self.crearIteradorEncuesta(self.encuestas, None)
        iteradorEncuestas.primero()
        while not iteradorEncuestas.haTerminado():
            encuestaActual = iteradorEncuestas.actual()
            if encuestaActual is not None:
                descripcionesPreguntas = encuestaActual.obtenerDescripcionesPreguntasDeRespuestasPosibles(
                    respuestasSeleccionadas)
                if len(descripcionesPreguntas) > 0:
                    self.descripcionEncuesta = encuestaActual.getDescripcionEncuesta()
                    break
            iteradorEncuestas.siguiente()

        # Implementacion anterior al rediseño con iterator
        # for encuesta in self.encuestas:
        #     descripcionesPreguntas = encuesta.obtenerDescripcionesPreguntasDeRespuestasPosibles(
        #         respuestasSeleccionadas)
        #     if len(descripcionesPreguntas) > 0:
        #         self.descripcionEncuesta = encuesta.getDescripcionEncuesta()
        #         break

        for i in range(len(respuestasSeleccionadas)):
            self.preguntasYRtasSeleccionadas.append([descripcionesPreguntas[i], valoresRespuestasSeleccionadas[i]])

        self.pantalla.pedirSeleccionSalida(
            self.nombreClienteDeLlamada,
            self.estadoLlamada,
            self.duracionLlamada,
            self.descripcionEncuesta,
            self.preguntasYRtasSeleccionadas)

    def tomarSeleccionCSV(self):
        self.generarCsv()

    # Flujo alternativo impresion
    def obtenerImpresoras(self):
        # win32print.PRINTER_ENUM_LOCAL para enumerar impresoras locales
        # El segundo parametro es el servidor de impresoras. Como queremos las locales, pasamos None
        # El tercer parametro es el nivel de detalle. 1 es el minimo
        impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
        # El nombre de la impresora es el segundo elemento de la tupla
        return [impresora[2] for impresora in impresoras]

    def tomarSeleccionImpresion(self):
        self.pantalla.pedirSeleccionImpresora(self.obtenerImpresoras())

    def imprimir(self, nombreImpresora):
        # Create a temporal txt file to print
        fileDir = 'temp.txt'
        # HARDCODED
        f = open('temp.txt', 'w+t')

        f.write('{}, {}, {}\n'.format(self.nombreClienteDeLlamada, self.estadoLlamada, self.duracionLlamada))
        for i in range(len(self.preguntasYRtasSeleccionadas)):
            f.write('{}, {}\n'.format(self.preguntasYRtasSeleccionadas[i][0], self.preguntasYRtasSeleccionadas[i][1]))

        f.close()

        # Print the txt file
        win32print.SetDefaultPrinter(nombreImpresora)
        for f in glob(fileDir, recursive=True):
            win32api.ShellExecute(0, "print", fileDir, None, ".", 0)

        self.finCU()

    def generarCsv(self):
        row_list = [[self.nombreClienteDeLlamada, self.estadoLlamada, self.duracionLlamada]]
        for preguntaYRta in self.preguntasYRtasSeleccionadas:
            row_list.append(preguntaYRta)

        with open('temp.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

        self.finCU()

    def finCU(self):
        pass
