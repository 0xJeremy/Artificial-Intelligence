import csv
import random
import math

random.seed(random.random())

#***************************************************
#				 Parameter Variables
#***************************************************

PATH = 'iris.data'
ALPHA = 0.005
EPOCH = 400
NEURON = [4, 8, 3]

#***************************************************
#				 Helper Functions
#***************************************************

def mat_mat(m1, m2, b):
	x = [[0 for i in range(len(m2[0]))] for i in range(len(m1))]    
	for i in range(len(m1)):
		for j in range(len(m2[0])):
			for k in range(len(m2)):
				x[i][j] += m1[i][k] * m2[k][j]
			x[i][j] += b[j]
	return x

def vec_mat(v1, m2, b):
	x = [0 for i in range(len(m2[0]))]
	for j in range(len(m2[0])):
		for k in range(len(m2)):
			x[j] += v1[k] * m2[k][j]
			x[j] += b[j]
	return x

def mat_vec(m1, v2):
	x = [0 for i in range(len(m1))]
	for i in range(len(m1)):
		for j in range(len(v2)):
			x[i] += m1[i][j] * v2[j]
	return x

def sigmoid(x):
	for i in range(len(x)):
		x[i] = 1 / (1 + math.exp(-x[i]))
	return x

#***************************************************
#			   Neural Network Class
#***************************************************

class NeuralNetwork():
	def __init__(self):
		print("Loading Data...")

		with open(PATH) as infile:
			readfile = csv.reader(infile)
			dataset = list(readfile)
		for row in dataset:
			row[4] = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"].index(row[4])
			row[:4] = [float(row[j]) for j in range(len(row))]

		random.shuffle(dataset)
		datatrain = dataset[:int(len(dataset) * 0.8)]
		datatest = dataset[int(len(dataset) * 0.8):]

		print("Loading Finished.")

		self.tx = [data[:4] for data in datatrain]
		self.ty = [data[4] for data in datatrain]
		self.testx = [data[:4] for data in datatest]
		self.testy = [data[4] for data in datatest]

		self.w = [[0 for j in range(NEURON[1])] for i in range(NEURON[0])]
		self.w2 = [[0 for j in range(NEURON[2])] for i in range(NEURON[1])]
		self.b = [0 for i in range(NEURON[1])]
		self.b2 = [0 for i in range(NEURON[2])]

		for i in range(NEURON[0]):
			for j in range(NEURON[1]):
				self.w[i][j] = 2 * random.random() - 1
		for i in range(NEURON[1]):
			for j in range(NEURON[2]):
				self.w2[i][j] = 2 * random.random() - 1

	def train(self):
		print("\n===== Training Started =====")
		for e in range(EPOCH):
			for y, x in enumerate(self.tx):
				
				h_1 = vec_mat(x, self.w, self.b)
				X_1 = sigmoid(h_1)
				h_2 = vec_mat(X_1, self.w2, self.b2)
				X_2 = sigmoid(h_2)
				
				target = [0, 0, 0]
				target[int(self.ty[y])] = 1

				delta_2 = []
				for j in range(NEURON[2]):
					delta_2.append(-1 * (target[j]-X_2[j]) * X_2[j] * (1-X_2[j]))

				for i in range(NEURON[1]):
					for j in range(NEURON[2]):
						self.w2[i][j] -= ALPHA * (delta_2[j] * X_1[i])
						self.b2[j] -= ALPHA * delta_2[j]
				
				delta_1 = mat_vec(self.w2, delta_2)
				for j in range(NEURON[1]):
					delta_1[j] = delta_1[j] * (X_1[j] * (1-X_1[j]))
				
				for i in range(NEURON[0]):
					for j in range(NEURON[1]):
						self.w[i][j] -=  ALPHA * (delta_1[j] * x[i])
						self.b[j] -= ALPHA * delta_1[j]
			
			if(e % 100 == 0):
				x = float(e) / EPOCH * 100
				print("%4d %% trained..." % x)

		print(" 100 % trained...")
		print("=====  Done Training  =====\n")

	def validate(self):
		pred = mat_mat(self.testx, self.w, self.b)
		pred_2 = mat_mat(pred, self.w2, self.b)
		prediction = []
		for x in pred_2:
			prediction.append(max(enumerate(x), key=lambda x:x[1])[0])
		correct = 0
		for i in range(len(pred_2)):
			if(prediction[i] == self.testy[i]):
				correct += 1
		percent = float(correct) / len(pred_2) * 100
		print("Neural Network Accuracy: %f%%\n" % percent)


	def query(self):
		y = []
		y.append(float(input("Sepal Length: ")))
		y.append(float(input("Sepal Width:  ")))
		y.append(float(input("Petal Length: ")))
		y.append(float(input("Petal Width:  ")))
		m = [y]

		pred = mat_mat(m, self.w, self.b)
		pred_2 = mat_mat(pred, self.w2, self.b)

		if(max(pred_2) == pred_2[0]):
			print("\nPrediction: Iris-setosa")
		elif(max(pred_2) == pred_2[1]):
			print("\nPrediction: Iris-versicolor")
		else:
			print("\nPrediction: Iris-virginica")

#***************************************************
#				 Main Function
#***************************************************

def main():
	iris = NeuralNetwork()
	iris.train()
	iris.validate()
	iris.query()


if __name__ == '__main__':
	main()