import database_functions as db

to_db_info = {
	    'user_id' : 34,
	    'full_name' : "Special boy",
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