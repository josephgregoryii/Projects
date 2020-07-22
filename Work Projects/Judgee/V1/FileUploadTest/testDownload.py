from google.cloud import storage

def downloadFileFromCloud(name):
	assert type(name) == str
	client = storage.Client.from_service_account_json('benkey.json')
	bucket = client.get_bucket('profile_photos777')
	blob = bucket.get_blob("/" + name)
	f = open("./downloadedFiles/" + name, "wb")
	blob.download_to_file(f)

downloadFileFromCloud("duke.jpg")