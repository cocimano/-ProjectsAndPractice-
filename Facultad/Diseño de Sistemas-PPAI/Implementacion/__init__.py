# Este proyecto usa pipenv para el manejo de dependencias
# https://pypi.org/project/pipenv/
# Para instalar pipenv, correr el siguiente comando y agregar al PATH: 
# pip install pipenv
# C:\Users\usuario\AppData\Roaming\Python\Python38\Scripts
# Para instalar paquetes: pipenv install <paquete>
# Para instalar las dependencias del proyecto: pipenv install --dev

from Implementacion.PantallaConsultarEncuesta import PantallaConsultarEncuesta
from Implementacion.GestorConsultarEncuesta import GestorConsultarEncuesta
from Implementacion.Entities.RespuestaPosible import GeneradoRrespuestasPosibles
from Implementacion.Entities.Pregunta import GeneradorPreguntas
from Implementacion.Entities.Llamada import GeneradorLlamadas
from Implementacion.Entities.Encuesta import GeneradorEncuestas

from Implementacion.Persistencia.PersistenciaEncuesta import PersistenciaEncuesta
from Implementacion.Persistencia.PersistenciaLlamada import PersistenciaLlamada


def main():
    # os.system('cls')
    llamadasDb, encuestasDb = PersistenciaLlamada().materializar()

    pantalla = PantallaConsultarEncuesta()
    gestor = GestorConsultarEncuesta(llamadas=llamadasDb, encuestas=encuestasDb)

    pantalla.setGestor(gestor)
    gestor.setPantalla(pantalla)
    pantalla.opcionConsultarEncuesta(gestor)


if __name__ == "__main__":
    main()
