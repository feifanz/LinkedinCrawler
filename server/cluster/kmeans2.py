# -*- coding: utf-8 -*-
# feature selection, TF-IDF on job filed

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import pandas as pd


class KmeamsByText:
    @classmethod
    def do_kmeans_cluster(cls, df):
        # delete duplication
        df.drop_duplicates('name', inplace=True)
        # select needed data
        documents = df['job']

        # IF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(documents)

        # kmeans clustering
        true_k = 3
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)

        # 3 clustered points groups
        label_pred = model.labels_
        df['label'] = pd.Series(label_pred)
        df_cluster_1 = df[df['label'] == 0]
        df_cluster_2 = df[df['label'] == 1]
        df_cluster_3 = df[df['label'] == 2]
        pointGroup = [df_cluster_1.values.tolist(),
                      df_cluster_2.values.tolist(),
                      df_cluster_3.values.tolist()]

        # top ten terms for each cluster
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        top_terms = []
        for i in range(true_k):
            tmp = []
            for idx in order_centroids[i, :10]:
                tmp.append(terms[idx].encode('utf-8'))
            top_terms.append(tmp)

        res = {'userGroup':pointGroup,'topTerms':top_terms}

        return res


