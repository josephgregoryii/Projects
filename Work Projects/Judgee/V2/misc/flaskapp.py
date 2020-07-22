import sys
import time
import hashlib
import flask_login
import database_functions as db
import cloudfunctions as cloud
from random import randint
from flask import Flask, request, render_template, redirect, url_for
from datetime import timedelta

# User will be logout after this time of inactivity
PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)
SESSION_REFRESH_EACH_REQUEST = True


app = Flask(__name__, template_folder="templates")
app.secret_key = "faifjjieawfjp"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

PRINT_DEBUG = False 

#User class to be passed through flask_login
class User(flask_login.UserMixin):
    def __init__(self, user_id, name=None, email=None):
        self.id = user_id
        self.name = name
        self._email = email

        #count variable for future implementation
        #currently, count gets reinitialized to 0
        #when reloaded per page
        self._count = 0

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self._email)

    def get_id(self):
        return self.id

#user_loader loads user when user is logged in
#if user is not logged in, it returns a 
@login_manager.user_loader
def user_loader(user_id):
    """
    login_manager required function. Loads the user on each page when called
    for current_user. Used for session tracking throughout the different
    web pages

    Args:
        user_id : int
    Returns:
        User(user_id, name : str, email : str)  : User object 
    """
    
    if PRINT_DEBUG:
        app.logger.info('user_loader')
        app.logger.info('current user_id: %d'%user_id)
        
    #items to reload user during flask_login and session
    account_details = db.getAccountDetails(user_id)
    full_name = account_details['full_name']
    email = db.getEmail(user_id)

    return User(user_id, name=full_name, email=email)

@app.errorhandler(404)
def error_404(e):
    """
    Handles routing error if page does not exist in website
    
    Args:
        None
    Returns:
        render_template() : main page with error
        render_template() : login page with error
    """

    #if user is not logged in, user will be an Anonymous User
    #where is_authenticated is defaulted to False
    user = flask_login.current_user
    
    error = 'Page does not exist'

    if user.is_authenticated:
        return render_template('main-page.html',error=error)

    return render_template('login.html',error=error)

@app.route('/')
def default():
    """
    Function checks if user is authenticated (logged in) and redirects
    user to main-page, otherwise gets redirected to login page
    Args:
        None
    Returns:
        redirect(url_for('mainPage')) : if user is logged in
        redirect(url_for('login'))    : else
    """

    #if user is not logged in, user will be an Anonymous User
    #where is_authenticated is defaulted to False
    user = flask_login.current_user

    if user.is_authenticated:
        return redirect(url_for('mainPage'))

    return redirect(url_for('login'))

@app.route('/invalid-login')
def login_error():
    """
    Error function to handle invalid credentials on login page
    
    Args:
        None
    Returns:
        render_template('login.html', error : str)
        
    """
    error = 'Invalid Login: Please try again'
    return render_template('login.html', error=error)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """
    Function handles login feature for application.
    Password is hashed using the following method:
        https://docs.python.org/3/library/hashlib.html
    Args:
        None
    Returns:
        redirect(url_for()) : redirects user to mainpage if login success
        render_template()   : renders html template for login
    """

    if request.method == 'GET':
        if PRINT_DEBUG:
            app.logger.info('Initial startup of login page')

        return render_template('login.html')

    email = request.form['email']
    passwd = request.form['passwd']

    #hased_pass is a hashliv object
    hashed_pass = hashlib.md5(passwd.encode())

    #remove user input of password 
    del(passwd)
    
    #database call to validate correct email and password for login
    if db.loginSuccess(email, hashed_pass.hexdigest()):

        #get user_id from database and account details for dynamic display
        user_id = db.returnUserId(email, hashed_pass.hexdigest())
        account_details = db.getAccountDetails(int(user_id))

        #store full_name for later usage
        full_name = account_details['full_name']

        user = User(user_id, full_name, email)

        #result is a boolean function
        result = flask_login.login_user(user, force=True)

        if PRINT_DEBUG:
            app.logger.info('%s logged in successfully with return value %s' % (email, str(result)))
            app.logger.info('logged in user' + str(user))

        return redirect(url_for('mainPage'))
    else:

        if PRINT_DEBUG:
            app.logger.info('%s did not log in successfully',email)

        return redirect(url_for('login_error'))
    

