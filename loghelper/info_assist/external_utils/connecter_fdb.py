import fdb
import time

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
SELECT 
    (uvedoc.nomztk || '/' || substring(uvedoc.drazm FROM 4 FOR 1) || '9' || 
    SUBSTRING(sum(1000000 + uvedoc.numitem) / count(prildoc.docid) FROM 2 FOR 7)) AS numer,
    uvedoc.drazm,
    uvedoc.numitem,
    uvedoc.transp_num,
    uvedoc.docstate,
    uvedoc.date_ss,
    uvedoc.regnum_pto,
    LIST(distinct custrazr.numtd, ';') AS numtd
FROM 
    uvedoc
LEFT OUTER JOIN 
    prildoc ON uvedoc.docid = prildoc.docid
LEFT OUTER JOIN 
    NSITYPDOC ON prildoc.typdid = NSITYPDOC.typdid
LEFT OUTER JOIN 
    custrazr ON uvedoc.docid = custrazr.docid
WHERE 
    uvedoc.drazm >= current_date - 1 
    AND prildoc.docid IS NOT NULL 
    AND uvedoc.numitem IS NOT NULL
GROUP BY 
    uvedoc.nomztk, 
    uvedoc.drazm, 
    uvedoc.numitem, 
    uvedoc.transp_num,
    uvedoc.docstate, 
    uvedoc.date_ss, 
    uvedoc.regnum_pto
"""
STATUS_DICT = {
    1: "Зарегистрировано",
    2: "Снят с контроля",
    4: "Аннулировано",
    6: "Ожидание",
    7: "Обрабатывается"
}


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения {func.__name__}: {execution_time:.2f} секунд")
        return result

    return wrapper


def remove_duplicates(element):
    if isinstance(element, str) and (';' in element or '; ' in element):
        items = element.replace('; ', ';').split(';')

        unique_items = '; '.join(sorted(set(item.strip() for item in items if item.strip())))
        return unique_items
    return element


@timeit
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
        processed_row[4] = STATUS_DICT.get(processed_row[4], processed_row[4])
        processed_row[3] = remove_duplicates(processed_row[3])
        records.append(processed_row)
    return records
