def makeLogin(mysql,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = """SELECT id_user
                FROM login_user
                WHERE username = %s and password = %s
                """
        cur.execute(sql, (request['username'],request["password"]))
        print("llego aca")
        # data = cur.fetchall()
        print(cur.rowcount)
        if cur.rowcount > 0:
            data_login = cur.fetchone()
            response["code"] = 200
            response["user_id"] = data_login[0]
            response["login"] = True
        else:
            response["code"] = 204
            response["login"] = False
        print(response)
        cur.close()
        return response
    except:
        print("Error getVoterbyId")
        return ({"code":409, "login": False})