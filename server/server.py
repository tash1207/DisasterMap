import bottle
import gridfs
import os
import pymongo
import sys

from base64 import decodestring
from bottle import get, post, redirect, request, static_file, template
from datetime import datetime
from bson import Binary, Code
from bson.json_util import dumps

@get('/images/<filename>')
def image(filename):
  dbname = 'grid_files'
  db = connection[dbname]
  fs = gridfs.GridFS(db)
  gridout = fs.get_last_version(filename=filename)
  bottle.response.content_type = 'image/jpeg'
  return gridout

@get('/upload')
def form_upload():
  return '''
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="data" />
      <input type="submit" value="submit">
    </form>
  '''

@get('/disasters')
def get_all_maps():
  hack_db = connection['hackathon']
  disasters = hack_db['disasters']
  return dumps(disasters.find({}, {'name': 1}))

@get('/map/<id>')
def get_map(id):
  hack_db = connection['hackathon']
  pictures = hack_db['pictures']
  return dumps(pictures.find("disaster": id), {'filename': 1, 'latitude':1, 'longitude': 1, 'datetime': 1})

@post('/upload')
def do_upload():
  data = request.files.data
  name, ext = os.path.splitext(data.filename)
  now = datetime.now()
  date_filename = now.strftime("%Y%m%d-%H%M%S") + ext
  print date_filename
  if ext not in ('.png', '.jpg', '.jpeg'):
    return "File extension not allowed."
  if data and data.file:
    # Store the image in the grid_files db
    raw = data.file.read()
    #filename = data.filename
    grid_db = connection['grid_files']
    fs = gridfs.GridFS(grid_db)
    fs.put(raw, filename=date_filename)
    # Insert the filename and other data in the pictures db
    hack_db = connection['hackathon']
    hack_db.pictures.insert_one(
        {'filename': date_filename,
         'datetime': now,
         'latitude': 0,
         'longitude': 0,
         'disaster': 0}
    )
    # Get the image back out
    image = fs.get_last_version(filename=date_filename)
    bottle.response.content_type = 'image/jpeg'
    return image
  return "Upload failed"

@post('/uploadFromApp')
def do_upload_from_app():
  picture = request.forms.get('picture')
  lat = request.forms.get('latitude')
  lng = request.forms.get('longitude')

  raw = decodestring(picture)
  now = datetime.now()
  date_filename = now.strftime("%Y%m%d-%H%M%S") + '.jpg'
  print date_filename
  grid_db = connection['grid_files']
  fs = gridfs.GridFS(grid_db)
  fs.put(raw, filename=date_filename)
  # Insert the filename and other data in the pictures db
  hack_db = connection['hackathon']
  hack_db.pictures.insert_one(
      {'filename': date_filename,
       'datetime': now,
       'latitude': lat,
       'longitude': lng,
       'disaster': 0}
  )
  # Get the image back out
  image = fs.get_last_version(filename=date_filename)
  bottle.response.content_type = 'image/jpeg'
  return image

connection = pymongo.MongoClient()

bottle.debug(True)
bottle.run(host='0.0.0.0', port=8080)

