import numpy as np
import matplotlib.pyplot as plt


class DynamicSystem:

    def __init__(self, A, x0):
        self.A = A
        n_rows, n_cols = A.shape
        assert n_rows == n_cols
        self.n = n_rows
        assert len(x0) == self.n
        self.x = x0

    def run(self, n_steps):
        # the result, as a matrix where each column represents x,
        # for the initial value and for the n_steps steps
        x_res = np.zeros([self.n, n_steps+1])
        x_res[:, [0]] = self.x
        for i in range(n_steps):
            nx = np.matmul(self.A, self.x)
            x_res[:, [i+1]] = nx
            self.x = nx
        return x_res


def line():
    A = np.array([[1/2, 1/2], [1/2, 1/2]])
    x0 = np.array([[1, 2]]).T
    d_sys = DynamicSystem(A, x0)
    x_res = d_sys.run(5)
    print(x_res)


def star(n_steps):
    A = np.array([[1/5, 1/5, 1/5, 1/5, 1/5],
                  [1/2, 1/2, 0, 0, 0],
                  [1/2, 0, 1/2, 0, 0],
                  [1/2, 0, 0, 1/2, 0],
                  [1/2, 0, 0, 0, 1/2]])
    x0 = np.array([[-2, -1, 0, 1, 2]]).T
    d_sys = DynamicSystem(A, x0)
    x_res = d_sys.run(n_steps)
    print(x_res[:, 0])
    print(x_res[:, -1])
    plt.plot(x_res.T)
    plt.savefig('star_plot.png')


def main():
    line()
    star(100)


main()
