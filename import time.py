import time
from datetime import datetime
import calendar
import os
import subprocess
def timeinput():
    while True:
        try:
            h=int(input("input hour:"))
            if h<0 or h>24:
                print('invalid hour')
                continue
            break
        except ValueError:
            print('invalid input')

    while True:
        try:
            m=int(input("input minute:"))
            if m==60:
                h=h+1
                m=0
                break
            if m>59 or m<0:
                print('invalid minute')
            else:
                break
        except ValueError:
            print('invalid value')
    return h,m
hour,minute=timeinput()

def dateinput():
    while True:
        try:
            year = int(input('Input year: '))
            break
        except ValueError:
            print('Invalid input. Please enter a number.')
    
    while True:
        try:
            month=int(input('input month:'))
            if month<1 or month>12:
                print('invalid month')
                continue
            break
        except ValueError:
            print('invalid input')
            
    _, max_day=calendar.monthrange(year,month)
    
    while True:
        try:
            day=int(input('input day:'))
            if day<1 or day>31:
                print('invalid day')
                continue
            if day>max_day:
                day=max_day
            break
        except ValueError:
            print('invalid input')
    return month,day,year
month,day,year=dateinput()

shutdown_time = datetime(year, month, day, hour, minute)
time_now=datetime.now()
delta= shutdown_time - time_now
remaining=int(delta.total_seconds())

repeat=input('repeat everyday?')
if repeat=='yes' or 'y':
    time=f'{hour:02d}:{minute:02d}'
    task_name = "DailyShutdown"
    command = f'''schtasks /Create /SC DAILY /TN {task_name} /TR "shutdown /s /f /t 600" /ST {time} /F'''

if remaining <= 0:
    print("The scheduled time is in the past. Shutdown will not be scheduled.")
else:
    print(f"Shutdown scheduled for {shutdown_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"System will shut down in {remaining} seconds.")
    os.system(f"shutdown /s /t {remaining}")
