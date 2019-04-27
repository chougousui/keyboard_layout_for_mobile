import numpy as np


def generate_cost_dict():
    def inner_func(i, j):
        x1 = i % 10
        y1 = i // 10
        x2 = j % 10
        y2 = j // 10

        alpha = 5
        x_center = 5.5
        x_radius = 7.5
        y_center = 1
        y_radius = 4.5

        dist = np.sqrt(47 * 47 * np.square(x1 - x2) + 77 * 77 * np.square(y1 - y2))
        force1 = np.exp(-1 * alpha * (
                1 / (np.sqrt(np.square(x1 - x_center) + np.square(x_radius / y_radius * (y1 - y_center))) - x_radius) +
                1 / x_radius))
        force2 = np.exp(-1 * alpha * (
                1 / (np.sqrt(np.square(x2 - x_center) + np.square(x_radius / y_radius * (y2 - y_center))) - x_radius) +
                1 / x_radius))

        res = (force1 + force2) / 2 * dist
        return res

    cost_dict = np.delete(np.delete(np.fromfunction(
        lambda i, j: inner_func(i, j),
        (28, 28)), 20, axis=0), 20, axis=1)
    return cost_dict
