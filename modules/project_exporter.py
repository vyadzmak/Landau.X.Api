import xlsxwriter
import json
from settings import EXPORT_FOLDER
import os
import uuid
import unicodedata
import string
from transliterate import translit, get_available_language_codes
valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
import datetime
import zlib
import base64
import copy
def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:

        filename = filename.replace(r, '_')

    filename = filename.replace('(','')
    filename = filename.replace(')','')
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)

def generate_cell_style(workbook,data):
    try:
        font_color = data["color"]
        background_color = data["bgc"]
        width = data["width"]
        font_family = data["ff"]
        font_weight = data["fw"]
        text_align = data["ta"]
        font_size = data["fz"]
        fm = data["fm"]
        format = workbook.add_format()
        format.set_bg_color(background_color)
        format.set_font_color(font_color)
        format.set_border(1)
        # format.set_font_family(font_family)
        format.set_font_size(font_size)
        if (str(font_weight)=='bold'):
            format.set_bold()
        if (fm=="money||2|none"):
            format.set_num_format('#,##0.00')
        elif (fm!='' and fm!="money||2|none"):
            pass
        format.set_align(text_align)
        format.set_font_name(font_family)
        #format.set_text_wrap()
        return format
        pass
    except Exception as e:
        return None



def export_cells(id,workbook,worksheet, cells):
    try:
        # row, col, value


        for cell in cells:
            if (cell["sheet"]==id):
                row = int(cell["row"])

                col = int(cell["col"])
                if (row==0 or col==0):
                    continue
                value = cell["json"]["data"]
                _format = generate_cell_style(workbook,cell["json"])
                if (_format!=None):
                    worksheet.write(row-1, col-1, value,_format)
                else:
                    worksheet.write(row-1, col-1, value)


    except Exception as e:
        pass

def get_widths(index,cells):
    widths =[]
    for cell in cells:
        row = int(cell["row"])
        sheet = int(cell["sheet"])
        col = int(cell["col"])
        if (row==0 and sheet==index):
            s_width = 6
            if (col==1):
                s_width = 8
            width =round(int(cell["json"]["width"])/s_width,1)
            widths.append(width)

    return widths
    pass

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of bytes

def check_utf8(bytes_or_str):
    try:
        value = bytes_or_str.decode(encoding='utf-8')
        print("Convert to UTF-8 - OK")
        return True
    except Exception as e:
        return False

def to_str(bytes_or_str):
    try:
        if isinstance(bytes_or_str, bytes):
            if (check_utf8(bytes_or_str)):
                print("Encode to utf-8")
                value = bytes_or_str.decode(encoding='utf-8')  # uses 'utf-8' for encoding
            else:
                print("Encode to utf-16")
                value = bytes_or_str.decode(encoding='utf-16')

            print('bytes or string OK')
            # value = bytes_or_str.decode()  # uses 'utf-8' for encoding
        else:
            value = bytes_or_str
        return value
    except Exception as e:
        print('TO STR ERROR '+str(e))


def t_load(report):
    try:
        s_cmpstr = copy.deepcopy(report)

        s_cmpstr = s_cmpstr.replace("b'", "", 1)

        s_cmpstr = s_cmpstr.replace("'", "")
        b_cmpstr = to_bytes(s_cmpstr)
        b_cmpstr = base64.b64decode(b_cmpstr)

        tmp = zlib.decompress(b_cmpstr)
        del s_cmpstr
        del b_cmpstr

        rr = to_str(tmp)
        del tmp
        f_cmpstr = rr
        # f_cmpstr = f_cmpstr.replace("'", "")
        rr = json.loads(f_cmpstr)
        return rr
    except Exception as e:
        return None


def export_project(project_name,report):
    try:

        rr= t_load(report)

        if (rr==None):
            s_cmpstr = copy.deepcopy(report)
            rr =json.loads(s_cmpstr)

        data =rr


        dir_id = str(uuid.uuid4().hex)
        project_folder = os.path.join(EXPORT_FOLDER, dir_id)
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)

        project_name = str(project_name).replace('"',' ')
        project_name = translit(project_name, 'ru', reversed=True)

        dt =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt = str(dt).replace('-','')
        project_name=project_name+"_"+str(dt)

        file_name = clean_filename(project_name)
        file_name = file_name.replace('__', "_")
        file_path = os.path.join(project_folder,file_name+".xlsx")

        if (len(file_path)>255):
            file_path = os.path.join(project_folder,dir_id+".xlsx")


        workbook = xlsxwriter.Workbook(file_path)

        for sheet in data['sheets']:
            name = sheet['name']
            id = sheet['id']

            worksheet = workbook.add_worksheet(name)
            widths = get_widths(id,data['cells'])
            index =0
            for width in widths:
                worksheet.set_column(index,index,width)
                index+=1
            # Write some numbers, with row/column notation.
            export_cells(id,workbook,worksheet,data["cells"])


        workbook.close()
        return project_folder,file_name+".xlsx"
        pass
    except Exception as e:
        pass