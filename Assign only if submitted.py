import os
import shutil
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def sanitize_filename(filename):
    return filename.replace(' ', '_').replace(':', '').replace('\n', '')

def allocate_screens(df, pdf_directory):
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['start time (local time)'] = pd.to_datetime(df['start time (local time)'], format='%H:%M:%S').dt.time

    unique_dates = df['date'].unique()
    session_labels = ['session 1', 'session 2']

    for date in unique_dates:
        start_times = sorted(df[df['date'] == date]['start time (local time)'].unique())
        for session_label, start_time in zip(session_labels, start_times):
            screen_number = 1
            in_person_rows = df[(df['date'] == date) & (df['start time (local time)'] == start_time) & (
                        df['In-person or Virtual'].str.lower().str.strip() == 'in-person') &
                        (df['Paid or not'].str.lower().str.strip().isin(['paid', 'partially_paid']))]
            virtual_rows = df[(df['date'] == date) & (df['start time (local time)'] == start_time) & (
                        df['In-person or Virtual'].str.lower().str.strip() == 'virtual') &
                        (df['Paid or not'].str.lower().str.strip().isin(['paid', 'partially_paid']))]

            for index, row in in_person_rows.iterrows():
                abstract_id = str(row['Abstract Submission ID'])
                pdf_filename = f"submission_{sanitize_filename(abstract_id)}.pdf"
                pdf_path = os.path.join(pdf_directory, pdf_filename)
                if os.path.exists(pdf_path):
                    df.at[index, 'Screen number'] = screen_number
                    screen_number += 1

            for index, row in virtual_rows.iterrows():
                abstract_id = str(row['Abstract Submission ID'])
                pdf_filename = f"submission_{sanitize_filename(abstract_id)}.pdf"
                pdf_path = os.path.join(pdf_directory, pdf_filename)
                if os.path.exists(pdf_path):
                    df.at[index, 'Screen number'] = screen_number
                    screen_number += 1

    return df

def copy_and_rename_pdfs(df, pdf_directory, output_dir):
    unique_dates = df['date'].unique()
    session_labels = ['session 1', 'session 2']

    for date in unique_dates:
        date_str = date.strftime('%Y-%m-%d')
        date_dir = os.path.join(output_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)
        start_times = sorted(df[df['date'] == date]['start time (local time)'].unique())
        for session_label, start_time in zip(session_labels, start_times):
            for format_type in ['In-Person', 'Virtual']:
                format_dir = os.path.join(date_dir, session_label, format_type)
                os.makedirs(format_dir, exist_ok=True)
                rows = df[(df['date'] == date) & (df['start time (local time)'] == start_time) & (
                            df['In-person or Virtual'].str.lower().str.strip() == format_type.lower()) &
                            (df['Paid or not'].str.lower().str.strip().isin(['paid', 'partially_paid']))]
                for index, row in rows.iterrows():
                    abstract_id = str(row['Abstract Submission ID'])
                    pdf_filename = f"submission_{sanitize_filename(abstract_id)}.pdf"
                    pdf_path = os.path.join(pdf_directory, pdf_filename)

                    screen_number = row['Screen number']
                    if pd.notna(screen_number):
                        new_pdf_filename = f"{screen_number}_{sanitize_filename(abstract_id)}.pdf"
                        destination_path = os.path.join(format_dir, new_pdf_filename)

                        if os.path.exists(pdf_path):
                            shutil.copy(pdf_path, destination_path)
                            print(f"Copied {pdf_filename} to {destination_path}")
                        else:
                            print(f"PDF {pdf_filename} not found in {pdf_directory}")

    print("All PDFs copied and renamed successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    pdf_directory = filedialog.askdirectory(title="Select Directory with PDF Files")

    if pdf_directory:
        excel_file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])

        if excel_file_path:
            df = pd.read_excel(excel_file_path)
            print("Column names in the DataFrame:", df.columns)

            df = allocate_screens(df, pdf_directory)

            output_dir = filedialog.askdirectory(title="Select Output Directory for Poster Sessions")

            if output_dir:
                copy_and_rename_pdfs(df, pdf_directory, output_dir)

                df.to_excel(excel_file_path, index=False)
                print("Updated Excel file with screen numbers.")
            else:
                print("No output directory selected.")
        else:
            print("No Excel file selected.")
    else:
        print("No directory selected.")
