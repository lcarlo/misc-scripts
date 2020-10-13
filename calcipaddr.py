# Funcion que obtiene la mascara en formato decimal.
def get_ddn_mask(num_mask):
    if num_mask >= 8:
        first_octet = '255'
    else:
        first_octet = getpowerof2(num_mask)
    sec_octet = '0'
    third_octet = '0'
    fourth_octet = '0'
    if num_mask >= 16:
        sec_octet = '255'
    elif num_mask > 8:
        sec_octet = getpowerof2(num_mask - 8)
    third_octet = '0'
    fourth_octet = '0'        
    if num_mask >= 24:
        third_octet = '255'
    elif num_mask > 16:
        third_octet = getpowerof2(num_mask - 16)
    fourth_octet = '0'
    if num_mask == 32:
        fourth_octet = '255'
    elif num_mask > 24:
        fourth_octet = getpowerof2(num_mask - 24)
    mask = str(first_octet) + '.' + str(sec_octet) + '.' + str(third_octet) + '.' + str(fourth_octet)
    return mask, first_octet, sec_octet, third_octet, fourth_octet

# Funcion que calcula el equivalente de un decimal en potencias de 2.
def getpowerof2(num_mask):
    cont = num_mask
    potencia = 7
    octet = 0
    while cont != 0:
        octet += pow(2,potencia)
        cont -= 1
        potencia -= 1
    octet = str(octet)
    return octet

# Funcion que calcula la mascara en formato barra partiendo de la decimal.
def getslashmask(fo, so, to, foo):
    analize = [fo, so, to, foo]
    acum = 0
    for octeto in analize:
        cont = 7
        while cont != -1:
            if octeto & pow(2,cont) == pow(2,cont):
                acum += 1
            cont -= 1
    slashvalue = '/' + str(acum)
    return slashvalue

# Funcion que obtiene el subnet ID y la direccion de Broadcast.
def getnetinfo(ip_info, mask_info):
    interesting_octet = 0
    if mask_info['first_octet'] == 255:
        net_ipfo = ip_info['first_octet']
        broad_ipfo = ip_info['first_octet']
    else:
        interesting_octet = 1
        net_ipfo = calcnetid(ip_info['first_octet'],mask_info['first_octet'])
        broad_ipfo = calcbroadip(ip_info['first_octet'], mask_info['first_octet'])
    net_ipso = '0'
    net_ipto = '0'
    net_ipfoo = '0'
    broad_ipso = '255'
    broad_ipto = '255'
    broad_ipfoo = '255'
    if mask_info['sec_octet'] == 255:
        net_ipso = ip_info['sec_octet']
        broad_ipso = ip_info['sec_octet']
    else:
        interesting_octet = 2
        net_ipso = calcnetid(ip_info['sec_octet'],mask_info['sec_octet'])
        broad_ipso = calcbroadip(ip_info['sec_octet'], mask_info['sec_octet'])
    net_ipto = '0'
    net_ipfoo = '0'
    broad_ipto = '255'
    broad_ipfoo = '255'
    if mask_info['third_octet'] == 255:
        net_ipto = ip_info['third_octet']
        broad_ipto = ip_info['third_octet']
    else:
        interesting_octet = 3
        net_ipto = calcnetid(ip_info['third_octet'],mask_info['third_octet'])
        broad_ipto = calcbroadip(ip_info['third_octet'], mask_info['third_octet'])
    net_ipfoo = '0'
    broad_ipfoo = '255'
    if mask_info['fourth_octet'] == 255:
        net_ipfoo = ip_info['fourth_octet']
        broad_ipfoo = ip_info['fourth_octet']
    else:
        interesting_octet = 4
        net_ipfoo = calcnetid(ip_info['fourth_octet'],mask_info['fourth_octet'])
        broad_ipfoo = calcbroadip(ip_info['fourth_octet'], mask_info['fourth_octet'])
    broadcast = str(broad_ipfo) + '.' + str(broad_ipso) + '.' + str(broad_ipto) + '.' + str(broad_ipfoo)
    netid = str(net_ipfo) + '.' + str(net_ipso) + '.' + str(net_ipto) + '.' + str(net_ipfoo)  
    return broadcast, netid

