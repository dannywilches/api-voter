from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mysqldb import MySQL
from citys import *
from departments import *
from polling_places import *
from voters import *
from leaders import *
from login import makeLogin
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
FlaskJSON(app)

CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'api_voters'
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'super-secret'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Por favor inicie sesión'}), 403
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({'message': 'Token invalido'}), 403

        return f(*args,**kwargs)
    return decorated

# @app.route('/unprotected')
# def unprotected():
#     return jsonify({'message': 'Cualquiera puede acceder'})

# @app.route('/protected')
# @token_required
# def protected():
#     return jsonify({'message': 'Solo disponible a usuarios logeados'})


def result_to_response(result):
    response = []
    if result["code"] == 200:
        message = "Correct!"
        response = json.loads(result["data"])
    elif result["code"] == 202:
        message = "No se pudo ejecutar la acción"
    elif result["code"] == 204:
        message = "Resultado sin información"
    elif result["code"] == 400:
        message = "Los datos enviados son incosistentes o hacen falta datos"
    elif result["code"] == 403:
        message = "Por favor inicia sesión"
    elif result["code"] == 405:
        message = "El uso del método no está permitido"
    elif result["code"] == 409:
        message = "No se pudo completar la petición"
    return json_response(status=result["code"], message=message, data=response)

@app.route('/')
def index():
    return("Welcome Index")

# Function Login

