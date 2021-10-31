from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

POSTGRES = {
    'user': 'rocketlane',
    'pw': 'rocketlane',
    'db': 'rocketlane',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# Database instance 
db = SQLAlchemy(app)


def get_json(customer):
     return jsonify({
            "firstName": customer.firstName,
            "lastName": customer.lastName,
            "address": customer.address,
            "city": customer.city,
            "email": customer.email,
            "mobile": customer.mobile,
            "id": customer.id,
        })

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)

    def __init__(self, firstName, lastName, email, mobile, address, city) -> None:
        super().__init__()
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobile = mobile
        self.address = address
        self.city = city


@app.route('/', methods=["POST"])
def index():
    if request.method == 'POST':
        customer = Customers(firstName=request.form.get('firstName'), lastName=request.form.get('lastName'), address=request.form.get('address'),
                             city=request.form.get('city'), email=request.form.get('email'), mobile=request.form.get('mobile'))
        db.session.add(customer)
        db.session.commit()
        return get_json(customer)


@app.route('/<int:id>',methods= ["PUT","GET","DELETE"])
def get(id):
    customer = Customers.query.filter_by(id=id).first()
    if request.method == 'GET':
        print(customer)
        return get_json(customer)

    elif request.method == 'PUT':
        print(request.form.get('email'))
        customer.firstName = request.form.get("firstName")  if request.form.get("firstName") is not None else customer.firstName
        customer.lastName = request.form.get("lastName")  if request.form.get("lastName") is not None else customer.lastName
        customer.address = request.form.get("address")  if request.form.get("address") is not None else customer.address
        customer.city = request.form.get("city")  if request.form.get("city") is not None else customer.city
        customer.email = request.form.get("email")  if request.form.get("email") is not None else customer.email
        customer.mobile = request.form.get("mobile")  if request.form.get("mobile") is not None else customer.mobile
        db.session.commit()
        return get_json(customer) 

    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"deleted":True})


if __name__ == '__main__':
    db.create_all()
    db.init_app(app)
    app.run(debug=True)
