#!/usr/bin/python
# 
# Authors: Joseph Gregory, Kyle Diodati 
#
# 
import argparse
import numpy as np


# Process arguments for k-NN classification
def handle_args():
    parser = argparse.ArgumentParser(description=
                 'Make predictions using the k-NN algorithms.')

    parser.add_argument('-k', type=int, default=1, help='Number of nearest neighbors to consider')
    parser.add_argument('--varnorm', action='store_true', help='Normalize features to zero mean and unit variance')
    parser.add_argument('--rangenorm', action='store_true', help='Normalize features to the range [-1,+1]')
    parser.add_argument('--exnorm', action='store_true', help='Normalize examples to unit length')
    parser.add_argument('train',  help='Training data file')
    parser.add_argument('test',   help='Test data file')

    return parser.parse_args()


# Load data from a file
def read_data(filename):
  data = np.genfromtxt(filename, delimiter=',', skip_header=1)
  x = data[:, 0:-1]
  y = data[:, -1]
  return (x,y)


# Distance between instances x1 and x2
def dist(x1, x2):
  distance = np.sqrt(np.sum(np.power(x1-x2, 2))) # Euclidean Distance Function
  return distance

  
# Predict label for instance x, using k nearest neighbors in training data
def classify(train_x, train_y, k, x):
  import operator

  distances = []
  for i in range(len(train_x)):
    distance = dist(x, train_x[i])
    distances.append([train_x[i], distance, train_y[i]])
  distances.sort(key=operator.itemgetter(1))

  neighbors = []
  for i in range(k):
    neighbors.append(distances[i][2])

  votes = {}
  for i in range(len(neighbors)):
    response = neighbors[i]
    if response in votes:
      votes[response] += 1
    else:
      votes[response] = 1 
  sorted_votes = sorted(votes.items(), key=operator.itemgetter(1))
  return sorted_votes[-1][0]


# Process the data to normalize features and/or examples.
def normalize_data(train_x, test_x, rangenorm, varnorm, exnorm):
  print(train_x) # Testing
  if rangenorm: # Normalize features to the range [-1, +1]
    new_train = train_x
    new_test = test_x

    train_lowest = np.amin(train_x, axis=0)
    train_highest = np.amax(train_x, axis=0)

    for i, x in enumerate(train_x):
      new_train[i] = np.nan_to_num(-1 + (((x - train_lowest) * (2) ) / (train_highest - train_lowest)))

    test_lowest= np.amin(test_x,axis=0)
    test_highest = np.amax(test_x,axis=0)

    for i, x in enumerate(test_x):
      new_train[i] = np.nan_to_num(-1 + (((x - test_lowest) * (2) ) / (test_highest - test_lowest)))

    train_x = new_train
    test_x = new_test
    #pass

  if varnorm: # Normalize features to zero mean and unit variance
    new_train = train_x
    new_test = test_x

    train_mean = np.mean(train_x, axis=0)
    train_std = np.std(train_x, axis=0)

    for i, x in enumerate(train_x):
      new_train[i] = np.nan_to_num((x - train_mean) / train_std)

    test_mean = np.mean(test_x, axis=0)
    test_std = np.std(test_x, axis=0)

    for i, x in enumerate(test_x):
        new_test[i] = np.nan_to_num((x - test_mean) / test_std)
    train_x = new_train
    test_x = new_test

  if exnorm: # Normalize examples to unit length
    new_train = train_x
    new_test = test_x
    for i, x in enumerate(train_x):
      new_train[i] = x / np.sqrt(np.dot(x,x))
    for i, x in enumerate(test_x):
      new_test[i] = x / np.sqrt(np.dot(x,x))
    train_x = new_train
    test_x = new_test

  print(train_x) # Testing
  return train_x, test_x


# Run classifier and compute accuracy
def runTest(test_x, test_y, train_x, train_y, k):
  correct = 0
  for (x,y) in zip(test_x, test_y):
    if classify(train_x, train_y, k, x) == y:
      correct += 1
  acc = float(correct)/len(test_x)
  return acc


# Load train and test data.  Learn model.  Report accuracy.
def main():
  args = handle_args()

  # Read in lists of examples.  Each example is a list of attribute values,
  # where the last element in the list is the class value.
  (train_x, train_y) = read_data(args.train)
  (test_x, test_y)   = read_data(args.test)

  # Normalize the training data
  (train_x, test_x) = normalize_data(train_x, test_x, 
                          args.rangenorm, args.varnorm, args.exnorm)
    
  acc = runTest(test_x, test_y,train_x, train_y,args.k)
  print("Accuracy: ",acc)

if __name__ == "__main__":
  main()
