from geolocation import getGeolocation
import json

def getLeaders(mysql):
    try:
        response = {}
        cur = mysql.connection.cursor()
        print("""SELECT L.id_user, L.names, L.last_names, L.document, L.phone, L.address_show, L.latitude, L.lenght, L.id_city, C.city, L.id_profile, P.description
                    FROM users as L INNER JOIN citys as C ON L.id_city = C.id_city INNER JOIN profiles as P ON L.id_profile = P.id_profile
                    WHERE L.id_profile = 2
                    """)                    
        cur.execute("""SELECT L.id_user, L.names, L.last_names, L.document, L.phone, L.address_show, L.latitude, L.lenght, L.id_city, C.city, L.id_profile, P.description
                    FROM users as L INNER JOIN citys as C ON L.id_city = C.id_city INNER JOIN profiles as P ON L.id_profile = P.id_profile
                    WHERE L.id_profile = 2
                    """)
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                print (row)
                result[row[0]] = { "id_leader": row[0], "names": row[1], "last_names": row[2], "document": row[3], "phone": row[4], "address_show": row[5], "latitude": row[6], "lenght": row[7], "id_city": row[8], "city": row[9], "id_profile": row[10], "profile": row[11] }
            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        print("Error getLeaders")
        return ({"code":409})

def getLeaderbyId(mysql,id_leader):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = """SELECT L.id_user, L.names, L.last_names, L.document, L.phone, L.address_show, L.latitude, L.lenght, L.id_city, C.city, L.id_profile, P.description
                FROM users as L INNER JOIN citys as C ON L.id_city = C.id_city INNER JOIN profiles as P ON L.id_profile = P.id_profile
                WHERE L.id_user = %s
                """
        cur.execute(sql, (id_leader,))
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                print (row)
                result[row[0]] = { "id_leader": row[0], "names": row[1], "last_names": row[2], "document": row[3], "phone": row[4], "address_show": row[5], "latitude": row[6], "lenght": row[7], "id_city": row[8], "city": row[9], "id_profile": row[10], "profile": row[11] }

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        print(response)
        cur.close()
        return response
    except:
        print("Error getLeaderbyId")
        return ({"code":409})

def insertLeader(mysql,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        print("esto",request)
        sql = """SELECT city
                FROM citys 
                WHERE id_city = %s
                """
        cur.execute(sql, (request["id_city"],))
        data_city = cur.fetchone()
        # data = cur.fetchall()
        print(data_city[0])
        # print(cur.fetchone())
        array_address = getGeolocation(request["address"],data_city[0])
        print(array_address)
        if type(request["id_city"]) == int and request["names"] != "" and request["last_names"] != "" and request["document"] != "" and request["phone"] != "" and array_address["address_show"] != "" and array_address["latitude"] != "" and array_address["lenght"] != "": 
            sql = """INSERT INTO users (names, last_names, document, phone, address_show, latitude, lenght, id_city, id_profile, status_user)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,2,1)
            """
            print(sql)
            cur.execute(sql,(request["names"],request["last_names"],request["document"],request["phone"],array_address["address_show"],array_address["latitude"],array_address["lenght"],request["id_city"]))
            if cur.rowcount > 0:
                mysql.connection.commit()
                response["code"] = 200
                response["data"] = str(cur.lastrowid)
            else:
                response["code"] = 202
        else:
            response["code"] = 400                
        print(response)
        cur.close()
        return response
    except:
        print("Error insertLeader")
        return ({"code":409})

def updateLeader(mysql,id_leader,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        print("esto",request)
        sql = """SELECT city
                FROM citys 
                WHERE id_city = %s
                """
        cur.execute(sql, (request["id_city"],))
        data_city = cur.fetchone()
        # data = cur.fetchall()
        print(data_city[0])
        # print(cur.fetchone())
        array_address = getGeolocation(request["address"],data_city[0])
        print(array_address)
        print(type(id_leader))
        if type(id_leader) == int and type(request["id_city"]) == int and request["names"] != "" and request["last_names"] != "" and request["document"] != "" and request["phone"] != "" and array_address["address_show"] != "" and array_address["latitude"] != "" and array_address["lenght"] != "":
            sql = """UPDATE users 
                    SET names= %s, last_names= %s, document= %s, phone= %s, address_show= %s, latitude= %s, lenght= %s, id_city= %s
                    WHERE id_user = %s
            """
            cur.execute(sql, (request["names"],request["last_names"],request["document"],request["phone"],array_address["address_show"],array_address["latitude"],array_address["lenght"],request["id_city"],id_leader))
            if cur.rowcount > 0:
                mysql.connection.commit()
                response["code"] = 200
                response["data"] = '1'
            else:
                response["code"] = 202
        else:
            response["code"] = 400                
        print(response)
        cur.close()
        return response
    except:
        print("Error updateLeader")
        return ({"code":409})

def deleteLeader(mysql,id_leader):
    try:
        response = {}
        cur = mysql.connection.cursor()
        if id_leader and id_leader != "": 
            sql = "DELETE FROM users WHERE id_user = {0} AND id_profile = 2"
            cur.execute(sql.format(id_leader))
            if cur.rowcount > 0:
                mysql.connection.commit()
                response["code"] = 200
                response["data"] = '1'
            else:
                response["code"] = 202
        else:
            response["code"] = 400                
        print(response)
        cur.close()
        return response
    except:
        print("Error deleteLeader")
        return ({"code":409})

