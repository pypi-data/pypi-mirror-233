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
            #print('1')
            #print(str(e))
            return False
        else:
            mx_record = records[0].exchange
            mx_record = str(mx_record)
            return True

            # SMTP lib setup (use debug level for full output)
            #server = smtplib.SMTP()
            #server.set_debuglevel(0)

            # Conversación SMTP
            #try:
            #    server.connect(mx_record)
            #except Exception as e:
                #print(str(e))
                #print('2')
            #    return False
            #else:
            #    server.helo(server.local_hostname) # Se obtiene el hostname del servidor local
            #    server.mail(from_address)
            #    code, message = server.rcpt(str(address_to_verify)) # smtplib.SMTPServerDisconnected: Connection unexpectedly closed cuando el correo es gmail
            #    server.quit()

                # SMTP responde 250 si es success
            #    if code == 250:
                    #print(code)
            #        return True
            #    else:
                    #print(code)
            #        return False
    
def normalize(string):
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
    for a, b in replacements:
        string = string.replace(a, b).replace(a.upper(), b.upper())
    return string

