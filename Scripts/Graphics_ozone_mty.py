from Graphics_ozone_cdmx import *


def read_data(path="", file=""):
    data = np.loadtxt("{}{}".format(path,
                                    file),
                      skiprows=1,
                      usecols=[col for col in range(1, 17)],
                      delimiter=",")
    data = np.transpose(data)
    return data


if __name__ == "__main__":
    parameters = {
        "path data": "../Data/",
        "file data": "ozono_mty.csv",
        "path graphics": "../Graphics/",
        "graphics name": "ozone_mty.png",
        "Date initial": "2005-01-01",
        "Date final": "2020-12-31"
    }
    data = read_data(parameters["path data"],
                     parameters["file data"])
    plot = plot_data(parameters=parameters,
                     data=data)
