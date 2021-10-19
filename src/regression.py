import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from satellites import get_quant_table

plt.style.use('seaborn-poster')

def calculate_rmse(predicted, actual):
    """Calculate the Root Mean Squared Error."""
    return sqrt(np.abs(np.subtract(predicted, actual)).mean())

def predict(x, y, alpha):
    """"""
    predicted =  alpha[0] * x + alpha[1]
    rmse = calculate_rmse(predicted, y)
    return predicted, rmse

def linear_least_sq(x, y):
    """Implementation of the Least Squares linear regression method.
    
    Split the given data into training and testing subsets, implement the Least Squares Method on 
    the training data, and predict using the test data.
    """
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.33) #, random_state=0)

    # Least squares method
    A = np.vstack([x_train, np.ones(len(x_train))]).T  # create matrix of independent variables
    matrix_dot = np.dot(np.linalg.inv(np.dot(A.T, A)), A.T) 
    alpha = np.dot(matrix_dot, y_train)  # parameters to estimate

    # Using the results of the least squares method, estimate the dependent variables and get error
    predicted, rmse = predict(x_test, y_test, alpha)

    return alpha, predicted, rmse

# plot the results
def plot(x, y, alpha, rmse):
    """Plot the results of the prediction against the actual data."""
    plt.figure(figsize = (10,8))
    plt.plot(x, y, 'b.')
    plt.plot(x, alpha[0]*x + alpha[1], 'r')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    print(alpha)
    print(rmse)

# Linear Example
x = np.linspace(0, 1, 101)
y = 1 + x + x * np.random.random(len(x))
alpha, predicted, rmse = linear_least_sq(x, y)
plot(x, y, alpha, rmse)

# Not exactly linear... but let's see it anyways
table = get_quant_table()
x = table['day']
y = table['n_satellites']
alpha, predicted, rmse = linear_least_sq(x, y)
plot(x, y, alpha, rmse)
