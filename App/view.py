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
from DISClib.ADT import orderedmap as od
from App import controller
assert config
import datetime

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
    print("4- Conocer los accidentes anteriores a una fecha")
    print("5- Conocer los accidentes en un rango de fechas")
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
            print(type(initialDate))
            severity= input("Severidad que desea consultar: ")
            numseverity = controller.getCrimesBySeverity(cont, initialDate,
                                                        severity)
            print("\nTotal de ofensas tipo: " + severity + " en esa fecha:  " +
                str(numseverity))
        except:
            print("La fecha es inválida.")
            

    elif int(inputs[0]) == 5:
        InitialDate=input("Ingrese una fecha inicial de la forma YYYY-MM-DD: ")
        FinalDate=input("Ingrese una fecha final de la forma YYYY-MM-DD: ")
        try:
            fecha1=int(str(InitialDate[0:4])+str(InitialDate[5:7])+str(InitialDate[8:10]))
            fecha2=int(str(FinalDate[0:4])+str(FinalDate[5:7])+str(FinalDate[8:10]))
            if  9<len(InitialDate)<11  and 9<len(FinalDate)<11 :
                a=controller.requerimiento3(cont,InitialDate,FinalDate)
                print("La cantidad de acidentes que sucedieron durante las fechas "+InitialDate+" y "+FinalDate+" son "+str(a[1])+" y el mayor tipo de severidad que sucedio fue "+ str(a[0]) )
        except:
            print("La fecha es Invalida")


    elif int(inputs[0]) == 4:
        BeforeDate=input("Fecha (YYYY-MM-DD): ")
        try:
            Retorno=controller.GetAccidentsBeforeDate(cont,BeforeDate)
            print("Total de accidentes antes de la fecha: "+str(lt.getElement(Retorno,1)))
            
            print("---------------")
            print("Dia con mas accidentes: "+str(lt.getElement(Retorno,2)))
            print("---------------")
        except:
            print("La fecha es invalida")


    else:
        sys.exit(0)
sys.exit(0)
