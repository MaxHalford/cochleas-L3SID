import pandas as pd
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA as sklearnPCA
import numpy as np
import scipy.stats as stats

# Script settings
normalization = True
plotExample = True
plotDifferences = False
plotLinks = False
plotPCA = False

# Prepare the data
data = {'male' : [], 'female' : []}
maleFiles = [f for f in os.listdir(os.getcwd() + '/data/male/')]
femaleFiles = [f for f in os.listdir(os.getcwd() + '/data/female/')]
c = ['x', 'y', 'z']

# Read each file into a dataframe
data['male'] = [pd.read_table('data/male/'+m, delimiter=r"\s+", names=c).dropna() for m in maleFiles]
data['female'] = [pd.read_table('data/female/'+f, delimiter=r"\s+", names=c).dropna() for f in femaleFiles]

# Plot some cochleas
if plotExample:
    ax = plt.axes(projection='3d')
    for d in data['male'][3:4]:
        ax.scatter(d['x'], d['y'], d['z'], c = d['x']*d['y']*d['z'])
    plt.show()

# Save the data before normalizing for plotting later on
pData = data.copy()

# We might as well normalize the data
if normalization:
    normalize = lambda df: (df - df.mean()) / (df.var())
    data['male'] = [normalize(indi) for indi in data['male']]
    data['female'] = [normalize(indi) for indi in data['female']]

# Get the distances between each point (1000 * 999 / 2) for each dataframe
maleDist = [squareform(pdist(male)) for male in data['male']]
femaleDist = [squareform(pdist(female)) for female in data['female']]

# And the mean distances to get an idea of the difference between male and female
meanMaleDist = sum(maleDist) / len(maleDist)
meanFemaleDist = sum(femaleDist) / len(femaleDist)
difference = meanMaleDist - meanFemaleDist

# Plot the differences
if plotDifferences:
    f, ax = plt.subplots(1, 3)
    ax[0].imshow(meanMaleDist)
    ax[0].set_title('Male mean cochlea point distances')
    ax[1].imshow(meanFemaleDist)
    ax[1].set_title('Female mean cochlea point distances')
    ax[2].imshow(difference)
    ax[2].contour(difference)
    ax[2].set_title('Difference')
    plt.show()

# Collect the points of difference
p1 = (890, 343, 416, 519, 744, 604, 899, 893)
p2 = (521, 196, 255, 348, 512, 12, 255, 38)

# Plot them
if plotLinks:
    ax = plt.axes(projection='3d')
    cochleas = [pData['male'][0], pData['female'][0]]
    # For each individual
    for d in cochleas:
        # Plot the cochlea
        ax.scatter(d['x'], d['y'], d['z'], c = d['x']*d['y']*d['z'])
        # For each distance of interest
        for i in range(len(p1)):
            # Plot the link
            x = (d.iloc[p1[i]]['x'], d.iloc[p2[i]]['x'])
            y = (d.iloc[p1[i]]['y'], d.iloc[p2[i]]['y'])
            z = (d.iloc[p1[i]]['z'], d.iloc[p2[i]]['z'])
            ax.plot(x, y, z)
    plt.show()

# Individual significant distances
index = ['M' + str(i) for i in range(0, 12)] + \
        ['F' + str(i) for i in range(0, 10)] + \
        ['Mean_M', 'Mean_F'] 
columns = [p for p in zip(p1, p2)]
distances = pd.DataFrame(0.0, index=index, columns=columns)

# Zip the x and y together
for p in zip(p1, p2):
    for i, _ in enumerate(maleDist):
        distances[p]['M' + str(i)] = round(maleDist[i][p[0], p[1]], 5)
    for i, _ in enumerate(femaleDist):
        distances[p]['F' + str(i)] = round(femaleDist[i][p[0], p[1]], 5)
    distances[p]['Mean_M'] = round(meanMaleDist[p[0], p[1]], 5)
    distances[p]['Mean_F'] = round(meanFemaleDist[p[0], p[1]], 5)
# Save the dataframe
distances.to_csv('distances')

# Confidence intervals
def meanConfidenceInterval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t._ppf((1 + confidence)/2., n-1)
    return round(m, 5), round(m-h, 5), round(m+h, 5)

maleIndex = index[:12]
femaleIndex = index[12:-2]
ciDf = pd.DataFrame()

# For each distance
for column in distances.columns:
    # Male
    list = []
    # Fill the list
    for i in maleIndex:
        list.append(distances[column][i])
    ci = meanConfidenceInterval(list)
    row = pd.Series(['M', str(column), ci[0], ci[1], ci[2]])
    ciDf = ciDf.append(row, ignore_index=True)
    # Female
    list = []
    # Fill the list
    for i in femaleIndex:
        list.append(distances[column][i])
    ci = meanConfidenceInterval(list)
    row = pd.Series(['F', str(column), ci[0], ci[1], ci[2]])
    ciDf = ciDf.append(row, ignore_index=True)
# Set the dataframe columns
ciDf.columns = ('gender', 'distance', 'mean', 'lowerBound', 'upperBound')
# Save the dataframe
ciDf.to_csv('confidence_intervals', index=False)

# PCA
if plotPCA:
    pca = sklearnPCA(n_components=3).fit_transform(difference)
    x = [p[0] for p in pca]
    y = [p[1] for p in pca]
    z = [p[2] for p in pca]
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, z)
    plt.show()

