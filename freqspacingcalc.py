#Some script I made to calculate which frequencies were available by calculating the current used frequencies based on the existing radio links.
def calculaespacio(name, Histring, Lowstring, spacingstring):
    if spacingstring.replace('.','').isnumeric():    
        spacing = float(spacingstring)
        a = spacing / 2
    else:
        while (not spacingstring.replace('.','').isnumeric()):
            spacingstring = input('Error en el spacing del enlace. Escriba el spacing del enlace ' + name + ' (SOLO NUMEROS).\n')
            if spacingstring.replace('.','').isnumeric():
                spacing = float(spacingstring)
                a = spacing / 2
    if Histring.replace('.','').isnumeric():
        HiHi = float(Histring) + a
        HiLow = float(Histring) - a
    else:
        while (not Histring.replace('.','').isnumeric()):
            Histring = input('Error en el canal HI del enlace. Escriba el canal HI del enlace ' + name + ' (SOLO NUMEROS).\n')
            if Histring.replace('.','').isnumeric():
                HiHi = float(Histring) + a
                HiLow = float(Histring) - a
    if Lowstring.replace('.','').isnumeric():
        LowHi = float(Lowstring) + a
        LowLow = float(Lowstring) - a
    else:
        while (not Lowstring.replace('.','').isnumeric()):
            Lowstring = input('Error en el canal LO del enlace. Escriba el canal LOW del enlace ' + name + ' (SOLO NUMEROS).\n')
            if Lowstring.replace('.','').isnumeric():
                LowHi = float(Lowstring) + a
                LowLow = float(Lowstring) - a
    return HiHi, HiLow, LowHi, LowLow

def compararfreq(main, enlaces):
    for link in enlaces:
        interferencia = False
        if (link['HiHivalue'] >= main['HiLowvalue'] and link['HiHivalue'] <= main['HiHivalue']) or (link['HiLowvalue'] >= main['HiLowvalue'] and link['HiLowvalue'] <= main['HiHivalue']):
            print('Solapamiento en canales HI:')
            print('El canal HI del enlace ' + link['nombre'] + ' ('+ str(link['HiLowvalue']) + '-' + str(link['HiHivalue']) + ') ' + ' interfiere con la configuracion deseada.')
            print ('Configuracion deseada: ' + str(main['HiLowvalue']) + '-' + str(main['HiHivalue']))
            interferencia = True
        if (link['LowHivalue'] >= main['LowLowvalue'] and link['LowHivalue'] <= main['LowHivalue']) or (link['LowLowvalue'] >= main['LowLowvalue'] and link['LowLowvalue'] <= main['LowHivalue']):
            print('Solapamiento en canales LOW:')
            print('El canal LOW del enlace ' + link['nombre'] + ' ('+ str(link['LowLowvalue']) + '-' + str(link['LowHivalue']) + ') ' + ' interfiere con la configuracion deseada.')
            print ('Configuracion deseada: ' + str(main['LowLowvalue']) + '-' + str(main['LowHivalue']))
            interferencia = True
        if (link['HIfreq'] == main['HIfreq']) or (link['LOfreq'] == main['LOfreq']):
            print('Solapamientos de canales; el enlace ' + link['nombre'] + ' posee el mismo canal deseado configurado:')
            print('Canal HI: ' + link['HIfreq'])
            print('Canal LO: ' + link['LOfreq'])
            interferencia = True
        if not interferencia:
            print('No se encontro solapamiento entre ' + main['nombre'] + ' y ' + link['nombre'] + ' (configuracion de ' + link['nombre'] + ': ' + str(link['LowLowvalue']) + '-' + str(link['LowHivalue']) + '; ' + str(link['HiLowvalue']) + '-' + str(link['HiHivalue']) + ')')
    return

enlacemain = {}

print('TODAS LAS UNIDADES A USAR SON EN MHz!!!\n')

#Parametros iniciales
var_input = input('Escriba el nombre del enlace a analizar: \n')
enlacemain['nombre'] = var_input
var_input = input('Escriba la frecuencia HI del enlace: \n')
enlacemain['HIfreq'] = var_input
var_input = input('Escriba la frecuencia LO del enlace: \n')
enlacemain['LOfreq'] = var_input
var_input = input('Escriba el spacing de canal que desea utilizar: \n')
enlacemain['spacing'] = var_input
enlacemain['HiHivalue'], enlacemain['HiLowvalue'], enlacemain['LowHivalue'], enlacemain['LowLowvalue'] = calculaespacio(enlacemain['nombre'], enlacemain['HIfreq'], enlacemain['LOfreq'], enlacemain['spacing'])

#Para comparar con otros enlaces
enlaces = []
one_more = 'y'
while ('y' in one_more):
    nuevo_enlace = {}
    var_input = input('Escriba el nombre del proximo enlace: \n')
    nuevo_enlace['nombre'] = var_input
    var_input = input('Escriba la frecuencia HI del enlace ' + nuevo_enlace['nombre']+ ':\n')
    nuevo_enlace['HIfreq'] = var_input
    var_input = input('Escriba la frecuencia LO del enlace ' + nuevo_enlace['nombre'] + ':\n')
    nuevo_enlace['LOfreq'] = var_input
    var_input = input('Escriba el spacing de canal del enlace ' + nuevo_enlace['nombre'] + ':\n')
    nuevo_enlace['spacing'] = var_input
    nuevo_enlace['HiHivalue'], nuevo_enlace['HiLowvalue'], nuevo_enlace['LowHivalue'], nuevo_enlace['LowLowvalue'] = calculaespacio(nuevo_enlace['nombre'], nuevo_enlace['HIfreq'], nuevo_enlace['LOfreq'], nuevo_enlace['spacing'])
    enlaces.append(nuevo_enlace)
    var_input = input('Desea agregar otro enlace para comparar?(y/n)\n')
    one_more = var_input

#Se comparan los enlaces
compararfreq(enlacemain, enlaces)
