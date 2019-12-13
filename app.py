from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from project.mongo import mongoData
from project.health_check import HealthCheck
from project.swagger import Swagger
from flask_restful import Resource, Api, reqparse
import requests
import json
import logging

app = Flask(__name__)
CORS(app)
api = Api(app)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger()

logging.info("Started Service")


class Artist(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument("artist", type=str)

        args = parser.parse_args()

        mongo = mongoData(app)

        artist_from_db = mongo.get_one({"artist": args.artist})

        if artist_from_db:
            logging.info("Found artist in service database")
            return jsonify(artist=artist_from_db["artist"])
        
        response = requests.get("https://api.vagalume.com.br/search.art?q={artist}".format(artist=args.artist)).text
        
        artist_list = json.loads(response).get("response").get("docs")

        sanitized_artist_list = []

        for artist in artist_list:
            sanitized_artist_list.append({"artist": artist["band"]})

        artist_json = jsonify(sanitized_artist_list)
        
        mongo.add_many(sanitized_artist_list)
            
        return artist_json


class CheckLyricService(Resource):
    def get(self):
        response = requests.get("http://lyric-service-app.herokuapp.com").text
        json_response = "Lyric service responded with {}".format(jsonify(response))
        logging.info("Healthy")
        return json_response
            

api.add_resource(HealthCheck, '/')
api.add_resource(CheckLyricService, '/api/v1/lyric_check')
api.add_resource(Swagger, '/docs')
api.add_resource(Artist, '/api/v1/artist')

if __name__ == '__main__':
    port = int(getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
