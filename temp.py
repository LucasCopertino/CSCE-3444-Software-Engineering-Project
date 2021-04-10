import datetime

rn = datetime.datetime.now()
if rn.hour in range(16,24):
    print("yes")