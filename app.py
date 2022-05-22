from flask import Flask, request, jsonify
import boto3
from flask_restful import Api, Resource
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)
api = Api(app)

# Constantes
dynamodb = boto3.resource('dynamodb')
TABLE = dynamodb.Table('ListaNegraMail')

def revisarMailExiste(mail):
    response = TABLE.query(
        KeyConditionExpression=Key('PK').eq(mail)
    )
    items = response['Items']
    if len(items) > 0:
        return True
    return False

# Retorna un diccionario con dos keys: Attributes y ResponseMetadata. Attributes trae el objeto despues de ser actualizado
def insertarMail(mail,idAppCliente,motivo,dirIp,fechaRegistro):
    updatedElement = TABLE.update_item(
    Key={
        'PK': mail
    },
    UpdateExpression='SET idAppCliente = :idAppCliente,motivo = :motivo,dirIp = :dirIp,fechaRegistro = :fechaRegistro',
    ExpressionAttributeValues={
        ':idAppCliente': idAppCliente,
        ':motivo':motivo,
        ':dirIp':dirIp,
        ':fechaRegistro':fechaRegistro,
    },
    ReturnValues="ALL_NEW"
    )
    return updatedElement

class listaNegraMailRecurso(Resource):
    def get(self):
        response = {}
        mail = request.args.get('mail')
        mailExiste = revisarMailExiste(mail)
        response["response"] = mailExiste
        return jsonify(response)

    def post(self):
            response = {}
            # Validacion inicial
            if not (request.json) or not ({'mail','idAppCliente'} <= request.json.keys()):
                response["response"] = 0
                response["message"] = "El request no tiene todos los campos necesarios para insertar el mail"
                return jsonify(response)
            
            # Obtener campos
            mail = request.json['mail']
            idAppCliente = request.json['idAppCliente']
            motivo = request.json.get('motivo','')
            dirIp = request.remote_addr
            fechaRegistro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if len(motivo) > 255:
                response["response"] = 0
                response["message"] = "El campo 'motivo' no puede exceder los 255 caracteres"
                return jsonify(response)

            result = insertarMail(mail,idAppCliente,motivo,dirIp,fechaRegistro)
            responseCode = result["ResponseMetadata"].get("HTTPStatusCode","")
            if str(responseCode) == "200":
                response["response"] = 200
                response["message"] = "El mail fue insertado correctamente en la lista negra"
            else:
                response = result["ResponseMetadata"]
                response["response"] = 0
            return jsonify(response)

api.add_resource(listaNegraMailRecurso, '/listaNegraMail')

if __name__ == '__main__':
    app.run(debug=True)