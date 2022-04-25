import os
from datetime import timedelta, date, datetime
import requests
#Exceciones propias
class FechaFueraDeRango(Exception):
    pass


def main():
    try:
        fecha_inicial = input("Ingrese la fecha inical así -> dd-MM-yyyy.\n"
                              "Por ejemplo: 20-08-2020.\n"
                              "Fecha Inicial -> ")
        fechaA = datetime.strptime(fecha_inicial, '%d-%m-%Y')
        print("Tu fecha inicial es: ")
        print(str(fechaA))
        fecha_final = input("Ingrese la fecha final así -> dd-MM-yyyy.\n "
                            "Por ejemplo: 20-08-2021.\n"
                            "Fecha Final -> ")
        fechaB = datetime.strptime(fecha_final, '%d-%m-%Y')
        print("Tu fecha final es: ")
        print(str(fechaB))
        total_dias_habiles = calculadora_dias_habiles(fechaA, fechaB)
        print("El total de dias habiles es -> " + str(total_dias_habiles))
    except ValueError:
        print("\n Formato de fecha incorrecto. Intente de nuevo")
    except FechaFueraDeRango:
        print("Una o mas fechas estan fuera de rango. Verifique la configuracion en el archivo limites.txt.txt o si desea no tener limites.txt, elimine el archivo.")
    return 0
#funcion de calculo principal
def calculadora_dias_habiles(fecha_inicial, fecha_final):
    #verificacion de limites. Para este ejemplo: Entre agosto de 2020 y agosto de 2021
    fuera_de_limites = verificarLimites(fecha_inicial, fecha_final)
    if not fuera_de_limites:
        raise FechaFueraDeRango()
    diasHabiles = 0
    dia_contador = fecha_inicial
    año_actual = dia_contador.year
    print(año_actual)
    festivos = cargar_lista_festivos(año_actual)
    while dia_contador<=fecha_final:
        if año_actual!=dia_contador.year:
            año_actual=dia_contador.year
            festivos = cargar_lista_festivos(año_actual)
        if dia_habil(dia_contador, festivos) == True:
            diasHabiles+=1
        dia_contador+=timedelta(1)
    return diasHabiles
#Verificacion de si un dia es habil o no
def dia_habil(dia, festivos):
    dia_formateado = dia.strftime('%d-%m-%Y')
    dia_semana = dia.weekday()
    if dia_semana == 5 or dia_semana == 6 or (dia_formateado in festivos):
        return False
    else:
        return True

#Conexion HTTP a la API
def cargar_lista_festivos(año):
    festivos = []
    hosting = "https://calendarific.com/api/v2/holidays?"
    api_key = "70accceb3d04c32bf63415e8b0b1daf56bd51bc6"
    pais = "CO"
    year = str(año)
    URL_api = hosting+"&api_key="+api_key+"&country="+pais+"&year="+year
    respuesta = requests.get(URL_api)
    jsonRespuesta = respuesta.json()
    for festivo in jsonRespuesta['response']['holidays']:
        if 'National holiday' in festivo['type']:
            festivos.append(datetime.strptime(festivo['date']['iso'],'%Y-%m-%d').strftime('%d-%m-%Y'))
    return festivos
#Verificacion de los limites en el archivo
def verificarLimites(fecha_inicial, fecha_final):
    if not os.path.exists('limites.txt'):
        return True
    archivo_limites = open('limites.txt')
    lineas = archivo_limites.readlines();
    limiteInf = datetime.strptime(lineas[0].replace('\n',''),'%d-%m-%Y')
    limiteSuperior = datetime.strptime(lineas[1].replace('\n',''),'%d-%m-%Y')
    if fecha_inicial<limiteInf or fecha_final > limiteSuperior:
        return False
    return True
main()
