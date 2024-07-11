import fdb

SETTINGS_PATH = r'C:\Program Files\Firebird\settings.txt'

with open(SETTINGS_PATH, 'r') as file:
    lines = file.readlines()

stream_data = {}
for line in lines:
    key, value = line.strip().split('=')
    stream_data[key.strip()] = value.strip().strip("'")

HOSTNAME = stream_data.get('HOSTNAME')
DATABASE_PATH = stream_data.get('DATABASE_PATH')
USERNAME = stream_data.get('USERNAME')
PASSWORD = stream_data.get('PASSWORD')

QUERY = """
SELECT (uvedoc.nomztk ||'/'||substring(uvedoc.drazm FROM 4 FOR 1)||'9'||
SUBSTRING(sum(1000000 + uvedoc.numitem) / count(prildoc.docid) FROM 2 FOR 7)) AS numer,
uvedoc.drazm,
uvedoc.numitem,
uvedoc.transp_num,
LIST (prildoc.numdoc, '; ') AS numdoc,
LIST (prildoc.typdid, '; ') AS typdid,
LIST(NSITYPDOC.naim,'; ') AS naim,
LIST(prildoc.dtdoc, '; ') AS dtdoc,
uvedoc.docstate,
uvedoc.date_ss,
uvedoc.regnum_pto,
LIST (distinct custrazr.numtd, ';') AS numtd
FROM uvedoc
LEFT OUTER JOIN prildoc ON uvedoc.docid = prildoc.docid
LEFT OUTER JOIN NSITYPDOC ON prildoc.typdid = NSITYPDOC.typdid
LEFT OUTER JOIN custrazr ON uvedoc.docid = custrazr.docid
WHERE
uvedoc.drazm >= current_date -1
GROUP BY uvedoc.nomztk, uvedoc.drazm, uvedoc.numitem, uvedoc.transp_num,
uvedoc.docstate, uvedoc.date_ss, uvedoc.regnum_pto
"""
CYRILLIC_TO_LATIN = {
        'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O',
        'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'а': 'a', 'е': 'e', 'о': 'o',
        'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x'
    }

STATUS_DICT = {
    1: "Зарегистрировано",
    2: "Снят с контроля",
    4: "Аннулировано",
    6: "Ожидание",
    7: "Обрабатывается"
}


def replace_cyrillic_with_latin(text):
    return ''.join(CYRILLIC_TO_LATIN.get(char, char) for char in text)


def remove_duplicates(element):
    if isinstance(element, str) and (';' in element or '; ' in element):

        items = element.replace('; ', ';').split(';')

        unique_items = '; '.join(sorted(set(item.strip() for item in items if item.strip())))
        return unique_items
    return element


def get_data_fdb():
    dsn = f'{HOSTNAME}:{DATABASE_PATH}'
    con = fdb.connect(dsn=dsn, user=USERNAME, password=PASSWORD)
    cur = con.cursor()
    cur.execute(QUERY)

    data = list(cur.fetchall())

    cur.close()
    con.close()

    records = []
    for row in data:
        processed_row = list(row)
        processed_row[8] = STATUS_DICT.get(processed_row[8], processed_row[8])
        records.append(processed_row)
    return records
