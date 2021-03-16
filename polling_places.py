from geolocation import getGeolocation
import json

def getPollingPlaces(mysql):
    try:
        response = {}
        cur = mysql.connection.cursor()
        cur.execute("""SELECT P.id_place, P.name_place, P.address_show, P.id_city, C.city, P.latitude, P.lenght
                    FROM polling_places as P INNER JOIN citys as C ON P.id_city = C.id_city
                    """)
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                result[row[0]] = { "id_place": row[0], "name_place": row[1], "address_show": row[2], "id_city": row[3], "city": row[4], "latitude": row[5], "lenght": row[6] }

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        return ({"code":409})

def getPollingPlacebyId(mysql,id_place):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = """SELECT P.id_place, P.name_place, P.address_show, P.id_city, C.city, P.latitude, P.lenght
                FROM polling_places as P INNER JOIN citys as C ON P.id_city = C.id_city
                WHERE P.id_place = %s
                """
        cur.execute(sql, (id_place,))
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                result[row[0]] = { "id_place": row[0], "name_place": row[1], "address_show": row[2], "id_city": row[3], "city": row[4], "latitude": row[5], "lenght": row[6] }

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        return ({"code":409})

def insertPollingPlace(mysql,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = """SELECT city
                FROM citys 
                WHERE id_city = %s
                """
        cur.execute(sql, (request["id_city"],))
        data_city = cur.fetchone()
        # data = cur.fetchall()
        array_address = getGeolocation(request["address"],data_city[0])
        if type(request["id_city"]) == int and request["name_place"] != "" and array_address["address_show"] != "" and array_address["latitude"] != "" and array_address["lenght"] != "": 
            sql = """INSERT INTO polling_places (name_place, address_show, latitude, lenght, id_city)
                    VALUES (%s,%s,%s,%s,%s)
            """
            cur.execute(sql,(request["name_place"],array_address["address_show"],array_address["latitude"],array_address["lenght"],request["id_city"]))
            if cur.rowcount > 0:
                mysql.connection.commit()
                response["code"] = 200
                response["data"] = str(cur.lastrowid)
            else:
                response["code"] = 202
        else:
            response["code"] = 400                
        cur.close()
        return response
    except:
        return ({"code":409})

def updatePollingPlace(mysql,id_place,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = """SELECT city
                FROM citys 
                WHERE id_city = %s
                """
        cur.execute(sql, (request["id_city"],))
        data_city = cur.fetchone()
        # data = cur.fetchall()
        array_address = getGeolocation(request["address"],data_city[0])
        if type(id_place) == int and type(request["id_city"]) == int and request["name_place"] != "" and array_address["address_show"] != "" and array_address["latitude"] != "" and array_address["lenght"] != "":
            sql = """UPDATE polling_places 
                    SET name_place = %s, address_show = %s, latitude = %s, lenght = %s, id_city = %s 
                    WHERE id_place = %s
            """
            cur.execute(sql, (request["name_place"],array_address["address_show"],array_address["latitude"],array_address["lenght"],request["id_city"],id_place))
            if cur.rowcount > 0:
                mysql.connection.commit()
                response["code"] = 200
                response["data"] = '1'
            else:
                response["code"] = 202
        else:
            response["code"] = 400                
        cur.close()
        return response
    except:
        return ({"code":409})

def deletePollingPlace(mysql,id_place):
    try:
        response = {}
        cur = mysql.connection.cursor()
        if id_place and id_place != "": 
            sql = "DELETE FROM polling_places WHERE id_place = {0}"
            cur.execute(sql.format(id_place))
            # cur.execute(sql, (request["city"],id_place))
            if cur.rowcount > 0:
                mysql.connection.commit()
                response["code"] = 200
                response["data"] = '1'
            else:
                response["code"] = 202
        else:
            response["code"] = 400                
        cur.close()
        return response
    except:
        return ({"code":409})

