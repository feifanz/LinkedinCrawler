# simple restful server
# status: 1 means success, 2 means failure
# using .csv files in static to do temporary store
from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import numpy as np

from crawler.crawler_factory import CrawlingThread
from cluster.kmeans import KmeansByNumber
from cluster.kmeans2 import KmeamsByText

app = Flask(__name__)
api = Api(app)

# store the crawler thread
store = {'crawling_thread': None}

# serve crawler api
class Crawling(Resource):
    def get(self, option):
        try:
            if option == 'start':
                # start crawler, current only support single thread
                if store['crawling_thread'] is None or not store['crawling_thread'].isAlive():
                    store['crawling_thread'] = CrawlingThread(1, "Thread-1")
                    store['crawling_thread'].start()
                    return {'status': 0}
                else:
                    return {'status': 1}
            elif option == 'status':
                # check crawler status, return data has been collected
                if store['crawling_thread'] is None:
                    return {'status': 0, 'data': {'runningFlag': False}}
                else:
                    return {'status': 0, 'data': {'runningFlag': store['crawling_thread'].isAlive(),
                                                  'userList': store['crawling_thread'].getUserList()}}
            elif option == 'stop':
                # stop crawler thread
                store['crawling_thread'].stop()
                return {'status': 0}
        except Exception as e:
            return {'status': 1, 'data':str(e)}

# serve fetch userinfo
class UserInfo(Resource):
    def get(self, file):
        # read data from newly fetched data
        try:
            df = pd.read_csv('static/' + file).replace(np.nan, ' ', regex=True)
            return {'status': 0, 'data': df.values.tolist()}
        except Exception as e:
            return {'status': 1}

# serve k-means cluster
# type: 0 for kmeans.py, 1 for kmeans2.py
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


# add router
api.add_resource(Crawling, '/api/crawler/<string:option>')
api.add_resource(UserInfo, '/api/userinfo/<string:file>')
api.add_resource(Kmeans, '/api/kmeans/<int:type>/<string:file>')

if __name__ == '__main__':
    app.run(debug=True)
