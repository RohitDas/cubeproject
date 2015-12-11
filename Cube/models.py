from google.appengine.ext import ndb

class Content(ndb.Model):
	pass


class Cube(ndb.Model):
	"""
		This is the definition of the cube model.
	"""
	created_by = ndb.KeyProperty()
	name = ndb.StringProperty(required=True)
	content_list = ndb.KeyProperty(Content,repeated=True)
	shared_list = ndb.KeyProperty(repeated=True) #List of keys shared by the user.
	created_on = ndb.DateTimeProperty()


class  Content(ndb.Model):
	created_by = ndb.KeyProperty()
	content_shared_list = ndb.KeyProperty(repeated=True)
	assocated_with_cube = ndb.KeyProperty(Cube)
	independent_content = ndb.BooleanProperty(default=False)
	link = ndb.StringProperty() #Could be changed later