@app.route('/logout')
@flask_login.login_required
def logout():
    """
    Logout function that logs out user using flask_login

    Args:
        None
    Returns:
        redirect(url_for('login'))
    """

    user = flask_login.current_user

    #if the user is not logged in, redirect to login
    if not user.is_authenticated:
        return redirect(url_for('login'))

    #log out and remove user form session
    flask_login.logout_user()
    return redirect(url_for('login'))

@app.route('/delete-account')
@flask_login.login_required
def deleteAccount():
    """
    function gets called from my-profile.html after button confirmation
    Args:
        None
    Returns:
        redirect(url_for('login'))
    """

    user = flask_login.current_user
    if not user.is_authenticated:
        return redirect(url_for('login'))

    user = flask_login.current_user
    user_id = user.id

    #remove user from database
    db.deleteUser(user_id)

    #logout user from session
    #logging out ensures redirection to login
    flask_login.logout_user()
    return redirect(url_for('login'))


#credits is not currently active
@flask_login.login_required
@app.route('/credit')
def credits():
    """
    Currently under development
    
    Args:
        None
    Returns:
        redirect(url_for('login'))
    """

    user = flask_login.current_user
    if not user.is_authenticated:
        return redirect(url_for('login')) 

    user_id = user.get_id()
    img_to_front = cloud.download(str(user_id))
    full_name = user.name
    credits = db.getCredit(user_id)
    return render_template("credits.html", full_name = user.name, credits=credits, user_img = img_to_front)


@flask_login.login_required
@app.route('/main-page', methods = ['GET'])
def mainPage():
    """
    Main page loader - Checks to ensure user is logged in.
    Otherwise, user gets redirected to login page
    
    Args:
        None
    Returns:
        render_template('main-page.html', full_name : str)
        redirect(url_for('login'))
    """
    user = flask_login.current_user

    if not user.is_authenticated:
        return redirect(url_for('login'))

    user_id = user.get_id()
    img_to_front = cloud.download(str(user_id))
    full_name = user.name
    
    if PRINT_DEBUG:
        app.logger.info('main')
        app.logger.info('current_user: %s' % user)

    return render_template('main-page.html',full_name = full_name, user_img=img_to_front)

@flask_login.login_required
@app.route('/my-feedback')
def myFeedback():
    """
    Routing for feedback from user's id. Gets info from data and
    handles unrated feedback if feedback is not in database
    
    Args:
        None
    Returns:
        redirect(url_for('login'))
        render_template('my-feedback.html', to_front: list of dicts, to_front_bar : dict, user.name : str) 
    """

    user = flask_login.current_user

    if not user.is_authenticated:
        return redirect(url_for('login'))

    user_id = user.get_id()

    #dynamic display
    img_to_front = cloud.download(str(user_id))

    if PRINT_DEBUG:
        app.logger.info('current user %s' % user)
        app.logger.info('current user id: %d' % user_id)

    #dictionary from database
    #key : tuple(total_rate_num, average_rate)
    from_db = db.getFeedback(user_id)

    #dictionary for bar graph graph display
    to_front_bar = {
                        #traits initialized for bar graph
                        #incase user has no feedback available
                        'smart'       : 0,
                        'creative'    : 0,
                        'attrative'   : 0,
                        'dependable'  : 0,
                        'social'      : 0,
                        'insecure'    : 0,
                        'cooperative' : 0
                        }

#------------------------No Feedback Available--------------------------------#
    #base case if user has no ratings
    if len(from_db) == 0:
        
        db_front = {
                    'trait' : 'No Feedback Rating Available',
                    'average_score' : 0,
                    'total_rate_num': 0 
                   }
        to_front = [db_front]
        return render_template('my-feedback.html', items = to_front, bar=to_front_bar, full_name = user.name, user_img=img_to_front)

#------------------------Feedback Available-----------------------------------#
    else:

        #list contains dictionaries to_front_table
        #to display for table
        items = []

        #loop adds each item from database with corresponding key and value
        #to display in bar chart
        for key in from_db:
            to_front_bar[str(key)] = from_db[key][1] *10 

            #dictionary to append to items list
            #for table representation of data on
            #front end
            to_front_table = {
                            'trait'          : str(key).capitalize(),
                            'total_rate_num' : from_db[key][0],
                            'average_score'  : from_db[key][1]
                            }
            
            #items will contain number of feedback dictionaries
            #to display on myFeedback page
            items.append(to_front_table)

        return render_template("my-feedback.html", items = items, bar=to_front_bar, full_name = user.name, user_img=img_to_front)

