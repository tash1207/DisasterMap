import gridfs
import os
import pymongo
import sys

from bottle import get, post, redirect, request, run, static_file, template
from datetime import datetime

@get('/images/<filename>')
def image(filename):
  dbname = 'pictures'
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

@post('/upload')
def do_upload():
  data = request.files.data
  name, ext = os.path.splitext(data.filename)
  if ext not in ('.png', '.jpg', '.jpeg'):
    return "File extension not allowed."
  # Logic to add image to pictures collection
  return "Upload succeeded!"
