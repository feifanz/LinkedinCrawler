from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import numpy as np
from flask import send_from_directory

from crawling.crawler import CrawlingThread
from cluster.kmeans import KmeansByNumber
from cluster.kmeans2 import KmeamsByText

app = Flask(__name__)
api = Api(app)

# store the crawling thread
store = {'crawling_thread': None}


#static

class serve_page(Resource):
    def get(self, path):
        print path
        return send_from_directory('static/build/', path)


# serve crawling api
class Crawling(Resource):
    def get(self, option):
        if option == 'start':
            print store
            if store['crawling_thread'] is None or not store['crawling_thread'].isAlive():
                store['crawling_thread'] = CrawlingThread(1, "Thread-1")
                store['crawling_thread'].start()
                return {'status': 0}
            else:
                return {'status': 1}
        elif option == 'status':
            if store['crawling_thread'] is None:
                return {'status': 0, 'data': {'runningFlag': False}}
            else:
                return {'status': 0, 'data': {'runningFlag': store['crawling_thread'].isAlive(),
                                              'userList': store['crawling_thread'].getUserList()}}
        elif option == 'stop':
            store['crawling_thread'].stop()
            return {'status': 0}


# serve fetch userinfo
class UserInfo(Resource):
    def get(self, file):
        # read data from newly fetched data
        df = pd.read_csv('static/' + file).replace(np.nan, ' ', regex=True)
        return {'status': 0, 'data': df.values.tolist()}


class Kmeans(Resource):
    def get(self, type, file):
        try:
            if type == 0:
                df = pd.read_csv('static/' + file)
                data = KmeansByNumber.do_kmeans_cluster(df)
                return {'status': 0, 'data': data}
            elif type == 1:
                df = pd.read_csv('static/' + file).replace(np.nan, ' ', regex=True)
                data = KmeamsByText.do_kmeans_cluster(df)
                return {'status': 0, 'data': data}
        except Exception as e:
            return {'status': 1, 'data': str(e)}

api.add_resource(serve_page, '/<string:path>')
api.add_resource(Crawling, '/api/crawling/<string:option>')
api.add_resource(UserInfo, '/api/userinfo/<string:file>')
api.add_resource(Kmeans, '/api/kmeans/<int:type>/<string:file>')

if __name__ == '__main__':
    app.run(debug=True)
