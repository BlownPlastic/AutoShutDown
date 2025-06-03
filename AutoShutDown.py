import time
from datetime import datetime
import calendar
import os
import subprocess
from tkinter import *
from tkinter import messagebox

def get_user_input():
    try:
        h = int(e0.get())
        if h < 0 or h > 23:  # Changed to 23 since 24 is invalid
            messagebox.showerror("Error", "Invalid hour (0-23)")
            return None
        
        m = int(e1.get())
        if m == 60:
            h = h + 1
            m = 0
        elif m > 59 or m < 0:
            messagebox.showerror("Error", "Invalid minute (0-59)")
            return None

        # Check if "Use today's date" is selected
        if today_var.get():
            # Use today's date
            today = datetime.now()
            year = today.year
            month = today.month
            day = today.day
        else:
            # Get and validate user-entered date
            year = int(e2.get())
            
            month = int(e3.get())
            if month < 1 or month > 12:
                messagebox.showerror("Error", "Invalid month (1-12)")
                return None
            
            _, max_day = calendar.monthrange(year, month)
            day = int(e4.get())
            if day < 1 or day > max_day:
                messagebox.showerror("Error", f"Invalid day for {month}/{year} (1-{max_day})")
                return None
        
        return year, month, day, h, m
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")
        return None

def toggle_date_fields():
    """Enable/disable date fields based on today checkbox"""
    if today_var.get():
        # Disable date fields and fill with today's date
        e2.config(state='disabled')
        e3.config(state='disabled') 
        e4.config(state='disabled')
        # Fill with today's date for display
        today = datetime.now()
        e2.delete(0, END)
        e2.insert(0, str(today.year))
        e3.delete(0, END)
        e3.insert(0, str(today.month))
        e4.delete(0, END)
        e4.insert(0, str(today.day))
    else:
        # Enable date fields
        e2.config(state='normal')
        e3.config(state='normal')
        e4.config(state='normal')

def schedule_shutdown():
    result = get_user_input()
    if result is None:
        return
    
    year, month, day, hour, minute = result

    shutdown_time = datetime(year, month, day, hour, minute)
    time_now = datetime.now()
    delta = shutdown_time - time_now
    remaining = int(delta.total_seconds())
    
    if remaining <= 0:
        messagebox.showwarning("Warning", "The scheduled time is in the past!")
        return

    repeat = repeat_var.get()  
    
    if repeat:
        time_str = f'{hour:02d}:{minute:02d}'
        task_name = "DailyShutdown"
        command = f'''schtasks /Create /SC DAILY /TN {task_name} /TR "shutdown /s /f /t 600" /ST {time_str} /F'''
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            subprocess.run(command, shell=True, check=True, startupinfo=startupinfo)
            messagebox.showinfo("Success", f"Daily shutdown scheduled for {time_str}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to create scheduled task")
    else:
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            subprocess.run(f"shutdown /s /t {remaining}", shell=True, startupinfo=startupinfo)
            messagebox.showinfo("Success", 
                f"Shutdown scheduled for {shutdown_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"System will shut down in {remaining} seconds.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule shutdown: {e}")

# Create the main window
window = Tk()
window.title("AutoShutDown")
window.geometry("259x500")

Label(window, text="Hour:").pack(pady=5)
e0 = Entry(window)
e0.pack(pady=5)

Label(window, text="Minute:").pack(pady=5)
e1 = Entry(window)
e1.pack(pady=5)

# Create checkbox for today's date
today_var = BooleanVar()
today_checkbox = Checkbutton(window, text="Use today's date", variable=today_var, command=toggle_date_fields)
today_checkbox.pack(pady=10)

Label(window, text="Year:").pack(pady=5)
e2 = Entry(window)
e2.pack(pady=5)

Label(window, text="Month:").pack(pady=5)
e3 = Entry(window)
e3.pack(pady=5)

Label(window, text="Day:").pack(pady=5)
e4 = Entry(window)
e4.pack(pady=5)

repeat_var = BooleanVar()
repeat_checkbox = Checkbutton(window, text="Repeat everyday", variable=repeat_var)
repeat_checkbox.pack(pady=10)

submit = Button(window, text="Schedule Shutdown", command=schedule_shutdown)
submit.pack(pady=10)

window.mainloop()