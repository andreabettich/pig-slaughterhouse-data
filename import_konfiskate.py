import psycopg2
import csv
import datetime

konfiskate = []


def toFloat(numb):
    return float(numb.replace(',', '.'))


with open('example_import_konfiskate.csv') as csvfile:
    fields = ['schlachtdatum', 'eingangsnr', 'anzahl', 'bezeichnung', 'shit', 'label']
    reader = csv.DictReader(csvfile, fieldnames=fields, delimiter=';')
    rowCount = 0
    for row in reader:

        if rowCount > 0 and len(row['schlachtdatum']) > 0:
            year = row['schlachtdatum'][0:4]
            month = row['schlachtdatum'][4:6]
            day = row['schlachtdatum'][6:8]
            schlachtdatum_date = datetime.datetime(int(year), int(month), int(day))
            konfiskate_csv = {
                'posten_id': row['eingangsnr'],
                'schlachtdatum_date': schlachtdatum_date,
                'anzahl': int(row['anzahl']),
                'bezeichnung': row['bezeichnung'],
                'label': row['label']
            }
            konfiskate.append(konfiskate_csv)
        rowCount += 1


def import_konfiskate(cur):
    count = 0
    for konfiskat in konfiskate:
        print('KONFISKATE PROGRESS => %s of %s' % (count, len(konfiskate)))
        print(konfiskat)
        cur.execute("""INSERT INTO konfiskate (posten_id, anzahl, bezeichnung, label) VALUES (
            (SELECT id FROM posten WHERE schlachthof = %s AND schlachtdatum = %s AND betrieb_id = (SELECT id FROM betrieb WHERE bid = %s)),
            %s,
            %s,
            %s
            )""", (
            'BB',
            konfiskat['schlachtdatum_date'],
            konfiskat['posten_id'],
            konfiskat['anzahl'],
            konfiskat['bezeichnung'],
            konfiskat['label']
        ))
        count += 1


try:
    conn = psycopg2.connect("""
        dbname='piggy' user='piggy' host='localhost' password='piggy'
        """)
    cur = conn.cursor()
    print('Import Konfiskate')
    import_konfiskate(cur)
    conn.commit()
    print('Import Betriebe Finish')
    conn.close()
except Exception as error:
    print(error)
    print("I am unable to connect to the database")
