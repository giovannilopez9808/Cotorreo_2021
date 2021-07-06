import matplotlib.pyplot as plt
import numpy as np
parameters = {
    "path data": "../Stations/noreste/Results_SMARTS_DM/",
    "path graphics": "../Graphics/",
    "file data": "150111.txt",
    "file graphics": "Irradiance.png"
}
hour, irradiance = np.loadtxt("{}{}".format(parameters["path data"],
                                            parameters["file data"]),
                              unpack=True)
plt.plot(hour, irradiance,
         color="#7209b7",
         lw=3)
plt.xlim(8, 17)
plt.xticks([hour for hour in range(8, 18)])
plt.xlabel("Local time (h)")
plt.ylim(0, 800)
plt.yticks([y for y in range(0, 900, 100)])
plt.ylabel("Irradiance solar $\\left(\\frac{W}{m^2}\\right)$")
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.tight_layout()
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["file graphics"]))
