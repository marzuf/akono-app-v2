#import pandas as pd
import os
#import re
#import sqlite3
#import datetime
#from datetime import datetime
from datetime import date
from settings import *
from data_processing import *

database_folder = "data"
os.makedirs(database_folder,exist_ok=True)

# Spécifiez le chemin vers votre fichier CSV
datafolder = '../LOG_300524'
all_files = [os.path.join(datafolder, file) for file in os.listdir(datafolder) if file.endswith('.CSV')]
all_files.sort()
datafile = all_files[0]
db_file = os.path.join(database_folder, 'akonolinga_database_demo.db')

# all_files=[datafolder+"/LG240421.CSV"]

if os.path.exists(db_file):
    newfile = db_file.replace('.db',
                              "_" + datetime.now().strftime('%Y%m%d%H%M')+"_OLD.db")
    assert not os.path.exists(newfile)
    os.rename(db_file, newfile)

logfile  = os.path.join(database_folder, f"logs_importInDB_{ date.today()}.txt")
if os.path.exists(logfile):
    os.remove(logfile)
if os.path.exists(db_file):
    os.remove(db_file)
if not os.path.exists(os.path.dirname(db_file)):
    os.makedirs(os.path.dirname(db_file))
datafile = all_files[0]

for datafile in all_files[:3]:
    print("***** " + datafile)
    try:
        print("... start reading " + datafile)
        prepdata_output = file2tables(datafile)
        print(prepdata_output['error'])
        print(prepdata_output['success'])
        print(":-) data reading success for " + datafile)
        with open(logfile, 'a') as file:
            file.write(f"***** START {os.path.basename(datafile)}\n")
            file.write(f"{os.path.basename(datafile)}\twhile reading :\n")
            file.write(prepdata_output['error'] + "\n")
            file.write(prepdata_output['success'] + "\n")

    except:
        print("!!! data reading failed for " + datafile)
        with open(logfile, 'a') as file:
            file.write(f"{os.path.basename(datafile)}\tfailure\n")
        continue
    try :
        print("... start inserting in DB " + datafile)

        # Connexion à la base de données SQLite
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Créer les tables si pas existant
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbTime_name + "(" +
                  ','.join([x + " TEXT" for x in time_txt_cols]) + ","+
        ','.join([x + " REAL" for x in time_real_cols+time_added_cols]) + '''
            )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbDayP_name + "(" +
                  ','.join([x + " TEXT" for x in day_txt_cols]) + "," +
                  ','.join([x + " REAL" for x in dayP_real_cols]) + '''
              )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbDayI_name + "(" +
                  ','.join([x + " TEXT" for x in day_txt_cols]) + "," +
                  ','.join([x + " REAL" for x in dayI_real_cols]) + '''
              )''')
        conn.commit()

        # Insérer les données dans la base de données
        prepdata_output['time_data'].to_sql(dbTime_name, conn,
                                            if_exists='append', index=False)
        prepdata_output['dayP_data'].to_sql(dbDayP_name, conn,
                                            if_exists='append', index=False)
        prepdata_output['dayI_data'].to_sql(dbDayI_name, conn,
                                            if_exists='append', index=False)

        # Il est important de fermer la connexion une fois que toutes les opérations sont complétées
        conn.close()

        print(":-) inserting in DB success for " + datafile)

        with open(logfile, 'a') as file:
            file.write(f"{os.path.basename(datafile)}\tinsert in DB success\n")

    except  :
        print("!!! inserting in DB failed for " + datafile)
        with open(logfile, 'a') as file:
            file.write(f"{os.path.basename(datafile)}\tinsert in DB failure\n")
        continue

print("output file " + db_file + " exists : " + str(os.path.exists(db_file)))

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:

        print("Try reading file : " + filename)


        day_dt = prep_table(pd.read_csv(io.StringIO(decoded.decode(enc)),
                             skiprows=nHeaderSkip, nrows=60 * 24, sep=csvSep, header=None),"time")

        curr_day = day_dt[time_txt_cols[0]][0].split(' ')[0]

        ######## 2ème table : bilan journier P

        # p_dt = pd.read_csv(datafile, skiprows=nHeaderSkip + 60 * 24,
        #                    nrows=nRowsDayP, encoding=enc,
        #                    sep=csvSep, header=None)
        p_dt = prep_table(pd.read_csv(io.StringIO(decoded.decode(enc)),
                             skiprows=nHeaderSkip + 60 * 24,
                           nrows=nRowsDayP, sep=csvSep, header=None),"dayP", curr_day)
        # p_dt = pd.read_csv(io.StringIO(decoded.decode(enc)),
        #                      skiprows=nHeaderSkip + 60 * 24,
        #                    nrows=nRowsDayP, sep=csvSep, header=None)
        #
        # assert p_dt.iloc[:, nColsDayP].isna().all()
        # p_dt = p_dt.iloc[:, 0:nColsDayP].T
        # p_dt.columns = p_dt.iloc[0]
        # p_dt = p_dt[1:]
        # p_dt.insert(0, day_txt_cols[0], curr_day)

        ######## 3ème table : bilan journier I

        # i_dt = pd.read_csv(datafile, skiprows=nHeaderSkip + 60 * 24 + nRowsDayP,
        #                    nrows=nRowsDayI, encoding=enc,
        #                    sep=csvSep, header=None)
        i_dt = prep_table(pd.read_csv(io.StringIO(decoded.decode(enc)),
                             skiprows=nHeaderSkip + 60 * 24 + nRowsDayP,
                           nrows=nRowsDayI, sep=csvSep, header=None),
                          "dayI", curr_day)

        # assert i_dt.iloc[:, nColsDayI].isna().all()
        # i_dt = i_dt.iloc[:, 0:nColsDayI].T
        # i_dt.columns = i_dt.iloc[0]
        # i_dt = i_dt[1:]
        # i_dt.insert(0, day_txt_cols[0], curr_day)

        print(":-) data reading success for " + filename)

        # Connexion à la base de données SQLite
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Créer les tables si pas existant
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbTime_name + "(" +
                  ','.join([x + " TEXT" for x in time_txt_cols]) + ","+
        ','.join([x + " REAL" for x in time_real_cols+time_added_cols]) + '''
            )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbDayP_name + "(" +
                  ','.join([x + " TEXT" for x in day_txt_cols]) + "," +
                  ','.join([x + " REAL" for x in dayP_real_cols]) + '''
              )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbDayI_name + "(" +
                  ','.join([x + " TEXT" for x in day_txt_cols]) + "," +
                  ','.join([x + " REAL" for x in dayI_real_cols]) + '''
              )''')
        conn.commit()

        # Insérer les données dans la base de données
        day_dt.to_sql(dbTime_name, conn, if_exists='append', index=False)
        p_dt.to_sql(dbDayP_name, conn, if_exists='append', index=False)
        i_dt.to_sql(dbDayI_name, conn, if_exists='append', index=False)

        # Il est important de fermer la connexion une fois que toutes les opérations sont complétées
        conn.close()

        print("données ajoutées à la DB")

        return html.Div([
            'Successfully uploaded and inserted: {}'.format(filename)
        ])

        # if 'csv' in filename:
        #     # Assume that the user uploaded a CSV file
        #     df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        #     # Optionally, convert and clean the data as necessary
        #     insert_data(df)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing the file : ' + filename
        ])
