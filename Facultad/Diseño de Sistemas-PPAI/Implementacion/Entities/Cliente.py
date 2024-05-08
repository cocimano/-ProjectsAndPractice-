import random


class Cliente:
    def __init__(self, dni, nombreCompleto, nroCelular):
        self.dni = dni
        self.nombreCompleto = nombreCompleto
        self.nroCelular = nroCelular

    def esCliente(self):
        return True

    def getNombre(self):
        return self.nombreCompleto

    def getDni(self):
        return self.dni
    
    def __str__(self):
        r = ''
        r += '{:<40}'.format("DNI: " + str(self.dni))
        r += '{:<40}'.format("Nombre y Apellido: " + self.nombreCompleto)
        r += '{:<40}'.format("Numero celular: " + str(self.nroCelular))
        return r


class GeneradorClientes:
    def obtenerClienteRandom(self):
        # Nombres aleatorios
        descNombres = ["Juan","Joaquin","Fabrizio", "Luciana","Matias","Mateo","Federico",
            "Santiago","Lucia","Valentina","Victoria", "Ana", "María","Pedro","Josefina",
            "Jose","Lucio","Patricia","Natalia"]
        # Apellidos aleatorios
        descApellidos = ["Sposetti","Gonzalez", "Rodriguez", "Lopez", "Martinez", 
            "Perez", "Gomez", "Sanchez", "Fernandez", "Torres", "Ramirez", "Hernandez", 
            "Garcia", "Silva", "Rojas", "Moreno", "Navarro", "Cruz", "Ortega", "Vargas", "Mendoza"]
        
        dni = random.randint(100000, 46000000)
        nombreCompleto = random.choice(descNombres) + " " + random.choice(descApellidos)
        nroCelular = random.randint(540000000000, 550000000000)

        # Creo objeto Cliente con datos random
        cliente = Cliente(dni, nombreCompleto, nroCelular)
        return cliente

def test():
    for i in range(10):
        cliente = GeneradorClientes().obtenerClienteRandom()
        print(cliente)
        #print("Get nombre: ", cliente.getNombre())

if __name__ == "__main__":
    test()