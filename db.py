import pyodbc, uuid

class ItemDatabase:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-66BPO70S;DATABASE=cafe')
        self.cursor = self.conn.cursor()

    def get_items(self):
        result = []
        query = "SELECT * From item"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["id"], item_dict["name"], item_dict["price"] = row
            result.append(item_dict)
        return result

    def get_item(self, item_id):
        query = f"select * from item where id = '{item_id}'" 
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["id"], item_dict["name"], item_dict["price"] = row
            return [item_dict]

    def add_item(self, id, body):
        query = f"insert into item(id, name, price) values ('{id}', '{body['name']}', {body['price']})" 
        self.cursor.execute(query)
        self.conn.commit()

    def update_item(self, id, body):
        query = f"update item set name = '{body['name']}', price = '{body['price']}' where id = '{id}'"
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_item(self, id):
        query = f"delete from item where id = '{id}'" 
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount > 0


# db = ItemDatabase()
# print(db.get_items())
# print(db.get_item('96128a4f82c7435f8defc9a72c28c7e3'))

# db.add_item(id=uuid.uuid4().hex, body={'name':'rudra', 'price':80})
# db.update_item(id='bd801ccd6df24779879c8b0e239eecaf', body={'name':'Rewa', 'price':80})
# print(db.delete_item('db2f047a62354481b381e0fa7b834549'))