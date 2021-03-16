def makeLogin(mysql,request):
    try:
        response = {}
        cur = mysql.connection.cursor()
        sql = """SELECT id_user
                FROM login_user
                WHERE username = %s and password = %s
                """
        cur.execute(sql, (request['username'],request["password"]))
        # data = cur.fetchall()
        if cur.rowcount > 0:
            data_login = cur.fetchone()
            response["code"] = 200
            response["user_id"] = data_login[0]
            response["login"] = True
        else:
            response["code"] = 204
            response["login"] = False
        cur.close()
        return response
    except:
        return ({"code":409, "login": False})