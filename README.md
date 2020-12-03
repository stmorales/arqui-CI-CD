# IIC2173 - Entrega 1 - Levantando clusters hechos por estudiantes de arquitectura de sistemas de software

FrontEnd URL: `http://frontend-grupo14-arqui.tk`
BackEnd URL: `https://backend-grupo14-arqui.tk`

Connect to Front: `ssh -i "grupo_14.pem" ec2-user@ec2-52-1-189-235.compute-1.amazonaws.com`
Connect to Back: `ssh -i "grupo_14.pem" ec2-user@ec2-3-94-48-120.compute-1.amazonaws.com`


## Requisitos
Esta entrega consiste en dos partes, la parte mínima (que todos deben lograr) que vale **50%** de la nota final y una parte variable que también vale **50%**. Sobre la parte variable, tendrán 3 opciones para trabajar, de las que deberán escoger 2. Cada una de las que escojan para evaluar vale **25%** de la nota final, y realizar una tercera parte puede dar hasta 3 décimas.

---

## Parte mínima

### Sección mínima (50%) (30p)

#### **Autentificación**
* **RF1:** Añadir un servicio completamente independiente para manejar la sesión de los usuarios. La sesión debe contener información para permitir a laaplicación acceder a la información que le corresponda. Se recomienda el uso de JWT o SAML. :heavy_check_mark:
* **RF2:** La implementación debe considerar algún protocolo como OAuth, de manera que se externalice la identificación y nivel de acceso de los usuarios.Con esta implementación debe permitir que se pueda desarrollar una nueva aplicación que consuma sus servicios, así como también manejar el acceso desus usuarios.

* **RF3:** El mismo sistema debe considerar el acceso de administrador. Es decir, si el usuario tiene acceso a la aplicación de mensajería también deberíausar la misma cuenta para administrador. (Single Sign On, a.k.a SSO). :heavy_check_mark:
* **RF4:** Implementar 2FA en su solución. Esto debe ser implementado mediante un correo o SMS

#### **CI/CD**
* **RF1:**  Debe documentarse un flujo de integración en el repositorio de código. Debe incluirse semantic versioning en todos sus commits (Visto en clases). :heavy_check_mark: (Los commits no se hicieron porque este item fue el último que hicimos, pero la documentación de la integración se encuentra en el Integration.md)
* **RF2:** Cada vez que haya se haga un merge a master se debe automatizar el despliegue en un ambiente (ya sea staging o producción) utilizando algunaherramienta como Travis/CodeBuild/Jenkins u otro. (Generar y almacenar las imágenes si correspnde) :heavy_check_mark:
* **RF3:** Se deben incorporar tests de funcionalidad (unitarios y de integración) antes de hacer el paso real. Se piden algunos tests para mostrar sufuncionamiento (Al menos tres tests unitarios simbólicos pero que den resultados). Se encuentran en `test_main.py` :heavy_check_mark:
* **RF4:** El sistema de despliegue continuo debe hacerse cargo de manejar las variables de entorno de manera segura. :heavy_check_mark:

