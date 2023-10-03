
#<-------------------------------- Utilidades -------------------------------------------------------->

def email(email):

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
    #1 DIGITO ALFANUMERICO
    #1 numero al final 

    if cantidad ==18:
            string = list(string)
            for i in string:
                cont += 1
                if (cont <=4):
                    p = i.isalpha()
                    if not p:
                        return False
                elif (cont == 11 and i not in ['H','M']):
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
                        if cont in range(17,18):
                            p = i.isdigit()
                            if not p :
                                p = i.isalpha()
                                if not p :
                                    return False
                        elif cont in range(18,19):
                                p = i.isdigit()
                                if not p :
                                    return False
    else:
        return False

    return True
