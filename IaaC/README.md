# Aclaraciones Generales

Se utilizó cloudFormation para la implementación de IaaC

# Instrucciones para subir el CloudFormation File

Primero que todo se tiene que ingresar a la consola de aws con una cuenta y verificar que tu cuenta esté en US East (N. Virgina). Luego en el buscador de servicios que provee AWS buscas "cloudFormation". Una vez que te sale en el buscador, le das click. A continuación te aparecerá una opción con el nombre de "Create Stack", y le das click.

Una vez que estás creando el stack, le das a la opción de "Template is ready", luego le das a la opción de "Upload a template file", luego escoges el archivo a subir, que en este caso es "cloudFormationFile.yaml".

Con todo eso hecho, le das a "Next", y tendrás que ponerle un nombre al stack que estas subiendo. Puedes darle el nombre que tu quieras.

Luego le das nuevamente a "Next", y por último a "Create Stack".

Luego simplemente hay que esperar a que se creen los servicios que se indicaron en el "cloudFormationFile.yaml". Puedes ir verificando si todo está yendo bien apretando el boton de actualizar en "Events".

Asimismo en "Outputs" podrás ver los valores de las ElasticIP que fueron creadas.

# Explicación del Código

Los archivos .yaml van desde lo general hacia lo específico. Por lo que se parte especificando que vamos a incorporar "Resources". En ellos agregamos primero una instancia EC2 que se usará para el backend de nuestra aplicación y más abajo le asignamos una ElasticIP. Se realiza el mismo proceso, solamente que con una instancia que se usará como Frontend.

Por último el apartado de "Outputs" es simplemente para que en la consola de AWS, cuando ves la información de un stack que fue subido, te aparezcan los valores de las elasticIPS.