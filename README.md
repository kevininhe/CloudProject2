# Proyecto 2 - Desarrollo de soluciones Cloud

## Dependencias

Las dependencias se encuentran en el archivo "requirements.txt", y funcionan con la versión 3.9.12 de Python. En caso de que se necesiten instalar las dependencias manualmente, el listado es el siguiente (se recomienda usar un entorno virtual):
- pip3 install wheel
- pip3 install flask
- pip3 install flask-restful
- pip3 install boto3

Para desplegar la aplicación en AWS Lambda se puede usar la librería "zappa", que se instala con:
- pip3 install zappa

Finalmente, el siguiente tutorial muestra de forma detallada como se puede hacer el despliegue en AWS Lambda usando zappa: https://towardsdatascience.com/deploy-a-python-api-on-aws-c8227b3799f0
