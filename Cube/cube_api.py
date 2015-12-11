import os, sys
import cgi
import webapp2
from google.appengine.ext import ndb
from  datetime import datetime
import json
from Cube.models import Cube, Content
import logging
#Get Functionality.



class CubeHandler(webapp2.RequestHandler):
    def  post(self):
        # try:
            cube_fields = json.loads(self.request.body)
            logging.info(cube_fields)
            if cube_fields:
                cube = Cube()
                self.createCube(cube,cube_fields)
                cube.put()
            else:
                logging.info("No input data")
                return
        # except Exception as e:
        #     logging.info("Error posting a Content")


    def get(self):
            user = dict(self.request.params)["user"]
            logging.info(user)
            response = {"personal": [], "shared": []}
            lists = []
            #Do a gql Query to fetch the personal; queries
            query_1 = ndb.gql("SELECT * FROM Cube WHERE created_by=:1",ndb.Key(urlsafe=str(user))).fetch()
            if query_1:
                response["personal"] = convert_query_to_dict(query_1)
                #Another gql query shall fetch the shared.
            logging.info(response["personal"])

            query_2 = ndb.gql("SELECT * FROM Cube WHERE shared_list=:1", ndb.Key(urlsafe=str(user))).fetch()
            #Code to convert an instance to a dictionary value
            logging.info(query_2)
            if query_2:
                logging.info("adfad")
                response["shared"] = convert_query_to_dict(query_2)
            logging.info(response)
            return self.response.write(json.dumps(response))

    def put(self):
        # """
    	# 	This shall handle the Cube Share Functionality
    	# """
        # try:
            cube_shared_fields = json.loads(self.request.body)
            user_to_be_shared_with = cube_shared_fields["user"]
            cube_key = cube_shared_fields["cube"]
            #First Update the CUBE.
            cube = ndb.Key(urlsafe=str(cube_key)).get()
            list_of_contents = cube.content_list
            logging.info(list_of_contents)
            shared_list = [key.urlsafe() for key in cube.shared_list]
            shared_list.append(user_to_be_shared_with)
            cube.shared_list = [ndb.Key(urlsafe=str(key)) for key in list(set(shared_list))]


            #Fetch all the contents and input the user2 key.
            for content in list_of_contents:
                logging.info(content)
                content_instance = content.get()
                shared_with_users = [user.urlsafe() for user in content_instance.content_shared_list]
                shared_with_users.append(user_to_be_shared_with)
                content_instance.content_shared_list = [ndb.Key(urlsafe=user) for user in list(set(shared_with_users))]
                content_instance.put()
            cube.put()
        # except Exception as e:
        #     logging.info("Error while sharing a cube")


    def delete(self):
        """ This handles the delete functionality"""
        pass


    def createCube(self,cube, cube_fields):
    	"""
    		A helper Function that initializes a cube during a post request.
    	"""
        cube.name = cube_fields["name"]
        cube.created_by = ndb.Key(urlsafe=str(cube_fields["user"]))
        cube.create_on = datetime.now()
        return  cube



