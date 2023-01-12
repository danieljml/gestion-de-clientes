from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "system"

mysql = MySQL(app)

@app.route('/api/customer/<int:id>') #GET
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT id, firstname, lastname, email, phone, address FROM customers WHERE id={id}")
    data = cur.fetchall()
    for row in data:
        return jsonify({'id': row[0], 'firstname': row[1], 'lastname': row[2], 'email': row[3], 'phone': row[4], 'address': row[5]})

@app.route('/api/customer') #GET
@cross_origin()
def getAllCustomer():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, firstname, lastname, email, phone, address FROM customers")
    data = cur.fetchall()
    result = []
    for row in data:
        result.append({'id': row[0], 'firstname': row[1], 'lastname': row[2], 'email': row[3], 'phone': row[4], 'address': row[5]})
    return jsonify(result)

@app.route('/api/customer', methods=['POST']) #POST
@cross_origin()
def saveCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `phone`, `address`) VALUES (NULL, %s, %s, %s, %s, %s);", 
                (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address']))
    mysql.connection.commit()
    return "Cliente guardado"

@app.route('/api/customer', methods=['PUT']) #POST
@cross_origin()
def updateCustomer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `customers` SET `firstname` = %s, `lastname` = %s, `email` = %s, `phone` = %s, `address` = %s WHERE `customers`.`id` = %s;", 
                (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address'], request.json['id']))
    mysql.connection.commit()
    return "Cliente guardado"


@app.route('/api/customer/<int:id>', methods=['DELETE']) #DELETE
@cross_origin()
def deleteCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM `customers` WHERE `customers`.`id` = {id}")
    mysql.connection.commit()
    return f"El id del cliente eliminado es {id}"

@app.route('/')
@cross_origin()
def index():
    return "Hello Daniel"

app.run(None, 3000, True)
    