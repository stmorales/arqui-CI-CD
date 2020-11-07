# IIC2173 - Entrega 1 - Levantando clusters hechos por estudiantes de arquitectura de sistemas de software

FrontEnd URL: `http://frontend-grupo14-arqui.tk`
BackEnd URL: `https://backend-chat-arqui.tk`

Connect to Front: `ssh -i "grupo_14.pem" ec2-user@ec2-52-1-189-235.compute-1.amazonaws.com`
Connect to Back: `ssh -i "grupo_14.pem" ec2-user@ec2-3-94-48-120.compute-1.amazonaws.com`


## Requisitos
Esta entrega consiste en dos partes, la parte mínima (que todos deben lograr) que vale **50%** de la nota final y una parte variable que también vale **50%**. Sobre la parte variable, tendrán 3 opciones para trabajar, de las que deberán escoger 2. Cada una de las que escojan para evaluar vale **25%** de la nota final, y realizar una tercera parte puede dar hasta 3 décimas.

---

## Parte mínima

### Sección mínima (50%) (30p)

#### **Backend**
* **RF1: (3p)** Se debe poder enviar mensajes y se debe registrar su timestamp. Estos mensajes deben aparecer en otro usuario, ya sea en tiempo real o refrescando la página. :heavy_check_mark:
* **RF2: (5p)** Se deben exponer endpoints HTTP que realicen el procesamiento y cómputo del chat para permitir desacoplar la aplicación. :heavy_check_mark:

* **RF3: (7p)** Establecer un AutoScalingGroup con una AMI de su instancia EC2 para lograr autoescalado direccionado desde un ELB (_Elastic Load Balancer_).
    * **(4p)** Debe estar implementado el Load Balancer :heavy_check_mark:
    * **(3p)** Se debe añadir al header del request información sobre cuál instancia fue utilizada para manejar el request. Se debe señalar en el Readme cuál fue el header agregado.
* **RF4: (2p)** El servidor debe tener un nombre de dominio de primer nivel (tech, me, tk, ml, ga, com, cl, etc). :heavy_check_mark:

* **RF4: (3p)** El dominio debe estar asegurado por SSL con Let's Encrypt. No se pide *auto renew*. Tambien pueden usar el servicio de certificados de AWS para el ELB :heavy_check_mark:
    * **(2p)** Debe tener SSL. :heavy_check_mark:
    * **(1p)** Debe redirigir HTTP a HTTPS. :heavy_check_mark:

#### **Frontend**
* **RF5: (3p)** Utilizar un CDN para exponer los *assets* de su frontend. (ej. archivos estáticos, el mismo *frontend*, etc.). Para esto recomendamos fuertemente usar cloudfront en combinacion con S3. :heavy_check_mark:
* **RF6: (7p)** Realizar una aplicación para el *frontend* que permita ejecutar llamados a los endpoints HTTP del *backend*. :heavy_check_mark:
    * **(3p)** Debe hacer llamados al servidor correctamente. :heavy_check_mark:
    * Elegir **$1$** de los siguientes. No debe ser una aplicación compleja en diseño. No pueden usar una aplicacion que haga rendering via template de los sitios web. Debe ser una app que funcione via endpoints REST
        * **(4p)** Hacer una aplicación móvil (ej. Flutter, ReactNative)
        * **(4p)** Hacer una aplicación web (ej. ReactJS, Vue, Svelte) :heavy_check_mark:

---

## Sección variable

Deben completar al menos 2 de los 3 requisitos

### Caché (25%) (15p)
Para esta sección variable la idea es implementar una capa de Caché para almacenar información y reducir la carga en el sistema. Para almacenar información para la aplicación recomendamos el uso de **Redis**, así como recomendamos Memcached para fragmentos de HTML o respuestas de cara al cliente. 

