import mysql.connector
import random

# receive dictionaries from createAccount, login, personalitySurvey, rateOthers pages
# send dictionaries for myFeedback, accountDetails pages

# Traits:
#1. smart
#2. creative
#3. attractive
#4. dependable
#5. social
#6. insecure
#7. cooperative


# function to connect to database via python and return the connection
def connectDatabase():
    # try to connect to cloud sql server
    try:
        mydb = mysql.connector.connect(
            host = "judgeedb.ctlyzwmrbgux.us-west-2.rds.amazonaws.com",
            user = "admin_joe",
            passwd = "U69g0321j_o",
            database = "judgee_db"
            )
        #if mydb.is_connected():
            #print('connection established.')
        #else:
            #print('connection failed.')
        return mydb

    except mysql.connector.Error as e:
        print(e)


# function to return email for user
def getEmail(user_id):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT email FROM Users WHERE user_id = %d" % user_id
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")

    # if something is returned, then email and pwd are valid
    if len(result) == 0:
        #print("user doesn't exist")
        return None
    else:
        return result[0][0]



# function to check if a user exists in a given table_name
# tables that have user_id: Users, Demographics, Feedback, Personality_survey
def userExists(table_name, user_id):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT user_id FROM %s WHERE user_id = %d" % (table_name, user_id)
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")

    # if something is returned, then email and pwd are valid
    if len(result) == 0:
        #print("user doesn't exist")
        return False
    else:
        #print("user exists")
        return True



# function to return login success or failure
# checks if email exists and password is correct
def loginSuccess(email, pwd):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT email, passwd FROM Users WHERE email = '%s' AND passwd = '%s'" % (email,pwd)
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")

    # if something is returned, then email and pwd are valid
    if len(result) == 0:
        #print("username and password not valid")
        return False
    else:
        #print("valid username and password")
        return True



# function that takes in a dictionary containing email and password and inserts into user table
# called when create account on login page
# returns newly inserted userID
def saveLogInInfo(dictionary):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "INSERT INTO Users (email, passwd, traits) VALUES (%s, %s, %s)"
        val = (dictionary['email'], dictionary['passwd'], "1,2,3,4,5,6,7")
        mycursor.execute(query, val)

        # commit changes
        mydb.commit()

        # get newly inserted user's id
        id = mycursor.lastrowid
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    
    return id



# function to return user_id AFTER logging in
# this assumes that the user is already stored in table
# takes in email and password
def returnUserId(email, password):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor(buffered=True)
        query = "SELECT user_id FROM Users WHERE email = '%s' AND passwd = '%s'" % (email, password)
        #print(query)
        mycursor.execute(query)

        # commit changes
        mydb.commit()
        result = mycursor.fetchall()
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    
    return int(result[0][0])



