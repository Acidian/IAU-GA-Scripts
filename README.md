# IAU-GA Scripts
This repository contains the Python scripts used during the 2024 International Astronomical Union General Assembly (IAU-GA) e-poster sessions. These scripts facilitate the management, display, and assignment of poster sessions across multiple Raspberry Pi devices and screens, streamlining presentations for a smooth participant experience.

Note: All scripts use a standardized dataset in a specified, hardcoded location. Some scripts require input from Excel sheets. If you're using custom data, adjust the code to match the column structure of your Excel files. The scripts were also created to function on a Raspberry Pi 5 and may need to be modified for other platforms. 

Scripts Overview
1. PDF Display Script (IAUScript.py)
Purpose: Opens and resizes PDF files to fit the screen for easy screen-sharing during presentations.
Functionality: Uses window management utilities (e.g., wmctrl) to retrieve information about open windows, allowing for organization and control of active windows during sessions. This setup minimizes interference from Zoom overlays, making it simpler to present.
Requirements: Ensure window management utilities are available on your system for proper functionality.
2. Distribute Scripts to All Pis (create_distribute_scripts.py)
Purpose: Automates the distribution and execution of poster-related scripts across multiple Raspberry Pi devices.
Functionality: Reads poster and screen assignments from a CSV file, then generates and schedules SSH commands to remotely execute the display script on the assigned Pi devices based on session dates and times.
3. Assign Screens to Presenters (Assign_only_if_submitted.py)
Purpose: Manages the assignment of up to 100 screens per session based on poster submission status and payment verification.
Functionality: Processes data from Excel sheets to determine qualifying presenters, then assigns screens to eligible participants.
4. Create Program Based on Assigned Screens (Program.py)
Purpose: Generates a session program with details of each poster, including presenter, assigned screen, and scheduled time.
Functionality: Uses output from the screen assignment script to create an Excel file that lists day, time, presenter, and screen/Zoom room assignments.
5. Summarize Screen Utilization (Summarize_max_screens.py)
Purpose: Analyzes and summarizes screen usage to identify peak times and optimize resource allocation.
Functionality: Reads an Excel file to calculate maximum screen usage for morning and evening sessions across various dates, generating a pivot table of screen numbers and start times. The summarized data is saved in a new Excel file.
