from flask import Flask, jsonify, request, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carparts.dbs'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# class carPartsStore(db.Model):
#     __tablename__ = 'carParts'
#     id = db.column(db.Integer, primary_key = True)
#     carModel = db.collumn(db.String(30), nullable = False)
#     carPartCategory = db.collumn(db.String(30), nullable = False)


#     def __init__(self, carModel, carPartCategory):
#         self.carModel = carModel
#         carPartCategory = carPartCategory
#     def __repr__(self):
#         return 'id {}'.format(self.id)
    
@app.route("/")
def index():
    return "helloHEH"
if __name__ == "__main__":
    app.run(debug=True, port = 5000)

# @app.route('/carparts', methods=['GET'])
# def get_all():
#     carparts = carPartsStore.query.all()