@flask_login.login_required
@app.route('/my-profile',methods=['GET','POST'])
def myProfile():
    """
    Routing for user account details. Gets info from data and
    handles account changes for email, password and photo 
    
    Args:
        None
    Returns:
        redirect(url_for('login'))
        render_template('account-details.html', email : str, account_details : dict, user.name : str) 
        return render_template('account-details.html',email=email, account_details = account_details, error=error, full_name = user.name)
    """

    #error handling for dynamic display
    error = None

    #dictionary to send to front end
    user = flask_login.current_user

    if not user.is_authenticated:
        return redirect(url_for('login'))
    
    if PRINT_DEBUG:
        app.logger.info('current_user: %s' % user)

    user_id = user.get_id()
    account_details = db.getAccountDetails(user_id) 
    img_to_front= cloud.download(str(user_id))

    email = user._email

    if request.method == 'POST':
        
        #delete account
        

        #change password only
        cur_passwd = request.form['cur_passwd']
        print("cur",cur_passwd)

        
        #hash the password enter in form for checking
        hashed_current_password = hashlib.md5(cur_passwd.encode())

        #check if entered current password is the same as saved password
        #if passwords match, we can change either email or password, or both
        if db.loginSuccess(email, hashed_current_password.hexdigest()):

#------------------------change email-----------------------------------------#
            new_email = request.form['email']

            #if user wants to change current email
            if new_email:
                db.changeLogInInfo(user_id, email=new_email)
                
                email = new_email

                user._email = new_email
                

#------------------------change photo--------------------------------------------#
            new_photo = request.files['photo']
            if new_photo:
                #rename the filename to the user_id
                new_photo.filename = str(user_id) 

                #upload image file to cloud
                cloud.upload(str(user_id),new_photo)

                #replace display picture
                img_to_front = cloud.download(str(user_id))

#------------------------change password-----------------------------------------#
            #get new passwords
            new_password = request.form['new_passwd']
            new_repeated_password = request.form['new_reppasswd']

            #check if passwords match
            if ((new_password == new_repeated_password) and (len(new_password) != 0)):
                
                print('new',new_password)

                hashed_pass = hashlib.md5(new_password.encode())
                db.changeLogInInfo(user_id, password=hashed_pass.hexdigest())
                app.logger.info('user password changed successfully')

                #delete passwords from memory
                del(new_password)
                del(new_repeated_password)
                del(cur_passwd)
                
            elif (new_password != new_repeated_password):
                error = 'New passwords do not match'
                return render_template('account-details.html',email=email, account_details = account_details, error=error, full_name = user.name, user_img=img_to_front)
        else:
            error = 'Current password does not match our records'
            return render_template('account-details.html',email=email, account_details = account_details, error=error, full_name = user.name, user_img=img_to_front)

#------------------------Initial page render-------------------------------------#

    #contains the information to display on account-details.html
    account_details = db.getAccountDetails(user_id) 
    return render_template("account-details.html",email=email, account_details=account_details, error=error, full_name = user.name, user_img = img_to_front)

