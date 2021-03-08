from modules.csvToolbox import labeled_csv_lines_to_dict, rename_dict_key, array_to_csv_lines
from modules.dateToolbox import Date
from modules.fileToolbox import read_file_lines, write_file_lines, files_in_dir

def strip_key_names(d):
    keys = list(d.keys())
    for key in keys[1:]:
        d = rename_dict_key(d, key, key.split(" - ")[-1])  # look into the use of pointers in python
    return d

def remove_newlines(d):
    last_key = list(d.keys())[-1]
    last_col = d[last_key]
    for i in range(len(last_col)):
        last_col[i] = last_col[i][:-1]
    d[last_key] = last_col
    d = rename_dict_key(d, last_key, last_key[:-1])
    return d

def string_to_float_list(l):
    float_list = []
    for s in l:
        if s == "": s = "0"
        float_list.append(float(s))
    return float_list

def float_to_string_list(l):
    str_list = []
    for fl in l:
        str_list.append(str(fl))
    return str_list

def replace_string_dates_with_Dates(d, key):
    dates = d[key]
    for col in range(len(dates)):
        dates[col] = dates[col][:10]
        dates[col] = Date(dates[col])
    d[key] = dates
    return d

def extract_dict_for_period(d, start_i, end_i):
    keys = list(d.keys())
    extracted_d = {}
    for key in keys:
        extracted_d[key] = d[key][start_i:end_i+1]
    return extracted_d

def key_by_month(d):
    dicts = {}
    dates = d["Timestamp"]
    start_i = 0
    end_i = 0
    current_key = dates[0].m

    def add_dict():
        if current_key in dicts:
            dicts[current_key] += extract_dict_for_period(d, start_i, end_i)
        else:
            dicts[current_key] = extract_dict_for_period(d, start_i, end_i)

    for i in range(1, len(dates)):
        key = dates[i].m
        if key == current_key:
            end_i += 1
        else:
            add_dict()
            start_i = end_i = i
            current_key = key
    add_dict()
    return dicts

def key_by_year(d):
    dicts = {}
    dates = d["Timestamp"]
    start_i = 0
    end_i = 0
    current_key = dates[0].y

    def add_dict():
        if current_key in dicts:
            dicts[current_key] += extract_dict_for_period(d, start_i, end_i)
        else:
            dicts[current_key] = extract_dict_for_period(d, start_i, end_i)

    for i in range(1, len(dates)):
        key = dates[i].y
        if key == current_key:
            end_i += 1
        else:
            add_dict()
            start_i = end_i = i
            current_key = key
    add_dict()
    return dicts

def sum_month_data(year_d):
    for year in list(year_d.keys()):
        month_d = year_d[year]
        for month in list(month_d.keys()):
            csv_d = month_d[month]
            csv_d["Timestamp"] = csv_d["Timestamp"][0].m_name
            for key in list(csv_d.keys())[1:]:
                csv_d[key] = sum(string_to_float_list(csv_d[key]))
            month_d[month] = csv_d
        year_d[year] = month_d
    return year_d

def round_and_convert(year_d):
    for year in list(year_d.keys()):
        month_d = year_d[year]
        for month in list(month_d.keys()):
            csv_d = month_d[month]
            for key in list(csv_d.keys())[1:]:
                csv_d[key] = str(round(csv_d[key], 1))
            month_d[month] = csv_d
        year_d[year] = month_d
    return year_d

def get_asko_year_dict(file):
    csv_dict = labeled_csv_lines_to_dict(read_file_lines(file), ";")
    csv_dict = strip_key_names(csv_dict)
    csv_dict = remove_newlines(csv_dict)
    csv_dict = replace_string_dates_with_Dates(csv_dict, "Timestamp")
    year_dict = key_by_year(csv_dict)
    for key in list(year_dict.keys()):
        year_dict[key] = key_by_month(year_dict[key])
    year_dict = sum_month_data(year_dict)
    year_dict = round_and_convert(year_dict)
    return year_dict

def get_keys(year_d):
    years = list(year_d.keys())
    first_month_d = year_d[years[0]]
    months = list(first_month_d.keys())
    first_csv_d = first_month_d[months[0]]
    return list(first_csv_d.keys())

'''
def generate_array(rows, cols, filler = ""):
    arr = []
    for row in range(rows):
        arr.append([])
        for col in range(cols):
            arr[row].append(filler)
    return arr
'''

def format_to_array(year_d):
    keys = get_keys(year_d)[1:]
    cols = len(keys)
    sub_arrs = []
    arr = []
    for year in list(year_d.keys()):
        month_d = year_d[year]
        sub_arr = []
        sub_arr.append(["Month"] + keys)
        for month in list(month_d.keys()):
            csv_d = month_d[month]
            sub_arr.append([csv_d["Timestamp"]])
            for key in keys:
                sub_arr[-1].append(csv_d[key])
        sub_arrs.append(sub_arr)
        arr.append([year] + [""]*cols)
        arr += sub_arr
        arr.append([""]*(cols+1))
    return arr

def sum_asko_csv_file(file):
    year_dict = get_asko_year_dict("csv/" + file)
    arr = format_to_array(year_dict)
    csv_lines = array_to_csv_lines(arr, ";")
    write_file_lines("sum_csv/sum_" + file, csv_lines)

def main():
    csv_files = files_in_dir("csv")
    for f in csv_files:
        sum_asko_csv_file(f)

main()