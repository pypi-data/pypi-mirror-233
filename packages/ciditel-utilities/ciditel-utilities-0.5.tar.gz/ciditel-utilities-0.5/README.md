# Utilidades

```
pip install verificaciones==1.0

import verificaciones

```
```
from verificaciones import validate

```
* Email:

> Permite a través de un string como parámetro
> devolver True or False en caso de ser
> un email válido o no  

```

Args:
    string: email a verificar.

Returns:
    True: email válido
    Or
    False: email no válido 

```

* CURP: 

> Verificación simple de que un string
>  sea un CURP válido,

```

Args:
    string: CURP a validar.

Returns:
    True: CURP Válido.
    Or
    False: CURP no Válido.

```

```
from ciditel-utilities import strings

```

* Normalize

> Permite pasar un string 
> y recibir la misma palabra, sin acentos
> de puntuación 

```

Args:
    string: palabra con signos de puntuación.

Returns:
    string: palabra sin signos de puntuación

```

* Named:

> Permite pasar un string 
> y recibir nombre/segundo_nombre/apellido/segundo_apellido
> nota: de no poseer se toma como  " "

```

Args:
    string: nombre completo.

Returns:
    nombre: string
    segundo_nombre: string
    apellido: string
    segundo_apellido: string

```