@flask_login.login_required
@app.route('/rate-others', methods=['GET','POST'])
def rateOthers():
    """
    RateOthers keeps track of the current user and gets a new user and trait from database.
    Function handles:
        1) if trait exists for user
        2) if trait does not exist for user
        3) if trait exists but has only been rated once

    Args:
        None
    Returns:
        redirect(url_for('login'))
        render_template('rate-others.html, trait : str, img_to_front : photo file || url link, user.name : str)
    """

    user = flask_login.current_user
    
    if not user.is_authenticated:
        return redirect(url_for('login'))
    
    #store current user's id
    current_user_id = user.get_id()

    #dynamic display
    user_img_to_front = cloud.download(str(current_user_id))

    #initialize variables
    from_db = None
    trait = None
    trait_id = None
    user_id = None

    #get dictionary of random user and trait for rating
    from_db = db.chooseRandomUserAndTrait(current_user_id)

    #variable stored for html display 
    trait = from_db['trait_name']

    #variables stored for functionality purposes
    user_id = from_db['user_id']
    trait_id = from_db['trait_id']

    #image file to display on front end
    img_to_front = cloud.download(str(user_id))

    #check to make sure image.filename is in database
    #filename is associated with user_id
    while img_to_front is None:
        if PRINT_DEBUG:
            app.logger.info('img is none')
        
        from_db = db.chooseRandomUserAndTrait(current_user_id)

        trait = from_db['trait_name']

        user_id = from_db['user_id']
        trait_id = from_db['trait_id']

        img_to_front = cloud.download(str(user_id))
        

    if request.method == 'POST':
        #1)
        rating = request.form['rate']
        if PRINT_DEBUG:
            app.logger.info('rating user: %s' % user)
            
        #2) - trait rating for user currently exists
        if db.traitFeedbackExists( user_id, trait_id ):
            ratings_from_db = db.getRatings( user_id, trait_id)

            #get number of ratings and increment by 1
            num_ratings = ratings_from_db['num_ratings']
            num_ratings += 1


            #add new num_ratings to dict
            ratings_from_db['num_ratings'] = num_ratings

            #get average rating score
            avg_rating = ratings_from_db['avg_rating']

            #3) - trait has multiple ratings 
            #num ratings has to be greater than 1
            #in order to get total rating score
            if num_ratings > 1:

                #average is getting total score / number of ratings
                #so to get the total rating score, multiply by current num_ratings - 1
                total_rating_score = avg_rating * (num_ratings-1)

                #add the rating that current_user has rated by
                total_rating_score = total_rating_score + int(rating)

                #get new average rating
                new_avg_rating = total_rating_score / num_ratings

                #update existing avg_rating with new average
                ratings_from_db['avg_rating'] = new_avg_rating

                db.updateFeedback(ratings_from_db)


            #3) - update feedback if its second rating or greater 
            else:
                #basically, this will be rating / 1 
                new_avg_rating = rating / num_ratings 

                #rewrite to dict
                ratings_from_db['avg_rating'] = int(new_avg_rating)


                db.updateFeedback(ratings_from_db)

        #2) insert feedback     
        else:
            to_db = {
                    'user_id'       : int(user_id),
                    'trait_id'      : int(trait_id),
                    'num_ratings'   : 1,
                    'avg_rating'    : int(rating)
                    }
            
            db.insertFeedback(to_db)

        #update current user's currency
        current_rates = db.getUserRates(current_user_id)
        print("current rates:",current_rates)
        current_rates += 1

        #Add credit to user
        if current_rates == 3:
            current_rates = 0
            result = db.getCredit(current_user_id)
            result += 1
            db.updateCredit(current_user_id, result)
            updated = db.getCredit(current_user_id)
            print("updated:",updated)

        db.updateUserRates(current_user_id, current_rates)



        
        return render_template("rate-others.html",trait=trait, img=img_to_front, full_name = user.name, user_img = user_img_to_front)
    
    #1) - return initial viewing
    return render_template("rate-others.html", trait=trait, img=img_to_front, full_name = user.name, user_img = user_img_to_front)

