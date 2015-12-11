import webapp2
import logging
from urls import url_patterns_new
logging.info(url_patterns_new)

application = webapp2.WSGIApplication(url_patterns_new, debug=True)