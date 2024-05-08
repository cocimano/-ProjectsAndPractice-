from datetime import datetime, timedelta
import random


def obtenerFechaHoraRandom(startDate=datetime(day=1, month=1, year=1990), endDate=datetime(day=1, month=1, year=2022)):
    # Calcular el rango de fechas
    dateRange = endDate - startDate

    # Generar un numero aleatorio en el rango
    randomDays = random.randint(0, dateRange.days)

    # Agregar el numero aleatorio de dias
    randomDate = startDate + timedelta(days=randomDays)

    # Agregar hora, minutos y segundos random
    randomDate = randomDate + timedelta(seconds=random.randint(1, 59), minutes=random.randint(1, 59),
                                        hours=random.randint(1, 23))

    return randomDate
