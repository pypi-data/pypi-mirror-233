import openpyxl

# Load the Excel file
workbook = openpyxl.load_workbook('C:/EDRW/09 Zambales_23.xlsx')

# Choose the worksheet
worksheet = workbook['Q2']  # Replace 'Sheet1' with the name of your sheet

# Iterate through the cells with hyperlinks and edit them
for row in worksheet.iter_rows():
    for cell in row:
        if cell.hyperlink:
            cell.hyperlink.target = 'new_link_url'  # Replace with the new URL

# Save the modified Excel file
workbook.save('modified_excel_file.xlsx')

# Close the workbook
workbook.close()
