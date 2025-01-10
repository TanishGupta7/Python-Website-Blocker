import datetime
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import platform
from plyer import notification  # For notifications

# Global variables
site_block = []
host_path = ""
redirect = "127.0.0.1"

# Function to get the correct hosts file path based on the OS
def get_host_path():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/System32/drivers/etc/hosts"
    elif system == "Linux" or system == "Darwin":  # Darwin is macOS
        return "/etc/hosts"
    else:
        raise Exception("Unsupported operating system")

# Function to block websites
def block_websites(end_time):
    global site_block, host_path, redirect
    host_path = get_host_path()
    while True:
        if datetime.datetime.now() < end_time:
            print("Start Blocking")
            with open(host_path, "r+") as host_file:
                content = host_file.read()
                for website in site_block:
                    if website not in content:
                        host_file.write(redirect + " " + website + "\n")
            # Show notification
            notification.notify(
                title="Website Blocker",
                message="Websites are now blocked!",
                timeout=5
            )
        else:
            with open(host_path, "r+") as host_file:
                content = host_file.readlines()
                host_file.seek(0)
                for lines in content:
                    if not any(website in lines for website in site_block):
                        host_file.write(lines)
                host_file.truncate()
            # Show notification
            notification.notify(
                title="Website Blocker",
                message="Websites are now unblocked!",
                timeout=5
            )
            break
        time.sleep(5)

# Function to add a website to the block list
def add_website():
    website = website_entry.get()
    if website:
        site_block.append(website)
        website_listbox.insert(tk.END, website)
        website_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a website to block.")

# Function to remove a website from the block list
def remove_website():
    selected = website_listbox.curselection()
    if selected:
        website = website_listbox.get(selected)
        site_block.remove(website)
        website_listbox.delete(selected)
    else:
        messagebox.showwarning("Selection Error", "Please select a website to remove.")

# Function to start blocking
def start_blocking():
    try:
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
        end_time = datetime.datetime.now() + datetime.timedelta(hours=hours, minutes=minutes)
        block_websites(end_time)
        messagebox.showinfo("Success", f"Websites will be blocked for {hours} hours and {minutes} minutes.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter valid numbers for hours and minutes.")

# GUI Setup
root = tk.Tk()
root.title("Website Blocker")
root.geometry("500x600")
root.config(bg="#2E3440")

# Custom Fonts
title_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 12)

# Title Label
title_label = tk.Label(root, text="Website Blocker", font=title_font, bg="#2E3440", fg="#D8DEE9")
title_label.pack(pady=10)

# Website Entry Frame
entry_frame = tk.Frame(root, bg="#2E3440")
entry_frame.pack(pady=10)

website_label = tk.Label(entry_frame, text="Enter Website:", font=label_font, bg="#2E3440", fg="#D8DEE9")
website_label.grid(row=0, column=0, padx=5)

website_entry = tk.Entry(entry_frame, font=label_font, width=20)
website_entry.grid(row=0, column=1, padx=5)

add_button = tk.Button(entry_frame, text="Add", font=button_font, bg="#5E81AC", fg="#D8DEE9", command=add_website)
add_button.grid(row=0, column=2, padx=5)

# Website Listbox
website_listbox = tk.Listbox(root, font=label_font, bg="#3B4252", fg="#D8DEE9", selectbackground="#5E81AC")
website_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

remove_button = tk.Button(root, text="Remove Selected", font=button_font, bg="#5E81AC", fg="#D8DEE9", command=remove_website)
remove_button.pack(pady=10)

# Block Duration Frame
duration_frame = tk.Frame(root, bg="#2E3440")
duration_frame.pack(pady=10)

hours_label = tk.Label(duration_frame, text="Hours:", font=label_font, bg="#2E3440", fg="#D8DEE9")
hours_label.grid(row=0, column=0, padx=5)

hours_entry = tk.Entry(duration_frame, font=label_font, width=5)
hours_entry.grid(row=0, column=1, padx=5)

minutes_label = tk.Label(duration_frame, text="Minutes:", font=label_font, bg="#2E3440", fg="#D8DEE9")
minutes_label.grid(row=0, column=2, padx=5)

minutes_entry = tk.Entry(duration_frame, font=label_font, width=5)
minutes_entry.grid(row=0, column=3, padx=5)

# Start Blocking Button
start_button = tk.Button(root, text="Start Blocking", font=button_font, bg="#5E81AC", fg="#D8DEE9", command=start_blocking)
start_button.pack(pady=20)

# Start the main loop
root.mainloop()