@app.route('/create-account',methods = ['GET', 'POST'])
def createAccount():
    """
    getCreateAccount pulls request from create account front end form and
    sends information to database
    Args:
        None
    Returns: render_template: input of .hmtl file
    """
    
    #handle for if user is already logged in
    user = flask_login.current_user.is_authenticated
    if user:
        return redirect(url_for('mainPage'))

    #dictionary to store variables
    to_db_info = {}
    to_db_login= {}
    error = None

    #1) - check form post
    if request.method == 'POST':
        #login information
        email = request.form['email']
        passwd = request.form['passwd']
        repasswd = request.form['repasswd']
       
        #2) - check if passwords match
        if passwd == repasswd:

            #account information and demographics
            img = request.files['photo']
            if img is None:
                error = 'Please upload a current photo of yourself to continue account creation'
                return render_template('create-account.html', error=error)

            full_name = request.form['full_name']
            birthdate = request.form['birthdate']
            race = request.form['race']
            ethnicity = request.form['ethnicity']
            sex = request.form['sex']
            gender = request.form['gender']
            orientation = request.form['orientation']
            height = request.form['height']
            weight = request.form['weight']
            marital_status = request.form['marital_status']
            num_children = request.form['num_children']
            education_level = request.form['education_level']
            employment_status = request.form['employment_status']
            employment_field = request.form['employment_field']
            annual_income = request.form['annual_income']
            parental_income = request.form['parental_income']
            ideology = request.form['ideology']
            smoking_status = request.form['smoking_status']
            drinks_per_week = request.form['drinks_per_week']
            weed_per_week = request.form['weed_per_week']
            substance_use = request.form['substance_use']
            dieting_status = request.form['dieting_status']
            num_partners = request.form['num_partners']
            safe_sex = request.form['safe_sex']

            hashed_pass = hashlib.md5(passwd.encode())
            
            to_db_login = {
                'email': email,
                'passwd' : hashed_pass.hexdigest() 
            }

            #send login information to db to retrieve user_id
            user_id = db.saveLogInInfo(to_db_login)

            #rename the filename to the user_id
            img.filename = str(user_id) 

            #upload image file to cloud
            cloud.upload(str(user_id),img)

            #dict to send to db for account info
            to_db_info = {
                'user_id' : user_id,
                'full_name' : full_name,
                'birthdate': birthdate,
                'race' : race,
                'ethnicity' : ethnicity,
                'sex' : sex,
                'gender' : gender,
                'orientation' : orientation,
                'height' : height,
                'weight' : weight,
                'marital_status' : marital_status,
                'num_children' : num_children,
                'education_level' : education_level,
                'employment_status' : employment_status,
                'employment_field' : employment_field,
                'annual_income' : annual_income,
                'parental_income' : parental_income,
                'ideology' : ideology,
                'smoking_status' : smoking_status,
                'drinks_per_week': drinks_per_week,
                'weed_per_week' : weed_per_week,
                'substance_use' : substance_use,
                'dieting_status' : dieting_status,
                'num_partners' : num_partners,
                'safe_sex' : safe_sex,
                
                #check https://www.geeksforgeeks.org/python-increment-value-in-dictionary/
                # for incrementing credit value
                'credit' : 0
                }

            db.saveAccountInfo(to_db_info)

            user = User(user_id, full_name, email)
            app.logger.info('new user: %s' % user)

            flask_login.login_user(user)

            #remove user input of password from memory
            del(passwd)
            del(repasswd)
            return render_template('personality-survey.html') 

        #2) - passwords do not match
        else:

            error = "Passwords do not match!"
            return render_template('create-account.html', error=error)

    #1) - webpage display
    else:
        app.logger.info('Returning initial create-account.html')

        #initial render on loading of create account page if form is empty
        return render_template('create-account.html')


