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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dates'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer["Severity"]= om.newMap(omaptype='RBT',
                                      comparefunction=compareSeverity)
    return analyzer

# Funciones para agregar informacion al catalogo
def newSeverityEntry(severitygrp, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    seventry = {'Severity': None, 'lstSeverity': None}
    seventry['Severity'] = severitygrp
    seventry['lstSeverity'] = lt.newList('SINGLELINKED', compareSeverity)
    return seventry

def addAccident(analyzer, accident):
    """
    """

    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dates'], accident)
    return analyzer
    
def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    
    addDateIndex(datentry, accident)
    return map
def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    
    SeverityIndex = datentry['SeverityIndex']
    
    sevntry = m.get(SeverityIndex, accident['Severity'])
    if (sevntry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstSeverity'], accident)
        m.put(SeverityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(sevntry)
        lt.addLast(entry['lstSeverity'], accident)
    return datentry
def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': None, 'lstaccidents': None}
    entry['SeverityIndex'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


# ==============================
# Funciones de consulta
# ==============================
def accidentSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dates'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dates'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dates'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dates'])
def getCrimesByRangeCode(analyzer, initialDate, Severity):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    severitydate = om.get(analyzer['dates'], initialDate)
    if severitydate['key'] is not None:
        severitymap = me.getValue(severitydate)['SeverityIndex']
        numSeverity = m.get(severitymap, Severity)
        if numSeverity is not None:
            return m.size(me.getValue(numSeverity)['lstSeverity'])
        

# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def compareSeverity(keyname, Severity):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    seventry = me.getKey(Severity)
    if (keyname == seventry):
        return 0
    elif (keyname > seventry):
        return 1
    else:
        return -1