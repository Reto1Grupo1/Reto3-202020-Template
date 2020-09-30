"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidents_file = 'us_accidents_small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________








def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Buscar accidentes por fecha y severidad")
    print("4- Requerimento 2")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
            print("\nCargando información de crimenes ....")
        
            controller.loadData(cont, accidents_file)
            print('Crimenes cargados: ' + str(controller.accidentSize(cont)))
            print('Altura del arbol: ' + str(controller.indexHeight(cont)))
            print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
            print('Menor Llave: ' + str(controller.minKey(cont)))
            print('Mayor Llave: ' + str(controller.maxKey(cont)))
        
            print("La fecha no está registrada")
        

    elif int(inputs[0]) == 3:
        print("\nBuscando crimenes x grupo de Severity en una fecha: ")
        try:
            initialDate = input("Fecha (YYYY-MM-DD): ")
            severity= input("Severidad que desea consultar: ")
            numseverity = controller.getCrimesBySeverity(cont, initialDate,
                                                        severity)
            print("\nTotal de ofensas tipo: " + severity + " en esa fecha:  " +
                str(numseverity))
        except:
            print("La fecha es inválida.")

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 1 del reto 3: ")

    else:
        sys.exit(0)
sys.exit(0)