# Calcula el octeto 'interesante' del subnet ID.
def calcnetid(ip_octet, mask_octet):
    spec_num = 256 - int(mask_octet)
    multiplo = ip_octet // spec_num
    net_octet = spec_num * multiplo
    return net_octet

# Calcula el octeto 'interesante' de la direccion de Broadcast.
def calcbroadip(ip_octet, mask_octet):
    spec_num = 256 - int(mask_octet)
    multiplo = (ip_octet // spec_num) + 1
    broad_octet = (spec_num * multiplo) - 1
    return broad_octet

# Funcion que se llama de las excepciones en el programa y lo cierra luego de imprimir advertencia.
def errormsg(x):
    if x == 0:
        print("Error en la escritura.")
    elif x == 1:
        print('La direccion introducida no es valida.')
    elif x == 2:
        print('La mascara introducida no es valida.')
    sys.exit()
    return

#------------------------------------------------
#MAIN
#------------------------------------------------

# Para usar sys.exit()
import sys
# Se mantiene en un loop constante para poder calcular varias IP.
while True:
    try:
        # Diccionarios para guardar la info de la direccion IP y la mascara introducidas.  
        mask_info = {}
        ip_info = {}
        # User input Prompt.
        var_input = input("Escriba la direccion a analizar junto con su mascara (separar con espacio) o Ctrl+C para salir: \n")
        # En caso de que no se escriba bien la direccion y/o la mascara.
        if not " "  in var_input or not "." in var_input:
            errormsg(0)
        # Analiza en caso de que se introduzca la mascara en formato barra.    
        elif '/' in var_input:
            ip_addr, mask_info['slash'] = var_input.split(' ')
            mask = mask_info['slash'].replace('/','')
            num_mask = int(mask)
            # Si la mascara posee numeros no validos, entra a la funcion error.
            if num_mask < 0 or num_mask > 32:
                errormsg(2)
            mask_info['DDN'], mask_info['first_octet'], mask_info['sec_octet'], mask_info['third_octet'], mask_info['fourth_octet'] = get_ddn_mask(num_mask)
        # Analiza en caso de que se introduzca la mascara en formato decimal.
        else:
            ip_addr, mask_info['DDN'] = var_input.split(' ')
            # Verifica que la mascara este escrita completa.
            try:
                fo, so, to, foo = mask_info['DDN'].split('.')
            except ValueError:
                errormsg(2)
            mask_info['first_octet'] = int(fo)
            mask_info['sec_octet'] = int(so)
            mask_info['third_octet'] = int(to)
            mask_info['fourth_octet'] = int(foo)
            # Si la mascara posee numeros no validos, entra a la funcion error.
            if (int(fo) < 0 or int(fo) > 256) or (int(so) < 0 or int(so) > 256) or (int(to) < 0 or int(to) > 256) or (int(foo) < 0 or int(foo) > 256):
                errormsg(2)
            mask_info['slash'] = getslashmask(int(fo),int(so),int(to),int(foo))
        # Captura la direccion IP y verifica si esta escrita correctamente.
        try:
            ip_info['DDN'] = ip_addr
            ipfo , ipso, ipto, ipfoo = ip_addr.split('.')
        except ValueError:
            errormsg(1)
        ip_info['first_octet'] = int(ipfo)
        ip_info['sec_octet'] = int(ipso)
        ip_info['third_octet'] = int(ipto)
        ip_info['fourth_octet'] = int(ipfoo)
        # Si la direccion IP no tiene numeros validos, entra a la funcion error.
        if (int(ipfo) < 0 or int(ipfo) > 256) or (int(ipso) < 0 or int(ipso) > 256) or (int(ipto) < 0 or int(ipto) > 256) or (int(ipfoo) < 0 or int(ipfoo) > 256):
            errormsg(1)
        # Llama a la funcion que calcula el subnet ID y la direccion de Broadcast.
        broadcast, netid = getnetinfo(ip_info, mask_info)
        # Imprime los resultados del calculo.
        print("Subnet ID: " + netid + ' ||| ' + mask_info['DDN'] + ' ||| ' + mask_info['slash'])
        print("Broadcast address: " + broadcast + ' ||| ' + mask_info['DDN'] + ' ||| ' + mask_info['slash'])
        print("----------------------------")
    except KeyboardInterrupt:
        print("See you later.")
        sys.exit()
