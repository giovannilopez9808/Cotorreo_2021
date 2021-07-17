import matplotlib.pyplot as plt
import numpy as np
import os


def read_data(path='', file=''):
    hour, data = np.loadtxt('{}{}'.format(path,
                                          file),
                            unpack=True)
    return hour, data


parameters = {
    'path data': '../Data/Mty/noreste/Results_SMARTS_DM/',
    'path RD': '../Data/Mty/noreste/',
    'path measurement': '../Data/Mty/Stations/noreste/Mediciones/',
    'path graphics': '../Graphics/',
    'file measurement': '150111.txt',
    'file RD': 'test.csv',
    'file graphics': 'Different_RD_values.png',
    'Hour initial': 8,
    'Hour final': 17,
    'Fontsize': 14,
}
AOD_list, RD_list = np.loadtxt('{}{}'.format(parameters['path RD'],
                                             parameters['file RD']),
                               delimiter=',',
                               usecols=[5, 6],
                               skiprows=1,
                               unpack=True)
measurement_hour, measurement_data = read_data(parameters['path measurement'],
                                               parameters['file measurement'])
files = sorted(os.listdir(parameters['path data']))
fig, axs = plt.subplots(2, 2,
                        sharex=True,
                        sharey=True,
                        figsize=(8, 7))
axs = np.reshape(axs, 4)
for ax, file, AOD, RD in zip(axs, files, AOD_list, RD_list):
    SMARTS_hour, SMARTS_data = read_data(parameters['path data'],
                                         file)
    ax.plot(SMARTS_hour, SMARTS_data,
            label='SMARTS',
            lw=3,
            color='#ff79c6',)
    ax.plot(measurement_hour, measurement_data,
            label='Measurement',
            lw=3,
            color='#6272a4',
            marker='o')
    ax.set_xlim(parameters['Hour initial'],
                parameters['Hour final'])
    ax.set_xticks([hour for hour in range(parameters["Hour initial"],
                                          parameters["Hour final"])])
    ax.set_ylim(0, 700)
    ax.grid(ls='--',
            color='#000000')
    ax.set_title('AOD={}    RD={}'.format(AOD, RD),
                 fontsize=parameters['Fontsize'])
fig.text(0.45, 0.025, 'Local time (h)',
         fontsize=parameters['Fontsize'])
fig.text(0.01, 0.32, 'Irradiance Solar $\\left(W/m^2\\right)$',
         fontsize=parameters['Fontsize'],
         rotation=90)
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels,
           loc='upper center',
           frameon=False,
           ncol=2,
           fontsize=parameters['Fontsize'])
plt.subplots_adjust(left=0.1,
                    bottom=0.11,
                    right=0.975,
                    top=0.9,
                    wspace=0.066,
                    hspace=0.158)
plt.savefig('{}{}'.format(parameters['path graphics'],
                          parameters['file graphics']),
            dpi=400)
