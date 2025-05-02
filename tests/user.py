from flask_restful import Resource

class TestAPI(Resource):
    def get(self):
        return {'message':'hello world'}
    
