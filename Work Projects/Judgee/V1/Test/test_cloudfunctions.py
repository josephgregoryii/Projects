import cloudfunctions
import os


if __name__ == "__main__":
    files = os.listdir("./photo_examples")
    print(files[0])
    print(type(files[0]))
    cloudfunctions.uploadFileToCloud(files[0])
    cloudfunctions.downloadFileFromCloud(files[0])
    
