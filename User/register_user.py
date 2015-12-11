import os, sys
import cgi
import webapp2, json
from datetime import datetime
from google.appengine.ext import ndb
from User.models import User
import logging
#Get Functionality.



class RegisterHandler(webapp2.RequestHandler):
	def  post(self):

			register_fields = json.loads(self.request.body)
			#Check if email exists:
			email = register_fields["email"]
			name = register_fields["name"]
			city = register_fields["city"]
			query = ndb.gql("SELECT * FROM User WHERE email=:1", email).fetch()
			if not query:
				user = User()
				user.email = email
				user.name = name
				user.city = city
				user.put()
			else:
				logging.info("User exists")
		# except Exception as e:
		# 	logging.info("Unable to Register User.")
        #