* **RF1: (4p)** Levantar la infraestructura necesaria de caché. Se puede montar en otra máquina o usando el servicios administrado por AWS. Se debe indicar como funciona en local y en producción.  :heavy_check_mark:
* **RF2: (6p)** Utilizar la herramienta seleccionada de caché para almacenar las información para al menos 2 casos de uso. Por ejemplo las salas y sus últimos mensajes o credenciales de acceso (login). 
    * **Restricción** Por cada caso de uso debe utilizar alguna configuración distinta (reglas de entrada FIFO/LIFO, estructura de datos o bien el uso de reglas de expiración)
* **RF3: (5p)** Documentar y explicar la selección de la tecnología y su implementación en el sistema. Responder a preguntas como: "¿por qué se usó el FIFO/LRU o almacenar un hash/list/array?" para cada caso de uso implementado. 


### Trabajo delegado (25%) (15p)
Para esta sección de delegación de trabajo recomendamos el uso de "Functions as a Service" como el servicio administrado de AWS, _Lambda Functions_, o bien el uso de más herramientas como AWS SQS y AWS SNS. 

Se pide implementar al menos **3 casos de uso con distinto tipo de integración**.


1.- Mediante una llamada web (AWS API Gateway)
2.- Mediante código incluyendo la librería (sdk)
3.- Como evento a partir de una regla del AutoScalingGroup
4.- Mediante Eventbridge para eventos externos (NewRelic, Auth0 u otro)
5.- Cuando se esté haciendo un despliegue mediante CodeCommit 
6.- Cuando se cree/modifique un documento a S3

Alternativamente pueden integrar más servicios para realizar tareas más lentas de la siguiente forma: 
1.- Al crear un mensaje se registra en una cola (SQS) que llama a una función en lambda (directamente o a través de SNS)
2.- En Lambda se analiza ciertos criterios (si es positivo o negativo, si tiene "garabatos" o palabras prohibidas en el chat) y con este resultado se "taggea" el comentario. 
Si se crean en "tópics" distintos se consideran como 2 casos de uso (por el uso de distintas herramientas). 

Seguir el siguiente tutorial cuenta como 3 (https://read.acloud.guru/perform-sentiment-analysis-with-amazon-comprehend-triggered-by-aws-lambda-7363db23651f o https://medium.com/@manojf/sentiment-analysis-with-aws-comprehend-ai-ml-series-454c80a6114). No es necesaro que entiendan a cabalidad como funciona el código de estas funciones, pero sí que comprendan el flujo de la información y cómo es que se ejecuta.

Se deben documentar las decisiones tomadas. 

* **RF: (5p)** Por cada uno de los 3 tipos de integración.
    * **(3p)** Por la implementación. :heavy_check_mark: : 1/3
    * **(2p)** Por la documentación. :heavy_check_mark: 2/3

### Mensajes en tiempo real (25%) (15p)
El objetivo de esta sección es implementar la capacidad de enviar actualizaciones hacia otros servicios. Servicios recomendados a utilizar: SNS, Sockets (front), AWS Pinpoint entre otras. 

* **RF1: (5p)** Cuando se escriben mensajes en un chat/sala que el usuario está viendo, se debe reflejar dicha acción sin que éste deba refrescar su aplicación. :heavy_check_mark:
* **RF2: (5p)** Independientemente si el usuario está conectado o no, si es nombrado con @ o # se le debe enviar una notificación (al menos crear un servicio que diga que lo hace, servicio que imprime "se está enviando un correo") :heavy_check_mark:
* **RF3: (5p)** Debe documentar los mecanismos utilizados para cada uno de los puntos anteriores indicando sus limitaciones/restricciones. :heavy_check_mark:


#### Caso borde
Si su grupo implementó varias funcionalidades como comandos en los chats, es posible utilizar dichas funciones en Lambdas y manejarlas en paralelo utilizando SQS y SNS en conjunto. Pueden aprovechar su desarrollo para implementar las secciones variables 2 y 3 en conjunto.


---

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

En un principio se usaba la carpeta "server" para hacer el chat en tiempo real, pero luego se decidió dejar todo en el backend, que corresponde a la carpeta Code.

Es decir, server NO LA ESTAMOS USANDO!