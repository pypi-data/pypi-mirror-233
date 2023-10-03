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

def named(cadena):

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