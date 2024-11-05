import pandas as pd
from tkinter import Tk, filedialog

# Open a file picker dialog to select the input Excel file
def select_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx")])
    root.destroy()
    return file_path

# Function to determine the session (morning/evening)
def determine_session(time_str):
    time = pd.to_datetime(time_str, format='%H:%M').time()
    if time < pd.Timestamp('12:00').time():
        return 'morning'
    else:
        return 'evening'

# Main function to process the file
def process_file(file_path):
    # Load the provided spreadsheet
    df = pd.read_excel(file_path)

    # Add a session column to the dataframe
    df['session'] = df['start time (local time)'].apply(determine_session)

    # Group by date and session to find the highest screen number
    result = df.groupby(['date', 'session']).apply(lambda x: x.loc[x['Screen number'].idxmax()])

    # Select the necessary columns for the output
    output_df = result[['date', 'start time (local time)', 'Screen number', 'session']].reset_index(drop=True)

    # Pivot the dataframe to have morning and evening sessions in separate columns
    pivot_df = output_df.pivot(index='date', columns='session', values=['start time (local time)', 'Screen number']).reset_index()
    pivot_df.columns = ['_'.join(col).strip() for col in pivot_df.columns.values]
    pivot_df.rename(columns={'date_': 'date', 'start time (local time)_morning': 'morning_start_time', 'Screen number_morning': 'morning_screen_number', 'start time (local time)_evening': 'evening_start_time', 'Screen number_evening': 'evening_screen_number'}, inplace=True)

    # Save the result to a new spreadsheet
    output_file_path = 'max_numbers.xlsx'
    pivot_df.to_excel(output_file_path, index=False)

    print(f"File saved as {output_file_path}")

# Select the input file
input_file_path = select_file()

# Process the selected file
process_file(input_file_path)
