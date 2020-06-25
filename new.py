import mysql.connector

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
import jsonpickle

# Create connection to DB


def connection_to_db():
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='crud'
    )
    return connection

# Create User class


class User:
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location


app = Flask(__name__)


@app.route('/users', methods=['GET'])
# Create getUser function to show data from DB
def getUsers():
    users = []
    connection = connection_to_db()
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM data'
    cursor.execute(query)

    for row in cursor:
        users.append(User(row['id'], row['name'], row['location']))

    connection.close()

    return Response(jsonpickle.encode(users, unpicklable=False), mimetype='application/json')


@app.route('/users', methods=['POST'])
# Create addUser function to insert data to DB
def addUser():
    request_data = request.get_json()

    try:
        connection = connection_to_db()
        cursor = connection.cursor()

        query = 'INSERT INTO data(name, location) VALUES(%(name)s, %(location)s)'
        cursor.execute(query, request_data)
        connection.commit()

    except mysql.connector.errors.IntegrityError as error:
        return jsonify(detail=error.msg), 400
    finally:
        connection.close()

    return request_data, 201

# Create function to update existing User in DB


@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    request_data = request.get_json()
    request_data['id'] = id

    try:
        connection = connection_to_db()
        cursor = connection.cursor()

        query = 'UPDATE data SET name=%(name)s, location=%(location)s WHERE id=%(id)s'
        cursor.execute(query, request_data)
        connection.commit()

    except mysql.connector.errors.IntegrityError as error:
        return jsonify(detail=error.msg), 400
    finally:
        connection.close()

    return request_data

# Create function to delete user from DB


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    request_data = {}
    request_data['id'] = id
    try:
        connection = connection_to_db()
        cursor = connection.cursor()

        query = 'DELETE from data WHERE id=%(id)s'
        cursor.execute(query, request_data)
        connection.commit()

    except mysql.connector.errors.IntegrityError as error:
        return jsonify(detail=error.msg), 400
    finally:
        connection.close()
    return jsonify()


app.run()
