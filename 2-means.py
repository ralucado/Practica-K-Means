from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from random import randint

def llegirDades():
	# obrim el fitxer de dades
	fitxerDades = open("dataset2D.txt", "r")

	# llegim el fitxer linea per linea
	dadesLines = fitxerDades.readlines()

	n = int(dadesLines[0])
	trainData = [[], []]
	# traindata = [ [color1, color2, color3...], [altura1, altura2, altura3...]]

	for i in range(1, n+1):
		color, altura = dadesLines[i].split(' ')
		
		trainData[0].append(int(color))
		trainData[1].append(int(altura))
		
	m = int(dadesLines[n+1])
	predictData = [[], []]

	for i in range(n+2, n+m+2):
		color, altura = dadesLines[i].split(' ')
		
		predictData[0].append(int(color))
		predictData[1].append(int(altura))

	return (trainData, predictData)

def train(data):
	n = len(data[0])

	# afegeixo els 2 centroides aleatoris c1 i c2
	# els faig una mica separats perque no hi hagi corner cases
	# casos on tot peti (per exemple si c1 = c2)
	c = [[0,0], [10, 80]]

	iteracions = 100
	for it in range(iteracions):
		proxima_C1 = []
		proxima_C2 = []

		for i in range(n):
			d1 = (data[0][i] - c[0][0])**2 + (data[1][i] - c[0][1])**2
			d2 = (data[0][i] - c[1][0])**2 + (data[1][i] - c[1][1])**2
			
			if (d1 < d2): proxima_C1.append(i)
			else: proxima_C2.append(i)

		total_punts1 = len(proxima_C1)
		total_punts2 = len(proxima_C2)

		if (total_punts1 != 0): c[0] = [0,0]
		if (total_punts2 != 0): c[1] = [0,0]

		for i in range(total_punts1):
			c[0][0] = c[0][0] + data[0][proxima_C1[i]]
			c[0][1] = c[0][1] + data[1][proxima_C1[i]]

		for i in range(total_punts2):
			c[1][0] = c[1][0] + data[0][proxima_C2[i]]
			c[1][1] = c[1][1] + data[1][proxima_C2[i]]

		if (total_punts1 != 0):
			c[0][0] = c[0][0]/total_punts1
			c[0][1] = c[0][1]/total_punts1
		if (total_punts2 != 0):
			c[1][0] = c[1][0]/total_punts2
			c[1][1] = c[1][1]/total_punts2
			
	return c

def plotClusters(c, data):
	temp = []
	for i in range(len(data[0])):
		d1 = (data[0][i] - c[0][0])**2 + (data[1][i] - c[0][1])**2
		d2 = (data[0][i] - c[1][0])**2 + (data[1][i] - c[1][1])**2

		if (d1 < d2):
			temp.append('red')
		else:
			temp.append('blue')

	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.scatter(data[0], data[1], c=temp)
	ax.scatter(c[0][0], c[0][1], alpha=0.5, s=200, c='red')
	ax.scatter(c[1][0], c[1][1], alpha=0.5, s=200, c='blue')
	ax.set_xlabel('Color (1-Blanc 10-Lila)')
	ax.set_ylabel('altura (cm)')
	plt.show()  # depen de l'ordinador plt.show() no funciona be
				# si show no funciona, useu plt.save('grafica.png')

def main():
	trainData, predictData = llegirDades()
	'''
	# ens guardem un 10% de les dades etiquetades per fer test
	ind = int(9.0*len(trainData[0])/10) # aprox particio 90-10%
	testData = [[],[],[]]
	testData[0] = trainData[0][ind:]
	testData[1] = trainData[1][ind:]
	trainData[0] = trainData[0][:ind]
	trainData[1] = trainData[1][:ind]
	'''
	centroids = train(trainData)

	for i in range(len(predictData[0])):
		d1 = (predictData[0][i] - centroids[0][0])**2 + (predictData[1][i] - centroids[0][1])**2
		d2 = (predictData[0][i] - centroids[1][0])**2 + (predictData[1][i] - centroids[1][1])**2
		
		if (d1 < d2):
			print("Prediction ", i, ": Group 1 (Red)")
		else:
			print("Prediction ", i, ": Group 2 (Blue)")

	plotClusters(centroids, trainData)


if __name__ == '__main__':
	main()