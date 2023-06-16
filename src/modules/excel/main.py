import openpyxl, csv, xlrd


# 读取 .xls 文件
def xlsFile():
    wb = xlrd.open_workbook('excel.xls')
    sheet = wb.sheet_by_index(0)
    list = []
    for row in range(sheet.nrows):
        row_data = sheet.row_values(row)
        list.append(row_data)
    return list


# 读取xlsx文件
def xlsxFile():
    wb = openpyxl.load_workbook('excel.xlsx')
    sheet = wb.active
    list = []
    for row in sheet.iter_rows(values_only=True):
        list.append(row)
    wb.close()
    return list


# 打开 CSV 文件
def csvFile():
    with open('excel.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        list = []
        for row in reader:
            list.append(row)
    return list


def save_to_csv(data_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['Column 1', 'Column 2', 'Column 3', 'Column 4',
             'Column 5'])  # 写入表头
        writer.writerows(data_list)  # 写入数据行


def search(list, col, keyword, exact_match=True):
    result = []
    for row in list:
        if exact_match:
            if keyword == row[col]:
                result.append(row)
                print(row)
        else:
            if keyword in row[col]:
                result.append(row)
                print(row)
    save_to_csv(result, "search_result.csv")
    return result


data = xlsFile()

search(data, 4, "圣彼得堡", False)