@flask_login.login_required
@app.route('/personality-survey',methods = ['GET','POST'])
def personalitySurvey():
    """
    Takes in new user after create account page and sends info to database

    Args:
        None
    Returns: 
        None
    """

    smart_dict = {}
    creative_dict = {}
    attractive_dict = {}
    dependable_dict = {}
    social_dict = {}
    insecure_dict = {}
    cooperative_dict = {}

    user = flask_login.current_user

    #number of traits variable for sending
    #each trait to databse
    num_traits = 7

    #store user_id
    user_id = user.get_id()
    if PRINT_DEBUG:
        app.logger.info('current user: %s' % user)

    #check to see if request.args.get('smart_q1') has been answered
    if 'smart_q1' in request.args:

        trait1 = 1 
        trait_affinity1 = int(request.args.get('smart_q1'))
        certaint1 = int(request.args.get('smart_q2'))
        importance1 = int(request.args.get('smart_q3'))

        smart_dict = {
            'user_id' : user_id,
            'trait_id' : trait1,
            'trait_affinity' : trait_affinity1,
            'certainty' : certaint1,
            'importance' : importance1
        }

        trait2 = 2
        trait_affinity2 = int(request.args.get('creative_q1'))
        certaint2 = int(request.args.get('creative_q2'))
        importance2 = int(request.args.get('creative_q3'))
        
        creative_dict = {
            'user_id' : user_id,
            'trait_id' : trait2,
            'trait_affinity' : trait_affinity2,
            'certainty' : certaint2,
            'importance' : importance2
        }

        trait3 = 3 
        trait_affinity3 = int(request.args.get('attractive_q1'))
        certaint3 = int(request.args.get('attractive_q2'))
        importance3 = int(request.args.get('attractive_q3'))

        attractive_dict = {
            'user_id' : user_id,
            'trait_id' : trait3,
            'trait_affinity' : trait_affinity3,
            'certainty' : certaint3,
            'importance' : importance3
        }
        
        trait4 = 4 
        trait_affinity4 = int(request.args.get('dependable_q1'))
        certaint4 = int(request.args.get('dependable_q2'))
        importance4 = int(request.args.get('dependable_q3'))

        dependable_dict = {
            'user_id' : user_id,
            'trait_id' : trait4,
            'trait_affinity' : trait_affinity4,
            'certainty' : certaint4,
            'importance' : importance4
        }

        trait5 = 5 
        trait_affinity5 = int(request.args.get('social_q1'))
        certaint5 = int(request.args.get('social_q2'))
        importance5 = int(request.args.get('social_q3'))

        social_dict = {
            'user_id' : user_id,
            'trait_id' : trait5,
            'trait_affinity' : trait_affinity5,
            'certainty' : certaint5,
            'importance' : importance5
        }

        trait6 = 6 
        trait_affinity6 = int(request.args.get('insecure_q1'))
        certaint6 = int(request.args.get('insecure_q2'))
        importance6 = int(request.args.get('insecure_q3'))

        insecure_dict = {
            'user_id' : user_id,
            'trait_id' : trait6,
            'trait_affinity' : trait_affinity6,
            'certainty' : certaint6,
            'importance' : importance6
        }

        trait7 = 7 
        trait_affinity7 = int(request.args.get('cooperative_q1'))
        certaint7 = int(request.args.get('cooperative_q2'))
        importance7 = int(request.args.get('cooperative_q3'))

        cooperative_dict = {
            'user_id' : user_id,
            'trait_id' : trait7,
            'trait_affinity' : trait_affinity7,
            'certainty' : certaint7,
            'importance' : importance7
        }

        rank1 = request.args.get('rank_1')
        rank2 = request.args.get('rank_2')
        rank3 = request.args.get('rank_3')
        rank4 = request.args.get('rank_4')
        rank5 = request.args.get('rank_5')
        rank6 = request.args.get('rank_6')
        rank7 = request.args.get('rank_7')
        
        #rank_list holds each ranking in order of personality survey form
        rank_list = [rank1,rank2,rank3,rank4,rank5,rank6,rank7]
        check_list = []
        for item in rank_list:
            if item not in check_list:
                check_list.append(item)
            else:
                error = 'Please rate each trait only once'
                return render_template('personality-survey.html', error=error)

        for i in range(num_traits):
            if rank_list[i].lower() == 'smart':
                smart_dict['ranking'] = i+1 #1 <= i <= 7
            elif rank_list[i].lower() == 'creative':
                creative_dict['ranking'] = i+1
            elif rank_list[i].lower() == 'attractive':
                attractive_dict['ranking'] = i+1
            elif rank_list[i].lower() == 'dependable':
                dependable_dict['ranking'] = i+1
            elif rank_list[i].lower() == 'social':
                social_dict['ranking'] = i+1
            elif rank_list[i].lower() == 'insecure':
                insecure_dict['ranking'] = i+1
            elif rank_list[i].lower() == 'cooperative':
                cooperative_dict['ranking'] = i+1

        list_of_dicts = [
        smart_dict,
        creative_dict,
        attractive_dict,
        dependable_dict,
        social_dict,
        insecure_dict,
        cooperative_dict
        ]
        
        for j in range(num_traits):
            cur_dict = list_of_dicts[j]
            if PRINT_DEBUG:
                app.logger.info('sending trait number {} to DB'.format(j))
                app.logger.info('current dictionary being sent: \n{}\n'.format(cur_dict))
            db.savePersonalityInfo(cur_dict)

        return render_template('main-page.html', full_name = user.name)
    else:
        return render_template('personality-survey.html')

if __name__ == '__main__':
    if PRINT_DEBUG:
        db.getRecords('Users')
        db.getRecords('Demographics')

    app.debug = True
    app.run(host='0.0.0.0')
    




