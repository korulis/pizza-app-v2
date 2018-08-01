from bson.json_util import dumps,loads
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pprint import pprint
from Messenger import Messenger
from flask_cors import CORS, cross_origin
import uuid

app = Flask(__name__)
cors = CORS(app)

client = MongoClient('localhost', 27017)
db = client['test-database']
collection = db['test-collection']

@app.route("/orders/", methods=["DELETE"])
def DeleteAll():
    collection.delete_many({})

    return jsonify({}), 200

@app.route("/labas/")
@cross_origin()
def Hello():
    print("labas")
    return jsonify("Labas!")


@app.route("/orders/")
@cross_origin()
def GetAllOrders():
    all_docs = list(collection.find({}, {'_id': False}))
    print(all_docs)
    return jsonify(all_docs)


@app.route("/orders/<orderRef>")
def GetOne(orderRef):
    doc = collection.find_one({"orderRef": orderRef}, {'_id': False})

    if(doc is None):
        return jsonify({}), 404

    return jsonify(doc)


@app.route("/orders/<orderRef>", methods=["POST"])
@cross_origin()
def CreateOne(orderRef):
    order = request.json
    order["orderRef"] = orderRef
    duplicate = collection.find_one({"orderRef": orderRef})

    if(duplicate is not None):
        return jsonify({}), 409

    orderId = collection.insert_one(order).inserted_id
    return jsonify({"orderRef": orderRef}), 201


@app.route("/orders/<orderRef>", methods=["PUT"])
def UpdateOne(orderRef):
    order = request.json
    order["orderRef"] = orderRef

    collection.update({"orderRef": orderRef}, order, True)

    return jsonify({"orderRef": orderRef}), 202


@app.route("/orders/<orderRef>", methods=["DELETE"])
def RemoveOne(orderRef):
    target = collection.find_one({"orderRef": orderRef})

    if(target is None):
        return jsonify({}), 404

    collection.delete_one({"orderRef": orderRef})
    return jsonify({"orderRef": orderRef}), 202

if __name__ == '__main__':
    print("starting app")
    app.run(threaded = True, host="0.0.0.0")

