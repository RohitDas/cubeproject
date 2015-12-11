from google.appengine.ext import ndb


class User(ndb.Model):
    """
        This is the definition of the cube model.
	"""
    created_on = ndb.DateTimeProperty()
    email = ndb.StringProperty() # This would be the unique_id
    name = ndb.StringProperty()
    city = ndb.StringProperty()
  
