#!/usr/bin/python
#
# Perceptron
#
# Authors: Joseph Gregory, Kyle Diodati 
import argparse
import numpy as np

import re
from math import log
from math import exp


# Process arguments for perceptron
def handle_args():
    parser = argparse.ArgumentParser(description=
                 'Fit perceptron model and make predictions on test data.')
    parser.add_argument('--maxiter', type=int,   default=100, help='Maximum number of iterations')
    parser.add_argument('--model',  help='File for saving model parameters')
    parser.add_argument('train',    help='Training data file')
    parser.add_argument('test',     help='Test data file')

    return parser.parse_args()

# Load data from a file
def read_data(filename):
  f = open(filename, 'r')
  p = re.compile(',')
  header = f.readline().strip()
  varnames = p.split(header)
  f.close()

  # Read data
  data = np.genfromtxt(filename, delimiter=',', skip_header=1)
  x = data[:, 0:-1]
  y = data[:, -1]
  return ((x, y), varnames)


# Learn weights using the perceptron algorithm
def train_perceptron(train_x, train_y, maxiter=100):

  # Initialize weight vector and bias
  numvars = len(train_x[0])
  w = np.array([0.0] * numvars)
  b = 0.0

  for _ in range(maxiter):
    for (t_x, t_y) in zip(train_x,train_y):
      a = b
      for n in range(len(t_x)):
        a += t_x[n] * w[n]
        y = t_y

      if a * y <= 0:
        for d in range(len(t_x)):
          w[d] += y * t_x[d]
        b += y

  return (w,b)


# Compute the activation for input x.
def predict_perceptron(model, x):
  (w,b) = model
  
  a = b
  for i in range(len(x)):
    a += w[i] * x[i]

  return a


# Load train and test data.  Learn model.  Report accuracy.
def main():
  # Process command line arguments.
  args = handle_args()

  ((train_x, train_y), varnames) = read_data(args.train)
  ((test_x,  test_y), testvarnames) = read_data(args.test)

  # Train model
  (w,b) = train_perceptron(train_x, train_y, maxiter=args.maxiter)

  # Write model file
  if args.model:
    f = open(args.model, "w+")
    f.write('%f\n' % b)
    for i in range(len(w)):
      f.write('%s %f\n' % (varnames[i], w[i]))

  # Make predictions, compute accuracy
  correct = 0
  for (x,y) in zip(test_x, test_y):
    activation = predict_perceptron( (w,b), x )
    if activation * y > 0:
      correct += 1
  acc = float(correct)/len(test_y)
  print("Accuracy: ",acc)

if __name__ == "__main__":
  main()
