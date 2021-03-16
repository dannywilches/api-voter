import json

def getDepartments(mysql):
    try:
        response = {}
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_department, department FROM departments")
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                print (row)
                result[row[0]] = { "id_department":row[0], "department": row[1] }

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        print("Error getdepartments")
        return ({"code":409})

def getDepartmentbyId(mysql,id_department):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = "SELECT id_department, department FROM departments WHERE id_department = %s"
        cur.execute(sql, (id_department,))
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            for row in data:
                print (row)
                result[row[0]] = { "id_department":row[0], "department": row[1] }

            response["code"] = 200
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        print(response)
        cur.close()
        return response
    except:
        print("Error getDepartmentbyId")
        return ({"code":409})

def insertDepartment(mysql,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        print("esto",request)
        if type(request["id_department"]) == int and request["department"] != "": 
            sql = """INSERT INTO departments (id_department, country, department)
                    VALUES (%s,'CO',%s)
            """
            print(sql)
            cur.execute(sql,(request["id_department"],request["department"]))
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
        print("Error insertDepartment")
        return ({"code":409})

def updateDepartment(mysql,id_department,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        print("esto",request["department"])
        if request["department"] != "": 
            sql = "UPDATE departments SET department = %s WHERE id_department = %s"
            cur.execute(sql, (request["department"],id_department))
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
        print("Error updateDepartment")
        return ({"code":409})

def deleteDepartment(mysql,id_department):
    try:
        response = {}
        cur = mysql.connection.cursor()
        if id_department and id_department != "": 
            sql = "DELETE FROM departments WHERE id_department = {0}"
            cur.execute(sql.format(id_department))
            # cur.execute(sql, (request["department"],id_department))
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
        print("Error deleteDepartment")
        return ({"code":409})

