""'Purpose: To plot a path of straight lines based on user input'
import Functions as func

def main():
    # input list of x coordinates
    xcoord_list = [0, 1, 3]

    # input list of y coordinates
    ycoord_list = [0, 2, 5]

    # plot path as straight lines
    func.plotter(xcoord_list, ycoord_list)


if __name__ == "__main__":
    main()