@app.route('/login', methods=["POST"])
def login():
    print(request.get_json(force=True))
    data = request.get_json(force=True)
    auth = makeLogin(mysql,data)    
    if auth["login"]:
        token = jwt.encode({'user': auth["user_id"], 'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=30) }, app.config["SECRET_KEY"])
        return jsonify({'token:': token.decode('UTF-8')})

    return make_response('Without verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Functions Citys

@app.route('/citys', methods=["GET"])
@token_required
def showCitys():
    if request.method == 'GET':
        # data = request.get_json(force=True)
        response = getCitys(mysql)
        return result_to_response(response)

@app.route('/citys/<int:id_city>', methods=["GET"])
@token_required
def showCitysbyId(id_city):
    if request.method == 'GET':
        response = getCitybyId(mysql,id_city)
        return result_to_response(response)

@app.route('/citys/add', methods=["POST"])
@token_required
def addCity():
    if request.method == 'POST':
        data = request.get_json(force=True)
        response = insertCity(mysql,data)
        return result_to_response(response)

@app.route('/citys/update/<int:id_city>', methods=["PUT"])
@token_required
def updCity(id_city):
    if request.method == 'PUT':
        data = request.get_json(force=True)
        response = updateCity(mysql,id_city,data)
        return result_to_response(response)

@app.route('/citys/delete/<int:id_city>', methods=["DELETE"])
@token_required
def delCity(id_city):
    if request.method == 'DELETE':
        response = deleteCity(mysql,id_city)
        return result_to_response(response)

# Functions Departments

@app.route('/departments', methods=["GET"])
@token_required
def showDepartments():
    if request.method == 'GET':
        response = getDepartments(mysql)
        return result_to_response(response)

@app.route('/departments/<int:id_department>', methods=["GET"])
@token_required
def showDepartmentsbyId(id_department):
    if request.method == 'GET':
        response = getDepartmentbyId(mysql,id_department)
        return result_to_response(response)

@app.route('/departments/add', methods=["POST"])
@token_required
def addDepartment():
    if request.method == 'POST':
        data = request.get_json(force=True)
        response = insertDepartment(mysql,data)
        return result_to_response(response)

@app.route('/departments/update/<int:id_department>', methods=["PUT"])
@token_required
def updDepartment(id_department):
    if request.method == 'PUT':
        data = request.get_json(force=True)
        response = updateDepartment(mysql,id_department,data)
        return result_to_response(response)

@app.route('/departments/delete/<int:id_department>', methods=["DELETE"])
@token_required
def delDepartment(id_department):
    if request.method == 'DELETE':
        response = deleteDepartment(mysql,id_department)
        return result_to_response(response)

# Functions Polling Places

@app.route('/polling_places', methods=["GET"])
@token_required
def showPollingPlaces():
    if request.method == 'GET':
        response = getPollingPlaces(mysql)
        return result_to_response(response)

@app.route('/polling_places/<int:id_place>', methods=["GET"])
@token_required
def showPollingPlacebyId(id_place):
    if request.method == 'GET':
        response = getPollingPlacebyId(mysql,id_place)
        return result_to_response(response)

@app.route('/polling_places/add', methods=["POST"])
@token_required
def addPollingPlace():
    if request.method == 'POST':
        data = request.get_json(force=True)
        response = insertPollingPlace(mysql,data)
        return result_to_response(response)

@app.route('/polling_places/update/<int:id_place>', methods=["PUT"])
@token_required
def updPollingPlace(id_place):
    if request.method == 'PUT':
        data = request.get_json(force=True)
        response = updatePollingPlace(mysql,id_place,data)
        return result_to_response(response)

@app.route('/polling_places/delete/<int:id_place>', methods=["DELETE"])
@token_required
def delPollingPlace(id_place):
    if request.method == 'DELETE':
        response = deletePollingPlace(mysql,id_place)
        return result_to_response(response)

# Functions Voters

@app.route('/voters', methods=["GET"])
@token_required
def showVoters():
    if request.method == 'GET':
        response = getVoters(mysql)
        return result_to_response(response)

@app.route('/voters/<int:id_voter>', methods=["GET"])
@token_required
def showVoterbyId(id_voter):
    if request.method == 'GET':
        response = getVoterbyId(mysql,id_voter)
        return result_to_response(response)

@app.route('/voters/add', methods=["POST"])
@token_required
def addVoter():
    if request.method == 'POST':
        data = request.get_json(force=True)
        response = insertVoter(mysql,data)
        return result_to_response(response)

@app.route('/voters/update/<int:id_voter>', methods=["PUT"])
@token_required
def updVoter(id_voter):
    if request.method == 'PUT':
        data = request.get_json(force=True)
        response = updateVoter(mysql,id_voter,data)
        return result_to_response(response)

@app.route('/voters/delete/<int:id_voter>', methods=["DELETE"])
@token_required
def delVoter(id_voter):
    if request.method == 'DELETE':
        response = deleteVoter(mysql,id_voter)
        return result_to_response(response)

# Functions Leaders

@app.route('/leaders', methods=["GET"])
@token_required
def showLeaders():
    if request.method == 'GET':
        response = getLeaders(mysql)
        return result_to_response(response)

@app.route('/leaders/<int:id_leader>', methods=["GET"])
@token_required
def showLeaderbyId(id_leader):
    if request.method == 'GET':
        response = getLeaderbyId(mysql,id_leader)
        return result_to_response(response)

@app.route('/leaders/add', methods=["POST"])
@token_required
def addLeader():
    if request.method == 'POST':
        data = request.get_json(force=True)
        response = insertLeader(mysql,data)
        return result_to_response(response)

@app.route('/leaders/update/<int:id_leader>', methods=["PUT"])
@token_required
def updLeader(id_leader):
    if request.method == 'PUT':
        data = request.get_json(force=True)
        response = updateLeader(mysql,id_leader,data)
        return result_to_response(response)

@app.route('/leaders/delete/<int:id_leader>', methods=["DELETE"])
@token_required
def delLeader(id_leader):
    if request.method == 'DELETE':
        response = deleteLeader(mysql,id_leader)
        return result_to_response(response)

# Functions Reports

# @app.route('/login', methods=["GET"])
# def showLeaders():
#     if request.method == 'GET':
#         response = getLeaders(mysql)
#         return result_to_response(response)

# @app.route('/leaders/<int:id_leader>', methods=["GET"])
# def showLeaderbyId(id_leader):
#     if request.method == 'GET':
#         response = getLeaderbyId(mysql,id_leader)
#         return result_to_response(response)

# @app.route('/leaders/add', methods=["POST"])
# def addLeader():
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#         response = insertLeader(mysql,data)
#         return result_to_response(response)

# @app.route('/leaders/update/<int:id_leader>', methods=["PUT"])
# def updLeader(id_leader):
#     if request.method == 'PUT':
#         data = request.get_json(force=True)
#         response = updateLeader(mysql,id_leader,data)
#         return result_to_response(response)

# @app.route('/leaders/delete/<int:id_leader>', methods=["DELETE"])
# def delLeader(id_leader):
#     if request.method == 'DELETE':
#         response = deleteLeader(mysql,id_leader)
#         return result_to_response(response)

if __name__ == "__main__":
    app.run(port= 3000, debug=True)
    