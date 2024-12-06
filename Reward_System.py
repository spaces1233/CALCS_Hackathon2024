# -*- coding: utf-8 -*-

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Function to assign points for Bronze Tier activities
def assign_bronze_points(activity):
    if activity == 'Logging into the CALCS Platform':
        return 5
    elif activity == 'Completing a Self-Assessment Quiz':
        return 10
    elif activity == 'Viewing a Resource':
        return 5
    elif activity == 'Checking Event Calendar':
        return 5
    elif activity == 'Participating in a Wellness Poll or Survey':
        return 10
    elif activity == 'Inviting a Friend to Join the Platform':
        return 5
    elif activity == 'RSVPing to an Event':
        return 10
    return 0

# Function to assign points for Silver Tier activities
def assign_silver_points(activity):
    if activity == 'Attending a Virtual Workshop or Event':
        return 25
    elif activity == 'Participating in a Wellness Challenge':
        return 30
    elif activity == 'Completing a Self-Care Activity':
        return 20
    elif activity == 'Posting or Responding in the Peer Support Forum':
        return 20
    elif activity == 'Joining a Monthly Wellness Challenge':
        return 30
    elif activity == 'Using the Live Chat with CALCS Staff':
        return 20
    return 0

# Function to assign points for Gold Tier activities
def assign_gold_points(activity):
    if activity == 'Leading a Peer Support Group':
        return 50
    elif activity == 'Organizing a Wellness Event':
        return 60
    elif activity == 'Completing a Mental Health First Aid Course':
        return 50
    elif activity == 'Being a CALCS Ambassador':
        return 70
    return 0

# Function to process the data and calculate total points and money reward
def process_data(df):
    # Apply point system to Bronze, Silver, and Gold Tier activities
    df['Bronze Points'] = df['Bronze Activity'].apply(assign_bronze_points)
    df['Silver Points'] = df['Silver Activity'].apply(assign_silver_points)
    df['Gold Points'] = df['Gold Activity'].apply(assign_gold_points)

    # Calculate total points
    df['Total Points'] = df['Bronze Points'] + df['Silver Points'] + df['Gold Points']

    # Calculate money reward ($1 for every 10 points)
    df['Money Reward ($)'] = df['Total Points'] * 0.1

    # Group by participant name and sum up the points and rewards
    df_grouped = df.groupby('Participant Name').sum()

    # Reset the index to keep the 'Participant Name' column
    df_grouped.reset_index(inplace=True)

    return df_grouped

# Function to load CSV file and display the table
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Process the data to calculate points and rewards
            df_grouped = process_data(df)

            # Clear any previous data in the treeview
            for i in tree.get_children():
                tree.delete(i)

            # Insert the data into the treeview
            for index, row in df_grouped.iterrows():
                tree.insert('', 'end', values=(row['Participant Name'], row['Bronze Points'], 
                                               row['Silver Points'], row['Gold Points'], 
                                               row['Total Points'], f"${row['Money Reward ($)']:.2f}"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

# Set up the Tkinter window
root = tk.Tk()
root.title("CALCS Engagement Points Table")

# Increase the font size
font_style = ('Helvetica', 14)

# Create and configure a style for the Treeview headings
style = ttk.Style()
style.configure('Treeview.Heading', font=font_style)  # Font for headings
style.configure('Treeview', font=font_style)  # Font for rows

# Create a frame to hold the Treeview
frame = tk.Frame(root)
frame.pack(pady=10)

# Create Treeview widget for displaying data
tree = ttk.Treeview(frame, columns=('Name', 'Bronze Points', 'Silver Points', 'Gold Points', 
                                   'Total Points', 'Money Reward'), show='headings')

# Define columns and increase their widths to ensure full visibility of the headings
tree.heading('Name', text='Participant Name')
tree.column('Name', width=250)  # Increased width

tree.heading('Bronze Points', text='Bronze Points')
tree.column('Bronze Points', width=150, anchor='center')  # Increased width

tree.heading('Silver Points', text='Silver Points')
tree.column('Silver Points', width=150, anchor='center')  # Increased width

tree.heading('Gold Points', text='Gold Points')
tree.column('Gold Points', width=150, anchor='center')  # Increased width

tree.heading('Total Points', text='Total Points')
tree.column('Total Points', width=150, anchor='center')  # Increased width

tree.heading('Money Reward', text='Money Reward ($)')
tree.column('Money Reward', width=180, anchor='center')  # Increased width

# Pack the Treeview widget into the frame
tree.pack(fill='both', expand=True)

# Create and configure a style for the buttons
button_style = ttk.Style()
button_style.configure('TButton', font=font_style)

# Use ttk.Button with the defined style
load_button = ttk.Button(root, text="Upload CSV", command=load_file, style='TButton')
load_button.pack(pady=5)

close_button = ttk.Button(root, text="Close", command=root.quit, style='TButton')
close_button.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()
