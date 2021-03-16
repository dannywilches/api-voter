import json

def getCitys(mysql):
    try:
        response = {}
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_city, city FROM citys")
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                result[row[0]] = { "id_city":row[0], "city": row[1] }

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        return ({"code":409})

def getCitybyId(mysql,id_city):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = "SELECT id_city, city FROM citys WHERE id_city = %s"
        cur.execute(sql, (id_city,))
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                result[row[0]] = { "id_city":row[0], "city": row[1] }

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        return ({"code":409})

def insertCity(mysql,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        if type(request["id_city"]) == int and request["city"] != "" and request["id_department"] != "": 
            sql = """INSERT INTO citys (id_city, country, id_department, city)
                    VALUES (%s,'CO',%s,%s)
            """
            cur.execute(sql,(request["id_city"],request["id_department"],request["city"]))
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

def updateCity(mysql,id_city,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        if request["city"] != "": 
            sql = "UPDATE citys SET city = %s WHERE id_city = %s"
            cur.execute(sql, (request["city"],id_city))
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

def deleteCity(mysql,id_city):
    try:
        response = {}
        cur = mysql.connection.cursor()
        if id_city and id_city != "": 
            sql = "DELETE FROM citys WHERE id_city = {0}"
            cur.execute(sql.format(id_city))
            # cur.execute(sql, (request["city"],id_city))
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

