import numpy
#from keras.datasets import mnist	#this is a set of images
from keras.utils import np_utils
import pickle
from models import baseline_model, simple_CNN_model, larger_CNN_model
import json
from time import time
from datasets import get_train_data

seed = 7
numpy.random.seed(seed)
#(x_train, y_train), (x_val, y_val) = mnist.load_data()


def training(model_type, x_train, y_train, x_val, y_val):
	'''
	format of mnist:
	((([x_train], dtype = unit8), ([y_train])), (([x_val]), dtype = unit8), ([y_val])))
	'''
	# flatten 28*28 images to a 784 vector for each image
	num_pixels = x_train.shape[1] * x_train.shape[2]
	x_train = x_train.reshape(x_train.shape[0], num_pixels).astype('float32')
	x_val = x_val.reshape(x_val.shape[0], num_pixels).astype('float32')

	#one hot encoding -> converts the 26 alphabets(represented as integers) to a categorical system where the machine understands
	y_train = np_utils.to_categorical(y_train)
	y_val = np_utils.to_categorical(y_val)
	num_classes = y_val.shape[1]

	# build the model
	model = model_type(num_pixels, num_classes)

	# Fit the model
	model.fit(x_train, y_train, validation_data=(x_val, y_val), nb_epoch=10, batch_size=200, verbose=2)

	# Final evaluation of the model
	scores = model.evaluate(x_val, y_val, verbose=0)

#	model.summary()

	return scores, model

if __name__ == '__main__':
	del_val_from_train = input('Do you want to remove validation images(y/n)?\n')
	if del_val_from_train == 'y':
		del_val_from_train = True
	elif del_val_from_train == 'n':
		del_val_from_train = False

	(x_train, y_train), (x_val, y_val) = get_train_data(del_val_from_train)
	# with open('./data/train_removed_True.pkl', 'rb') as a:
	# 	mydataset = pickle.load(a)
	# 	(x_train, y_train) = mydataset

	# with open('./data/val.pkl', 'rb') as a:
	# 	mydataset = pickle.load(a)
	# 	(x_val, y_val) = mydataset

	#selects model
	select = input('Select model:\n(1 = baseline model, 2 = simple CNN model, 3 = larger CNN model)\n')
	start = time()
	if int(select) == 1:
		func = baseline_model
		filepath_weight = './data/baseline.m'
		filepath_architechture = './data/baseline.json'

	elif int(select) == 2:
		func = simple_CNN_model
		filepath_weight = './data/simple_CNN_model.m'
		filepath_architechture = './data/simple_CNN_model.json'

	elif int(select) == 3:
		func = larger_CNN_model
		filepath_weight = './data/larger_CNN_model.m'
		filepath_architechture = './data/larger_CNN_model.json'

	#Runs model
	scores, model = training(func, x_train, y_train, x_val, y_val)

	#Saves model weights
	model.save_weights(filepath_weight)
	print('Model weights saved in {}.'.format(filepath_weight))

	#saves model architechture
	with open(filepath_architechture, 'w') as outfile:
		json.dump(model.to_json(), outfile)
	print('Model architechture saved in.'.format(filepath_architechture))

	print('Baseline Error: {}%'.format(100-scores[1]*100))
	print('The program took: {}'.format(time() - start))
