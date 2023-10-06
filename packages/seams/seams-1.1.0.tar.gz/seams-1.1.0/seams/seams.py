#!/usr/bin/env python
from requests import Request, Session, utils, Response
from itertools import islice
import mimetypes
import tempfile
from seams.exceptions import SeamsException, SeamsAPIException
import json
import msal
import os
import time
import certifi
from requests_toolbelt import MultipartEncoder

class Seams(object):
    '''
    A Python interface for the Seams API
    '''
    
    def __init__(self, 
                 URL: str):
        '''
        Create an instance of the Seams API interface
        '''

        # Remove any trailing slash, if any
        self.URL = URL.rstrip('/')
        self.connected = False
        self.schemas = None
        self.current_schema = None
        self.retry = self.__check_int(os.getenv("RETRY"))
        self.wait_time = self.__check_float(os.getenv("WAIT_TIME"))
        self.key = None
        if self.retry == None:
            self.retry = 5
        if self.wait_time == None:
            self.wait_time = .5


    def connect(self, key: str = None) -> None:
        '''
        Connect to the Seams API
        :param key:
            A secret API Key given by RJLG staff to access the Seams SDK  **REQUIRED**
        :returns:
            None
        '''
        
        if key is None:
            key = os.getenv("SEAMS_API_KEY")

        if key is None:
            raise SeamsAPIException("Error: API Key is required.")
        
        self.key = key

        self.token = self.acquire_token()
        

    def acquire_token(self) -> None:
        '''
        Calls the SEAMS APIKey Login Method
        '''
        session = Session()

        api_url = '{}{}'.format(self.URL, '/auth/apiKeyLogin')

        request = Request('POST', api_url, data={ 'key': self.key })
        prepared = session.prepare_request(request)
        response = session.send(prepared)

        self.connected = True
        return response.text

    
    def install_certs(self, filename:str) -> None:
        '''
        Installs a cert to your python PEM file from a given filename
        '''
        filepath = certifi.where()
        rjlg_cert = open(filename, "r")
        pem_file = open(filepath, "r")
        if rjlg_cert.read() not in pem_file.read():
            pem_file.close()
            rjlg_cert.close()
            rjlg_cert = open(filename, "r")
            pem_file = open(filepath, "a+")
            pem_file.write(rjlg_cert.read())
        pem_file.close()
        rjlg_cert.close()


    def disconnect(self) -> None:
        '''
        Disconnect from the Seams API 
        '''
        self.connected = False
        self.schemas = None
        self.current_schema = None


    def me(self) -> str:
        '''
        Verifies the user is connected and returns data relating to the graph database

        :returns:
            JSON object representing the graph database
        '''
        
        response = self.__seams_api_request('GET', '/auth/me', schema_api_url=False)
        return response.json()


    def whoami(self) -> str:
        '''
        Gives info on the connection information of the current Seams object

        :returns:
            The bearer token, URL, connected status, and secret
        '''

        try:
            response = {
                'url': self.URL,
                'connected': self.connected
            }
            return response
        except:
            return {'url': self.URL, 'connected': self.connected}


    def get_schemas(self, refresh = False) -> dict:
        '''
        Gets the list of available schemas in the current database

        :param refresh
            Refresh the list of schemas from the database or use the local cached copy
        :returns:
            JSON object representing the schema graph databases
        '''

        if (self.schemas is not None and refresh is False):
            return self.schemas

        schemas = {}

        response = self.me()
        for schema in response["tenants"]:
            name = schema["tenant"]["name"]
            schemas[name] = schema["tenant"]

        self.schemas = schemas

        return schemas


    def get_schema_by_name(self, schema_name:str) -> dict:
        '''
        Get the schema by name

        :param schema_name:
            The name of the schema to get  **REQUIRED**
        :returns:
            A graph dictionary
        '''
        return self.get_schemas()[schema_name]


    def get_schema_by_id(self, schema_id: str) -> dict:
        '''
        Get the current schema for the Id

        :returns:
            The schema matching the Id
        '''
        schemas = self.get_schemas()
        for schema_name, schema_properties in schemas.items():
            if schema_properties["id"] == schema_id:
                return schemas[schema_name]

        return None


    def get_current_schema(self) -> dict:
        '''
        Get the current schema

        :returns:
            The current schema
        '''
        return self.current_schema


    def get_current_schema_id(self) -> dict:
        '''
        Get the current schema Id

        :returns:
            The current schema Id
        '''
        if self.current_schema is None:
            return None
        return self.current_schema["id"]


    def set_current_schema(self, schema: dict) -> None:
        '''
        Set the current schema

        :returns:
            None
        '''
        self.current_schema = schema


    def set_current_schema_by_id(self, schema_id: str) -> None:
        '''
        Set the current schema from the id

        :returns:
            None
        '''
        self.current_schema = self.get_schema_by_id(schema_id) 


    def get_vertex_by_id( self, 
                          vertex_id: str,
                          schema_id = None ) -> str:
        '''
        Get a vertex by vertex id

        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A vertex
        '''

        response = self.__seams_api_request('GET', '/vertex/{}'.format(vertex_id) , schema_id=schema_id)
        if response is None:
            return None

        return response.json()
    

    def get_vertices_by_label(self, 
                              vertex_label: str,
                              schema_id: str = None) -> str:
        '''
        Get all vertices with a specific label

        :param vertex_label:
            The label of the vertex the user is getting  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            JSON formatted list of vertices
        '''

        response = self.__seams_api_request('GET', '/vertices/{}'.format(vertex_label) , schema_id=schema_id)
        if response is None:
            return None

        return response.json()


    def update_vertex(self, 
                      vertex_id: str, 
                      vertex_label: str, 
                      attributes: dict,
                      schema_id: str = None,
                      chunk_attributes: bool = False) -> str:
        '''
        Update a vertex 

        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is getting  **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            JSON formatted vertex with the updates
        '''


        response = None
        if not chunk_attributes:
            body = self.__properties_formatter(vertex_label, attributes)
            response = self.__seams_api_request('PUT', '/vertex/update/{}'.format(vertex_id), content_type='application/json', data=body, schema_id=schema_id)

        # Chunk the attributes
        for attributeChunk in self.__chunk_attributes(attributes, 10):
            body = self.__properties_formatter(vertex_label, attributeChunk)
            response = self.__seams_api_request('PUT', '/vertex/update/{}'.format(vertex_id), content_type='application/json', data=body, schema_id=schema_id)

        return response.json()


    def create_vertex(self, 
                      vertex_label: str,
                      vertex_name: str, 
                      attributes: dict = None,
                      schema_id: str = None,
                      chunk_attributes: bool = False ) -> str:
        '''
        Create a vertex

        :param vertex_label:
            The label of the vertex the user is creating  **REQUIRED**
        :param vertex_name:
            The name of the vertex the user is creating **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A JSON formatted object representing the new vertex
        '''
        body = {}

        if not chunk_attributes:
            # Create the vertex with no chunking
            body = self.__properties_formatter(vertex_label, attributes, vertex_name=vertex_name)
            response = self.__seams_api_request('POST', '/vertex/create', content_type='application/json', data=body, schema_id=schema_id)
            return response.json()

        # Chunk the attributes
        if attributes:
            body = self.__properties_formatter(vertex_label, {"name":vertex_name}, vertex_name=vertex_name)

        # Create the initial vertex
        response = self.__seams_api_request('POST', '/vertex/create', content_type='application/json', data=body, schema_id=schema_id)

        # Chunk the properties as updates
        for attributeChunk in self.__chunk_attributes(attributes, 10):
            body = self.__properties_formatter(vertex_label, attributeChunk)
            response = self.__seams_api_request('PUT', '/vertex/update/{}'.format(response.json()['id']), content_type='application/json', data=body, schema_id=schema_id)

        return response.json()


    def upsert_vertex(self, 
                      vertex_label: str,
                      vertex_name: str, 
                      attributes:dict = None,
                      schema_id:str = None,
                      chunk_attributes: bool = False) -> dict:
        '''
        Create a vertex

        :param vertex_label:
            The label of the vertex the user is creating  **REQUIRED**
        :param vertex_name:
            The name of the vertex the user is creating **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A JSON formatted object representing the new vertex
        '''

        # Find an existing vertex with the label and exact name
        url_string = '/vertex?filter%5Blabel%5D={}&filter%5Bproperty%5D=name%3D{}&filter%5Bunique%5D=&orderBy=&limit=1&offset='.format(utils.quote(vertex_label), utils.quote(vertex_name))
        response = self.__seams_api_request('GET', url_string, schema_id=schema_id)
        existingVertex = None

        for vertex in response.json()["vertices"]:
            if vertex["name"] == vertex_name:
                existingVertex = vertex
        
        response = None
        if ( existingVertex ):
            vertex_id = existingVertex["id"]
            response = self.update_vertex(vertex_id, vertex_label, attributes, schema_id=schema_id, chunk_attributes=chunk_attributes)
        else:
            response = self.create_vertex(vertex_label, vertex_name, attributes=attributes, schema_id=schema_id, chunk_attributes=chunk_attributes)

        return response


    def delete_vertex(self, 
                      vertex_id: str,
                      schema_id: str = None) -> str:
        '''
        Delete a vertex

        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A message specifying if the delete was successful or not
        '''

        response = self.__seams_api_request('DELETE', '/vertex/delete/{}'.format(vertex_id), schema_id=schema_id)
        return response.text
        

    def get_edge_vertices(self, 
                            vertex_id: str, 
                            other_vertex_label: str, 
                            direction: str,
                            schema_id: str = None) -> str:
        '''
        Retreive all edges on a vertex based on direction

        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param other_vertex_label:
            The label of the vertex for the OTHER vertex (used to combine the vertex labels to create edge name)  **REQUIRED**
        :param direction:
            The direction of the edge  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A JSON formatted list of all edges on a vertex
        '''

        response = self.__seams_api_request('GET', '/edgeVertices/{}/{}/{}'.format(vertex_id, other_vertex_label, direction), schema_id=schema_id)
        if response is None:
            return None
        return response.json()
        

    def attach_edges(self, 
                    parent_id: str, 
                    child_vertices: list,
                    schema_id: str = None) -> str:
        '''
        Attach edge from one vertex to another

        :param parent_id:
            The vertex id of the parent vertex  **REQUIRED**
        :param child_vertices:
            A list of vertex id's to attach the edge to  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A success or fail message if the edges were attached
        '''
        body = {
            'parentVertex': parent_id,
            'edgeVertices': child_vertices
        }
        response = self.__seams_api_request('POST', '/edge/attach', json=body, schema_id=schema_id)

        return response.text
        

    def attach_label_to_edge(self, 
                             parent_label: str, 
                             edge_name: str, 
                             child_id: str,
                             schema_id: str = None) -> str:
        '''
        Attach label to an edge

        :param parent_label:
            The label of the parent vertex  **REQUIRED**
        :param edge_name:
            The name of the edge  **REQUIRED**
        :param child_id:
            A single vertex id of the child  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A success or fail message if the label was attached
        '''

        body = '{{"parentVertexLabel": "{}", "edgeName": "{}", "childVertex": "{}"}}'.format(parent_label, edge_name, child_id)
        response = self.__seams_api_request('POST', '/edge/attach/label/to', data=body, schema_id=schema_id)
        if response is None:
            return None
        return response.json()


    def attach_label_from_edge(self, 
                               parent_vertex: str, 
                               edge_name: str, 
                               child_label: str,
                               schema_id:str = None) -> str:
        '''
        Attach label from an edge

        :param parent_vertex:
            The parent vertex  **REQUIRED**
        :param edge_name:
            The name of the edge  **REQUIRED**
        :param child_label:
            The label of the child  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A success or fail message if the label was attached
        '''

        body = '{{"parentVertex": "{}", "edgeName": "{}", "childVertexLabel": "{}"}}'.format(parent_vertex, edge_name, child_label)
        response = self.__seams_api_request('POST', '/edge/attach/label/from', data=body, schema_id=schema_id)
        if response is None:
            return None

        return response.json()


    def upload_file(self, 
                    caption: str,
                    filename: str, 
                    file_type: str = 'File',
                    schema_id: str = None) -> str:
        '''
        Upload a sinlge file

        :param filename:
            Filename the user would like to upload  **REQUIRED**
        :param file_type:
            Can be 'File' or 'Image' - defaults to 'File'
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            A list of vertex id's for the uploaded files
        '''

        if not os.path.exists(filename):
            raise SeamsAPIException("File upload failed, file not found: {}".format(filename))

        mimetype = mimetypes.guess_type(filename)[0]
        if mimetype == "application/vnd.ms-excel":
            mimetype = "text/csv"

        encoder = MultipartEncoder(
            fields={'file': (filename, open(filename, 'rb'), mimetype) , 'fileType': file_type , 'caption': caption }
        )

        response = self.__seams_api_request('POST', '/upload/file', data=encoder, content_type=encoder.content_type, schema_id=schema_id)

        return response.json()


    def download_file(self, 
                      vertex_id: str,
                      schema_id: str = None,
                      path: str = None) -> str:
        '''
        Download a single file

        :param vertex_id:
            vertex id  of the file the user would like to download  **REQUIRED**
        :param schema_id:
            The id of the SEAMS schema to access  **OPTIONAL**
        :returns:
            Path of the file downloaded
        '''
        
        response = self.__seams_api_request('GET', '/download/file/{}'.format(vertex_id), schema_id=schema_id)
        file_path = self.__build_file_name(response, path)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
        return file_path
    

    def create_chart_from_file(self,
                               parent_vertex_id:str,
                               file_vertex_id:str,
                               chart_name:str, 
                               x_label_column:str, 
                               y_label_column:str, 
                               chart_type:str, 
                               y_label_column_2:str=None) -> tuple[str,str]:
        '''
        Creates a chart vertex type and attaches an edge to connect it to the parent

        :param parent_vertex_id:
            Vertex id of the vertex the edge is coming from
        :param file_vertex_id:
            Vertex id of the file you want to create the chart from
        :param chart_name"
            Name of the chart, this will also be the name of the Chart vertex (something like "Pressure vs Time")
        :param x_label_column:
            X data column name
        :param  y_label_column:
            Y data column name
        :param chart_type:
            Type of chart to display "line", "pie", "doughnut", "scatter", "vertical", "horizontal" (last two are different types of bar charts)
        :param y_label_column_2: OPTIONAL
            Optional parameter for if there are two datasets that need to overlap on one chart

        :returns (edge_result, chart_vertex_id): 
            Tuple of edge connection result and new chart vertex id
        '''
        attributes = {
            "datasource_file_id": file_vertex_id,
            "title": chart_name,
            "dataset_1_labels_column": x_label_column,
            "dataset_1_values_column": y_label_column,
            "type": chart_type
        }
        if y_label_column_2 is not None:
            attributes["dataset_2_values_column"] = y_label_column_2
        chart_vertex = self.create_vertex("Chart", chart_name, attributes)
        edge_result = self.attach_edges(parent_vertex_id, [chart_vertex["id"]])
        return (edge_result, chart_vertex["id"])

    
    def __build_file_name(self,
                          response: Response,
                          path: str = None):
        file_path = ""
        if path:
            file_path = os.path.join(path, self.__file_name_formatter(response.headers['filename']))
        else:
            file_path = os.path.join(tempfile.gettempdir(), self.__file_name_formatter(response.headers['filename']))
        return file_path


    def __file_name_formatter(self, 
                              file_name):
        '''
        Private helper function that formats the filename and allows the use of '-' in filenames
        '''

        file_name_list = file_name.split('-')
        del file_name_list[0:5]
        if len(file_name_list) > 1:
            new_file = ''
            for item in file_name_list:
                new_file = new_file + '-' + item
            file_name_list[0] = new_file[1:]
        return file_name_list[0]


    def __properties_formatter(self, 
                               vertex_label: str, 
                               args,
                               vertex_name = None) -> str:
        '''
        Private helper function that formats a list of key value pairs for properties on a vertex
        '''
        for item in args:
            if item != 'status':
                if isinstance(args[item], list):
                    args[item] = json.dumps(args[item])

        if vertex_name:
            return '{{"vertexLabel": "{}", "vertexName": "{}", "properties": {}}}'.format(vertex_label, vertex_name, json.dumps(args)).replace("'", "")
        else:
            return '{{"vertexLabel": "{}", "properties": {}}}'.format(vertex_label, json.dumps(args)).replace("'", "")


    def __seams_api_request(self, 
                       req_type: str, 
                       url:str, 
                       data: dict = None, 
                       content_type :str = None, 
                       files = None,
                       json = None,
                       schema_id:str = None,
                       schema_api_url = True):
        '''
        Private helper function that makes a specific type of HTTP request to SEAMS
        '''
        
        bearer = self.token
        header = {'Authorization': 'Bearer {}'.format(bearer)}
        if content_type:
            header['Content-Type'] = content_type

        session = Session()

        # Get the full URL path
        if schema_api_url:
            if schema_id is None:
                schema_id = self.get_current_schema_id()
                if schema_id is None:
                    raise SeamsAPIException("Error: You must provide a schema id for this API call.  There is no current schema Id set or sent.")
            api_url = '{}/tenant/{}{}'.format(self.URL, schema_id, url)
        else:
            api_url = '{}{}'.format(self.URL, url)

        request = Request(req_type, api_url, headers=header, data=data, files=files, json=json)
        prepared = session.prepare_request(request)
        # Retry the HTTPS request, break loop if it returns good status code
        error = None
        for x in range(self.retry):
            timeout = False
            try:
                response = session.send(prepared)
            except Exception as e:
                timeout = True
                print(e)
                error = e
                continue

            # Raise any HTTP response errors (if any)
            if response.status_code >= 400 or timeout is True:
                time.sleep(self.wait_time*x)
                self.connect()
            else:
                break
        
        if timeout is True:
            raise error

        if response.status_code >= 400:
            raise SeamsAPIException("Error {} {}".format(response.status_code, response.text) )

        # Otherwise, return the results
        return response
    

    def __chunk_attributes(self, data, SIZE):
        it = iter(data)
        for i in range(0, len(data), SIZE):
            yield {k:data[k] for k in islice(it, SIZE)}


    def __check_int(self, value):
        if value is None:
            return None
        try:
            return int(value)
        except:
            raise Exception("RETRY env variable should be an integer")
        
    def __check_float(self, value):
        if value is None:
            return None
        try:
            return float(value)
        except:
            raise Exception("WAIT_TIME env variable should be a float or an integer")

