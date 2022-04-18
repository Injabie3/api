
from flask_restx import Api, Namespace, Resource

api = Namespace("helloworld", description="Hello World, that is all.")
@api.route("")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

