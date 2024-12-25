import tkinter as tk
from tkinter import messagebox, filedialog
import time
import pygame
import threading

# Initialize pygame mixer for alarm sound
pygame.mixer.init()

# Function to play alarm sound
def play_alarm_sound():
    pygame.mixer.music.load(alarm_sound)  # Load the selected sound
    pygame.mixer.music.play(-1)  # Loop the sound indefinitely

# Function to stop the alarm sound
def stop_alarm_sound():
    pygame.mixer.music.stop()

# Function to open file dialog to select alarm sound
def select_alarm_sound():
    global alarm_sound
    alarm_sound = filedialog.askopenfilename(title="Select Alarm Sound", filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")])
    if alarm_sound:
        label_sound.config(text=f"Sound: {alarm_sound.split('/')[-1]}")  # Show the selected file name

# Function to check the alarm time
def check_alarm():
    while True:
        current_time = time.strftime('%H:%M:%S')
        for alarm in alarms:
            if alarm["time"] == current_time:
                play_alarm_sound()
                messagebox.showinfo("Alarm", f"Time for alarm: {alarm['time']}")
                if alarm["snooze"]:
                    snooze_time = alarm["snooze_time"]
                    time.sleep(snooze_time * 60)  # Convert snooze time from minutes to seconds
                    stop_alarm_sound()
                break
        time.sleep(1)

# Function to set an alarm
def set_alarm():
    alarm_time = entry_time.get()
    snooze = var_snooze.get()
    snooze_time = int(entry_snooze_time.get()) if snooze else 0

    if alarm_time:
        alarms.append({"time": alarm_time, "snooze": snooze, "snooze_time": snooze_time})
        listbox_alarms.insert(tk.END, alarm_time)
        entry_time.delete(0, tk.END)
        entry_snooze_time.delete(0, tk.END)
    else:
        messagebox.showerror("Input Error", "Please enter a valid time.")

# Function to remove an alarm
def remove_alarm():
    try:
        selected_alarm_index = listbox_alarms.curselection()[0]
        listbox_alarms.delete(selected_alarm_index)
        alarms.pop(selected_alarm_index)
    except IndexError:
        messagebox.showerror("Selection Error", "Please select an alarm to remove.")

# Function to toggle snooze option
def toggle_snooze():
    if var_snooze.get():
        label_snooze.config(text="Snooze: ON")
        entry_snooze_time.config(state="normal")
    else:
        label_snooze.config(text="Snooze: OFF")
        entry_snooze_time.config(state="disabled")

# List to store alarm times and snooze status
alarms = []
alarm_sound = "alarm_sound.mp3"  # Default sound

# Creating the GUI window
window = tk.Tk()
window.title("Interactive Python Alarm Clock")

# Time input field
label_time = tk.Label(window, text="Enter alarm time (HH:MM:SS):")
label_time.pack()

entry_time = tk.Entry(window)
entry_time.pack()

# Snooze option
var_snooze = tk.BooleanVar()
checkbox_snooze = tk.Checkbutton(window, text="Enable Snooze", variable=var_snooze, command=toggle_snooze)
checkbox_snooze.pack()

# Snooze time input field
label_snooze_time = tk.Label(window, text="Snooze time (minutes):")
label_snooze_time.pack()

entry_snooze_time = tk.Entry(window)
entry_snooze_time.pack()
entry_snooze_time.config(state="disabled")

label_snooze = tk.Label(window, text="Snooze: OFF")
label_snooze.pack()

# Buttons to set and remove alarms
button_set = tk.Button(window, text="Set Alarm", command=set_alarm)
button_set.pack()

button_remove = tk.Button(window, text="Remove Alarm", command=remove_alarm)
button_remove.pack()

# Listbox to display active alarms
label_alarms = tk.Label(window, text="Active Alarms:")
label_alarms.pack()

listbox_alarms = tk.Listbox(window, height=5)
listbox_alarms.pack()

# Select sound button
button_select_sound = tk.Button(window, text="Select Alarm Sound", command=select_alarm_sound)
button_select_sound.pack()

label_sound = tk.Label(window, text=f"Sound: {alarm_sound.split('/')[-1]}")
label_sound.pack()

# Start the alarm checking thread
alarm_thread = threading.Thread(target=check_alarm, daemon=True)
alarm_thread.start()

# Run the GUI window
window.mainloop()
