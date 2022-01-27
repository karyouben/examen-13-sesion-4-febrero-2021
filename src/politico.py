# -*- coding: utf-8 -*-
'''
Created on 27 ene 2022

@author: willi
'''
from collections import namedtuple, Counter
import csv
import statistics
from parsers import *

Resultado = namedtuple('Resultado', 'fecha, provincia, ambito, votos, porcentaje_votos, puesto, porcentaje_abstencion')

def lee_archivo(fichero):
    with open(fichero,encoding = 'utf-8') as f:
        lector = csv.reader(f,delimiter = ";")
        next(lector)
        res = []
        for fecha, provincia, ambito, votos, porcentaje_votos, puesto, porcentaje_abstencion in lector:
            tupla = Resultado(parsea_fecha(fecha), provincia, ambito, int(votos), float(porcentaje_votos), int(puesto), float(porcentaje_abstencion))
            res.append(tupla)
    return res

def elecciones_mas_votos_emitidos(resultados,provincia,n=3):
    res = [t for t in resultados if t.provincia==provincia]
    lista_ordenada = sorted(res, key=lambda x:x.votos*100/x.procentaje_votos,reverse = True)[:n]
    return [(t.fecha,t.ambito) for t in lista_ordenada]
    
def ganadores_maxima_abstencion_por_provincias(resultados,ambito):
    dicc = agrupa_por_provincia(resultados, ambito)
    for clave, valor in dicc.items():
        dicc[clave]= max(valor, key = lambda x:x.porcentaje_abstencion)
    return dicc

def agrupa_por_provincia(resultados,ambito):
    dicc = {}
    for t in resultados:
        if t.ambito == ambito:
            clave = t.provincia
            if clave in dicc:
                dicc[clave].append(t)
            else:
                dicc[clave] = [t]
    return dicc
def agrupa_por_provincia_2(resultados,ambito):
    dicc = {}
    for t in resultados:
        if t.ambito == ambito or t.ambito ==None:
            clave = t.provincia
            if clave in dicc:
                dicc[clave].append(t)
            else:
                dicc[clave] = [t]
    return dicc
def provincia_menos_votantes_censados(resultados,ambito=None):
    dicc = agrupa_por_provincia_2(resultados, ambito)
    for clave, valor in dicc.items():
        dicc[clave]= min(valor,key = lambda x:(x.votos*100/x.procentaje_votos)*100/(100-x.porcentaje_abstencion))
    return dicc
    