"""
Project: RadarBook
File: kalman.py
Created by: Lee A. Harrison
One: 3/16/2019
Created with: PyCharm
"""
from scipy import matmul, sqrt
from scipy.linalg import inv, norm


class Kalman:
    """
    Kalman filter object.
    """
    def __init__(self, x, u, P, A, B, Q, H, R):
        self.x = x
        self.u = u
        self.P = P
        self.A = A
        self.B = B
        self.Q = Q
        self.H = H
        self.R = R

        self.state = []
        self.residual = []
        self.epsilon = []
        self.sigma = []
        self.process_noise = []

    def filter(self, z):
        """
        Perform the filtering operation on the measurements.
        :param z: The measurements.
        :return:
        """
        # Loop over all the measurements
        for zi in z:
            self.predict()
            self.update(zi)

    def filter_epsilon(self, z, threshold, scale):
        """
        Perform filtering on the measurements for adaptive Kalman filtering.
        :param z: The measurements.
        :param threshold: Threshold for adaptive filter.
        :param scale: Scale factor for the adaptive filter.
        :return:
        """
        # Loop over all the measurements
        for zi in z:
            self.predict()
            self.update(zi)
            self.adapt_epsilon(threshold, scale)

    def filter_sigma(self, z, n_sigma, scale):
        """
        Perform filtering on the measurements for adaptive Kalman filtering.
        :param z: The measurements.
        :param n_sigma: Threshold for adaptive filter.
        :param scale: Scale factor for the adaptive filter.
        :return:
        """
        # Loop over all the measurements
        for zi in z:
            self.predict()
            self.update(zi)
            self.adapt_sigma(n_sigma, scale)

    def predict(self):
        """
        The predict step in Kalman filtering.
        :return:
        """
        # Predict the state and covariance
        self.x = matmul(self.A, self.x) + matmul(self.B, self.u)
        self.P = matmul(matmul(self.A, self.P), self.A.T) + self.Q

    def update(self, z):
        """
        The update step in Kalman filtering.
        :param z: The measurements.
        :return:
        """
        # Calculate the Kalman gain
        S = matmul(matmul(self.H, self.P), self.H.T) + self.R;
        K = matmul(matmul(self.P, self.H.T), inv(S))

        # Correction based on the measurement
        residual = z - matmul(self.H, self.x)
        self.x = self.x + matmul(K, residual)
        self.P = self.P - matmul(matmul(K, self.H), self.P)

        self.state.append(self.x)
        self.residual.append(norm(residual))
        self.epsilon.append(matmul(residual.T, matmul(inv(S), residual)))
        self.sigma.append(sqrt(S[0, 0] ** 2 + S[1, 1] ** 2 + S[2, 2] ** 2))
        self.process_noise.append(self.Q[0, 0])

    def adapt_epsilon(self, threshold, scale):
        """
        Adaptive epsilon method.
        :param threshold: Threshold for the adaptive filtering.
        :param scale: The scale factor for the adaptive filtering.
        :return:
        """
        # Epsilon method
        if self.epsilon[-1] > threshold:
            self.Q *= scale
        else:
            self.Q /= scale

    def adapt_sigma(self, n_sigma, scale):
        """
        Adaptive sigma method.
        :param n_sigma: The number of standard deviations for the adaptive filtering.
        :param scale: The scale factor for the adaptive filtering.
        :return:
        """
        # Sigma method
        if self.residual[-1] > n_sigma * self.sigma[-1]:
            self.Q *= scale
        else:
            self.Q /= scale