class ContentHandler(webapp2.RequestHandler):
    """
	    This Handler handles all the requests for deleting or adding contents.
	"""

    def get(self):
        try:
            params = dict(self.request.params)
            user_id = params["user"]

            # Contents created by the user and the contents shared with the user.
            result = {"personal": None, "shared": None}
            #Query to read all the personalized contents
            query = ndb.gql("SELECT * FROM Content WHERE created_by=:1", ndb.Key(urlsafe=str(user_id))).fetch()
            if query:
                result["personal"] =  [str(query.link)   for query in query]
            query = ndb.gql("SELECT * FROM Content WHERE content_shared_list=:1", ndb.Key(urlsafe=str(user_id))).fetch()
            if query:
                result["shared"] =  [str(query.link)   for query in query]
            return self.response.write(json.dumps(result))
        except Exception as e:
            logging.info("Error in Getting the List")

    def post(self):
        # try:
            content_fields = json.loads(self.request.body)
            content = Content()
            cubes = content_fields["cubes"] if content_fields.has_key("cubes") else None
            logging.info(cubes)
            content.created_by = ndb.Key(urlsafe=content_fields["user"])
            content.link = content_fields["link"]
            content.created_on = datetime.now()

            if cubes:


                    content.put()
                    key = content.key
                    for cube in cubes:
                    #Fetch the cube and append it to the list of contents.
                        cube_instance = ndb.Key(urlsafe=str(cube)).get()
                        logging.info(cube_instance)
                        cube_instance.content_list.append(key)
                        cube_instance.put()

            else:
                content.independent_content = True
                content.put()


        # except Exception as e:
        #     logging.info("Error in creating a Content")


    def put(self):
        # """
        # 	Put Here amounts to Sharing a Content.
        # """
        # try:
            content_share_fields = json.loads(self.request.body)
            user_key_to_share = content_share_fields["user"]
            content_key = content_share_fields["key"]

            #Update the information.
            fetched_content = ndb.Key(urlsafe=str(content_key)).get()
            prev_content_list = fetched_content.content_shared_list
            if prev_content_list:
                prev_content_list.append(ndb.Key(urlsafe=str(user_key_to_share)))
            else:
                prev_content_list = [ndb.Key(urlsafe=str(user_key_to_share))]
            fetched_content.content_shared_list = prev_content_list
            fetched_content.put()
        #
        # except Exception as e:
        #     logging.info("Error in Sharing with others")

class CubeContentDeleteHandler(webapp2.RequestHandler):
    """  This class handles the delete functionality
	"""
    def get(self):
        pass

    def post(self):
        """
            This Handler takes a cube id and a content id.
        """
        fields = json.loads(self.request.body)
        logging.info(fields)
        cube = fields["cube"] if fields.has_key("cube") else None
        logging.info("adadads")
        content = fields["content"] if fields.has_key("content") else None
        logging.info(content)
        if cube:
            if content:
                #Fetch the Cube.
                cube_instance = ndb.Key(urlsafe=str(cube)).get()
                content_instance = ndb.Key(urlsafe=str(content)).get()
                cube_shared_list = [key.urlsafe() for key in cube_instance.shared_list]
                content_list = [content.urlsafe() for content in cube_instance.content_list]
                logging.info(content)
                logging.info(content_list)
                if content.urlsafe() in content_list:
                    logging.info("jbkjhjb")
                    index = content_list.index(content.urlsafe())
                    del content_list[index]
                cube_instance.content_list = [ndb.Key(urlsafe=str(key)) for key in list(set(content_list))]
                cube_instance.put()
                logging.info("sacdasdca")
                #Fetch the Content now.logging.info("sacdasdca")

                logging.info(content_instance)
                logging.info("sacdasdca")
                created_by = content_instance.created_by.urlsafe()
                shared_content_list = [key.urlsafe() for key in content_instance.content_shared_list]
                logging.info("sacdasdca")
                logging.info(content)
                if created_by in cube_shared_list:
                    for key in cube_shared_list:
                        index = shared_content_list.index(key)
                        del shared_content_list[index]

                if shared_content_list:
                    content_instance.created_by = ndb.Key(urlsafe=shared_content_list[0])
                else:
                    #Delete the instance.
                    pass


            else:
                #   Delete the Cube
                    ndb.Key(urlsafe=str(cube)).delete()
                    #Check for the





def convert_query_to_dict(query_object):
    query_list = []
    logging.info(query_object)
    for query in query_object:
        query_obj = {}
        query_obj["name"] = str(query.name)
        if query.content_list:
            query_obj["content_list"] =  [id.urlsafe() for id in query.content_list]
        query_list.append(query_obj)
    logging.info(query_list)
    return query_list

def get_name_from_key(content):
    return "www.google.com"