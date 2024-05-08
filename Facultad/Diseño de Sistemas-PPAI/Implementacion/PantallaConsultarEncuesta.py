# pip install PySimpleGUI
import PySimpleGUI as GUI
from datetime import datetime

class PantallaConsultarEncuesta:
    dateFormat = '%d/%m/%Y'

    # PySimpleGUI no permite utilizar 2 veces el mismo elemento de layout en dos windows distintos
    # Por lo que definimos un string y luego lo evaluamos para obtener cada vez un nuevo elemento
    def __init__(self,
                 gestorConsultarEncuesta=None,
                 btnConsultarEncuesta="GUI.Button('Consultar Encuesta')",
                 btnCancelar="GUI.Button('Cancelar')",
                 lblPeriodo="GUI.Text('Ingrese el periodo de tiempo que desea consultar. \\nEl formato es DD/MM/AAAA. \\nTambien puede seleccionar del calendario.', justification='center')",
                 lblFechaInicio="GUI.Text('Fecha Inicio: ')",
                 txtFechaInicio="GUI.InputText(datetime.strftime(self.fechaInicio, self.dateFormat), disabled=False, key='txtFI', size = (15, 1))",
                 calendarBtnFechaInicio="GUI.CalendarButton(button_text='Calendario', \
                     key='BtnFI', target='txtFI', format=self.dateFormat)",
                 lblFechaFin="GUI.Text('Fecha Fin: ')",
                 txtFechaFin="GUI.InputText(datetime.strftime(self.fechaFin, self.dateFormat), disabled=False, key='txtFF', size = (15, 1))",
                 calendarBtnFechaFin="GUI.CalendarButton(button_text='Calendario', \
                    key='BtnFI', target='txtFF', format=self.dateFormat)",
                 btnSiguiente="GUI.Button('Siguiente')",
                 btnVolver="GUI.Button('Volver')",
                 lblSeleccionLlamada="GUI.Text('Seleccione una llamada: ')",
                 lblSalida="GUI.Text('Seleccione una salida: ')",
                 radioBtnSalidaCSV="GUI.Radio('CSV', 'salida', key='radioBtnCSV', default=True)",
                 radioBtnSalidaImpresion="GUI.Radio('Impresion', 'salida', key='radioBtnImpresion')",
                 lblSeleccionImpresion="GUI.Text('Seleccione una impresora: ')",
                 comboImpresoras="GUI.Combo(impresoras, default_value=impresoras[0], key='comboImpresoras', readonly=True)"
                 ):
        self.gestor = gestorConsultarEncuesta
        self.btnConsultarEncuesta = btnConsultarEncuesta
        self.btnCancel = btnCancelar
        self.lblPeriodo = lblPeriodo
        self.lblFechaInicio = lblFechaInicio
        self.txtFechaInicio = txtFechaInicio
        self.calendarBtnFechaInicio = calendarBtnFechaInicio
        self.lblFechaFin = lblFechaFin
        self.txtFechaFin = txtFechaFin
        self.calendarBtnFechaFin = calendarBtnFechaFin
        self.btnSiguiente = btnSiguiente
        self.btnVolver = btnVolver
        self.lblSeleccionLlamada = lblSeleccionLlamada
        self.lblSalida = lblSalida
        self.radioBtnSalidaCSV = radioBtnSalidaCSV
        self.radioBtnSalidaImpresion = radioBtnSalidaImpresion
        self.lblSeleccionImpresion = lblSeleccionImpresion
        self.comboImpresoras = comboImpresoras

        self.fechaInicio = datetime(day=1, month=1, year=1990)
        self.fechaFin = datetime(day=1, month=1, year=2022)

    def setGestor(self, gestorConsultarEncuesta):
        self.gestor = gestorConsultarEncuesta

    # Opción para Consultar Encuesta (inicio del CU)
    def opcionConsultarEncuesta(self, gestor):
        self.gestor = gestor
        self.habilitarVentana()

    def habilitarVentana(self):
        layout = [
            [GUI.VPush()],
            [GUI.Push(), eval(self.btnConsultarEncuesta), GUI.Push()],
            [GUI.VPush()],
            [GUI.Push(), eval(self.btnCancel)]
        ]
        window = GUI.Window('Consultar Encuesta', layout,
                            resizable=False, size=(300, 100), finalize=True)

        # Asignacion de shortcuts a eventos (los eventos son tkinter keynames)
        window.bind('<Return>', 'Consultar Encuesta')
        window.bind('<Right>', 'Consultar Encuesta')
        window.bind('<Escape>', 'Cancelar')

        while True:
            event, values = window.read()

            if event == 'Consultar Encuesta':
                window.close()
                self.gestor.nuevaConsultaEncuesta()

            if event in (GUI.WIN_CLOSED, 'Cancelar'):
                break

        window.close()

    def pedirPeriodo(self):
        col1 = GUI.Column([[eval(self.lblFechaInicio)], [eval(self.lblFechaFin)]])
        col2 = GUI.Column([[eval(self.txtFechaInicio)], [eval(self.txtFechaFin)]])
        col3 = GUI.Column([[eval(self.calendarBtnFechaInicio)], [eval(self.calendarBtnFechaFin)]])
        dateFrame = GUI.Frame('Periodo', [
            [GUI.Push(), eval(self.lblPeriodo), GUI.Push()],
            [col1, col2, col3]
        ])
        layout = [
            [dateFrame],
            [GUI.Push(), eval(self.btnSiguiente), eval(self.btnCancel)]
        ]

        window = GUI.Window('Consultar Encuesta', layout, resizable=False, finalize=True)

        window.bind('<Return>', 'Siguiente')
        window.bind('<Right>', 'Siguiente')
        window.bind('<Escape>', 'Cancelar')

        while True:
            event, values = window.read()

            if event == 'Siguiente':
                try:
                    self.fechaInicio = datetime.strptime(values['txtFI'], self.dateFormat)
                    self.fechaFin = datetime.strptime(values['txtFF'], self.dateFormat).replace(hour=23, minute=59,
                                                                                                second=59)

                    if self.fechaInicio > self.fechaFin:
                        GUI.popup('La fecha de inicio debe ser anterior a la fecha de fin', title='Error')
                    else:
                        window.close()
                        self.tomarPeriodo()
                except ValueError:
                    GUI.popup('Debe seleccionar un periodo valido', title='Error')

            if event == GUI.WIN_CLOSED or event == 'Cancelar':
                break

        window.close()

    def tomarPeriodo(self):
        self.gestor.tomarPeriodo(self.fechaInicio, self.fechaFin)

    def pedirSeleccionLlamada(self, fechasLlamadasAMostrar):
        self.llamadasAMostrar = fechasLlamadasAMostrar

        toprow = ['Fila', 'Fecha Llamada']
        rows = []
        for i in range(len(self.llamadasAMostrar)):
            rows.append([str(i + 1), self.llamadasAMostrar[i]])

        tbl = GUI.Table(values=rows, headings=toprow,
                        key='tblLlamadas',
                        num_rows=10,
                        expand_x=True,
                        auto_size_columns=True,
                        display_row_numbers=False,
                        justification='center',
                        enable_events=True,
                        enable_click_events=True,
                        select_mode=GUI.TABLE_SELECT_MODE_BROWSE
                        )
        layout = [
            [GUI.Frame('Llamadas', [[eval(self.lblSeleccionLlamada)], [tbl]])],
            [GUI.Push(), eval(self.btnVolver), eval(self.btnSiguiente), eval(self.btnCancel)]
        ]

        window = GUI.Window('Consultar Encuesta', layout, resizable=True, finalize=True)

        window.bind('<Left>', 'Volver')
        window.bind('<Return>', 'Siguiente')
        window.bind('<Right>', 'Siguiente')
        window.bind('<Escape>', 'Cancelar')

        fila = None

        while True:
            event, values = window.read()

            if event == 'Volver':
                window.close()
                self.pedirPeriodo()

            if event == 'Siguiente':
                if fila is None:
                    GUI.popup('Debe seleccionar una llamada', title='Error')
                else:
                    window.close()
                    self.tomarSeleccionLlamada(fila)

            # La tabla genera el evento +CLICKED+ cuando se hace click en una celda
            # El valor del evento es ('-TABLE-', '+CLICKED+', (fila, columna))
            # Por lo tanto, se debe verificar que +CLICKED+ este en el evento,
            # Pero antes se debe verificar que no sea None, para no intentar iterarlo
            if event is not None and '+CLICKED+' in event:
                fila = event[2][0]

            if event == GUI.WIN_CLOSED or event == 'Cancelar':
                break

        window.close()

    # Flujo alternativo no hay llamadas de periodo
    def mostrarNoHayLlamadas(self):
        GUI.popup('No hay llamadas para el periodo seleccionado\nPor favor, seleccione otro periodo',
                  title='Consultar Encuesta')
        self.pedirPeriodo()

    def tomarSeleccionLlamada(self, indexLlamada):
        self.gestor.tomarSeleccionLlamada(indexLlamada)

    def pedirSeleccionSalida(self, nombreCliente, estadoActual, duracion, encuestaRealizada, preguntas):
        self.nombreCliente = nombreCliente
        self.estadoActual = estadoActual
        self.duracion = duracion
        self.encuestaRealizada = encuestaRealizada
        self.preguntas = preguntas

        toprow = ['Pregunta', 'Respuesta seleccionada']
        rows = []
        for i in range(len(preguntas)):
            rows.append(preguntas[i])

        tbl = GUI.Table(values=rows, headings=toprow,
                        key='tblPreguntas',
                        num_rows=3,
                        expand_x=True,
                        auto_size_columns=True,
                        display_row_numbers=False,
                        justification='left',
                        enable_events=True,
                        enable_click_events=True,
                        select_mode=GUI.TABLE_SELECT_MODE_NONE
                        )
        encuestaFrame = GUI.Frame('Encuesta', [
            [GUI.Text('Nombre cliente: {}'.format(nombreCliente))],
            [GUI.Text('Estado actual: {}'.format(estadoActual))],
            [GUI.Text('Duracion: {}'.format(duracion))],
            [GUI.Text('Encuesta realizada: {}'.format(encuestaRealizada))],
            [tbl]
        ], size=(900, 225))
        salidaFrame = GUI.Frame('Salida', [
            [eval(self.lblSalida), eval(self.radioBtnSalidaCSV), eval(self.radioBtnSalidaImpresion)]])
        layout = [
            [encuestaFrame],
            [salidaFrame],
            [GUI.Push(), eval(self.btnVolver), eval(self.btnSiguiente), eval(self.btnCancel)]
        ]

        window = GUI.Window('Consultar Encuesta', layout, resizable=False, finalize=True)

        window.bind('<Left>', 'Volver')
        window.bind('<Return>', 'Siguiente')
        window.bind('<Right>', 'Siguiente')
        window.bind('<Escape>', 'Cancelar')

        while True:
            event, values = window.read()

            if event == 'Siguiente':
                window.close()
                if values['radioBtnCSV']:
                    self.tomarSeleccionSalida('csv')
                elif values['radioBtnImpresion']:
                    self.tomarSeleccionSalida('imprimir')

            if event == 'Volver':
                window.close()
                self.pedirSeleccionLlamada(self.llamadasAMostrar)

            if event == GUI.WIN_CLOSED or event == 'Cancelar':
                break

        window.close()

    def tomarSeleccionSalida(self, seleccion):
        if seleccion == 'csv':
            GUI.popup('CSV Generado!', title='Consultar Encuesta')
            self.gestor.tomarSeleccionCSV()
        elif seleccion == 'imprimir':
            self.gestor.tomarSeleccionImpresion()

    def pedirSeleccionImpresora(self, impresoras):
        impresionFrame = GUI.Frame('Impresion', [
            [eval(self.lblSeleccionImpresion)],
            [eval(self.comboImpresoras)]
        ])

        layout = [
            [impresionFrame],
            [GUI.Push(), eval(self.btnVolver), eval(self.btnSiguiente), eval(self.btnCancel)]
        ]

        window = GUI.Window('Consultar Encuesta', layout, resizable=False, finalize=True)

        window.bind('<Left>', 'Volver')
        window.bind('<Return>', 'Siguiente')
        window.bind('<Right>', 'Siguiente')
        window.bind('<Escape>', 'Cancelar')

        while True:
            event, values = window.read()

            if event == 'Volver':
                window.close()
                self.pedirSeleccionSalida(self.nombreCliente, self.estadoActual, self.duracion, self.encuestaRealizada,
                                          self.preguntas)

            if event == 'Siguiente':
                window.close()
                self.tomarSeleccionImpresora(values['comboImpresoras'])

            if event == GUI.WIN_CLOSED or event == 'Cancelar':
                break

        window.close()

    def tomarSeleccionImpresora(self, nombreImpresora):
        self.gestor.imprimir(nombreImpresora)
