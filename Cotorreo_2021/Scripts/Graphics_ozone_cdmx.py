import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def consecutive_day_to_date(year=2000, day=365):
    date = datetime.date(year, 1, 1)+datetime.timedelta(day)
    date = pd.to_datetime(date)
    return date


def obtain_month_names():
    names = []
    for i in range(1, 13):
        date = datetime.date(2000, i, 1)
        names.append(date.strftime("%b"))
    return names


def obtain_month_days():
    month_days = []
    for month in range(1, 13):
        day = (datetime.date(2019, month, 28) - datetime.date(2019, 1, 1)).days
        month_days.append(day)
    return month_days


class OMI_data:
    def __init__(self, parameters={}):
        self.parameters = parameters
        self.read_data()

    def read_data(self):
        self.data = pd.read_fwf("{}{}".format(self.parameters["path data"],
                                              self.parameters["file data"]),
                                skiprows=27)
        self.clean_data()
        self.format_data()
        self.select_data_in_period()
        self.obtain_daily_mean()

    def clean_data(self):
        columns = self.data.columns
        columns = columns.drop(["Ozone", "Datetime"])
        self.data = self.data.drop(columns, 1)

    def format_data(self):
        self.data["Date"] = self.data["Datetime"].astype(
            str).str[0:4]+"-"+self.data["Datetime"].astype(str).str[4:6]+"-"+self.data["Datetime"].astype(str).str[6:8]
        self.data.index = pd.to_datetime(self.data["Date"])
        self.data = self.data.drop(["Datetime", "Date"], 1)

    def select_data_in_period(self):
        self.data = self.data[self.data.index >=
                              self.parameters["Date initial"]]
        self.data = self.data[self.data.index <= self.parameters["Date final"]]

    def obtain_daily_mean(self):
        self.data = self.data.resample("D").mean()


class Matrix_data:
    def __init__(self, parameters={}, data=pd.DataFrame()):
        self.parameters = parameters
        self.data = data
        self.create_matrix()
        self.obtain_monthly_mean()
        self.fill_matrix()

    def obtain_monthly_mean(self):
        self.monthly_mean = self.data.resample("MS").mean()
        self.data = self.data.fillna(0)

    def create_matrix(self):
        self.year_initial = pd.to_datetime(
            self.parameters["Date initial"]).year
        self.year_final = pd.to_datetime(self.parameters["Date final"]).year
        years = self.year_final-self.year_initial+1
        self.matrix_data = np.zeros([years, 365])

    def fill_matrix(self):
        dates = self.data.index
        for year in range(self.year_initial, self.year_final+1):
            for day in range(1, 366):
                date = consecutive_day_to_date(year, day)
                day = day-1
                if date in dates and self.data["Ozone"][date] != 0:
                    data = self.data["Ozone"][date]
                else:
                    data = self.read_monthly_mean_data(date)
                self.matrix_data[year-self.year_initial, day] = data

    def read_monthly_mean_data(self, date=pd.Timestamp):
        month = str(date.month).zfill(2)
        year = date.year
        date = pd.to_datetime("{}-{}-01".format(year,
                                                month))
        return self.monthly_mean["Ozone"][date]


class plot_data:
    def __init__(self, parameters={}, data=np.array([])):
        self.parameters = parameters
        self.data = data
        self.plot()

    def plot(self):
        plt.contourf(self.data)
        self.obtain_xticks()
        plt.xticks(self.month_days, self.month_names,
                   fontsize=12)
        plt.xlabel("Months",
                   fontsize=16)
        self.obtain_yticks()
        plt.yticks(self.years_position, self.years,
                   fontsize=14)
        plt.ylabel("Years",
                   fontsize=12)
        plt.grid(ls="--",
                 color="#000000")
        cbar = plt.colorbar()
        cbar.ax.set_ylabel("Total Ozone Column (DU)",
                           rotation=-90,
                           va="bottom",
                           fontsize=16)
        plt.tight_layout()
        plt.savefig("{}{}".format(self.parameters["path graphics"],
                                  self.parameters["graphics name"]),
                    dpi=400)

    def obtain_xticks(self):
        self.month_names = obtain_month_names()
        self.month_days = obtain_month_days()

    def obtain_yticks(self):
        year_initial = int(self.parameters["Date initial"].split("-")[0])
        year_final = int(self.parameters["Date final"].split("-")[0])
        self.years = np.arange(year_initial+1, year_final+1, 2)
        self.years_position = self.years-year_initial


if __name__ == "__main__":
    parameters = {
        "path data": "../Data/",
        "file data": "ozono_cdmx.csv",
        "path graphics": "../Graphics/",
        "graphics name": "ozone_cdmx.png",
        "Date initial": "2005-01-01",
        "Date final": "2020-12-31"
    }
    OMI = OMI_data(parameters)
    data = Matrix_data(parameters=parameters,
                       data=OMI.data)
    plot = plot_data(parameters=parameters,
                     data=data.matrix_data)
