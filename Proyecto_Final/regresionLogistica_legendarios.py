from scipy.optimize import fmin_tnc as tnc
from ML_UtilsModule import Data_Management
from ML_UtilsModule import Normalization
from matplotlib import pyplot as plt
from sklearn.preprocessing import PolynomialFeatures as pf
import numpy as np
import sys

learning_rate = 1.0
POLY = 2

def polinomial_features(X, grado):
    poly = pf(grado)
    return poly, poly.fit_transform(X)

def J(theta, X, Y):
    m = np.shape(X)[0]
    n = np.shape(X)[1]
    theta = np.reshape(theta, (1, n))
    var1 = np.dot(np.transpose((np.log(g(np.dot(X, np.transpose(theta)))))), Y)
    
    aux1 = np.dot(X, np.transpose(theta))
    aux2 = 1 - g(aux1)
    aux3 = np.log(aux2)
    
    var2 = np.dot(np.transpose(aux3), (1 - Y))
    var3 = (learning_rate/(2*m)) * np.sum(theta[1:]**2)
    return (((-1/m)*(var1 + var2)) + var3)

def gradient(theta, X, Y):
    m = np.shape(X)[0]
    n = np.shape(X)[1]
    theta = np.reshape(theta, (1, n))
    var1 = np.transpose(X)
    var2  = g(np.dot(X, np.transpose(theta)))-Y
    
    theta = np.c_[[0], theta[:, 1:]]
    var3 = (learning_rate/m) * theta
    return ((1/m) * np.dot(var1, var2)) + np.transpose(var3)

def g(z):
    """
    1/ 1 + e ^ (-0^T * x)
    """
    return 1/(1 + np.exp(-z))

def swapColumns(X):
    Xinv = np.array(np.transpose(X))

    auxTr = np.array(Xinv[0])
    Xinv[0] = Xinv[1]
    Xinv[1] = auxTr
    Xinv = np.transpose(Xinv)
    
    return Xinv

def draw_data(X, Y):
    pos = np.where(Y == 0)[0] #vector with index of the Y = 1
    plt.scatter(X[pos, 0], X[pos, 1], marker='.', c='r')
    pos = np.where(Y == 1)[0].ravel() #vector with index of the Y = 1
    plt.scatter(X[pos, 0], X[pos, 1], marker='.', c='y')

def draw_decision_boundary(theta, X, Y, poly):
    x0_min, x0_max = X[:,0].min(), X[:,0].max()
    x1_min, x1_max = X[:,1].min(), X[:,1].max()
    xx1, xx2 = np.meshgrid(np.linspace(x0_min, x0_max), np.linspace(x1_min, x1_max))
    
    sigm = g(poly.fit_transform(np.c_[ xx1.ravel(), xx2.ravel()]).dot(theta))
    sigm = sigm.reshape(xx1.shape)

    plt.contour(xx1, xx2, sigm, [0.5], linewidths = 1, colors = 'g')

def draw(theta, X, Y, poly):
    plt.figure()
    draw_data(X, Y)
    draw_decision_boundary(theta, X, Y, poly)
    plt.show()

def training_examples_test_with_theta(X, Y, theta):
    test = g(np.dot(X, np.transpose(theta)))
    test = np.around(test)
    test = np.reshape(test, (np.shape(test)[0], 1))
    mask = (Y == test)
    return (len(Y[mask])/len(Y)) * 100 

X, y = Data_Management.load_csv_svm("pokemon.csv", ["capture_rate", "base_egg_steps"])

X, y, trainX, trainY, validationX, validationY, testingX, testingY = Data_Management.divide_legendary_groups(X, y)

trainXinv = swapColumns(trainX)

#------------------------------------------------------------------------------------------------- 
poly, X_poly = polinomial_features(trainX, POLY)
theta = np.zeros([1, np.shape(X_poly)[1]], dtype=float)

theta = tnc(func=J, x0=theta, fprime=gradient, args=(X_poly, trainY))[0]

draw(theta, trainX, trainY, poly)
print("Porcentaje de aciertos: " + str(training_examples_test_with_theta(X_poly, trainY, theta)) + "%")
#------------------------------------------------------------------------------------------------- 
#------------------------------------------------------------------------------------------------- 
polyInv, X_poly_inv = polinomial_features(trainXinv, POLY)
thetaInv = np.zeros([1, np.shape(X_poly_inv)[1]], dtype=float)

thetaInv = tnc(func=J, x0=thetaInv, fprime=gradient, args=(X_poly_inv, trainY))[0]

draw(thetaInv, trainXinv, trainY, polyInv)
print("Porcentaje de aciertos: " + str(training_examples_test_with_theta(X_poly_inv, trainY, thetaInv)) + "%")