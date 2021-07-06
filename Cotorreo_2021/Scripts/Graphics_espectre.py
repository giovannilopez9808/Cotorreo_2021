import matplotlib.pyplot as plt
import pandas as pd
parameters = {
    "path data": "../Data/",
    "path graphics": "../Graphics/",
    "File data": "SMARTS_espectre.csv",
    "Graphics name": "spectre_solar_smarts.png",
}
data = pd.read_csv("{}{}".format(parameters["path data"],
                                 parameters["File data"]))
plt.xlim(280, 680)
plt.xticks([wave for wave in range(280, 720, 40)])
plt.xlabel("Wavelength (nm)")
plt.ylim(0, 1.2)
plt.ylabel("Solar Spectre $\\left(\\frac{W}{m^2 nm}\\right)$")
plt.plot(data["Wvlgth"], data["Global_horizn_irradiance"],
         color="#2a9d8f",
         lw=2)
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.tight_layout()
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["Graphics name"]))
