import psycopg2
import csv
import datetime

betriebe = []
posten = {}
pigs = []


mpa = dict.fromkeys(range(32))


def toFloat(numb):
    return float(numb.translate(mpa).replace(',', '.'))


def import_file(filename):
    print('Start import of File %s ' % (filename))
    with open(filename) as csvfile:
        fields = ['schlachthof', 'schlachtdatum', 'eingangsnr', 'label', 'schlachtgewicht', 'pufa', 'jodzahl', 'mfa', 'speckmass', 'fleischmass']
        reader = csv.DictReader(csvfile, fieldnames=fields, delimiter=';')
        rowCount = 0
        for row in reader:
            if rowCount > 0 and len(row['schlachtdatum']) > 0:
                if row['eingangsnr'] not in betriebe and len(row['eingangsnr']) > 0:
                    betriebe.append(row['eingangsnr'])
                day, month, year = row['schlachtdatum'].split('.')
                schlachtdatum_date = datetime.datetime(int(year), int(month), int(day))

                posten['%s%s%s_%s_%s' % (
                    year,
                    month,
                    day,
                    row['eingangsnr'],
                    row['schlachthof']
                )] = {
                    'eingangsnr': row['eingangsnr'],
                    'schlachtdatum': schlachtdatum_date,
                    'schlachthof': row['schlachthof']
                }
                pig_dict = {
                    'eingangsnr': row['eingangsnr'],
                    'schlachtdatum': schlachtdatum_date,
                    'schlachthof': row['schlachthof'],
                    'label': row['label'],
                    'schlachtgewicht': toFloat(row['schlachtgewicht']),
                    'pufa': toFloat(row['pufa']),
                    'jodzahl': toFloat(row['jodzahl']),
                    'mfa': toFloat(row['mfa']),
                    'speckmass': toFloat(row['speckmass']),
                    'fleischmass': toFloat(row['fleischmass'])
                }
                pigs.append(pig_dict)
            rowCount += 1


def import_betriebe(cur):
    count = 0
    for betrieb in betriebe:
        print('BETRIEB PROGRESS => %s of %s' % (count, len(betriebe)))
        try:
            cur.execute("INSERT INTO betrieb (bid) VALUES (%s)", (betrieb,))
        except Exception as error:
            print(error)
            print("Betrieb with number %s already exists" % (betrieb))
        count += 1


def import_posten(cur):
    count = 0
    for key, value in posten.items():
        print('POSTEN PROGRESS => %s of %s' % (count, len(posten)))
        cur.execute("""INSERT INTO posten (schlachthof, schlachtdatum, betrieb_id) VALUES (%s, %s, (SELECT id FROM betrieb WHERE bid = %s))""", (value['schlachthof'], value['schlachtdatum'], value['eingangsnr'],))
        count += 1


def import_pigs(cur):
    count = 0
    for pig in pigs:
        print('PIG PROGRESS => %s of %s' % (count, len(pigs)))
        cur.execute("""
            INSERT INTO schwein (posten_id,
                                label,
                                gewicht,
                                mfa,
                                jodzahl,
                                pufa,
                                speckmass,
                                fleischmass)
            VALUES (
                (SELECT id FROM posten WHERE schlachthof = %s AND schlachtdatum = %s AND betrieb_id = (SELECT id FROM betrieb WHERE bid = %s)),
                %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        pig['schlachthof'],
                        pig['schlachtdatum'],
                        pig['eingangsnr'],
                        pig['label'],
                        pig['schlachtgewicht'],
                        pig['mfa'],
                        pig['jodzahl'],
                        pig['pufa'],
                        pig['speckmass'],
                        pig['fleischmass'],
                    )
                    )
        count += 1


def import_db():
    try:
        conn = psycopg2.connect("""
            dbname='piggy' user='piggy' host='localhost' password='piggy'
            """)
        cur = conn.cursor()
        print('Import Betriebe')
        import_betriebe(cur)
        conn.commit()
        print('Import Betriebe Finish')
        print('Import Posten')
        import_posten(cur)
        conn.commit()
        print('Import Posten Finish')
        print('Import Pigs')
        import_pigs(cur)
        conn.commit()
        print('Import Pigs Finish')
        conn.close()
    except Exception as error:
        print(error)
        print("I am unable to connect to the database")


def init():
    import_file('example_import.csv')
    import_db()


init()
