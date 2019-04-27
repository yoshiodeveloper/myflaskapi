# -*- encoding: utf-8 -*-

from bson.objectid import ObjectId
from flask import Flask
from flask import jsonify
from flask import request
from flask.json import JSONEncoder
from pymongo import MongoClient


class MongoJSONEncoder(JSONEncoder):
    """ Classe utilizada para codificar os objetos em JSON.
    É utilizado pela função jsonify do Flask.
    Em especial são transformados os IDs do tipo ObjectId do Mongo em strings.
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            # Se o tipo for um ObjectId então converte para a sua forma em string.
            return str(o)
        else:
            # Se for de outros tipos utiliza o método "defaul" do JSONEncoder.
            return super().default(o)


app = Flask(__name__)
app.json_encoder = MongoJSONEncoder
mongo = MongoClient('mongodb://127.0.0.1:27017/')


@app.route("/", methods=('GET',))
def mongo_info():
    """ Lista informações sobre o MongoDB. """
    result = {'ok': False, 'data': None, 'error': None, 'description': 'Este endpoint retorna informações sobre o MongoDB.'}  # Valores que serão retornados.    
    result['data'] = {
        'databases': mongo.list_database_names(),
        'version': mongo.server_info()['version'],
    }
    result['ok'] = True
    return jsonify(result)


@app.route("/<db_name>", methods=('GET',))
def dbs(db_name):
    """ Lista informações sobre um DB específico. """
    result = {'ok': False, 'data': None, 'error': None, 'description': 'Este endpoint retorna informações sobre um DB específico.'}
    db = mongo.get_database(db_name)
    result['data'] = {
        'collections': db.list_collection_names(),
    }
    result['ok'] = True
    return jsonify(result)


@app.route("/<db_name>/<collection_name>", methods=('GET',))
def collections(db_name, collection_name):
    """ Lista informações sobre uma collection específica. """
    result = {'ok': False, 'data': None, 'error': None, 'description': 'Este endpoint retorna informações sobre uma collection específica. Pode-se utilizar os parâmetros "skip" e/ou "limit".'}
    limit = request.args.get('limit', 10)
    skip = request.args.get('skip', 0)
    # Algumas validações. ---------->
    try:
        limit = int(limit)
    except:
        result['error'] = 'O parâmetro limit não é um inteiro válido.'
        return jsonify(result)
    if limit < 1:
        result['error'] = 'O parâmetro limit não pode ser menor que 1.'
        return jsonify(result), 400  # Bad Request
    try:
        skip = int(skip)
    except:
        result['error'] = 'O parâmetro skip não é um inteiro válido.'
        return jsonify(result), 400  # Bad Request
    if skip < 0:
        result['error'] = 'O parâmetro skip não pode ser menor que 0.'
        return jsonify(result), 400  # Bad Request
    # <---------- fim das validações
    db = mongo.get_database(db_name)
    # Converter para lista, pois um cursor não pode ser convertido para JSON
    documents = list(db.get_collection(collection_name).find().skip(skip).limit(limit))
    count = db.get_collection(collection_name).count_documents({})
    result['data'] = {
        'documents': documents,
        'count': count,
    }
    result['ok'] = True
    return jsonify(result)