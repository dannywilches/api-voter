from geolocation import getGeolocation
import json

def getVoters(mysql):
    try:
        response = {}
        cur = mysql.connection.cursor()
        cur.execute("""SELECT V.id_voter, V.names, V.last_names, V.document, V.phone, V.address_show, V.latitude, V.lenght, V.id_city, C.city, V.id_leader, CONCAT(U.names,' ',U.last_names), V.id_place, V.voting_table
                    FROM voters as V INNER JOIN citys as C ON V.id_city = C.id_city INNER JOIN users as U ON V.id_leader = U.id_user
                    """)
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                print (row)
                result[row[0]] = { "id_voter": row[0], "names": row[1], "last_names": row[2], "document": row[3], "phone": row[4], "address_show": row[5], "latitude": row[6], "lenght": row[7], "id_city": row[8], "city": row[9], "id_leader": row[10], "name_leader": row[11], "id_place": row[12], "voting_table": row[13] }
            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        print("Error getVoters")
        return ({"code":409})

def getVoterbyId(mysql,id_voter):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = """SELECT V.id_voter, V.names, V.last_names, V.document, V.phone, V.address_show, V.latitude, V.lenght, V.id_city, C.city, V.id_leader, CONCAT(U.names,' ',U.last_names), V.id_place, V.voting_table
                FROM voters as V INNER JOIN citys as C ON V.id_city = C.id_city INNER JOIN users as U ON V.id_leader = U.id_user
                WHERE V.id_voter = %s
                """
        cur.execute(sql, (id_voter,))
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                print (row)
                result[row[0]] = { "id_voter": row[0], "names": row[1], "last_names": row[2], "document": row[3], "phone": row[4], "address_show": row[5], "latitude": row[6], "lenght": row[7], "id_city": row[8], "city": row[9], "id_leader": row[10], "name_leader": row[11], "id_place": row[12], "voting_table": row[13]}

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        print(response)
        cur.close()
        return response
    except:
        print("Error getVoterbyId")
        return ({"code":409})

def insertVoter(mysql,request):
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
        if type(request["id_city"]) == int and type(request["id_place"]) == int and type(request["id_leader"]) == int and request["names"] != "" and request["last_names"] != "" and request["document"] != "" and request["phone"] != "" and array_address["address_show"] != "" and array_address["latitude"] != "" and array_address["lenght"] != "" and request["voting_table"] != "": 
            sql = """INSERT INTO voters (names, last_names, document, phone, address_show, latitude, lenght, id_city, id_place, id_leader, voting_table)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            print(sql)
            cur.execute(sql,(request["names"],request["last_names"],request["document"],request["phone"],array_address["address_show"],array_address["latitude"],array_address["lenght"],request["id_city"],request["id_place"],request["id_leader"],request["voting_table"]))
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
        print("Error insertVoter")
        return ({"code":409})

def updateVoter(mysql,id_voter,request):
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
        print(type(id_voter))
        print(type(request["id_place"]))
        if type(id_voter) == int and type(request["id_city"]) == int and type(request["id_place"]) == int and request["names"] != "" and request["last_names"] != "" and request["document"] != "" and request["phone"] != "" and array_address["address_show"] != "" and array_address["latitude"] != "" and array_address["lenght"] != "" and request["voting_table"] != "":
            print("""UPDATE voters 
                    SET names= %s, last_names= %s, document= %s, phone= %s, address_show= %s, latitude= %s, lenght= %s, id_city= %s, id_place= %s, voting_table= %s
                    WHERE id_voter = %s
            """)
            sql = """UPDATE voters 
                    SET names= %s, last_names= %s, document= %s, phone= %s, address_show= %s, latitude= %s, lenght= %s, id_city= %s, id_place= %s, voting_table= %s
                    WHERE id_voter = %s
            """
            cur.execute(sql, (request["names"],request["last_names"],request["document"],request["phone"],array_address["address_show"],array_address["latitude"],array_address["lenght"],request["id_city"],request["id_place"],request["voting_table"],id_voter))
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
        print("Error updateVoter")
        return ({"code":409})

def deleteVoter(mysql,id_voter):
    try:
        response = {}
        cur = mysql.connection.cursor()
        if id_voter and id_voter != "": 
            sql = "DELETE FROM voters WHERE id_voter = {0}"
            cur.execute(sql.format(id_voter))
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
        print("Error deleteVoter")
        return ({"code":409})

