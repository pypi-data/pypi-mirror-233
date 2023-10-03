
#<-------------------------------- Utilidades -------------------------------------------------------->

def validate_email_address(email):

    import re
    import smtplib
    import dns.resolver

    address_to_verify = email

    # Regex para chequear la sintaxis
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

    # Chequeando sintaxis
    match = re.match(regex, address_to_verify)

    if match == None:
        return False
    else:
        # Obteniendo el dominio para buscar el DNS
        split_address = address_to_verify.split('@')
        domain = str(split_address[1])

        # Buscando MX record
        try:
            records = dns.resolver.resolve(domain, 'MX')
        except Exception as e:
            return False
        else:
            mx_record = records[0].exchange
            mx_record = str(mx_record)
            return True
    
def normalize(string):
    #Reemplazando acentos

    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("à", "a"),
        ("è", "e"),
        ("ì", "i"),
        ("ò", "o"),
        ("ù", "u"),
    )

    #Insertar y retornar un string sin acentos
    for a, b in replacements:
        string = string.replace(a, b).replace(a.upper(), b.upper())

    return string

def validation(cadena):

    cadena = cadena.title().strip().split()
    nombre = cadena[0]
    segundo_nombre = ""
    apellido = ""
    segundo_apellido = ""

    #Validacioon de string para retornar 
    # nombre/segundo_nombre/apellido/segundo_apellido

    if len(cadena) == 2:
              apellido = cadena [1]
    else:
        if len(cadena) == 3:
            if  cadena[1] == "De":
                apellido = cadena[1]+" "+cadena[2]
            else:
                if  cadena[1] == "Del":
                    apellido = cadena[1]+" "+cadena[2]
                else:
                    apellido = cadena[1]
                    segundo_apellido = cadena[2]
        else:
            segundo_nombre = cadena[1]
            apellido = cadena[2]
            segundo_apellido = cadena[3]
            for row,i in enumerate(cadena):
                if i == "Los" or i == "La" or i == "Las":
                    if row <=2:
                        segundo_nombre = cadena[row-1]+" "+cadena[row]+" "+cadena[row+1]
                        apellido = cadena[row+2]
                        try:
                            segundo_apellido = cadena[row+3]
                        except Exception as e:
                            segundo_apellido = " "
                    else:
                        apellido = cadena[row-2]
                        segundo_apellido = cadena[row-1]+" "+cadena[row]+" "+cadena[row+1]
                else:
                    if i == "Del":
                        segundo_nombre = cadena[row]+" "+cadena[row+1]
                        apellido = cadena[row+2]
                        try:
                            segundo_apellido = cadena[row+3]
                        except Exception as e:
                            segundo_apellido = " "
                    else:
                        if i == "De":
                            apellido = cadena[row-1]
                            segundo_apellido = cadena[row]+" "+cadena[row+1]
                            
    return nombre, segundo_nombre, apellido,segundo_apellido

def curp(string):
    #Validación CURP
    cantidad = len(string)
    cont = 0
    string = string.upper()
    #CURP contiene 18 caracteres
    #4 letras (nombre)
    #6 numeros (fecha de nacimiento)
    #1 letra (genero H-M-N)
    #5 letras (lugar de nacimiento)
    #2 numeros al final 

    if cantidad ==18:
        string = list(string)
        for i in string:
            cont += 1
            if (cont <=4):
                p = i.isalpha()
                if not p:
                    return False
            elif (cont == 10 and i not in ['H','N','M']):
                return False
            else:
                if cont in range(5,11):
                    p = i.isdigit()
                    if not p:
                        return False
                elif (cont in range(11,17)):
                    p = i.isalpha()
                    if not p:
                        return False
                else:
                    if cont in range(17,19):
                        p = i.isdigit()
                        if not p:
                            return False
    else:
        return False

    return True
