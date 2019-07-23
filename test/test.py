import pandas as pd

from server.cluster import kmeans

df = pd.read_csv('userinfo_demo.csv')
kmeans.do_kmeans_cluster(df)