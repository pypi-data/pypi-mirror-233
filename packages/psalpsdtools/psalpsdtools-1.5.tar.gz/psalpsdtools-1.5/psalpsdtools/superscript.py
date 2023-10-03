import xlsxwriter

workbook = xlsxwriter.Workbook('your_modified_excel_file.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:A', 30)
superscript = workbook.add_format({'font_script': 1})
worksheet.write_rich_string('cell',
                            'hello',
                            superscript, 'world'
)
workbook.close()