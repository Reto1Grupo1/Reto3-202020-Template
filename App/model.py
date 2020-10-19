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
    analyzer['dates'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    analyzer["Severity"]= om.newMap(omaptype='BST',
                                      comparefunction=compareSeverity)
    analyzer["Llaves"]=om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    analyzer["Horas"]=om.newMap(omaptype='BST',
                                      comparefunction=compareHours)
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

def addFecha(analyzer,accident):
    key=accident["Start_Time"][0:10]
    if om.contains(analyzer["Llaves"],key)==False:
        Listvalues=lt.newList("ARRALIST",compareDates)
        lt.addFirst(Listvalues,accident)
        om.put(analyzer["Llaves"],key,Listvalues)
    else:
        Lista=om.get(analyzer["Llaves"],key)
        lt.addLast(Lista["value"],accident)
        NewValue=Lista["value"]
        om.put(analyzer["Llaves"],key,NewValue)

def addHora(analyzer,accident):
    key=accident["Start_Time"][11:15]
    if om.contains(analyzer["Horas"],key)==False:
        Listvalues=lt.newList("ARRALIST",compareDates)
        lt.addFirst(Listvalues,accident)
        om.put(analyzer["Horas"],key,Listvalues)
    else:
        Lista=om.get(analyzer["Horas"],key)
        lt.addLast(Lista["value"],accident)
        NewValue=Lista["value"]
        om.put(analyzer["Horas"],key,NewValue)

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
    print(severitydate['key'])
    if severitydate['key'] is not None:
        severitymap = me.getValue(severitydate)['SeverityIndex']
        numSeverity = m.get(severitymap, Severity)
        if numSeverity is not None:
            return m.size(me.getValue(numSeverity)['lstSeverity'])


def requerimiento3(analyzer,InitialDate,FinalDate):
    
    Initial=str(InitialDate)
    Final=str(FinalDate)
    yearI=Initial[0:4]
    monthI=Initial[5:7]
    dayI=Initial[8:10]
    yearF=Final[0:4]
    monthF=Final[5:7]
    dayF=Final[8:10]
    Total=0
    ListSeveridad=[]
    for year in range(int(yearI),int(yearF)+1):
        for month in range(1,13):
            if month < 10:
                month="0"+str(month)
            for day in range(1,32):
                if day < 10:
                    day="0"+str(day)
                fecha=str(year)+str(month)+str(day)
                key=str(year)+"-"+str(month)+"-"+str(day)
                if int(yearI+monthI+dayI)<= int(fecha) <= int(yearF+monthF+dayF):
                        valor=om.contains(analyzer["Llaves"],key)
                        if valor!=False:
                            valor=om.get(analyzer["Llaves"],key)
                            o=valor["value"]
                            CantidadA=int(lt.size(o))
                            Total=CantidadA+Total
                            for i in range(1,int(CantidadA)+1):
                                Causa=lt.getElement(valor["value"],i)
                                Severidad=Causa["Severity"]
                                ListSeveridad.append(Severidad)

    for j in range(0,len(ListSeveridad)):
        numbd=ListSeveridad.count(ListSeveridad[j])
        mayor=0
        if numbd>mayor:
            mayor=numbd
            Sev=ListSeveridad[j]
    Resultado=(Sev,Total)
    return Resultado


def GetAccidentsBeforeDate(analyzer,BeforeDate):
    
    BeforeDateYear="201"+str(BeforeDate[3])
    BeforeDateMonth=str(BeforeDate[5])+str(BeforeDate[6])
    BeforeDateDay=str(BeforeDate[8])+str(BeforeDate[9])
    MinDate=om.minKey(analyzer["Llaves"])
    
    if BeforeDateDay=="01":
        if BeforeDateMonth=="05" or BeforeDateMonth=="07" or BeforeDateMonth=="08" or BeforeDateMonth=="12":
            BeforeDateDay="30"
            BeforeDateMonth=(str(BeforeDateMonth[0]))+(str(int(BeforeDateMonth[1])-1))
        elif BeforeDateMonth=="02" or BeforeDateMonth=="04" or BeforeDateMonth=="06" or BeforeDateMonth=="09" or BeforeDateMonth=="11":
            BeforeDateDay="31"
            BeforeDateMonth=(str(BeforeDateMonth[0]))+(str(int(BeforeDateMonth[1])-1))
        elif BeforeDateMonth=="10":
            BeforeDateDay="30"
            BeforeDateMonth="09"
        elif BeforeDateMonth=="03":
            if BeforeDateYear=="2016":
                BeforeDateDay="29"
            else:
                BeforeDateDay="28"
            BeforeDateMonth="02"
        else:
            BeforeDateDay="31"
            BeforeDateMonth="12"
            BeforeDateYear="201"+str(int(BeforeDateYear[3])-1)
    elif BeforeDateDay[0]=="0":
        BeforeDateDay=str(BeforeDateDay[0])+str(int(BeforeDateDay[1])-1)
    elif BeforeDateDay=="10":
        BeforeDateDay="09"
    else:
        BeforeDateDay=str(int(BeforeDateDay)-1)

    
    MaxDate=BeforeDateYear+"-"+BeforeDateMonth+"-"+BeforeDateDay
    Dates=(om.keys(analyzer["Llaves"],MinDate,MaxDate))

    print(MinDate)
    print(MaxDate)

    TotalAccidents=0
    MaxAccidents=0
    MostAccidentsDate="YYYY-MM-DD"
    
    for i in range(1,(lt.size(Dates)+1)):
        Date=lt.getElement(Dates,i)
        Pair=om.get(analyzer["Llaves"],Date)
        Accidents=me.getValue(Pair)
        Number=lt.size(Accidents)
        TotalAccidents=TotalAccidents+Number
        if Number>MaxAccidents:
            MaxAccidents=Number
            MostAccidentsDate=Date
            
    Retorno=lt.newList("SINGLE_LINKED",compareIds)
    lt.addLast(Retorno,TotalAccidents)
    lt.addLast(Retorno,MostAccidentsDate)
    print("Retorno:")
    print(Retorno)
    print("TotalAccidents:")
    print(lt.getElement(Retorno,1))
    print("MostAccidentsDate:")
    print(lt.getElement(Retorno,2))
    return Retorno


def AccidentesPorHora(analyzer,HoraInicial,HoraFinal):
    print("funciona 2")
    HoraInicial=AproximacionHora(HoraInicial)
    HoraFinal=AproximacionHora(HoraFinal)
    print("funciona 3")
    ListaHoras=om.keys(analyzer["Horas"],HoraInicial,HoraFinal)
    Severity1=0
    Severity2=0
    Severity3=0
    Severity4=0
    print("funciona 4")
    for i in range(1,(lt.size(ListaHoras)+1)):
        Hora=lt.getElement(ListaHoras,i)
        Pareja=om.get(analyzer["Horas"],Hora)
        Accidente1=me.getValue(Pareja)
        for j in range(1,(lt.size(Accidente1)+1)):
            Accidente=lt.getElement(Accidente1,j)
            if Accidente["Severity"]=="1":
                Severity1+=1
            elif Accidente["Severity"]=="2":
                Severity2+=1
            elif Accidente["Severity"]=="3":
                Severity3+=1
            else:
                Accidente["Severity"]=="4"
                Severity4+=1
    print("funciona 5")
    Total=Severity1+Severity2+Severity3+Severity4
    Retorno=lt.newList("SINGLE_LINKED",compareIds)
    lt.addLast(Retorno,Severity1)
    lt.addLast(Retorno,Severity2)
    lt.addLast(Retorno,Severity3)
    lt.addLast(Retorno,Severity4)
    lt.addLast(Retorno,Total)
    print("funciona 6")
    return Retorno


def AproximacionHora(hora):
    horas=hora[0]+hora[1]
    minutos=hora[3]+hora[4]
    if int(minutos)>=0 and int(minutos)<=15:
        hora=horas+":00"
    elif int(minutos)>=16 and int(minutos)<=45:
        hora=horas+":30"
    else:
        if horas[0]=="0" and horas!="09":
            horas="0"+str(int(horas[1]+1))
        elif horas=="09":
            horas="10"
        else:
            horas=str(int(horas)+1)
        hora=horas+":00"
    return hora

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
def compareHours(hour1, hour2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
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