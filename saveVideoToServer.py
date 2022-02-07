import pyrebase
import os
import time
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

with open('camera.json', 'r') as f:
    camera = json.load(f)

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

def syncVideo():
    files = storage.list_files()

    if files is not None:
      for file in files:
        print(file.name)
        captures = database.child("Capture").order_by_child("name").equal_to(file.name).limit_to_first(1).get()
        if captures.each() is not None:
          for capture in captures.each():
            database.child("Capture").child(capture.key()).update({"is_online": 1})

class OnMyWatch:
  watchDirectory = 'Capture'

  def __init__(self):
    self.observer = Observer()

  def run(self):
    event_handler = Handler()
    self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
    self.observer.start()
    
    try:
      while True:
        time.sleep(5)
      
    except:
      self.observer.stop()
      print("Observer Stopped")
    
    self.observer.join()


class Handler(FileSystemEventHandler):

  @staticmethod
  def on_any_event(event):
    if event.is_directory:
      syncVideo()
      return None

    elif event.event_type == 'created':      
      capture_list = database.child("Capture").shallow().get().val()
      
      database.child("Camera").child(camera["camera_id"]).update({"detection": 1})
      
      if capture_list is not None:
          capture_count = len(capture_list)

      else:
          capture_count = 0


      data = {
        "capture_id": capture_count,
        "camera_id": camera['camera_id'],
        "name": event.src_path,
        "file_path": event.src_path,
        "is_online": 0,
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }

      database.child("Capture").child(capture_count).set(data)

      print(event.src_path)
    
    elif event.event_type == 'modified':
      path_on_cloud = event.src_path
      path_local = event.src_path
      storage.child(path_on_cloud).put(path_local)

    elif event.event_type == 'deleted':
      storage.delete(event.src_path)
      captures = database.child("Capture").order_by_child("name").equal_to(event.src_path).limit_to_first(1).get()
      if captures.each() is not None:
        for capture in captures.each():
          database.child("Capture").child(capture.key()).remove()
      
watch = OnMyWatch()
watch.run()
