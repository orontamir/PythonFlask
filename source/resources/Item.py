import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from source.models.item import ItemModel
items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="every item need store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':"An item with name '{}' already exist".format(name)},400

        data = Item.parser.parse_args()
       # item = {'name': name, 'price': data['price']}
        item = ItemModel(name,data['price'],data['store_id'])
        #item = ItemModel(name, **data)
        try:
          item.save_to_db()
        except:
            return {"message":"An error occurred inserting the item"},500
        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db

        ################################
        #global items
      #  items = list(filter(lambda x: x['name'] != name, items), None)

       ##########################################
       # connection = sqlite3.connect('data.db')
       # cursor = connection.cursor()
       # query = "DELETE from  items where name = ?"
       # cursor.execute(query, (name,))

       # connection.commit()
       # connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
       # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        #update_item = ItemModel(name,data['price'])#{'name': name,'price': data['price']}
        if items is None:
            item = ItemModel(name,data['price'])
           # try:
              #  update_item.insert()
           # except:
            #    return {"message": "An error occurred inserting the item"},500
        else:
            item.price = data['price']
          #  try:
           #     update_item.update()
         #   except:
          #      return {"message": "An error occurred updating the item"}, 500

        item.save_to_db()
        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}

        #return {'items': list(map(lambda x:x.json(),ItemModel.query.all()))}
       # connection = sqlite3.connect('data.db')
       # cursor = connection.cursor()
       # query = "select * from items"
       # result = cursor.execute(query)
       # items =[]
       # for row in result:
       #     items.append({'name':row[1],'price':row[2]})


      #  connection.close()
      #  return {'items': items}