# function that takes in a dictionary containing account info and inserts into Demographics table
# called on createAccount page
def saveAccountInfo(d):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = """INSERT INTO Demographics 
                   (full_name, birthdate, race, ethnicity, sex, gender, height, weight, orientation,
                   marital_status, num_children, education_level, employment_status, employment_field, 
                   annual_income, parental_income, ideology, smoking_status, drinks_per_week,
                   weed_per_week, substance_use, dieting_status, num_partners, safe_sex, credit) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                   %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (d['full_name'], d['birthdate'], d['race'], d['ethnicity'], d['sex'], d['gender'], d['height'],
              d['weight'], d['orientation'], d['marital_status'], d['num_children'], d['education_level'],
              d['employment_status'], d['employment_field'], d['annual_income'], d['parental_income'],
              d['ideology'], d['smoking_status'], d['drinks_per_week'], d['weed_per_week'], d['substance_use'],
              d['dieting_status'], d['num_partners'], d['safe_sex'], d['credit'])
        mycursor.execute(query, val)

        # commit changes
        mydb.commit()

        # get newly inserted user's id
        id = mycursor.lastrowid
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return id


# function to change log in info for a user
# user_id is required, email and password are not
def changeLogInInfo(user_id, email = None, password = None):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        # check if email and password needs to be changed
        if email and password:
            e = email
            p = password
            query = "UPDATE Users SET email = '%s', passwd = '%s' WHERE user_id = %d" % (e, p, user_id)
        if email and not password:
            e = email
            query = "UPDATE Users SET email = '%s' WHERE user_id = %d" % (e, user_id)
        if password and not email:
            p = password
            query = "UPDATE Users SET passwd = '%s' WHERE user_id = %d" % (p, user_id)
        
        mycursor.execute(query)

        # commit changes
        mydb.commit()
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return

def getUserRates(user_id):
    mydb = connectDatabase()
    
    try:
        mycursor = mydb.cursor()
        query = "SELECT ratings FROM Users WHERE user_id = %d" % user_id
        mycursor.execute(query)
        result = mycursor.fetchall()
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return result[0][0] 

def updateUserRates(user_id, rates):
    mydb = connectDatabase()
    try:
        mycursor = mydb.cursor()
        query = "UPDATE Users SET ratings = '%s' WHERE user_id = %d" % (rates, user_id)
        mycursor.execute(query)

        mydb.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return

def getCredit(user_id):

    #create connection
    mydb = connectDatabase()

    #create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT credit FROM Demographics WHERE user_id = %d" % user_id
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return result[0][0]

def updateCredit(user_id, currency, reset = None):
    if reset is not None:
        #implementation on resetting at a specific amount
        pass

    mydb = connectDatabase()

    try:
        mycursor = mydb.cursor()
        query = "UPDATE Demographics SET credit = %d WHERE user_id = %d" % (currency, user_id)
        mycursor.execute(query)
        mydb.commit()
        
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return
        
# function to retrieve user, demographics, and personality survey information from database
# takes in user_id to get info for that person
# return dictionary
def getAccountDetails(user_id):

    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT * FROM Demographics WHERE user_id = %d" % user_id 
        mycursor.execute(query)
        result = mycursor.fetchall()

        # create dictionary with result
        dictionary = {}
        for row in result:
            dictionary['full_name'] = row[1]
            dictionary['birthdate'] = row[2]
            dictionary['race'] = row[3]
            dictionary['ethnicity'] = row[4]
            dictionary['sex'] = row[5]
            dictionary['gender'] = row[6]
            dictionary['height'] = row[7]
            dictionary['weight'] = row[8]
            dictionary['orientation'] = row[9]
            dictionary['marital_status'] = row[10]
            dictionary['num_children'] = row[11]
            dictionary['education_level'] = row[12]
            dictionary['employment_status'] = row[13]
            dictionary['employment_field'] = row[14]
            dictionary['annual_income'] = row[15]
            dictionary['parental_income'] = row[16]
            dictionary['ideology'] = row[17]
            dictionary['smoking_status'] = row[18]
            dictionary['drinks_per_week'] = row[19]
            dictionary['weed_per_week'] = row[20]
            dictionary['substance_use'] = row[21]
            dictionary['dieting_status'] = row[22]
            dictionary['num_partners'] = row[23]
            dictionary['safe_sex'] = row[24]
            dictionary['credit'] = row[25]

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return dictionary


# function that takes in a dictionary containing personality survey info and inserts into Personality_survey table
# called on personalitySurvey page
def savePersonalityInfo(dictionary):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "INSERT INTO Personality_survey (user_id, trait_id, trait_affinity, certainty, importance, ranking) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (dictionary['user_id'], dictionary['trait_id'], dictionary['trait_affinity'], dictionary['certainty'], dictionary['importance'], dictionary['ranking'])
        mycursor.execute(query, val)

        # commit changes
        mydb.commit()
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")


# function that checks whether feedback for a particular trait for a particular user is already in Feedback table
# return boolean
def traitFeedbackExists(user_id, trait_id):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT user_id, trait_id FROM Feedback WHERE user_id = %d AND trait_id = %d" % (user_id,trait_id)
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")

    # if something is returned, then trait feedback already in table
    if len(result) == 0:
        #print("trait feeback doesn't exist")
        return False
    else:
        #print("trait feedback exists")
        return True


# function that takes in a dictionary containing rating info and inserts into Feedback table
# called when this trait and user id combo doesn't exist in Feedback table
def insertFeedback(dictionary):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "INSERT INTO Feedback (user_id, trait_id, num_ratings, avg_rating, purchased) VALUES (%s, %s, %s, %d)"
        val = (dictionary['user_id'], dictionary['trait_id'], dictionary['num_ratings'], dictionary['avg_rating'], 0)
        mycursor.execute(query, val)
        # commit changes
        mydb.commit()
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return

def purchaseFeedback(dictionary):
    # create connection
    mydb = connectdatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "UPDATE Feedback SET purchased = %d  WHERE user_id = %s AND trait_id = %s" % (1, dictionary['user_id'], dictionary['trait_id'])
        mycursor.execute(query)

        # commit changes
        mydb.commit()
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return
    
def countFeedback(user_id):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT COUNT(*) FROM Feedback WHERE user_id = %d AND purchased = %d" % (user_id, 1)
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")

    return result[0][0] 
    

# function that takes in a dictionary containing rating info and updates corresponding row in Feedback table
# called when the trait id AND user id already is a record in the table
# updates num_ratings and avg_rating
def updateFeedback(dictionary, purchased = False):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        if not purchased:
            query = "UPDATE Feedback SET num_ratings = %s, avg_rating = %s WHERE user_id = %s AND trait_id = %s" % (dictionary['num_ratings'], dictionary['avg_rating'], dictionary['user_id'], dictionary['trait_id'])
        else:
            query = "UPDATE Feedback SET purchased = %d WHERE user_id = %s AND trait_id = %s" % (dictionary['purchased'], dictionary['user_id'], dictionary['trait_id'])
        mycursor.execute(query)

        # commit changes
        mydb.commit()
   
    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return


# function to get num_ratings, avg_ratings, user_id, trait_id from Feedback table
# called when user and trait already exists in Feedback and we want to update the num_ratings and avg_ratings
# return dictionary: user_id, trait_id, num_ratings, avg_rating
def getRatings(user_id, trait_id):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT user_id, trait_id, num_ratings, avg_rating FROM Feedback WHERE user_id = %d AND trait_id = %d" % (user_id, trait_id)
        mycursor.execute(query)
        result = mycursor.fetchall()

        # create dictionary with result
        dictionary = {}
        for row in result:
            dictionary['user_id'] = row[0]
            dictionary['trait_id'] = row[1]
            dictionary['num_ratings'] = row[2]
            dictionary['avg_rating'] = row[3]

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return dictionary



# function to retrieve feedback info for given user from Feedback table
# return dictionary: trait as key and tuple as value
# first entry in tuple is num_ratings, second entry in tuple is avg_rating
def getFeedback(user_id, for_credit = False):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        if not for_credit:
            query = "SELECT t.trait_name, f.num_ratings, f.avg_rating FROM Feedback f JOIN Traits t USING (trait_id) WHERE f.user_id = %d AND f.purchased = 1" % user_id 
        else:
            query = "SELECT t.trait_name, f.num_ratings, f.avg_rating FROM Feedback f JOIN Traits t USING (trait_id) WHERE f.user_id = %d AND f.purchased = 0" % user_id 
        mycursor.execute(query)
        result = mycursor.fetchall()

        # create dictionary with result
        dictionary = {}
        for row in result:
            dictionary[row[0]] = (row[1], row[2])

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
    return dictionary

# function to find the number of users (aka max user_id)for creating the range to choose random person
def numberOfUsers(mydb):

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT MAX(user_id) FROM Users" 
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)

    return int(result[0][0])

def numberOfTraits(mydb):
    try:
        mycursor = mydb.cursor()
        query = "SELECT MAX(trait_id) FROM Traits"
        mycursor.execute(query)
        result = mycursor.fetchall()

    except mysql.connector.Error as e:
        print(e)

    return int(result[0][0])

# function to delete a user
def deleteUser(user_id):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "DELETE FROM Users WHERE user_id = %d" % user_id 
        mycursor.execute(query)
        mydb.commit()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")

# function to return a random user and a random trait from their list of traits (id and name) for rating page
# need to make sure a user doesnt rate on himself!!
# takes in a user_id, which is the user who is currently trying to rate other's pictures
def chooseRandomUserAndTrait(current_user, trait=True):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        # get total number of users
        num_users = numberOfUsers(mydb)

        #set random_id to current_user if just random trait
        random_id = current_user

        # generate a random user id within the range
        # keep generating if the chosen user_id is the same as the current_user

        if trait is True:
            while random_id == current_user and trait is True:
                random_id = random.randint(1, num_users)
        # retrieve the list of traits for this chosen user
        mycursor = mydb.cursor()
        query = "SELECT traits FROM Users WHERE user_id = %d" % random_id
        mycursor.execute(query)
        result = mycursor.fetchall()
        # result looks like this: [('1,2,3,4,5,6,7',)]
        result = result[0][0]    # there's only supposed to be one thing returned

        # turn string of trait id's into list 
        traits = result.split(",")
        list_length = len(traits) - 1
        # choose random index from traits list to generate a random trait id
        index = random.randint(0, list_length)
        trait_id = int(traits[index])

        # retrieve name of chosen trait from Traits table
        query = "SELECT trait_name FROM Traits WHERE trait_id = %d" % trait_id
        mycursor.execute(query)
        result = mycursor.fetchall()
        trait_name = result[0][0]

        # create dictionary to store randomly chosen user_id, trait_id, and trait_name
        dictionary = {}
        dictionary['user_id'] = random_id
        dictionary['trait_id'] = trait_id
        dictionary['trait_name'] = trait_name

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")

    return dictionary



# testing function to retrieve all records from given table
def getRecords(table_name):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        query = "SELECT * FROM %s" % table_name
        mycursor.execute(query)
        result = mycursor.fetchall()
        #print("Records from %s Table: \n" % table_name)
        for row in result:
            print(row)

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")



# function to delete all records from a given table name
def deleteAllRows(table_name):
    # create connection
    mydb = connectDatabase()

    # create cursor to execute SQL queries
    try:
        mycursor = mydb.cursor()
        # need to disable foreign key constraints before truncating Users table
        if table_name == "Users":
            query = "SET FOREIGN_KEY_CHECKS = 0"
            mycursor.execute(query)
            query = "TRUNCATE table Users"
            mycursor.execute(query)
            query = "SET FOREIGN_KEY_CHECKS = 1"
            mycursor.execute(query)
        else:
            query = "TRUNCATE TABLE %s" % table_name
            mycursor.execute(query)
        #print("Deleted all records from table: %s\n" % table_name)

    except mysql.connector.Error as e:
        print(e)
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("MySQL connection is closed")
