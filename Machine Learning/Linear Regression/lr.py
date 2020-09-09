#!/usr/bin/python
#
# Logistic Regression
#
# Authors: Joseph Gregory, Kyle Diodati 
# 
#
import argparse
import timeit
import numpy as np

import re
from math import log
from math import exp
from math import sqrt


# Process arguments for LR
def handle_args():
    parser = argparse.ArgumentParser(description=
                 'Fit logistic regression model and make predictions on test data.')

    parser.add_argument('--eta',     type=float, default=0.01,  help='Learning rate')
    parser.add_argument('--l2',      type=float, default=1.,    help='Strength of L2 regularizer')
    parser.add_argument('--maxiter', type=int,   default=100, help='Maximum number of iterations')
    parser.add_argument('--model',   help='File for saving model parameters')
    parser.add_argument('train',     help='Training data file')
    parser.add_argument('test',      help='Test data file')

    return parser.parse_args()

# Load data from a file
def read_data(filename):

  # Read names
  f = open(filename, 'r')
  p = re.compile(',')
  data = []
  header = f.readline().strip()
  varnames = p.split(header)
  f.close()

  # Read data
  data = np.genfromtxt(filename, delimiter=',', skip_header=1)
  x = data[:, 0:-1]
  y = data[:, -1]
  return ((x,y), varnames)


# Train a logistic regression model using batch gradient descent
def train_lr(train_x, train_y, eta, l2_reg_weight, maxiter=100):
  numvars = len(train_x[0])
  w = np.array([0.0] * numvars)
  b = 0.0

  for i in range(maxiter):
      #print("loop") #Used for debugging

      #temporary variables for calculations
      tempW = np.array([0.0] * numvars)
      tempB = 0.0
      
      #chain x and y values for training data
      for (x,y) in zip(train_x, train_y):
        a = 0
        for i in range(numvars):
          a += w[i] * x[i]
        a += b
        
        #update temporary bias
        tempB -= eta * (y / (1 + exp(y * a)))
        #using np.exp slowed down the process by a factor of 3
        #compared to pythons exp function
        
        for j in range(numvars):
          tempW[j] -= eta * (y * x[j] / (1 + exp(y * a)))
      
      for k in range(numvars):
        tempW[k] += eta * (l2_reg_weight * w[k])
      
      # set the bias to the temporary bias value
      b -= tempB
      
      #update weights over whole array
      for index in range(numvars):
        w[index] -= tempW[index]
  
  return (w,b)


# Predict the probability of the positive label (y=+1) given the
# attributes, x.
def predict_lr(model, x):
  (w,b) = model
  result = 0
  for i in range(len(x)):
    result += x[i] * w[i]

  return 1 / (1 + exp(-(result + b)))

# Load train and test data.  Learn model.  Report accuracy.
def main():

  args = handle_args()

  # Read in lists of examples.  Each example is a list of attribute values,
  # where the last element in the list is the class value.
  ((train_x, train_y), varnames) = read_data(args.train)
  ((test_x,  test_y),  varnames) = read_data(args.test)

  # Train model
  (w,b) = train_lr(train_x, train_y, args.eta, args.l2, maxiter=args.maxiter)


  # Write model file
  if args.model:
    f = open(args.model, "w+")
    f.write('%f\n' % b)
    for i in range(len(w)):
      f.write('%s %f\n' % (varnames[i], w[i]))

  # Make predictions, compute accuracy
  correct = 0
  for (x,y) in zip(test_x, test_y):
    prob = predict_lr( (w,b), x )
    #print(prob)
    if (prob - 0.5) * y > 0:
      correct += 1
  acc = float(correct)/len(test_y)
  print("Accuracy: ",acc)

if __name__ == "__main__":
  main()