#### **Documentación**
* **RF1:**  Debe documentar con diagramas de componentes el sistema a fines de esta entrega :heavy_check_mark:
* **RF2:** Debe documentar con diagramas de flujo los procesos de log in/sign up, envío de mensajes (considerando todos los procesos que ocurran a partirde ahí). :heavy_check_mark:
* **RF3:** Debe documentar con diagramas el proceso de despliegue. :heavy_check_mark:
* **RF4:** Debe documentar todas las posibles llamadas a sus APIs con algún estandar (Postman, Swagger u otra) :heavy_check_mark: (Esta documentación se encuentra en el siguiente link: https://backend-grupo14-arqui.tk/docs/)
---

## Sección variable

Deben completar al menos 2 de los 3 requisitos

### CRUD Admin (25%) (15p)

* **RF1:** Se implementa un menu para acceder a la información de los usuarios. Se puede revisar y modificar la información de éstos y bloquear el acceso
("borrar"). De ser necesario, debe interactuar con el sistema de auth implementado en la sección de Autenticación. :heavy_check_mark:
* **RF2:** Se implementa el menú para manejar grupos. Se pueden cerrar grupos, dejar públicos o privados. :heavy_check_mark:
* **RF3:** Se implementa el CRUD mensajes. Como admin puede enviar mensajes en grupos, ver y modificar los mensajes e incluye la censura de ellos. Al
modificar o censurar los mensajes no se puede perder el mensaje original. :heavy_check_mark:


### Encriptación (25%) (15p)

* **RF1:** Salas de chat privadas. :heavy_check_mark:
* **RF2:** Encriptación end-to-end en mensajes de un grupo. (incompleto)
* **RF3:** Debe documentar los mecanismos utilizados para cada uno de los puntos anteriores y su método de implementación. :heavy_check_mark:



---

### DOCUMENTACIÓN ENCRIPTACIÓN

Para la encriptación se utilizó el sistema Vault, para esto, primero se levantó un Vault server en una instancia de EC2.
En la branch vault-connection se encuentran los cambios en código realizados en el backend para conectarse con Vault, entre estos la función para encriptar y desencriptar en base64 como también el código para conectarse con la instancia de EC2 de Vault mediante el uso del token de cliente que tenemos. Nuestro backend está en FastApi por lo que se buscó la librería hvac de python para comunicarse como cliente con Vault.

El Vault server en la instancia de EC2 se encuentra funcionando bien, y está configurado con el secret engine Transit para que funcione como EaaS (Encryption as a Service). El Vault está unsealed y se consiguió el token de cliente para que tanto el backend como el frontend pudieran hacer las llamadas a vault pidiéndole encriptar o desencriptar mensajes.

Para conseguir la encriptación end-to-end lo que se prentendía hacer era que el frontend al recibir un mensaje en los chats de cualquier usuario, lo mandara en base64 Vault pidiéndole que lo encripte, luego Vault se lo devuelve encriptado al frontend y así recién es enviado al backend. Después, al llegar al backend este podría pedirle a Vault que se lo desencripte, Vault se lo manda en base64, el backend desencripta la base64 y obtiene el mensaje en texto plano para procesarlo si es necesario o sino simplemente cuando lo recibe encriptado lo guardaría en la base de datos sin desencriptar. De esta manera la comunicación end-to-end estaría encriptada, usando la seguridad que entrega la encriptación como servicio que ofrece Vault.

No se alcanzó a completar por completo esta funcionalidad, pero la instancia está funcionando perfecto con Vault, el código de backend que se alcanzó a hacer está en la branch vault-connection y puede revisarse, para la parte de frontend no se alcanzó a escribir código, pero el objetivo era el antes descrito.
Las salas de chat privadas se alcanzó a marcar la sala mediante un booleano si es privada o pública, para luego programar la funcionalidad de permitir o no el acceso basándose en esto.

### DOCUMENTACIÓN CHAT EN TIEMPO REAL

Se utilizó la librería `python-socketio` con el framework FastAPI y la librería `socket.io` para React. Para ello, cada vez que un cliente se conecta a una sala, este es ingresado en ese *room* para recibir las señales pertenecientes a esta.

Para un correcto funcionamiento de esta metodología es necesario:

1. Pertenecer a la sala a la que se envía el mensaje
2. Estar concectado para recibirlo en tiempo real.
3. Haber más de una persona en el grupo para que aparezcan los mensajes en tiempo real.

Las funciones encargadas de realizar la comunicación entre los sockets son `on` y `emit`. La primera recibe las llamadas cuando estas se emiten, y la segunda, emite (duuuh).

**Tres funciones en Backend:**

1. `sio` es el "server" encargado de los sockets en el backend, y cada vez que se emite la señal connect se agrega el socket conectado y también imprime en los logs que fue conectado.

```
    @sio.on('connect')
    def connect(sid, environ):
        print("SE HA CONECTADO", sid)
```

2. `sio` cuando escucha que algun socket emite la señal *join* lo une al *room* al cual se unió para comenzar a escuchar a los sockets que se encuentran ahí dentro.

``` 
    @sio.on('join')
    def join(sid, dataUser, *args):
        print('Se ha unido', sid)
        sio.enter_room(sid, dataUser['room'])
```

3. Cuando en el frontend se envía un mensaje, este mismo mensaje se envía a través del socket emisor al backend, este le agrega el *timestamp* y luego emite la señal message a todos los que pertenecen al *room* desde donde se emitió el mensaje, siendo todos notificados de este

``` 
    @sio.on('sendMessage')
    async def sendMessage(sid, dataUser, *args):
        dataUser['time'] = datetime.now().strftime("%H:%M")
        await sio.emit('message', dataUser, room=dataUser['room'])
```


**Tres funciones en FrontEnd:**

Todas las funcionalidades de los sockets se ven en el archivo `ChatRoom.js`, en donde cada vez que es enviado un mensaje, además de enviarlo a la API del backend para ser guardado, este mismo mensjae es emitido al socket del backend.

```
    socket.emit('sendMessage', newMessageSocket, (error) => {
        if (error) {
            return console.log(error)
        }
        console.log("Message delivered!")
    })
```

 El socket en el backend habiendo recibido el mensaje, les notifica a todos los integrantes de la sala del Chat que ese mensaje fue enviado y lo actualiza. La función con la que escuchan es:

 ```
    socket.on('message', (msg) => {
        const newMessages = [...this.state.messages];
        newMessages.push(msg);
        this.setState({messages: newMessages});
    });
```

También el `join` que notifica al backend que el usuario a ingresado a un *room* es:

 ```
    socket.emit('join', ObjectToSend, (error) => {
        if (error) {
            return console.log(error)
        }
        console.log("Usuario conectado!")
    });
```
**Documentación ELB:**

Se implementó el Load Balancer (se llama web-elb, está en North Virginia y tiene como availability zones us-east-1a y us-east-1b) y el AutoScalingGroup que crea las instancias según como fue definido. Sin embargo, cada vez que se crea la instancia en esa instancia no se inicia la aplicación, hay que entrar a cada una de ellas y hacerles el docker-compose build y docker-compose up. Quedó pendiente automatizar esas operaciones en las instancias, para que cada vez que se levante una automáticamente inicie la aplicación de esa forma.

El AutoScalingGroup está configurado con la AMI de nuestra instancia EC2 llamada backend.

No se pudo añadir información de la intancia al header, ya que no corre la aplicación en las nuevas instancias levantadas :c

**Documentación CDN:**

Se implemento un CDN llamado cloudfron en conjunto con S3. Para este caso lo usamos simplemente para guardar nuestros archivos estáticos, tales como fotografías, las cuales están siendo almacenadas en nuestro S3. Desde el CDN es que esta accediendo a nuestro S3 y sacando la inforación para luego llevarla directamente a nuestro FrontEnd.

**Documentación Caché:**

Se implemento una capa de Caché mediante el servicio administrado de AWS. Este es el llamado ElastiCache, el cual lo hicimos funcionar en conjunto con Redis. Esta fue la arquitectura que ocupamos. Practicamente lo que hace es crear un cluster con nodos donde se  va guardando la información como key:value. Esto se ocupa de esta forma debido a que a pesar de que ElastiCache ya tiene menos latencia que ir a buscar información a la base de datos, teniendo la información como recien lo expusimos hace que la velocidad sea aún mayor.


**Documentación Notificaciones:**

Una vez que se haya elegido un usuario en la aplicación. Debajo de los chats que tiene asociado el usuario, estarán las notificaciones.
Si el usuario no tiene notificaciones (no lo han mencionado) aparecerá:

'El usuario no ha recibido notificaciones'

De lo contrario, aparecerá el/los mensaje(s) en donde se mencionó al usuario. Asímismo, se puede hacer click sobre el mensaje en el que el usuario aparece notificado, el cual redirige inmediatamente al chatRoom en el que fue mencionado.

¿Cómo se menciona a un usuario?

@username

Por ejemplo:

-> @rodo como estás?
-> hola @francisco como va?

Es importante que haya un espacio antes del @, NO se puede hacer lo siguiente:
-> Hola@francisco como va?

También tiene que estar SOLAMENTE el nombre de usuario despues del @, NO se puede hacer lo siguiente:
-> hola @francisco, como va?


En cuanto al aspecto más técnico, en el frontEnd simplemente se manda el mensaje. Luego el backend revisa si el mensaje tiene "@", y hace el procesamiento de asociarlo con el usuario mencionado. Esto se ve en el archivo Code/main.py.

Se creó una lambda function en AWS en Ohio llamada NotificationSystem que es la que debiera mandar directamente la notificación por email o algún otro modo, de momento solo imprime 'Se está enviando la notificación por correo' (como se permitía según enunciado) y retorna status code 200. Esta lambda function se configuró con un API Gateway.

El backend le hace un get al url de NotificationSystem 'https://nysgme96oe.execute-api.us-east-2.amazonaws.com/default/NotificationSystem' y si recibe 200 confirma que se está enviando la notificación mediante un print en consola, y si falla con un print diferente.

Por último, desde el frontEnd, se hace un GET con el id del current user, para que el backend le devuelva todos los mensajes en los que ha sido mencionado, junto con el room asociado.

### DOCUMENTACIÓN CACHÉ

La infraestructura necesaria para el caché está montada en ElasticCache, pero la conexión con Redis no logró ser implementada. 

### DOCUMENTACIÓN TRABAJO DELEGADO

Para la sección de trabajo delegado implementamos [este](https://thecloudtutorials.com/2019/03/09/building-a-talking-app/) tutorial y el código correspondiente se encuentra en [este](https://github.com/iic2173/iic2173-proyecto-semestral-grupo14-frontend) repositorio.

En esta sección se agregó un boton `play` dentro de las salas de chat que al apretarlo reproduce una frase.

Se utiliza el framework serverless, por lo que la implementación de Lambda Functions se hace a traves del deploy del archivo `serverless.yml`, no directamente en la Consola de AWS. 

Lo que se hace es implementar una Lambda Function llamada `speak`, en la cual se utiliza la función `synthesizeSpeech` de Amazon Polly, importado desde la libreria `sdk`, para la transformación del texto en audio. Luego, se almacena el archivo de audio retornado en un bucket S3. Aqui se utiliza la libreria `uuid/v1` para crear una secuencia de caracteres unica que será usada para nombrar el archivo de audio y así evitar conflictos por nombres repetidos. Finalmente, se obtiene desde el S3 una URL correspondiente a dicho archivo, la cual se envía al frontend para que este pueda obtenerlo a través de ella y así reproducirlo cuando se presione el boton `play`. Todo esto se implementa dentro del archivo `handler.js`.

Lamentablemente, al implementarlo nos encontramos con un error de CORS que no pudimos solucionar ya que no encontramos la forma de habilitar esto desde las configuraciones de la API Gateway en la consola de AWS.

### DOCUMENTACIÓN COMO CORRER LA APLICACIÓN EN AWS

Para el BACKEND, una vez que se tenga clonado este repositorio en la instancia de Amazon, se tiene que hacer los siguientes comandos:

```
cd Code
docker-compose build
docker-compose up
docker-compose up     /*si no corre a la primera*/

```

Para el FRONTEND, una vez que se tenga clonado este repositorio en la instancia de Amazon, se tiene que hacer los siguientes comandos:

```
docker-compose build
docker-compose up

```

### DOCUMENTACIÓN COMO CORRER LA APLICACIÓN EN LOCAL

Como todo está hecho para que funcione en producción, se tiene que hacer cambios en 2 archivos, el primero de ellos está en:

```
cd client/src/components/Socket.js

```

y se tiene que cambiar esta línea:

```
let socket = io('https://backend-chat-arqui.tk')
```

por esta línea:

```
let socket = io('http://localhost:8000')
```

El segundo archivo que hay que cambiar, está en el siguiente path:

```
cd client/src/axios-fastapi.js

```

Y hay que cambiar la siguiente línea:

```
    baseURL: 'https://backend-chat-arqui.tk'

```

Por el siguiente código:

```
    baseURL: 'http://localhost:8000'

```

Luego para el BACKEND, una vez que se tenga clonado este repositorio en tu computador, se tiene que hacer los siguientes comandos:

```
cd Code
docker-compose build
docker-compose up
docker-compose up     /*si no corre a la primera*/

```

Para el FRONTEND, una vez que se tenga clonado este repositorio en tu computador, se tiene que hacer los siguientes comandos:

```
docker-compose build
docker-compose up

```

### ACLARACIONES GENERALES:

Este repositorio contiene el backend de la aplicación, en el otro repositorio de Frontend se encuentra el resto :)
