import database_functions

if __name__ == "__main__":

    database_functions.deleteAllRows('Users')
    database_functions.deleteAllRows('Demographics')
    database_functions.deleteAllRows('Traits')
    database_functions.deleteAllRows('Feedback')
    database_functions.deleteAllRows('Personality_survey')
        
    # insert login info
    logInInfo = {'email':'test@gmail.com', 'passwd':'1234test'}
    id = database_functions.saveLogInInfo(logInInfo)
    print("Inserted into Users table username: %s and passwd: %s\n" % (logInInfo['email'], logInInfo['passwd']))
    print("User ID = %d\n" % id)
    

    # insert another
    logInInfo = {'email':'test2@gmail.com', 'passwd':'1234test2'}
    id = database_functions.saveLogInInfo(logInInfo)
    print("Inserted into Users table username: %s and passwd: %s\n" % (logInInfo['email'], logInInfo['passwd']))
    print("User ID = %d\n" % id)
    # print users table
    database_functions.getRecords("Users")

    # insert another
    logInInfo = {'email':'test3@gmail.com', 'passwd':'1234test3'}
    id = database_functions.saveLogInInfo(logInInfo)
    print("Inserted into Users table username: %s and passwd: %s\n" % (logInInfo['email'], logInInfo['passwd']))
    print("User ID = %d\n" % id)

    # insert another
    logInInfo = {'email':'test4@gmail.com', 'passwd':'1234test4'}
    id = database_functions.saveLogInInfo(logInInfo)
    print("Inserted into Users table username: %s and passwd: %s\n" % (logInInfo['email'], logInInfo['passwd']))
    print("User ID = %d\n" % id)

    # insert another
    logInInfo = {'email':'test5@gmail.com', 'passwd':'1234test5'}
    id = database_functions.saveLogInInfo(logInInfo)
    print("Inserted into Users table username: %s and passwd: %s\n" % (logInInfo['email'], logInInfo['passwd']))
    print("User ID = %d\n" % id)

    database_functions.getRecords("Users")

    # test chooseRandomUserAndTrait function
    d = database_functions.chooseRandomUserAndTrait(1)
    print(d)

    
    # test loginSuccess function
    # correct one
    print("Testing username=test@gmail.com and password=1234test")
    database_functions.loginSuccess("test@gmail.com", "1234test")

    # wrong email
    print("Testing username=bad@gmail.com and password=1234test")
    database_functions.loginSuccess("bad@gmail.com", "1234test")


    # wrong email and password
    print("Testing username=bad@gmail.com and password=badtest")
    database_functions.loginSuccess("bad@gmail.com", "badtest")


    # wrong password
    print("Testing username=test2@gmail.com and password=badtest")
    database_functions.loginSuccess("test2@gmail.com", "badtest")


    # test saving demographics function
    dictionary = {}
    dictionary['full_name'] = 'Amy Miller'
    dictionary['birthdate'] = '01/23/1987'
    dictionary['race'] = 'White'
    dictionary['ethnicity'] = 'American'
    dictionary['sex'] = 'Female'
    dictionary['gender'] = 'Female'
    dictionary['height'] = 78
    dictionary['weight'] = 120
    dictionary['orientation'] = 'straight'
    dictionary['marital_status'] = 'single'
    dictionary['num_children'] = 0
    dictionary['education_level'] = 'Masters'
    dictionary['employment_status'] = 'Employed'
    dictionary['employment_field'] = 'Technology'
    dictionary['annual_income'] = 75000
    dictionary['parental_income'] = 53000
    dictionary['ideology'] = 'Conservative'
    dictionary['smoking_status'] = 0
    dictionary['drinks_per_week'] = 3
    dictionary['weed_per_week'] = 1
    dictionary['substance_use'] = 'Never'
    dictionary['dieting_status'] = 0
    dictionary['num_partners'] = 5
    dictionary['safe_sex'] = 4
    dictionary['credit'] = 10

    # save to Demographics table and try retrieving it
    ID = database_functions.saveAccountInfo(dictionary)
    print("Inserted a row into Demographics table\n")
    result = database_functions.getAccountDetails(ID)
    print(result)
    

