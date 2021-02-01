from flask import Flask, request, jsonify, make_response
import uuid
import jwt
import datetime
from functools import wraps
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
from blueprint import example_blueprint
from decorator import token_required

# Initialize Flask App
# Initialize Firestore DB

app = Flask(__name__)
app.register_blueprint(example_blueprint, url_prefix="/api/")


app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite://///home/michael/geekdemos/geekapp/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      print(token)
      # cred = credentials.Certificate('C:/Users/sudar/Downloads/springmltraining.json')
      # if not firebase_admin._apps:
      #   default_app = initialize_app(cred)
      # db = firestore.client()
      cred = credentials.ApplicationDefault()
      if not firebase_admin._apps:
         firebase_admin.initialize_app(cred, {
         'projectId': 'springmltraining',
         })

      db = firestore.client()  
      print('hii')

      data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
      print('hii2')
      current_user=db.collection('tennis_players').document('user_document').get()
      current_user=current_user.to_dict()
      if current_user['id']==data['id']:
          return f(*args, **kwargs)
            
      return jsonify({'message': 'token is invalid'})

      
   return decorator
@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
#   cred = credentials.Certificate('C:/Users/sudar/Downloads/springmltraining.json')
#   if not firebase_admin._apps:
#     default_app = initialize_app(cred)
#   db = firestore.client()
  cred = credentials.ApplicationDefault()
  if not firebase_admin._apps:
   firebase_admin.initialize_app(cred, {
   'projectId': 'springmltraining', 
   })
  

  db = firestore.client()   

  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  user = db.collection('tennis_players').document('user_document').get()  
  user=user.to_dict()
  print(user['password'])   
  if user['password']==auth.password:  
     token = jwt.encode({'id':1,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'],algorithm="HS256")  
     return jsonify({'token' : token}) 

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})   


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port,debug=True)   
      

     