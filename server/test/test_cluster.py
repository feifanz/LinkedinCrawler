# test cluster with visible chrome browser
import pandas as pd
import numpy as np
from cluster.kmeans import KmeansByNumber
from cluster.kmeans2 import KmeamsByText
import matplotlib.pyplot as plt

# test cluster KmeansByNumber
def test_kmeans():
    df = pd.read_csv('../static/userinfo_demo.csv')
    data = KmeansByNumber.do_kmeans_cluster(df)

    # plotting
    dic = {'job':[],'connection':[],'group':[]}
    for d in data:
        dic['job'].append(d['job'])
        dic['connection'].append(d['connection'])
        dic['group'].append(d['group'])
    df = pd.DataFrame(dic)
    df_center = df[df['group'] == 'center_point']
    df_0 = df[df['group'] == '0']
    df_1 = df[df['group'] == '1']
    df_2 = df[df['group'] == '2']

    # draw picture
    plt.scatter(df_center['job'], df_center['connection'])
    plt.scatter(df_0['job'], df_0['connection'])
    plt.scatter(df_1['job'], df_1['connection'])
    plt.scatter(df_2['job'], df_2['connection'])
    plt.show()

# test cluster KmeamsByText
def test_kmeans_2():
    df = pd.read_csv('../static/userinfo_demo.csv')
    data = KmeamsByText.do_kmeans_cluster(df)
    print 'Top Tne Terms'
    print 'cluster_0:', data['topTerms'][0]
    print 'cluster_1:', data['topTerms'][1]
    print 'cluster_2:', data['topTerms'][2]
    print ''
    print 'cluster number'
    print 'cluster_0:', len(data['userGroup'][0])
    print 'cluster_1:', len(data['userGroup'][1])
    print 'cluster_2:', len(data['userGroup'][2])

if __name__ == '__main__':
    test_kmeans()
    #test_kmeans_2()
