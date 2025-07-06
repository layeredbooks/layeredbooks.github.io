import numpy as np

import dynprog


def first_example():
    im = dynprog.Image(5, 5)
    values = np.array(
        [
            [3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
    )
    v_max = 4
    im.set_values(values)
    im.show("Original image", v_max)
    dp = dynprog.DynProg(im)
    dp.solve()
    dp.mark_solution_in_image(v_max)
    im.show("Ash line detection by dynamic programming", v_max)


def second_example():
    im = dynprog.Image(5, 5)
    values = np.array(
        [
            [3, 3, 3, 3, 3],
            [3, 6, 5, 6, 3],
            [3, 3, 3, 3, 3],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
    )
    im.set_values(values)
    v_max = 7
    im.show("Original image", v_max)
    dp = dynprog.DynProg(im)
    dp.solve()
    dp.mark_solution_in_image(v_max)
    im.show("Ash line detection by dynamic programming", v_max)


def third_example(challenge):
    im = dynprog.Image(200, 250)
    if challenge == 0:  # easy
        im.set_with_border(100, 15, 65, 15)
    elif challenge == 1:  # medium
        im.set_with_border(100, 15, 75, 15)
    elif challenge == 2:  # hard
        im.set_with_border(100, 15, 85, 15)
    else:
        assert False, f"Illegal challenge value: {challenge}"
    v_max = 150
    im.show("Original image", v_max)
    dp = dynprog.DynProg(im)
    dp.solve()
    dp.mark_solution_in_image(v_max)
    im.show("Ash line detection by dynamic programming", v_max)


def main():
    first_example()
    second_example()
    third_example(0)
    third_example(1)
    third_example(2)


main()
