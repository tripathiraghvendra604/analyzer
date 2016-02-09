import xlsxwriter
from app import connection
from .models import Student



def make_excel(branch, sem, colg_code='027'):
    workbook = xlsxwriter.Workbook('excel.xlsx')
    worksheet = workbook.add_worksheet()
    collection = connection.test.students
    merge_format = workbook.add_format({
        'bold': True,
        #'border': 1,
        'align': 'center',
        'valign': 'vcenter',

    })
    format = workbook.add_format()
    format.set_text_wrap()

    i = 0    # i is the index of which list we have to iterate in marks
    if int(sem) % 2 == 0:
        sem = str(int(sem) - 1)
        i = 1

    head = collection.Student.find_one({'branch_code': branch, 'college_code': colg_code, 'sem': sem})
    # print head['name']
    # print head['roll_no']
    # col_mark will find the number of subjects


    worksheet.merge_range('A1:AO1', head['college_name'] +
                          " - "
                          + head['branch_name'] +
                          '- Semester:  ' +
                          sem, merge_format)

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:C', 25)
    worksheet.write(1, 0, "Roll No.", merge_format)
    worksheet.write(1, 1, "Name", merge_format)
    worksheet.write(1, 2, "Father's Name", merge_format)
    col = len(head['marks'][i])
    print col
    j = 3
    # for sub code and internal, external and total
    for x in head['marks'][i]:
        if x['sub_code'][1:4] == 'OE0':
            worksheet.merge_range(1,j,1,j+2, "OE0", merge_format)
        else:
            worksheet.merge_range(1,j,1,j+2, x['sub_code'], merge_format)
        worksheet.write(2, j, 'External')
        worksheet.write(2, j+1, 'Internal')
        worksheet.write(2, j+2, 'Total')
        j = j + 3
        col = col - 1

    # for marks now
    row = 3
    j = 3
    for st in collection.Student.find({'branch_code': branch, 'college_code': colg_code, 'sem': sem}):
        worksheet.write(row, col, st['roll_no'])
        worksheet.write(row, col + 1, st['name'], format)
        worksheet.write(row, col + 2, st['father_name'], format)
        a = 3
        for mark in st['marks'][i]:
            worksheet.write(row, a, mark['sub_marks'][0])
            worksheet.write(row, a + 1, mark['sub_marks'][1])
            worksheet.write(row, a + 2, sum(mark['sub_marks'][ : -1 ]))
            a = a + 3

        row = row + 1

    workbook.close()

make_excel('31','3', '027')