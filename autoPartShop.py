from flask import Flask, jsonify, request, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.mutable import MutableSet
from sqlalchemy.ext.mutable import MutableDict
# from autoDaliuParduotuveUI import UI
app = Flask(__name__)

# app.register_blueprint(UI, url_prefix="/")
with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autoPartsShops.dbs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
# db.init_app(app)

class autoPartsStore(db.Model):
    __tablename__ = 'autoPartsShops'
    _shopId = db.Column("id", db.Integer, primary_key = True)
    owner = db.Column(db.String(50))
    listOfShops = db.Column(MutableList.as_mutable(PickleType), default=[])
    def __init__(self, shopId, owner, listOfShops):
        self.shopId = shopId
        self.owner = owner
        self.listOfShops = listOfShops
    def __repr__(self):
        return 'id {}'.format(self.shopId)
    def to_dict(self):
        return {
            'shopId': self._shopId,
            'owner': self.owner,
            'listOfShops': [part.to_dict() for part in self.listOfShops]
        }

class autoParts():
    def __init__(self, partId, name, manufacturer, carBrand, category):
        self.partId = partId
        self.name = name,
        self.manufacturer = manufacturer
        self.carBrand = carBrand
        self.category = category

    def to_dict(self):
        return {
        'partId': self.partId,
        'partName': self.name,
        'manufacturer': self.manufacturer,
        'carBrand': self.carBrand,
        'category': self.category
        }
    
    
# parts1 = [
#     autoParts(partId=2345, name='stabilizatorius', manufacturer='febi', carBrand='Ford', category='vaziuokle'),
#     autoParts(partId=2346, name='vairo kolonele', manufacturer='stihl', carBrand='Volvo', category='vairo mechanizmas'),
#     autoParts(partId=4555, name='tepalai', manufacturer='Liqui Molly', carBrand='Volvo', category='Aptarnavimas')
# ]
# store1 = autoPartsStore(shopId=0, owner='Rahul', listOfShops=parts1)

# parts2 = [
#     autoParts(partId=133, name='kaladeles', manufacturer='brembo', carBrand='bmw', category='stabdziai'),
#     autoParts(partId=999, name='stabdziu diskai', manufacturer='zimmerman', carBrand='audi', category='stabdziai')
# ]
# store2 = autoPartsStore(shopId=1, owner='Patel', listOfShops=parts2)

# db.session.add_all([store1, store2])
# db.session.commit()

# listOfParts1 = []
# listOfParts1.append(autoParts(2345, 'stabilizatorius', 'febi','Ford','vaziuokle'))
# listOfParts1.append(autoParts(2346, 'vairo kolonele', 'stihl','Volvo','vairo mechanizmas'))
# listOfParts1.append(autoParts(4555, 'tepalai', 'Liqui Molly','Volvo','Aptarnavimas'))

# listOfParts2 = []
# listOfParts2.append(autoParts(133, 'kaladeles', 'brembo','bmw','stabdziai'))
# listOfParts2.append(autoParts(999, 'stabdziu diskai', 'zimmerman','audi','stabdziai'))

# autoPartsStoreList = []
# autoPartsStoreList.append(autoPartsStore(1,"Rahul",listOfParts1))
# autoPartsStoreList.append(autoPartsStore(2,"Patel",listOfParts2))

# db.session.add(autoPartsStoreList)
# db.session.add(autoPartsStore(1,"Rahul",listOfParts1))
# db.session.add(autoPartsStore(2,"Patel", listOfParts2))


    
# class autoParts(db.Model):
#     _id = db.Column("id", db.Integer, primary_key = True)
#     def __init__(self, partId, manufacturer, make, category):
#         self.partId = partId
#         self.manufacturer = manufacturer
#         self.make = make
#         self.category = category



@app.route("/")
def index():
    return "welcome to the homePage"

@app.route("/all", methods=['GET'])
def showAll():

    stores = autoPartsStore.query.all()
    return jsonify([store.to_dict() for store in stores])


@app.route("/show/store/<int:store_ID>", methods=['GET'])
def show1(store_ID):
    store = autoPartsStore.query.get(store_ID)
    if store:
        return jsonify(store.to_dict())
    else:
        return jsonify({'message': 'Store not found'}), 404

@app.route("/show/part/<int:part_id>", methods=['GET'])
def show2(part_id):
    parts = []
    stores = autoPartsStore.query.all()
    
    for store in stores:
        for part in store.listOfShops:
            if part.partId == part_id:
                parts.append(part.to_dict())
                break

    if parts:
        return jsonify(parts)
    else:
        return jsonify({'message': 'Part not found'}), 404

@app.route('/update/<store_id>', methods=['PUT'])
def update2(store_id):
    store = autoPartsStore.query.get(store_id)

    if store:
        data = request.get_json()
        if 'owner'in data:
            store.owner = data['owner']
        updated_list = request.get_json()['listOfShops']
        store.listOfShops = [autoParts(**data) for data in updated_list]
        db.session.commit()
        return jsonify({'message': 'Store updated successfully'})
    else:
        return jsonify({'message': 'Store not found'}), 404

@app.route('/create/store', methods=['POST'])
def create_store():
    data = request.get_json()
    owner_name = data['owner']
    list_of_parts = [autoParts(**part_data) for part_data in data['listOfParts']]
    max_shop_id = db.session.query(db.func.max(autoPartsStore._shopId)).scalar()
    new_shop_id = (max_shop_id or 0) + 1  # Increment the maximum shopId by 1
    new_store = autoPartsStore(new_shop_id,owner=owner_name, listOfShops=list_of_parts)
    db.session.add(new_store)
    db.session.commit()

    return jsonify({'message': 'Store created successfully', 'id': new_store.shopId}), 201


@app.route('/delete/store/<int:id>', methods = ['DELETE'])
def delete(id):
    store = autoPartsStore.query.get(id)
    if store:
        db.session.delete(store)
        db.session.commit()
        return jsonify({'message': 'Store deleted successfully'})
    else:
        return jsonify({'message': 'Store not found'}), 404
    
@app.route('/deleteAll', methods=['DELETE'])
def deleteAll():
    try:
        # Delete all autoPartsStore records
        db.session.query(autoPartsStore).delete()
        db.session.commit()
        return jsonify({'message': 'All stores deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not autoPartsStore.query.first():
            parts1 = [
                autoParts(partId=2345, name='stabilizatorius', manufacturer='febi', carBrand='Ford', category='vaziuokle'),
                autoParts(partId=2346, name='vairo kolonele', manufacturer='stihl', carBrand='Volvo', category='vairo mechanizmas'),
                autoParts(partId=4555, name='tepalai', manufacturer='Liqui Molly', carBrand='Volvo', category='Aptarnavimas')
            ]
            store1 = autoPartsStore(shopId=1, owner='Rahul', listOfShops=parts1)
            db.session.add(store1)
            
            parts2 = [
                autoParts(partId=133, name='kaladeles', manufacturer='brembo', carBrand='bmw', category='stabdziai'),
                autoParts(partId=999, name='stabdziu diskai', manufacturer='zimmerman', carBrand='audi', category='stabdziai')
            ]
            store2 = autoPartsStore(shopId=2, owner='Patel', listOfShops=parts2)
            db.session.add(store2)

            db.session.commit()
    app.run(debug=True, port = 5000)