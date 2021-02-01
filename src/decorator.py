from flask import Flask, request, jsonify, make_response
import uuid
import jwt
import datetime
from functools import wraps
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      cred = credentials.ApplicationDefault()
      if not firebase_admin._apps:
         firebase_admin.initialize_app(cred, {
         'projectId': 'springmltraining',
         })

      db = firestore.client()  
      try:
         data = jwt.decode(token, 'Th1s1ss3cr3t',algorithms=["HS256"])
      except:
         return jsonify({'message': 'token invalid'})

      current_user=db.collection('tennis_players').document('user_document').get()
      current_user=current_user.to_dict()
      if current_user['id']==data['id']:
         return f(*args, **kwargs)
      else:
         return jsonify({'message': 'token incorrect'})        
               
   return decorator
