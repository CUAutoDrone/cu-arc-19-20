import matplotlib.pyplot as plt
import json

def plotter(xcoord_list, ycoord_list):
    # plot given points
    plt.plot(xcoord_list, ycoord_list)

    # add grid lines
    plt.grid()

    # format grid lines to have increments of 1
    plt.xticks(range(min(xcoord_list), max(xcoord_list) + 1, 1))

    # show graph
    plt.show()

"""Purpose: Save X and Y coordinate list into a JSON file """
def save_JSON(xcoord_list, ycoord_list):

    """with open(coordinates, 'wb') as outfile:
        json.dumps(xcoord_list)
        json.dumps(ycoord_list)"""