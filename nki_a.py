from dMRI2nx import dMRI2nx
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
import os 

gpickle_list = os.listdir('./gpickle_data')

csv = open("o.csv", "w")
csv.write('density, avg_clst, avg_deg, r2\n')

for gp in gpickle_list:
    G = dMRI2nx('./gpickle_data/{}'.format(gp))
    subject = gp[4:17]
    # compute density and avg clustering of nodes
    density = nx.density(G)
    avg_clustering = nx.average_clustering(G, weight='weight')
    #print('smlwrld: {}\n'.format(nx.sigma(G)))

    # graphing topological hierarchy (Negative correlation btwn degree
    # and clustering coefficient)
    clst_nodes = nx.clustering(G, weight='weight')
    deg_nodes = G.degree(weight='weight')

    cn_values = []
    for value in clst_nodes.values():
        cn_values.append(value)

    dg_values = []
    for i in range(len(deg_nodes)):
        dg_values.append(deg_nodes[i+1])

    avg_deg = sum(dg_values)/len(dg_values)

    # creating est fit line
    best_fit = np.poly1d(np.polyfit(dg_values, cn_values, 1))
    r2 = r2_score(cn_values, best_fit(dg_values))

    # saving to csv
    csv.write('{},{},{},{}\n'.format(density, avg_clustering, avg_deg, r2))


    # generating output plot
    plt.clf()
    plt.ylim(0, .12)
    plt.scatter(dg_values, cn_values)
    plt.plot(np.unique(dg_values), best_fit(np.unique(dg_values)))
    plt.xlabel("node degree")
    plt.ylabel("clustering coefficient")
    plt.suptitle("topological hierarchy | subject: {}".format(subject), fontweight='bold')
    plt.title("density: {0:.4f},  average clustering: {1:.4f},  r2: {2:.4f}".format(density, avg_clustering, r2))

    # save
    path_name = 'topohi/{}.png'.format(subject + 'TH')
    plt.savefig(path_name)

csv.close()