import numpy as np
import csv
import math as m


#Linear regression part
with open("./housing_train.txt", "r") as f:
	matrix_train = np.array([line.split() for line in f]).astype(float)

with open("./housing_test.txt", "r") as f:
	matrix_test = np.array([line.split() for line in f]).astype(float)

# get X_train and Y_train from file
X_train = np.delete(matrix_train, 13, 1)
Y_train = np.delete(matrix_train, np.s_[0:13], 1)

# get X_test and Y_test from file
X_test = np.delete(matrix_test, 13, 1)
Y_test = np.delete(matrix_test, np.s_[0:13], 1)

# append column of 1s to X
X_train_dummy = np.insert(X_train, 0, 1, axis=1)
X_test_dummy = np.insert(X_test, 0, 1, axis=1)

# compute optimum weight vector
w_dummy = np.matmul(np.linalg.inv(np.matmul(np.transpose(X_train_dummy), X_train_dummy)), np.matmul(np.transpose(X_train_dummy), Y_train))
w = np.matmul(np.linalg.inv(np.matmul(np.transpose(X_train), X_train)), np.matmul(np.transpose(X_train), Y_train))

# compute sum of squared error (SSE)
sse_train_dummy = 0
sse_test_dummy = 0
sse_train = 0
sse_test = 0

for idx, house in enumerate(X_train_dummy):
	prediction = np.dot(house, w_dummy)
	error = (Y_train[idx] - prediction)**2
	sse_train_dummy += error

for idx, house in enumerate(X_test_dummy):
	prediction = np.dot(house, w_dummy)
	error = (Y_test[idx] - prediction)**2
	sse_test_dummy += error

for idx, house in enumerate(X_train):
	prediction = np.dot(house, w)
	error = (Y_train[idx] - prediction) ** 2
	sse_train += error

for idx, house in enumerate(X_test):
	prediction = np.dot(house, w)
	error = (Y_test[idx] - prediction) ** 2
	sse_test += error

# mean squared error (MSE)
mse_train_dummy = sse_train_dummy / X_train_dummy.shape[0]
mse_test_dummy = sse_test_dummy / X_test_dummy.shape[0]
mse_train = sse_train / X_train.shape[0]
mse_test = sse_test / X_test.shape[0]

print("Training Results w/ dummy var:\nSSE: {}\tMSE: {}".format(float(sse_train_dummy), float(mse_train_dummy)))
print("Testing Results w/ dummy var:\nSSE: {}\tMSE: {}".format(float(sse_test_dummy), float(mse_test_dummy)))
print("Training Results:\nSSE: {}\tMSE: {}".format(float(sse_train), float(mse_train)))
print("Testing Results:\nSSE: {}\tMSE: {}".format(float(sse_test), float(mse_test)))




#generate N random features(d), insert them and calculate
row_num_train = X_train.shape[0]
row_num_test = X_test.shape[0]
features_train = []
features_test = []
sse_train_mod_d = []
sse_test_mod_d = []
mse_train_mod_d = [()]
mse_test_mod_d = [()]
mu, sigma = 0, 0.1 	#mean and standard deviation
N = 100 #number of features to test with

from copy import deepcopy
X_train_mod_d = deepcopy(X_train)
X_test_mod_d = deepcopy(X_test)

#generating list of additional features
for d in range(0, N):
	features_train.append(np.random.normal(mu, sigma, row_num_train))
	features_test.append(np.random.normal(mu, sigma, row_num_test))

for d in range(0, N):
	X_train_mod_d = np.insert(X_train_mod_d, 0, features_train[d], axis=1)
	X_test_mod_d = np.insert(X_test_mod_d, 0, features_test[d], axis=1)

	w_mod_d = np.matmul(np.linalg.inv(np.matmul(np.transpose(X_train_mod_d), X_train_mod_d)), np.matmul(np.transpose(X_train_mod_d), Y_train))

	tmp_err = 0
	for idx, house in enumerate(X_train_mod_d):
		prediction = np.dot(house, w_mod_d)
		error = (Y_train[idx] - prediction) ** 2
		tmp_err += error
	sse_train_mod_d.append(tmp_err)

	tmp_err = 0
	for idx, house in enumerate(X_test_mod_d):
		prediction = np.dot(house, w_mod_d)
		error = (Y_test[idx] - prediction) ** 2
		tmp_err += error
	sse_test_mod_d.append(tmp_err)

for d in range(0, N):
	mse_train_mod_d.append((d+1, (sse_train_mod_d[d] / X_train_mod_d.shape[0])[0]))
	mse_test_mod_d.append((d+1, (sse_test_mod_d[d] / X_test_mod_d.shape[0])[0]))

#write MSE data with additional features to csv file
header_train = ["mse train"]
header_test = ["mse test"]
with open("mse_add_feat.csv", 'w+', newline='') as csv_mse:
	mse_writer = csv.writer(csv_mse)
	mse_writer.writerow(header_train)
	mse_writer.writerows(mse_train_mod_d)
	mse_writer.writerow(header_test)
	mse_writer.writerows(mse_test_mod_d)


#Logistic regression part

tmp = []
with open("./usps-4-9-train.csv", "r") as csv_train:
	csv_reader = csv.reader(csv_train)
	for row in csv_reader:
		tmp.append(row)
	logistic_train = np.array(tmp).astype(float)

tmp = []
with open("./usps-4-9-test.csv", "r") as csv_test:
	csv_reader = csv.reader(csv_test)
	for row in csv_reader:
		tmp.append(row)
	logistic_test = np.array(tmp).astype(float)

pix_train = np.delete(logistic_train, 256, 1)
ans_train = np.delete(logistic_train, np.s_[0:256], 1)
pix_test = np.delete(logistic_test, 256, 1)
ans_test = np.delete(logistic_test, np.s_[0:256], 1)

pix_train = pix_train/255
pix_test = pix_test/255

w_log = np.zeros(256)
grad_des = np.zeros(256)

while (abs(grad_des) > m.exp(-3)):
	grad_des = np.zeros(256)
	for i in range(0, 256):
		pred_ans = 1/(1 + m.exp(-np.dot(np.transpose(w_log), pix_train[i])))
		grad_des