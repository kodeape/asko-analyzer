from numpy import array
try:
    from modules.fileToolbox import read_file_lines
except:
    from fileToolbox import read_file_lines

def get_col_contents(col, data):
    col_list = []
    for row in data:
        col_list.append(row[col])
    return col_list

def csv_lines_to_array(lines, sep = ","):
    arr = []
    for line in lines:
        arr.append(line.split(sep))
    return array(arr)

def labeled_csv_lines_to_dict(csv_lines, sep = ","):
    data = csv_lines_to_array(csv_lines, sep)
    keys = data[0]
    csv_dict = {}
    for col in range(len(keys)):
        csv_dict[keys[col]] = get_col_contents(col, data[1:])
    return csv_dict

def rename_dict_key(d, old_key, new_key):
    d[new_key] = d[old_key]
    del d[old_key]
    return d

def array_to_csv_lines(arr, sep = ","):
    lines = []
    for row in arr:
        for i in range(len(row)):
            row[i] = row[i]
        lines.append(sep.join(row))
    return lines
