library(vegan)
library(plot3D)

# Indiquer où se trouve les données
path = "/home/max/Dropbox/Courses/L3/Etudes de Cas Statistiques/Cochlées/data/"
# Obtenir les fichiers pour les hommes et les femmes
maleFiles = list.files(paste(path, 'male/', sep = '') , pattern = "*.am", full.names = TRUE)
femaleFiles = list.files(paste(path, 'female/', sep = '') , pattern = "*.am", full.names = TRUE)
# Lire les données
male = lapply(maleFiles, read.table, col.names=list('x','y','z'))
female = lapply(femaleFiles, read.table, col.names=list('x','y','z'))

#scatter3D(nData[[1]][[1]][,1], nData[[1]][[1]][,2], nData[[1]][[1]][,3])

# On calcule les distances entre chaque points ((1000*999)/2)
distM = vector('list', length(male))
for (i in 1:length(distM))
  distM[[i]] = as.matrix(dist(male[[i]]))
distF = vector('list', length(female))
for (i in 1:length(distF))
  distF[[i]] = as.matrix(dist(female[[i]]))

# Normaliser les données
for (i in 1:12)
  distM[[i]] = distM[[i]] / sum(diag(distM[[i]][-1000, -1]))

for (i in 1:10)
  distF[[i]] = distF[[i]] / sum(diag(distF[[i]][-1000, -1]))

# On cherche la distance moyenne pour chaque sexe
DM = matrix(0, 1000, 1000)
for (i in 1:length(distM))
  DM = DM + distM[[i]]
DM = DM / 12
DF = matrix(0, 1000, 1000)
for (i in 1:length(distF))
  DF = DF + distF[[i]]
DF = DF / 10

# On peut visualiser les écarts de distance
difference = DM - DF
par(mfrow = c(1, 2))
image(difference)
hist(difference)
abline(v = median(difference), col = 'red', lwd = 5)

# Calculons les t-tests
tTests = matrix(0, 1000, 1000)
for (i in 1:999){
  for (j in (i+1):1000){
    tmpMale = c()
    for (k in 1:length(male))
      tmpMale = c(tmpMale, distM[[k]][i, j])
    tmpFemale = c()
    for (k in 1:length(female))
      tmpFemale = c(tmpFemale, distF[[k]][i, j])
    tTests[i, j] = tTests[j, i] = t.test(tmpMale, tmpFemale)$p.value
  }
}
# Cherchons les points qui dévient beaucoup de la moyenne
alpha = 0.05
par(pty = 's')
image(difference)
contour(tTests < alpha, add=TRUE, nlevels = 1, labels = alpha)
legend('bottomright', col = heat.colors(12), legend = round(seq(min(difference), max(difference),,12), 3), lwd=17, bg='white')

# On récupère les points manuellement
p1 = locator(1)
p2 = locator(1)
p3 = locator(1)
p4 = locator(1)
p5 = locator(1)
p6 = locator(1)
p7 = locator(1)

# On extrait les coordonées cartésiennes
p1x = p1$x * 1000
p1y = p1$y * 1000
p2x = p2$x * 1000
p2y = p2$y * 1000
p3x = p3$x * 1000
p3y = p3$y * 1000
p4x = p4$x * 1000
p4y = p4$y * 1000
p5x = p5$x * 1000
p5y = p5$y * 1000
p6x = p6$x * 1000
p6y = p6$y * 1000
p7x = p7$x * 1000
p7y = p7$y * 1000

p1x = 206
p1y = 82
p2x = 343
p2y = 196
p3x = 416
p3y = 255
p4x = 519
p4y = 348
p5x = 744
p5y = 512
p6x = 604
p6y = 12
p7x = 899
p7y = 255

# Localisation des 6 points sur la cochlee d'un individu

ind = male[[1]]

scatter3D(ind[,1],ind[,2],ind[,3])
scatter3D(ind[c(p1x,p1y),1],ind[c(p1x,p1y),2],ind[c(p1x,p1y),3],type="o",add=TRUE,lwd=6,col="black")
scatter3D(ind[c(p2x,p2y),1],ind[c(p2x,p2y),2],ind[c(p2x,p2y),3],type="l",add=TRUE,lwd=6,col="black")
scatter3D(ind[c(p3x,p3y),1],ind[c(p3x,p3y),2],ind[c(p3x,p3y),3],type="l",add=TRUE,lwd=6,col="black")
scatter3D(ind[c(p4x,p4y),1],ind[c(p4x,p4y),2],ind[c(p4x,p4y),3],type="l",add=TRUE,lwd=6,col="black")
scatter3D(ind[c(p5x,p5y),1],ind[c(p5x,p5y),2],ind[c(p5x,p5y),3],type="l",add=TRUE,lwd=6,col="black")
scatter3D(ind[c(p6x,p6y),1],ind[c(p6x,p6y),2],ind[c(p6x,p6y),3],type="l",add=TRUE,lwd=6,col="black")
scatter3D(ind[c(p7x,p7y),1],ind[c(p7x,p7y),2],ind[c(p7x,p7y),3],type="l",add=TRUE,lwd=6,col="black")

