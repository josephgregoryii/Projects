import os
import hashlib
import database_functions as db
import cloudfunctions
import time
import boto3

files = os.listdir("./photo_examples")
db.deleteAllRows('Users')
db.deleteAllRows('Demographics')
db.deleteAllRows('Personality_survey')
db.deleteAllRows('Feedback')

count = 1

def upload(filename, f):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    s3 = boto3.client('s3')
    s3.upload_file(f, "judgee-bucket", filename)

for file in files:

    passwd = "a"

	        
    to_db_login = {
        'email': str(count) + "@fakemail.com",
        'passwd' : passwd 
    }

    user_id = db.saveLogInInfo(to_db_login)
    print('user_id',user_id)
    print('count', count)

    upload(str(user_id), 'photo_examples/'+file)

    to_db_info = {
        'user_id' : user_id,
        'full_name' : "Test Person " + str(count),
        'birthdate': "1989-01-01",
        'race' : "White",
        'ethnicity' : "White",
        'sex' : "Male",
        'gender' : "Male",
        'orientation' : "Heterosexual",
        'height' : 72,
        'weight' : 180,
        'marital_status' : "Single",
        'num_children' : 0,
        'education_level' : "High School",
        'employment_status' : "Unemployed",
        'employment_field' : "Technology",
        'annual_income' : 100000,
        'parental_income' : 100000,
        'ideology' : "Anarchist",
        'smoking_status' : 0,
        'drinks_per_week': 0,
        'weed_per_week' : 0,
        'substance_use' : 0,
        'dieting_status' : 0,
        'num_partners' : 69,
        'safe_sex' : 0,
        'credit' : 0
        }

    db.saveAccountInfo(to_db_info)

    smart_dict = {
        'user_id' : user_id,
        'trait_id' : 1,
        'trait_affinity' : 1,
        'certainty' : 1,
        'importance' : 1,
        'ranking' : 1
    }
    creative_dict = {
        'user_id' : user_id,
        'trait_id' : 2,
        'trait_affinity' : 1,
        'certainty' : 1,
        'importance' : 1,
        'ranking' : 2
    }

    attractive_dict = {
        'user_id' : user_id,
        'trait_id' : 3,
        'trait_affinity' : 1,
        'certainty' : 1,
        'importance' : 1,
        'ranking' : 3
    }

    dependable_dict = {
        'user_id' : user_id,
        'trait_id' : 4,
        'trait_affinity' : 1,
        'certainty' : 1,
        'importance' : 1,
        'ranking' : 4
    }

    social_dict = {
        'user_id' : user_id,
        'trait_id' : 5,
        'trait_affinity' : 1,
        'certainty' : 1,
        'importance' : 1,
        'ranking' : 5
    }

    insecure_dict = {
        'user_id' : user_id,
        'trait_id' : 6,
        'trait_affinity' : 1,
        'certainty' : 1,
        'importance' : 1,
        'ranking' : 6
    }

    cooperative_dict = {
        'user_id' : user_id,
        'trait_id' : 7,
        'trait_affinity' : 1,
        'certainty' : 1,
        'importance' : 1,
        'ranking' : 7
    }
    list_of_dicts = [
        smart_dict,
        creative_dict,
        attractive_dict,
        dependable_dict,
        social_dict,
        insecure_dict,
        cooperative_dict
    ]

    for j in range(7):
        cur_dict = list_of_dicts[j]
        print('cur_dict', cur_dict)
        db.savePersonalityInfo(cur_dict)
        time.sleep(2)

    count += 1
