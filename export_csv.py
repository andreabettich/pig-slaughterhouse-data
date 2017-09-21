import psycopg2
import csv


def avg(numbers):
    return "%.2f" % (float(sum(numbers)) / max(len(numbers), 1))


to_csv = []

try:
    conn = psycopg2.connect("""
        dbname='piggy' user='piggy' host='localhost' password='piggy'
        """)
    cur = conn.cursor()
    cur.execute("SELECT * FROM betrieb")
    betrieb_rows = cur.fetchall()
    print("\nShow me the databases:\n")
    cur.execute("""SELECT count(*) FROM posten""")
    countPosten = cur.fetchone()[0]
    countPostenProgress = 0
    for betrieb in betrieb_rows:
        betrieb_id = betrieb[0]
        betrieb_bid = betrieb[1]
        cur.execute("""SELECT * FROM posten WHERE betrieb_id = %s""",
                    (betrieb_id,))
        posten_rows = cur.fetchall()
        for posten in posten_rows:
            print('%s of %s  - Generating Avg Posten' % (countPostenProgress, countPosten))
            posten_id = posten[0]
            schlachthof = posten[1]
            schlachtdatum = posten[2]
            schlachtdatum_plain = schlachtdatum.strftime('%y%m%d')
            schlachtdatum_format = schlachtdatum.strftime('%d.%m.%Y')
            cur.execute("""SELECT * FROM schwein WHERE posten_id = %s""",
                        (posten_id,))
            pig_rows = cur.fetchall()
            pig_count = len(pig_rows)
            label = pig_rows[0][2]
            avg_gewicht = avg([n[3] for n in pig_rows])
            avg_mfa = avg([n[4] for n in pig_rows])
            avg_jod = avg([n[5] for n in pig_rows])
            avg_pufa = avg([n[6] for n in pig_rows])
            avg_speckmass = avg([n[7] for n in pig_rows])
            avg_fleischmass = avg([n[8] for n in pig_rows])
            magic_id = '%s_%s_%s' % (schlachthof, schlachtdatum_plain, betrieb_bid)
            data_for_csv = {
                'id': magic_id,
                'label': label,
                'schlachthof': schlachthof,
                'postenid': betrieb_bid,
                'schlachtdatum': schlachtdatum_format,
                'postensize': pig_count,
                'd_gewicht': avg_gewicht,
                'd_pufa': avg_pufa,
                'd_jodzahl': avg_jod,
                'd_mfa': avg_mfa,
                'd_speckmass': avg_speckmass,
                'd_fleischmass': avg_fleischmass
            }
            cur.execute("""SELECT * FROM konfiskate WHERE posten_id = %s""",
                        (posten_id,))
            konf_rows = cur.fetchall()
            for konfiskat in konf_rows:
                data_for_csv[konfiskat[3]] = konfiskat[2]
            print("""
            %s Betrieb %s Label %s hat am %s %s Schweine geschlachtet""" % (
                magic_id, betrieb_bid, label, schlachtdatum_format, pig_count)
            )
            '''
            print("""Gewicht: %s - PUFA: %s - Jodzahl: %s - MFA: %s -
                    Speck: %s - Fleisch: %s""" % (
                avg_gewicht,
                avg_pufa,
                avg_jod,
                avg_mfa,
                avg_speckmass,
                avg_fleischmass)
            )
            '''
            to_csv.append(data_for_csv)
            countPostenProgress += 1

except Exception as error:
    print(error)
    print("I am unable to connect to the database")
finally:
    with open('data.csv', 'w') as csvfile:
        fieldnames = [
            'id',
            'label',
            'schlachthof',
            'postenid',
            'schlachtdatum',
            'postensize',
            'd_gewicht',
            'd_pufa',
            'd_jodzahl',
            'd_mfa',
            'd_speckmass',
            'd_fleischmass',
            'Lungenabsz./lunge',
            'Lungenentz./Lunge',
            'Herzbeutelentz./Herz',
            'Div.Beanst./Zwerchf.',
            'Brustf.Entz./Lunge',
            'Div.Beanst./Leber',
            'Gelenkentz./Abschn.',
            'Absz.Schlacht/Abschn',
            'Kannibalismus',
            'Spulwurmbef.++/Leber',
            'Abszess WS / Abschn.',
            'Kopf',
            'Hautrotl./Schwarte',
            'Hautveränd./Schwarte',
            'Kochprobe',
            'alle Organe',
            'Immuno rein',
            'Herz',
            'Zwerchfell',
            'Leber',
            'Lunge',
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        to_csv_count = len(to_csv)
        count_csv_write = 0
        for row in to_csv:
            print('Writing to CSV %s of %s' % (count_csv_write, to_csv_count))
            writer.writerow(row)
            count_csv_write += 1
