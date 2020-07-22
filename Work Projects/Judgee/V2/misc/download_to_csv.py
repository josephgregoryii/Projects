import mysql.connector
import database_functions
import csv

if __name__ == "__main__":
    # create connection
    mydb = database_functions.connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        fp = open('demographics.csv', 'w')
        myFile = csv.writer(fp)
        # write column names
        query = "SHOW COLUMNS FROM Demographics"
        mycursor.execute(query)
        result = mycursor.fetchall()
        column_names = []
        for row in result:
            column_names.append(row[0])
        myFile.writerow(column_names)

        query = "SELECT * FROM Demographics" 
        mycursor.execute(query)
        result = mycursor.fetchall()

        # write data to csv file
        myFile.writerows(result)
        fp.close()


        # write personality survey and feedback info to csv
        mycursor = mydb.cursor()
        fp = open('traits.csv', 'w')
        myFile = csv.writer(fp)
        # write column names
        query = "SHOW COLUMNS FROM Personality_survey"
        mycursor.execute(query)
        result = mycursor.fetchall()
        column_names = []
        for row in result:
            column_names.append(row[0])
        query = "SHOW COLUMNS FROM Feedback"
        mycursor.execute(query)
        result = mycursor.fetchall()
        # append column names num and avg ratings from Feedback
        column_names.append(result[2][0])
        column_names.append(result[3][0])
        myFile.writerow(column_names)

        # combine personality_survey and feedback tables
        query = """ 
                SELECT p.*, f.num_ratings, f.avg_rating 
                FROM Personality_survey p
                LEFT JOIN Feedback f
                ON p.user_id = f.user_id AND p.trait_id = f.trait_id
                UNION ALL
                SELECT p.*, f.num_ratings, f.avg_rating 
                FROM Personality_survey p
                RIGHT JOIN Feedback f
                ON p.user_id = f.user_id AND p.trait_id = f.trait_id
                """ 
        mycursor.execute(query)
        result = mycursor.fetchall()

        # write to csv file
        if result:
            myFile.writerows(result)
        fp.close()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")
