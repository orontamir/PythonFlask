from flask_restful import Resource
from source.models.store import StoreModel


class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exist".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            {'message': "An error occurred while creating the store"}, 500
        return store.json(), 201


    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'nessage deleted'}





class SortList(Resource):
    def get(self):
        return {'stores':[x.json() for x in StoreModel.query.all()]}