import random


class RespuestaPosible:
    def __init__(self, des='', val=''):
        self.descripcion = des
        self.valor = val

    # Obtener atributos de RespuestaPosible
    def getDescripcionRta(self):
        return self.descripcion
    
    def getValorRta(self):
        return self.valor
    
    def __str__(self):
        r = ''
        r += '{:<50}'.format('Descripción de la respuesta: ' + self.descripcion)
        r += '{:<30}'.format('Valor de la respuesta: ' + str(self.valor))
        return r


# La clase adhoc es una clase auxiliar que se utiliza para generar respuestas posibles aleatorias
# para las preguntas de la encuesta
class GeneradoRrespuestasPosibles:
    def __init__(self):
        self.respuestas1Al10 = self.generarRespuestas1Al10()
        self.respuestasSiNo = self.generarRespuestasSiNo()

    # Respuestas a preguntas que se pueden responder con valor del 1 al 10
    def generarRespuestas1Al10(self):
        descrip = '1 al 10'
        rtasPosibles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # Agrego al array las respuestas posibles (del 1 al 10)
        respuestas = []
        for rtaPosible in rtasPosibles:
            respuestas.append(RespuestaPosible(descrip, rtaPosible))
        return respuestas
    
    # Respuestas a preguntas que se pueden responder con valor Si o No
    def generarRespuestasSiNo(self):
        descrip = 'Si/No'
        rtas = ['Si', 'No']
        # Agrego al array las respuestas posibles (Si, No)
        respuestas = []
        for rta in rtas:
            respuestas.append(RespuestaPosible(descrip, rta))
        return respuestas
    
    # Obtener las respuestas del 1 al l0
    def getRtas1Al10(self):
        return self.respuestas1Al10
    
    # Obtener las respuestas Si o No
    def getRtasSiNo(self):
        return self.respuestasSiNo

def main():
    adhocRespuestaPosible = GeneradoRrespuestasPosibles()

    rtas1Al10 = adhocRespuestaPosible.generarRespuestas1Al10()
    # Muestro respuestas del 1 al 10
    for rta1Al10 in rtas1Al10:
        print(rta1Al10)
    rtasSiNo = adhocRespuestaPosible.generarRespuestasSiNo()
    # Muestro respuestas Si o No
    for rtaSiNo in rtasSiNo:
        print(rtaSiNo)

if __name__ == '__main__':
    main()