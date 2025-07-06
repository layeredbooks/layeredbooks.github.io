import numpy as np
import matplotlib.pyplot as plt


class Image:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.arr = np.zeros([self.n_rows, self.n_cols])

    def set_values(self, values):
        assert values.shape == (self.n_rows, self.n_cols)
        self.arr = values

    def set_value(self, row, col, value):
        self.arr[row, col] = value

    def get_value(self, row, col):
        return self.arr[row, col]

    def set_with_border(self, m_above, std_above, m_below, std_below):
        # the border is the ash line, that we want to detect with DP
        border = []
        # random start row for the border
        r = np.random.randint(int(0.25 * self.n_rows), int(0.75 * self.n_rows))
        border.append(r)
        # remaining row values for the border
        for i in range(1, self.n_cols):
            # a ranom control signal, in the admissible set [-1, 0, 1]
            u = np.random.randint(0, 3)
            u -= 1
            x_i = border[-1]
            x_i = x_i + u
            border.append(x_i)
        # generate pixel values, with different means and standard deviations
        # for pixels above and below the border
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if r <= border[c]:
                    value = np.random.normal(loc=m_above, scale=std_above)
                else:
                    value = np.random.normal(loc=m_below, scale=std_below)
                self.arr[r][c] = value

    def show(self, title, v_max):
        plt.imshow(self.arr, cmap="gray", vmax=v_max)
        plt.title(title)
        plt.show()


class DynProg:

    def __init__(self, image):
        self.image = image

    def g(self, x_i, i):
        if x_i >= self.image.n_rows - 1:
            return 0
        grad = self.image.get_value(x_i, i) - self.image.get_value(x_i + 1, i)
        return grad

    def solve(self):
        N = self.image.n_cols - 1
        n_x_i = self.image.n_rows
        J_mat = np.zeros([n_x_i, N + 1])
        u_mat = np.zeros([n_x_i, N])
        u_values = np.array([-1, 0, 1])
        # fill in the last column of the J matrix
        for x_i in range(n_x_i):
            J_mat[x_i, -1] = self.g(x_i, N)
        # fill in the remaining columns, from right to left
        for k in range(N - 1, -1, -1):
            for x_i in range(n_x_i):
                # three values, one for each next state, with each of these
                # corresponding to one of the three control signal values -1, 0, and 1
                J_k_plus_1 = np.zeros(3)
                # the gradient
                g_x_i = self.g(x_i, k)
                # u = -1
                if x_i > 0:
                    J_k_plus_1[0] = J_mat[x_i - 1, k + 1]
                # u = 0
                J_k_plus_1[1] = J_mat[x_i, k + 1]
                # u = -1
                if x_i < n_x_i - 1:
                    J_k_plus_1[2] = J_mat[x_i + 1, k + 1]
                value_vec = g_x_i + J_k_plus_1
                # calculate the best u (there might be more than one, but we let argmax pick one)
                u_opt_index = np.argmax(value_vec)
                # the optimal J value
                J_k_value = value_vec[u_opt_index]
                # store optimal J value
                J_mat[x_i, k] = J_k_value
                # store optimal control signal
                u_mat[x_i, k] = u_values[u_opt_index]
        self.J_mat = J_mat
        self.u_mat = u_mat

    def mark_solution_in_image(self, mark_value):
        # the optimal solution starts at the best x_0
        x_0 = np.argmax(self.J_mat[:, 0])
        # the optimal control signal for x_0
        u = int(self.u_mat[x_0, 0])
        x_i = x_0
        # mark solution for first column
        self.image.set_value(x_i, 0, mark_value)
        for i in range(1, self.J_mat.shape[1]):
            x_i = x_i + u
            # mark solution for this x_i value
            self.image.set_value(x_i, i, mark_value)
            # no control signal defined for the rightmost column
            if i < self.J_mat.shape[1] - 1:
                u = int(self.u_mat[x_i, i])
