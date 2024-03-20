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

class autoParts():
    def __init__(self, partId, partName, manufacturer, carBrand, category):
        self.partId = partId
        self.name = partName,
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

listOfParts1 = []
listOfParts1.append(autoParts(2345, 'stabilizatorius', 'febi','Ford','vaziuokle'))
listOfParts1.append(autoParts(2346, 'vairo kolonele', 'stihl','Volvo','vairo mechanizmas'))
listOfParts1.append(autoParts(4555, 'tepalai', 'Liqui Molly','Volvo','Aptarnavimas'))

listOfParts2 = []
listOfParts2.append(autoParts(133, 'kaladeles', 'brembo','bmw','stabdziai'))
listOfParts2.append(autoParts(999, 'stabdziu diskai', 'zimmerman','audi','stabdziai'))
# autoPartsStore1 = autoPartsStore(1,"Rahul",listOfParts1)
# autoPartsStore2 = autoPartsStore(2,"Patel",listOfParts2)

autoPartsStoreList = []
autoPartsStoreList.append(autoPartsStore(1,"Rahul",listOfParts1))
autoPartsStoreList.append(autoPartsStore(2,"Patel",listOfParts2))



    
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

@app.route("/all")
def showAll():
    jasonObject = []
    for autoPartsShops in autoPartsStoreList:
        temporary = {}
        temporary['shopId'] = autoPartsShops.shopId
        temporary['owner'] = autoPartsShops.owner
        temporary['listOfShops'] = [part.to_dict() for part in autoPartsShops.listOfShops]
        jasonObject.append(temporary)
    return jsonify(jasonObject)

@app.route("/show/store/<int:store_ID>", methods=['GET'])
def show1(store_ID):
    jasonObject = []

    for autoPartsShop in autoPartsStoreList:
        if autoPartsShop.shopId == store_ID:
            temporary = {}
            temporary['shopId'] = autoPartsShop.shopId
            temporary['owner'] = autoPartsShop.owner
            temporary['listOfShops'] = [part.to_dict() for part in autoPartsShop.listOfShops]
            jasonObject.append(temporary)
            break
    return jsonify(jasonObject)

@app.route("/show/part/<int:part_id>", methods=['GET'])
def show2(part_id):
    jasonObject = []

    for autoPartsStore in autoPartsStoreList:
        for part in autoPartsStore.listOfShops:
            if part.partId == part_id:
                temporary = part.to_dict()
                jasonObject.append(temporary)
                break

    return jsonify(jasonObject)
# @app.route('/carparts', methods=['GET'])
# def get_all():
#     carparts = carPartsStore.query.all()
    

@app.route('/add/store', methods=['GET', 'POST'])
def add():
    return "1"
@app.route('/add/part', methods=['GET', 'POST'])
def add2():
    return "1"
@app.route('/update/store/<int:id>', methods=['GET', 'POST'])
def update():
    return "1"
@app.route('/update/part/<int:id>', methods=['GET', 'POST'])
def update2():
    return "1"
@app.route('/delete/store/<int:id>')
def delete():
    return "1"
@app.route('/delete/part/<int:id>')
def delete2():
    return "1"


if __name__ == "__main__":
    app.run(debug=True, port = 5000)