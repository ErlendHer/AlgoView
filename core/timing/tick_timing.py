import math

import gui.constants as c


def get_time_sync_list(speed):
    """
    Whenever we have an operation to run at a certain speed, we need to configure on which tick cycles we are to execute
    some logic, e.g the next generator step of an algorithm. This is done by converting the speed into a list of length
    c.TICK where each element in the list is the number of iterations to perform that specific clock cycle. Consider the
    example where c.TICK = 4, and the speed is 2.0, the output would be [2, 2, 2, 2], as on every clock cycle we should
    perform two iterations. Remember, that the list must be accessed by total_num_of_ticks % c.TICK, to loop around the
    list.

    :param speed: float multiplier of speed, e.g 1.0, 0.1, 3.4
    :return: list of length c.TICK containing how many operations to perform per clock cycle
    """
    # default value of our tick cycle
    base = math.floor(speed)

    # incremented value to perform to get a correct number of operations in a cycle
    step_up = base + 1

    # slope of function
    ax = speed - base

    # current value of our function
    step = 0
    # previous value of our function
    prev = 0

    result = []

    for i in range(c.TICK):

        # floor the current value of the function
        floored = math.ceil(step)

        # if the current value is different from the previous, this means that the function has incremented by one
        # since last increment, and we need to append the step_up value to our result, otherwise the base is appended.
        result.append(base if floored == prev else step_up)

        prev = floored
        # increment our function
        step += ax

    return result

