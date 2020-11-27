"""Построение графиков в matplot"""
import pandas as pd
import matplotlib.pyplot as plt

dates = ['2020-10-27', '2020-10-28', '2020-10-29', '2020-10-30', '2020-10-31', '2020-11-03', '2020-11-04', '2020-11-06']
value = [76.4443, 76.4556, 77.552, 78.8699, 79.3323, 80.5749, 80.0006, 78.4559]

df=pd.DataFrame({"date": dates,"value": value})
df["date"]=pd.to_datetime(df["date"])
plt.plot(df["date"], df["value"])
plt.gcf().autofmt_xdate()
plt.savefig("graph")
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import datetime as dt
#
# dates = ['01/02/2017','02/02/2017','03/02/2017','04/02/2017','05/02/2017']
# x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]
# data = np.array([[1,2],[2,5],[3,1],[4,0],[5,5]])
#
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator())
#
# fig = plt.figure()
#
# ax1 = fig.add_subplot(111)
#
# ax1.set_title("Plot title...")
# ax1.set_xlabel('your x label..')
# ax1.set_ylabel('your y label...')
#
# ax1.plot(x,data[:,0], c='r', label='data 1')
# ax1.plot(x,data[:,1], c='r', label='data 2')
# plt.gcf().autofmt_xdate()
#
# leg = ax1.legend()
#
# plt.show()

