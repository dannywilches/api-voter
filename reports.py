import json

def getReportGeneralbyLeader(mysql):
    try:
        response = {}
        cur = mysql.connection.cursor()
        cur.execute("""SELECT V.id_voter, CONCAT(V.names, ' ',V.last_names), V.document, V.phone, V.address_show, C.city, V.voting_table, CONCAT(L.names, ' ',L.last_names)
                    FROM voters as V INNER JOIN citys as C ON V.id_city = C.id_city INNER JOIN users as L ON V.id_leader = L.id_user
                """)
        data = cur.fetchall()
        if cur.rowcount > 0:
            result = {}
            cant = 0
            for row in data:
                print (row)
                result[row[0]] = { "id_voter":row[0], "name_voter": row[1], "document": row[2], "phone": row[3], "address_show": row[4], "city": row[5], "voting_table": row[6], "name_leader": row[7] }
                cant = cant+1

            response["code"] = 200
            response["data"]["quantity"] = cant
            response["data"] = json.dumps(result)
        else:
            response["code"] = 204
        cur.close()
        return response
    except:
        print("Error getGeneralbyLeader")
        return ({"code":409})

# def getCitybyId(mysql,id_city):
#     try:
#         response = {}
#         cur = mysql.connection.cursor()
#         sql = "SELECT id_city, city FROM citys WHERE id_city = %s"
#         cur.execute(sql, (id_city,))
#         data = cur.fetchall()
#         if cur.rowcount > 0:
#             result = {}
#             for row in data:
#                 print (row)
#                 result[row[0]] = { "id_city":row[0], "city": row[1] }

#             response["code"] = 200
#             response["data"] = json.dumps(result)
#         else:
#             response["code"] = 204
#         print(response)
#         cur.close()
#         return response
#     except:
#         print("Error getCitybyId")
#         return ({"code":409})
