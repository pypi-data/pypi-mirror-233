# Seams SDK


## Test Files
Test files for Seams can be found in the tests folder /seams/tests/test_api.py    /seams/tests/test_pipeline.py

## Importing Seams
The Seams SDK can be integrated into any Python file by simply calling an import statement and then initializing a new Seams class.

```python
from seams import Seams

seams = Seams()
```

## Set Pythonpath for testing
You must set the pythonpath to the Seams SDK if you wish to run the test files

```bash
set PYTHONPATH=%PYTHONPATH%,C:\Users\{user}\repos\seams-sdk\seams
```

## Connecting to the Seams API
To connect to the Seams API just run the connect() function and pass in the secret, app id, and tenant id, which all should have been given to you by an RJLG employee. The connect() function will not return anything. Once you call the connect() function you can then call seams.bearer to get the bearer token if desired. The bearer token is recorded in the Seams() class and used for each connection behind the scenes.

```python
seams.connect()
```

# Setting the Seams Schema Context

## Find a schema named "Materials"
To get a specific schema by name use the get_schema_by_name() method. This method takes one parameter, a string name of the schema and will return a dictionary that represents the whole schema.
```python
materials = seams.get_schema_by_name("Materials")
print("Materials Schema Id:" , materials["id"])
```

## Set the context of the current Schema
To set the schema simply use the set_current_schema() method. This method takes a single, dictionary parameter that represents the schema the user wishes to query against
```python
print("Setting Contect to Materials Schema")
seams.set_current_schema(materials)
```

## Seams connection information
After you run seams.connect() you'll be able to run seams.whoami() which will return a JSON formatted string of everything that makes up the seams API connection, including: bearer token, API URL, connection status, and the secret, app id, and tenant id that you provided during the connection. Note: if whoami() is run without running connect() first then it will only return the URL and the connected status of False.

```python
seams.whoami()
```

Returns:
```json
"{'url': 'http://localhost:4010/api', 'connected': True}"
```

## Verifying Connection
To verify that you are connected you can call the me() function which currently returns a giant blob of JSON that represents the graph DB for all the tenants.

```python
response = seams.me()
```

## Disconnecting from Seams
To disconnect from the Seams SDK call the disconnect() method. This is not required as there are no active connections open, but it is still best practice. 
```python
seams.disconnect()
```

# Vertex Methods

## Getting vertex by ID
To get a vertex by the vertex ID you can call the get_vertex_by_id(tenantId, id) function. You'll need the tenant id and vertex id to be able to call this function. 

```python
vertex = seams.get_vertex_by_id('704480ce-4e18-47b5-ae41-24cc9c61c075')
```

## Getting vertices by label
To get all vertices under the same label you can call the get_vertices_by_label(tenantId, label). You'll need the tenant id and the label name to be able to call this function. 

```python
label = seams.get_vertices_by_label("Chamber")
```

## Updating a vertex
To update a vertex call the update_vertex method with 3 required arguments: Tenant Id, Vertex Id, and Vertex Label. The last, optional parameter, is a dictionary of key/value pairs that will represent the data fields of the vertex.

```python
attributes = {
    'type':'Manganin', 
    'location':'upper right corner', 
    'description': 'This is a test vertex created from the sdk'
}

update = seams.update_vertex('de7f9c4b-748e-4887-a066-8dc1ba8eec4f', 'Manganin Sensor', attributes)
```

## Upserting a vertex
The upsert_vertex() function can be used to first check to see if a vertex with the given label exists, if it does exist then it will update the vertex with the given attributes, if it doesn't exist it will create the vertex. upsert_vertex() has 3 required arguments, tenant_id, vertex_label, and vertex_name; these are all strings. The last, optional parameter, is a dictionary of key/value pairs that will represent the data fields of the vertex.

```python
print("calling upsert_vertex")
upsert = seams.upsert_vertex("Subject","Test Subject 1", attributes)
print(upsert)
```

## Creating a vertex
To create a vertex call the create_vertex method with 3 required arguments: Tenant Id, Vertex Label, and Vertex Name. The last, optional parameter, is a dictionary of key/value pairs that will represent the data fields of the vertex.

```python
attributes = {
    'type':'Manganin', 
    'location':'upper right corner', 
    'description': 'This is a test vertex created from the sdk'
}

create = seams.create_vertex('Manganin Sensor', 'Manganin Sensor 1', attributes)
```

## Deleting a vertex
To delete a vertex call the delete_vertex method with 2 required arguments: Tenant Id and Vertex Id

```python
delete = seams.delete_vertex(create['id'])
```

## Finding the edges on a vertex
To find the vertices from a specific type of edge off of a vertex use the get_edge_vertices method. This method has 3 required arguments: Tenant Id, Vertex Id and direction.

```python
edges_out = seams.get_edge_vertices('9e2e8dcd-1b68-4b06-ab41-045d78f62e38', "Test", "out")
edges_in = seams.get_edge_vertices('9e2e8dcd-1b68-4b06-ab41-045d78f62e38', "Test", "in")
```


# Edge Methods

## Attaching edges to a vertex
To attach an edge to a vertex call the attach_edges method with 3 required arguments: Tenant Id, Vertex Id and a list of edges that you want to attach to the vertex.

```python
attributes = {
    'type':'Manganin', 
    'location':'upper right corner', 
    'description': 'This is a test vertex created from the sdk'
}
vertex_1 = seams.create_vertex('Manganin Sensor', attributes)
vertex_2 = seams.create_vertex('Manganin Sensor', attributes)
vertex_3 = seams.create_vertex('Manganin Sensor', attributes)

vertex_list = []
vertex_list.append(vertex_1['id'])
vertex_list.append(vertex_2['id'])
vertex_list.append(vertex_3['id'])

set_edges = seams.attach_edges("9e2e8dcd-1b68-4b06-ab41-045d78f62e38", vertex_list)
```

## Attaching a label TO an edge
To attach a label to an edge call the attach_label_to_edge method with 4 required arguments: Tenant Id, Parent Vertex Label, Edge Label and Vertex Id.

```python
set_label_to = seams.attach_label_to_edge("Manganin Sensor", "Manganin Sensor", vertex_1['id'])
```

## Attaching a label FROM an edge
To attach a label from an edge call the attach_label_from_edge method with 4 required arguments: Tenant Id, Parent Vertex Id, Edge Name and Child Label.

```python
set_label_from = seams.attach_label_from_edge(vertex_2['id'], "Manganin Sensor", "Manganin Sensor")
```


# File Methods

## Upload file
To upload a file call the upload_file method which has 2 required arguments, caption and file name.

```python
file1 = open('file-To-Upload.txt', 'w')
file1.write("This is a test text file that is being uploaded and downloaded from the Python SDK.")
file1.close()

upload = seams.upload_files("This is a test file upload", 'file-To-Upload.txt')
```

## Download file
To download a file call the download_file method which has 1 required argument, Vertex Id. This will download the file at the vertex given, writes it to a file, and 
gives the user the path of the downloaded file.

```python
download = seams.download_file(upload[0]['id'])
```