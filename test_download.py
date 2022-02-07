import pyrebase

config = {
  "apiKey": "AIzaSyBTdUpEpEcx-eie9LFU43B-DwTG9KImXXE",
  "authDomain": "hides-4821e.firebaseapp.com",
  "databaseURL": "https://hides-4821e-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "hides-4821e",
  "storageBucket": "hides-4821e.appspot.com",
  "messagingSenderId": "873480647084",
  "appId": "1:873480647084:web:8fd2d67591226a9a340a09",
  "measurementId": "G-F7S16RQPKC",
  "serviceAccount": "serviceAccount.json"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()

# storage.child('Capture/2021-11-02T14:34:06.mp4').download('video.mp4')

for item in storage.child("Capture").list_files():
  print(item.name)