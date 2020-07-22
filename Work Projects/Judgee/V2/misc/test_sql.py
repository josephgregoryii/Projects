import mysql.connector
print("making connection\n")
mydb = mysql.connector.connect(
    host="judgeedb.ctlyzwmrbgux.us-west-2.rds.amazonaws.com",
    user="admin_joe",
    password="U69g0321j_o",
    db="judgee_db"
    )
print("connection made")
print(mydb)
