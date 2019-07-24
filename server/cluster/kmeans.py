# -*- coding: utf-8 -*-
# feature selection, [the number of words used to describe current job, the number of connection]

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


class KmeansByNumber:
    # pre-process the data, with extra feature for the future upgrade
    @classmethod
    def _clean_data(cls, df):
        # delete duplication
        df.drop_duplicates('name', inplace=True)

        # process job to several different types
        df['job'] = df['job'].map(lambda x: str(x).lower())
        df['job_type_1'] = df['job'].map(lambda x: 'developer' in x)
        df['job_type_2'] = df['job'].map(lambda x: 'designer' in x)
        df['job_word_num'] = df['job'].map(lambda x: len(str(x).split()))

        # precess level from 1 to 4
        df['level'] = df['level'].replace(np.NaN, 4)
        df['level'] = df['level'].map(lambda x: str(x)[0])

        # process connection
        df['connection'] = df['connection'].replace(np.NaN, 0)
        df['connection'] = df['connection'].map(lambda x: str(x).split()[0])
        df['connection'] = df['connection'].replace('500+', '500')

        df2 = df.loc[0:, ['level', 'job_type_1', 'job_type_2', 'job_word_num', 'connection']]
        df2['level'] = df['level'].astype('int')
        df2['job_type_1'] = df['job_type_1'].astype('int')
        df2['job_type_2'] = df['job_type_2'].astype('int')
        return df2

    # do k-means, only using two feature currently
    @classmethod
    def do_kmeans_cluster(cls, df):
        df = cls._clean_data(df)
        df['connection'] = df['connection'].map(lambda x: float(x) / 100)
        df = df.loc[0:, ['job_word_num', 'connection']].reset_index(drop=True)

        # cluster using k-means
        estimator = KMeans(n_clusters=3)
        estimator.fit(df)
        label_pred = estimator.labels_
        centroids = estimator.cluster_centers_

        # center poitns
        df_center = pd.DataFrame(centroids)
        # add group labels
        df['label'] = pd.Series(label_pred)

        # process return date
        res = []
        for d in df_center.values.tolist():
            res.append({'group':'center_point','job':d[0],'connection':d[1]})
        for d in df.itertuples():
            res.append({'group': str(d[3]), 'job': d[1], 'connection': d[2]})

        return res

