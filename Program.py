import pandas as pd
import tkinter as tk
from tkinter import filedialog

def load_excel_file():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the Excel file
    file_path = filedialog.askopenfilename(title="Select Excel File",
                                           filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        return file_path
    else:
        raise ValueError("No Excel file selected.")

def save_excel_file(df):
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the output location
    file_path = filedialog.asksaveasfilename(title="Save Excel File",
                                             defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        df.to_excel(file_path, index=False)
        print(f"Program schedule saved to {file_path}")
    else:
        raise ValueError("No file path selected for saving the Excel file.")

def create_program_schedule(input_file_path):
    # Read the Excel file
    df = pd.read_excel(input_file_path)

    # Ensure the necessary columns are present
    required_columns = ['date', 'start time (local time)', 'Screen number', 'In-person or Virtual', 'Abstract Submission ID', 'Poster Presenter(s)', 'Poster title']
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the provided Excel sheet.")

    # Remove rows where 'Screen number' is not assigned (i.e., NaN or empty)
    df = df.dropna(subset=['Screen number'])

    # Process the data to create a user-friendly format
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['start time (local time)'] = pd.to_datetime(df['start time (local time)'], format='%H:%M:%S').dt.strftime('%H:%M')

    # Organize the information
    program_df = df[['date', 'start time (local time)', 'Screen number', 'In-person or Virtual', 'Abstract Submission ID', 'Poster Presenter(s)', 'Poster title']]

    # Sort the data by date and time
    program_df = program_df.sort_values(by=['date', 'start time (local time)', 'Screen number'])

    return program_df

if __name__ == "__main__":
    try:
        # Load the input Excel file
        input_file_path = load_excel_file()

        # Create the program schedule
        program_df = create_program_schedule(input_file_path)

        # Save the result to a new Excel file
        save_excel_file(program_df)

    except Exception as e:
        print(f"Error: {e}")
