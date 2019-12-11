from os import getenv
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import json
import logging

app = Flask(__name__)
api = Api(app)

mongo_password = getenv("MONGO_PASSWORD", "")

app.config['MONGO_URI'] = "mongodb+srv://admin:{}@cluster0-hb5he.mongodb.net/artist_service?retryWrites=true&w=majority".format(mongo_password)

mongo = PyMongo(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Artist Service"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

class HealthCheck(Resource):
    def get(self):
        return "Health check"

class GetArtist(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument("artist", type=str)

        args = parser.parse_args()

        artist = mongo.db.artists.find_one({"artist": args.artist})

        if artist:
            logging.info("Found artist in service database")
            print("Found artist in service database")
            return jsonify(artist=artist["artist"])
        
        response = requests.get("https://api.vagalume.com.br/search.art?q={artist}".format(artist=args.artist)).text
        
        artist_list = json.loads(response).get("response").get("docs")

        sanitized_artist_list = []

        for artist in artist_list:
            sanitized_artist_list.append({"artist": artist["band"]})

        artist_json = jsonify(sanitized_artist_list)
        
        mongo.db.artists.insert_many(sanitized_artist_list)
            
        return artist_json
            

api.add_resource(HealthCheck, '/')
api.add_resource(GetArtist, '/api/v1/get_artist')

if __name__ == '__main__':
    port = int(getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0',port=port)
