import os
import openpyxl as px

# Replace 'your_folder_path' with the path to your main folder containing the .xlsx files and subfolders
folder_path = 'C:/EDRW/Q2/Sources'

# Loop through all files and subdirectories
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith('.xlsx'):
            file_path = os.path.join(root, filename)
            
            # Load the .xlsx file
            wb = px.load_workbook(file_path)
            
            # Create a new .xlsm filename
            new_filename = os.path.splitext(filename)[0] + '.xlsm'
            new_file_path = os.path.join(root, new_filename)
            
            # Save the file as .xlsm
            wb.save(new_file_path)
            
            # Close the workbook
            wb.close()

print("Conversion complete. All .xlsx files in the folder and its subfolders have been converted to .xlsm format.")
