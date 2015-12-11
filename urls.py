import webapp2
from Cube.cube_api import *
from User.register_user import * 

url_patterns_new = [
		('/app/cube/add', CubeHandler),
		('/app/cube/delete', CubeContentDeleteHandler),
		('/app/cube/share', CubeHandler),
		('/app/cube/list', CubeHandler), 
		('/app/content/add', ContentHandler),
		('/app/content/delete', CubeContentDeleteHandler),
		('/app/content/share', ContentHandler),
		('/app/content/list', ContentHandler),
		('/app/register', RegisterHandler)

        ]



application = webapp2.WSGIApplication(url_patterns_new, debug=True)
