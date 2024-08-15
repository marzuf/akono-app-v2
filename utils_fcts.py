from settings import *
from datetime import timedelta
import numpy as np
import dash_daq as daq
from data_processing import *

def get_var_desc(col, db):
    if db == dbTime_name:
        desc_txt = "<b>" + col + "</b> : " + \
                   showcols_settings[col]['description']

    elif db == dbDayP_name:
        desc_txt = "<b>" + col + "</b> : " + \
                   dayPcols_settings[col]['description']

    elif db == dbDayI_name:
        desc_txt = "<b>" + col + "</b> : " + \
                   dayIcols_settings[col]['description']

    else:
        return None
    return desc_txt


# récupérer toutes les colonnes de la table "donnees" sauf "time"
def get_timedata_columns():
    conn = sqlite3.connect(db_file)
    query = f"PRAGMA table_info({dbTime_name})"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return [col for col in df['name'] if col != db_timecol]

def get_daydata_columns(dayType):
    conn = sqlite3.connect(db_file)
    if dayType == "P":
        query = f"PRAGMA table_info({dbDayP_name})"
    elif dayType == "I":
        query = f"PRAGMA table_info({dbDayI_name})"
    else:
        exit(1)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return [col for col in df['name'] if col != db_daycol]

# def prep_table(dt, dt_type, currday=None):
#     if dt_type == 'time':
#         assert re.search(r'00:00$', dt.iloc[0][0])
#         assert re.search(r'23:59$',dt.iloc[dt.shape[0] - 1][0])
#
#         #SQLite utilise le format ISO 8601 pour les dates et les heures, ce qui est très pratique
#         # pour les manipulations ultérieures et les requêtes. Le format ISO 8601 est sous la forme YYYY-MM-DD HH:MM:SS.
#         dt[0] = pd.to_datetime(dt[0], format='%d.%m.%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')
#
#         #assert dt.iloc[:, nColsTime].isna().all()
#         assert dt.iloc[:, nColsTime+1].isna().all()
#         dt = dt.iloc[:, 0:nColsTime]
#
#
#         dt.columns = time_txt_cols + time_real_cols #['col' + str(i) for i in range(1, len(dt.columns) + 1)]
#
#         ### ajouter les colonnes demandées
#         dt["XT_Iin_Aac_I3116_tot"] = (dt["XT_Iin_Aac_I3116_L1"]+
#                                          dt["XT_Iin_Aac_I3116_L2"])
#
#         dt["XT_Pin_a_kW_I3119_tot"] = (dt["XT_Pin_a_kW_I3119_L1_1"]+
#                                          dt["XT_Pin_a_kW_I3119_L2_2"])
#
#         dt["XT_Pout_a_kW_I3101_tot"] = (dt["XT_Pout_a_kW_I3101_L1_1"]+
#                                          dt["XT_Pout_a_kW_I3101_L2_2"])
#
#         ### arrondir au 10ème
#         dt["BSP_Tbat_C_I7033_1"] = dt['BSP_Tbat_C_I7033_1'].round(2)
#
#     elif dt_type == "dayP":
#         assert dt.iloc[:, nColsDayP].isna().all()
#         dtm = dt.melt(id_vars=[0],
#                             value_vars=list(dt.columns)[1:nColsDayP],
#                             var_name='variable',
#                             value_name='value')
#         dtm.iloc[:, 0] = dtm.iloc[:, 0] + "_" + dtm.iloc[:, 1].astype(str)
#         dtm.drop(columns=['variable'], inplace=True)
#         dt = dtm.T
#         dt.columns = dt.iloc[0]
#         dt = dt[1:]
#         dt.insert(0, day_txt_cols[0], currday)
#     elif dt_type == "dayI":
#         assert dt.iloc[:, nColsDayI].isna().all()
#
#         dtm = dt.melt(id_vars=[0],
#                             value_vars=list(dt.columns)[1:nColsDayI],
#                             var_name='variable',
#                             value_name='value')
#         dtm.iloc[:, 0] = dtm.iloc[:, 0] + "_" + dtm.iloc[:, 1].astype(str)
#         dtm.drop(columns=['variable'], inplace=True)
#         # dt = dt.iloc[:, 0:nColsDayI].T
#         dt = dtm.T
#         dt.columns = dt.iloc[0]
#         dt = dt[1:]
#         dt.insert(0, day_txt_cols[0], currday)
#
#     else:
#         exit(1)
#     return dt
#



# lire les 10 premières lignes de la base de données
def fetch_timedata(date=None):
    conn = sqlite3.connect(db_file)
    if date:
        # query = f"SELECT * FROM {dbTime_name} WHERE DATE({db_timecol}) = '{date}' LIMIT 10"
        query = f"SELECT * FROM {dbTime_name} WHERE DATE({db_timecol}) = '{date}'"
    else:
        # query = f"SELECT * FROM {dbTime_name}"
        query = f"SELECT * FROM {dbTime_name} LIMIT 10"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# # récupérer toutes les dates disponibles dans la base de données
# def get_timedata_dates():
#     conn = sqlite3.connect(db_file)
#     query = "SELECT DISTINCT DATE("+db_timecol+") as date FROM " + dbTime_name
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df[db_timecol].tolist()
#
# # Récupérer les dates disponibles
#all_dates = get_timedata_dates()
#print(','.join(all_dates))

# def fetch_dayPdata_dates():
#     conn = sqlite3.connect(db_file)
#     query = "SELECT DISTINCT " + day_txt_cols[0] + " FROM " + dbDayP_name
#     ## assumed that same data in dayP and dayI !!!
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df[db_daycol].tolist()
#


def fetch_timedata_dates():
    conn = sqlite3.connect(db_file)
    query = "SELECT DISTINCT " + time_txt_cols[0] + " FROM " + dbTime_name
    df = pd.read_sql(query, conn)
    conn.close()
    return df[db_timecol].tolist()


def fetch_dayPdata_dates(day_type):
    conn = sqlite3.connect(db_file)
    query = "SELECT DISTINCT " + day_txt_cols[0] + " FROM " + day_type#day_type=dbDayP_name
    df = pd.read_sql(query, conn)
    conn.close()
    return df[db_daycol].tolist()


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:

        print("Try reading file : " + filename)
        file_obj = io.StringIO(decoded.decode(enc))

        try:
            prepdata_output = file2tables(file_obj)
            print(prepdata_output['error'])
            print(prepdata_output['success'])
            print(":-) data reading success for " + filename)
        except:
            print("!!! data reading failed for " + filename)

        try:
            print("... start inserting in DB " + filename)
            create_and_insert(timeData=prepdata_output['time_data'],
                              daypData=prepdata_output['dayP_data'],
                              dayiData=prepdata_output['dayI_data'])
            print(":-) inserting in DB success for " + filename)


        except:
            print("!!! inserting in DB failed for " + filename)


        print("données ajoutées à la DB")

        return html.Div([
            'Successfully uploaded and inserted: {}'.format(filename)
        ])

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing the file : ' + filename
        ])

def get_db_dropdown(id) :
    return dcc.Dropdown(
                    id=id,
                    options=[
                        {'label': 'Données minutes', 'value': dbTime_name},
                        {'label': 'Données journalières P', 'value': dbDayP_name},
                        {'label': 'Données journalières I', 'value': dbDayI_name}
                    ],
                    placeholder="Choisissez la table de données"
                )


# def parse_contents(contents, filename):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     try:
#
#         print("Try reading file : " + filename)
#
#         # day_dt = pd.read_csv(io.StringIO(decoded.decode(enc)),
#         #                      skiprows=3, nrows=60 * 24, sep=";", header=None)
#         #
#         # print("file read...")
#         #
#         # print("first date : " + day_dt.iloc[0][0])
#         # print("laste date : " + day_dt.iloc[day_dt.shape[0] - 1][0])
#         # # vérifier que la 1ère ligne est 00:00
#         # assert re.search(r'00:00$', day_dt.iloc[0][0])
#         # assert re.search(r'23:59$', day_dt.iloc[day_dt.shape[0] - 1][0])
#         #
#         # # SQLite utilise le format ISO 8601 pour les dates et les heures, ce qui est très pratique
#         # # pour les manipulations ultérieures et les requêtes. Le format ISO 8601 est sous la forme YYYY-MM-DD HH:MM:SS.
#         # day_dt[0] = pd.to_datetime(day_dt[0], format='%d.%m.%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')
#         # day_dt.columns = time_txt_cols + time_real_cols  # ['col' + str(i) for i in range(1, len(day_dt.columns) + 1)]
#         #
#         # # Connexion à la base de données SQLite
#         # conn = sqlite3.connect(db_file)
#         # c = conn.cursor()
#         # # Créer une table avec la première colonne comme datetime et les autres comme REAL (float)
#         # c.execute('''
#         #     CREATE TABLE IF NOT EXISTS ''' + dbTime_name + "(" +
#         #           ','.join([x + " TEXT" for x in time_txt_cols]) + "," +
#         #           ','.join([x + " REAL" for x in time_real_cols]) + '''
#         #     ) ''')
#         # conn.commit()
#         #
#         # # Insérer les données dans la base de données
#         # day_dt.to_sql(dbTime_name, conn, if_exists='append', index=False)
#         #
#         # # important de fermer la connexion
#         # conn.close()
#
#
#         ######## 1ère table : les données heure par heure
#         # day_dt = pd.read_csv(io.StringIO(decoded.decode(enc)),
#         #                      skiprows=nHeaderSkip, nrows=60 * 24, sep=csvSep, header=None)
#         # # day_dt = pd.read_csv(datafile, skiprows=nHeaderSkip, nrows=60*24, encoding=enc,
#         # #                  sep=csvSep,header=None)
#         # # vérifier que la 1ère ligne est 00:00
#         # assert re.search(r'00:00$', day_dt.iloc[0][0])
#         # assert re.search(r'23:59$',day_dt.iloc[day_dt.shape[0] - 1][0])
#         #
#         # #SQLite utilise le format ISO 8601 pour les dates et les heures, ce qui est très pratique
#         # # pour les manipulations ultérieures et les requêtes. Le format ISO 8601 est sous la forme YYYY-MM-DD HH:MM:SS.
#         # day_dt[0] = pd.to_datetime(day_dt[0], format='%d.%m.%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')
#         #
#         # assert day_dt.iloc[:, nColsTime].isna().all()
#         # assert day_dt.iloc[:, nColsTime+1].isna().all()
#         # day_dt = day_dt.iloc[:, 0:nColsTime]
#         #
#         #
#         # day_dt.columns = time_txt_cols + time_real_cols #['col' + str(i) for i in range(1, len(day_dt.columns) + 1)]
#
#
#         day_dt = prep_table(pd.read_csv(io.StringIO(decoded.decode(enc)),
#                              skiprows=nHeaderSkip, nrows=60 * 24, sep=csvSep, header=None),"time")
#
#         curr_day = day_dt[time_txt_cols[0]][0].split(' ')[0]
#
#         ######## 2ème table : bilan journier P
#
#         # p_dt = pd.read_csv(datafile, skiprows=nHeaderSkip + 60 * 24,
#         #                    nrows=nRowsDayP, encoding=enc,
#         #                    sep=csvSep, header=None)
#         p_dt = prep_table(pd.read_csv(io.StringIO(decoded.decode(enc)),
#                              skiprows=nHeaderSkip + 60 * 24,
#                            nrows=nRowsDayP, sep=csvSep, header=None),"dayP", curr_day)
#         # p_dt = pd.read_csv(io.StringIO(decoded.decode(enc)),
#         #                      skiprows=nHeaderSkip + 60 * 24,
#         #                    nrows=nRowsDayP, sep=csvSep, header=None)
#         #
#         # assert p_dt.iloc[:, nColsDayP].isna().all()
#         # p_dt = p_dt.iloc[:, 0:nColsDayP].T
#         # p_dt.columns = p_dt.iloc[0]
#         # p_dt = p_dt[1:]
#         # p_dt.insert(0, day_txt_cols[0], curr_day)
#
#         ######## 3ème table : bilan journier I
#
#         # i_dt = pd.read_csv(datafile, skiprows=nHeaderSkip + 60 * 24 + nRowsDayP,
#         #                    nrows=nRowsDayI, encoding=enc,
#         #                    sep=csvSep, header=None)
#         i_dt = prep_table(pd.read_csv(io.StringIO(decoded.decode(enc)),
#                              skiprows=nHeaderSkip + 60 * 24 + nRowsDayP,
#                            nrows=nRowsDayI, sep=csvSep, header=None),
#                           "dayI", curr_day)
#
#         # assert i_dt.iloc[:, nColsDayI].isna().all()
#         # i_dt = i_dt.iloc[:, 0:nColsDayI].T
#         # i_dt.columns = i_dt.iloc[0]
#         # i_dt = i_dt[1:]
#         # i_dt.insert(0, day_txt_cols[0], curr_day)
#
#         print(":-) data reading success for " + filename)
#
#         # Connexion à la base de données SQLite
#         conn = sqlite3.connect(db_file)
#         c = conn.cursor()
#
#         # Créer les tables si pas existant
#         c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbTime_name + "(" +
#                   ','.join([x + " TEXT" for x in time_txt_cols]) + ","+
#         ','.join([x + " REAL" for x in time_real_cols+time_added_cols]) + '''
#             )''')
#         c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbDayP_name + "(" +
#                   ','.join([x + " TEXT" for x in day_txt_cols]) + "," +
#                   ','.join([x + " REAL" for x in dayP_real_cols]) + '''
#               )''')
#         c.execute('''CREATE TABLE IF NOT EXISTS ''' + dbDayI_name + "(" +
#                   ','.join([x + " TEXT" for x in day_txt_cols]) + "," +
#                   ','.join([x + " REAL" for x in dayI_real_cols]) + '''
#               )''')
#         conn.commit()
#
#         # Insérer les données dans la base de données
#         day_dt.to_sql(dbTime_name, conn, if_exists='append', index=False)
#         p_dt.to_sql(dbDayP_name, conn, if_exists='append', index=False)
#         i_dt.to_sql(dbDayI_name, conn, if_exists='append', index=False)
#
#         # Il est important de fermer la connexion une fois que toutes les opérations sont complétées
#         conn.close()
#
#         print("données ajoutées à la DB")
#
#         return html.Div([
#             'Successfully uploaded and inserted: {}'.format(filename)
#         ])
#
#         # if 'csv' in filename:
#         #     # Assume that the user uploaded a CSV file
#         #     df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#         #     # Optionally, convert and clean the data as necessary
#         #     insert_data(df)
#
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing the file : ' + filename
#         ])


def get_query_extractInterval(dbname, startday, endday):
    print("start get query")
    if not endday and not startday:
        return f"SELECT * FROM {dbname}"
    if dbname==dbTime_name:
        if startday and endday:
            return f"SELECT * FROM {dbname} WHERE DATE({db_timecol}) >= DATE('{startday}') AND DATE({db_timecol}) <= DATE('{endday}')"
        elif startday and not endday:
            return f"SELECT * FROM {dbname} WHERE DATE({db_timecol}) >= DATE('{startday}')')"
        elif endday and not startday:
            return f"SELECT * FROM {dbname} WHERE DATE({db_timecol}) <= DATE('{endday}')"
        return "ERREUR"
    else :
        if startday and endday:
            return f"SELECT * FROM {dbname} WHERE {db_daycol} >= '{startday}' AND {db_daycol} <= '{endday}'"
            # if startday == endday :
            #     return f"SELECT * FROM {dbname} WHERE {db_daycol} = '{startday}'"
            # else:
            #     return f"SELECT * FROM {dbname} WHERE {db_daycol} >= '{startday}' AND {db_daycol} <= '{endday}'"
        elif startday and not endday:
            return f"SELECT * FROM {dbname} WHERE {db_daycol} >= '{startday}'"
        elif endday and not startday:
            return f"SELECT * FROM {dbname} WHERE {db_daycol} <= '{endday}'"
        return "ERREUR"


def update_layout_cols(selcols):
    if len(selcols) > 0:
        yaxis_layout['title'] = selcols[0]
    if len(selcols) > 1:
        yaxis2_layout['title'] = selcols[1]
    if len(selcols) > 2:
        yaxis3_layout['title'] = selcols[2]
    if len(selcols) > 3:
        yaxis4_layout['title'] = selcols[3]


def get_range_picker(id):
    return dcc.DatePickerRange(
        id=id,
        # date=None,
        display_format='DD.MM.YYYY',  ## prend les dates seulement dayP -> assume partt les mm !!
        min_date_allowed=min(fetch_dayPdata_dates(dbDayP_name)),
        max_date_allowed=max(fetch_dayPdata_dates(dbDayP_name)),
        disabled_days=[pd.to_datetime(date).date() for date in
                       pd.date_range(start=min(fetch_dayPdata_dates(dbDayP_name)),
                                     end=max(fetch_dayPdata_dates(dbDayP_name))).
                       difference(pd.to_datetime(fetch_dayPdata_dates(dbDayP_name)))],
        minimum_nights=0,
        style={'display': 'none'}  # Initialement caché
    )


def get_period_dropdown(id):
    return dcc.Dropdown(
        id=id,
        options=[
            {'label': 'Jour', 'value': 'stat_day'},
            {'label': 'Semaine', 'value': 'stat_week'},
            {'label': 'Mois', 'value': 'stat_month'},
            {'label': 'Année', 'value': 'stat_year'},
            {'label': 'Tout', 'value': 'stat_all'},
            {'label': 'Personnalisé', 'value': 'stat_perso'}
        ],
        value='stat_day',
        placeholder="Période"
    )


def get_startrange_date(endd, period):
    if period == 'stat_week':
        return endd - timedelta(days=7)
    elif period == "stat_day":
        return endd
    elif period == 'stat_month':
        return endd - timedelta(days=30)
    elif period == 'stat_year':
        return endd - timedelta(days=365)
    return exit(1)

def get_plotdesc(col1, col2=None, db = dbTime_name, htmlFormat=True, settingsdict=None):
    if not settingsdict:
        if db == dbTime_name:
            settingsdict = showcols_settings
        elif db == dbDayI_name:
            settingsdict = dayIcols_settings
        elif db == dbDayP_name:
            settingsdict = dayPcols_settings
        else:
            exit(1)
    print("col1 in get_plotdesc = " + col1)
    col1_txt = settingsdict[col1]['description']
    if col2 :
        col2_txt = settingsdict[col2]['description']
    if htmlFormat:
        if col2:
            if col1_txt == col2_txt :
                fig_desc = "<u>" + col1 + "</u> et  <u>" + col2 + "</u> : " + col2_txt
            else :
                col1_desc = "<u>" + col1 + "</u> : " + col1_txt
                col2_desc = "<u>" + col2 + "</u> : " + col2_txt
                fig_desc = col1_desc + "<br>" + col2_desc
        else :
            fig_desc = "<u>" + col1 + "</u> : " + col1_txt

    else :
        if col2 :
            if col1_txt == col2_txt :
                fig_desc = col1 + " et " + col2 +  " : " + col2_txt
            else :
                col1_desc = col1 + " : " + col1_txt
                col2_desc = col2 + " : " + col2_txt
                fig_desc = col1_desc + "\n" + col2_desc
        else:
            fig_desc = col1 + "  : " + col1_txt
    return fig_desc
def get_dbTime_2vargraph(df, xcol, col1, col2=None,
                         dbName = dbTime_name,
                         htmlFormat=True, withQtLines = True, stacked=False,
                         settingsdict=None):
    fig_desc = get_plotdesc(col1, col2, db = dbName,
                            htmlFormat=htmlFormat,settingsdict=settingsdict)
    fig1 = go.Figure()
    if stacked:
        fig1.add_trace(go.Scatter(x=df[xcol], y=df[col1],
                                  mode='lines', name=col1, stackgroup='one'))
        if col2 :
            fig1.add_trace(go.Scatter(x=df[xcol], y=df[col2],
                                      mode='lines', name=col2, stackgroup='one'))
    else:
        fig1.add_trace(go.Scatter(x=df[xcol], y=df[col1],
                                 mode='lines', name=col1))
        if col2:
            fig1.add_trace(go.Scatter(x=df[xcol], y=df[col2],
                                     mode='lines', name=col2, yaxis='y2'))


    if col2:
        fig1.update_layout(
            # title=f'{col1} et {col2}',
        title=f'<b>{col1}</b> et <b>{col2}</b>',
        title_font=dict(size=20),
            xaxis_title=xcol,
            yaxis_title=col1,
            yaxis2=dict(
                title=col2,
                overlaying='y',
                side='right'
            ))
        qtcols = {col1 : "limegreen", col2 : "darkgreen"}
        all_cols = [col1,col2]
    else:
        fig1.update_layout(
            # title=f'{col1} et {col2}',
        title=f'<b>{col1}</b>',
        title_font=dict(size=20),
            xaxis_title=xcol,
            yaxis_title=col1)
        qtcols = {col1: "limegreen"}
        all_cols=[col1]

    if withQtLines:
        for icol in all_cols :
            q1 = df[icol].quantile(0.1)
            q9 = df[icol].quantile(0.9)
            # fig1.add_hline(y=q1, line=dict(color='green', width=2, dash='dash'), name='0.1-Qt ' +icol)
            # fig1.add_hline(y=q9, line=dict(color='green', width=2, dash='dash'), name='0.9-Qt ' + icol)
            fig1.add_trace(go.Scatter(
                x=[df[xcol].min(), df[xcol].max()],
                y=[q1, q1],
                mode="lines",
                line=dict(color=qtcols[icol], width=2, dash='dash'),
                name=f'0.1-0.9 Qt {icol}',
                showlegend=True
            ))
            fig1.add_trace(go.Scatter(
                x=[df[xcol].min(), df[xcol].max()],
                y=[q9, q9],
                mode="lines",
                line=dict(color=qtcols[icol], width=2, dash='dash'),
                name=f'0.9-Qt {icol}',
                showlegend=False
            ))

    return [fig1, fig_desc]

    # Fonction pour trouver les points d'intersection exacts
def find_intersections(df, col1, col2):
    intersections = []
    for i in range(len(df) - 1):
        if (df[col1][i] - df[col2][i]) * (df[col1][i + 1] - df[col2][i + 1]) < 0:
            x1, x2 = df.index[i], df.index[i + 1]
            y1_1, y2_1 = df[col1][i], df[col1][i + 1]
            y1_2, y2_2 = df[col2][i], df[col2][i + 1]

            # Calcul de l'intersection linéaire
            slope_1 = (y2_1 - y1_1) / (x2 - x1).total_seconds()
            slope_2 = (y2_2 - y1_2) / (x2 - x1).total_seconds()
            intersect_seconds = (y1_2 - y1_1) / (slope_1 - slope_2)
            intersect_day = x1 + pd.Timedelta(seconds=intersect_seconds)
            intersect_value = y1_1 + slope_1 * intersect_seconds
            intersections.append((intersect_day, intersect_value))
    return intersections
def get_intersectLines_plot(data, indexcol, col1, col2):
    # Trouver les points d'intersection
    intersections = find_intersections(data, col1=col1, col2=col2)

    # Ajouter les points d'intersection aux données
    intersect_df = pd.DataFrame(intersections, columns=[indexcol, col1])
    intersect_df[col2] = intersect_df[col1]
    intersect_df.set_index(indexcol, inplace=True)

    df = pd.concat([data, intersect_df]).sort_values(indexcol)

    # Créer la figure Plotly
    fig = go.Figure()

    # Tracer les lignes
    fig.add_trace(go.Scatter(x=df.index, y=df[col1],
                             mode='lines', name=col1, line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df[col2],
                             mode='lines', name=col2, line=dict(color='red')))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[col1],
        fill=None,
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=np.where(df[col1] > df[col2], df[col2], df[col1]),
        fill='tonexty',
        mode='none',
        line=dict(color='rgba(0,0,0,0)'),
        fillcolor='rgba(0,0,255,0.3)',
        showlegend=False
    ))

    # Zone rouge où I7008_1 est au-dessus
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[col2],
        fill=None,
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=np.where(df[col1] <= df[col2], df[col1], df[col2]),
        fill='tonexty',
        mode='none',
        line=dict(color='rgba(0,0,0,0)'),
        fillcolor='rgba(255,0,0,0.3)',
        showlegend=False
    ))

    # Configuration de la mise en page
    fig.update_layout(
         title=f'<b>{col1}</b> et <b>{col2}</b>',
                xaxis_title=indexcol,
                yaxis_title='Valeur',
                showlegend=True
    )

    return fig

def get_stacked_cmpgraph(initdf, xcol, col1, col2,
                         dbName = dbTime_name,
                         commoncol ='équilibre',
                         htmlFormat=True,
                         settingsdict=None):
    df = initdf.copy()
    df[commoncol] = np.minimum(df[col1], df[col2])

    # Mise à jour des colonnes I7007_1 et I7008_1
    df[col1] = df[col1] - df[commoncol]
    df[col2] = df[col2] - df[commoncol]

    fig_desc = get_plotdesc(col1, col2, db = dbName,
                            htmlFormat=htmlFormat,settingsdict=settingsdict)
    fig1 = go.Figure()

    # fig1.add_trace(go.Scatter(x=df[xcol], y=df[commoncol],
    #                           mode='lines',  line=dict(width=0), name=commoncol, stackgroup='one'))
    # fig1.add_trace(go.Scatter(x=df[xcol], y=df[col1],
    #                           mode='lines',  line=dict(width=0), name=col1, stackgroup='one'))
    #
    # fig1.add_trace(go.Scatter(x=df[xcol], y=df[col2],
    #                           mode='lines',   line=dict(width=0),name=col2, stackgroup='one'))
    # Ajouter les barres pour 'commoncol'
    fig1.add_trace(go.Bar(x=df[xcol], y=df[commoncol],
                          name=commoncol, marker=dict(color='grey')))

    # Ajouter les barres pour col1, empilées au-dessus de commoncol
    fig1.add_trace(go.Bar(x=df[xcol], y=df[col1],
                          name=col1, base=df[commoncol], marker=dict(color='blue')))

    # Ajouter les barres pour col2, empilées au-dessus de commoncol
    fig1.add_trace(go.Bar(x=df[xcol], y=df[col2],
                          name=col2, base=df[commoncol], marker=dict(color='red')))
    fig1.update_layout(
        barmode='stack' ,
    title=f'<b>{col1}</b> et <b>{col2}</b>',
    title_font=dict(size=20),
        xaxis_title=xcol,
        yaxis_title=col1,
        yaxis2=dict(
            title=col2,
            overlaying='y',
            side='right'
        ))

    return [fig1, fig_desc]



# def insert_data(df):
#     """
#     Insert the data from the dataframe into the SQLite database.
#     """
#     conn = sqlite3.connect(db_file)
#     df.to_sql(dbTime_name, conn, if_exists='append', index=False)
#     conn.close()
#

def get_modal_dashboard(id_mainDiv, id_childDiv, id_closeBtn, id_graph):
    return html.Div(
    id=id_mainDiv,
    style={"display": "none"},  # Initialement caché
    children=[
        html.Div(
            id=id_childDiv,
            children=[
                html.Button("Fermer", id=id_closeBtn ,n_clicks=0),
                dcc.Graph(id=id_graph,config= {
                                        'scrollZoom': True  # Activer le zoom avec la molette
                                    })
            ],
            style={
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "background-color": "white",
                "padding": "20px",
                "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.5)",
                "z-index": "1000",
                "width": "80%",
                "height": "80%",
                "overflow": "auto"
            }
        ),
        html.Div(
            style={
                "position": "fixed",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "background-color": "rgba(0, 0, 0, 0.5)",
                "z-index": "999"
            }
        )
    ]
    )

def generate_header_row(timestamp):
        return html.Div(
            className="row metric-row header-row",
            children=[
                html.Div(
                    className="one column metric-row-header",
                    children=html.Div("Mesures"),
                ),
                html.Div(
                    className="two columns metric-row-header",  # Élargi pour inclure le pourcentage
                    children=html.Div("# " + timestamp + " avec valeurs"),
                ),
                html.Div(
                    className="two columns metric-row-header",  # Élargi pour inclure le pourcentage
                    children=html.Div("# " + timestamp + " sans données"),
                ),
                html.Div(
                    className="four columns metric-row-header",
                    children=html.Div("Tendance"),
                ),
                html.Div(
                    className="four columns metric-row-header",
                    children=html.Div("Dispo. des données"),
                ),
            ],
        )


def generate_summary_row(id_suffix, column_name, minutes_with_data,
                             minutes_with_missing_data, sparkline_data,
                             time_data, btn_type):
        ooc_graph_id = f"ooc_graph_{id_suffix}"

        total_minutes = minutes_with_data + minutes_with_missing_data
        percentage_with_data = (minutes_with_data / total_minutes) * 100
        percentage_missing_data = (minutes_with_missing_data / total_minutes) * 100

        minutes_with_data_text = f"{minutes_with_data} ({percentage_with_data:.0f}%)"
        minutes_with_missing_data_text = f"{minutes_with_missing_data} ({percentage_missing_data:.0f}%)"

        sparkline_figure = go.Figure(
            {
                "data": [
                    {
                        "x": time_data,
                        "y": sparkline_data,
                        "mode": "lines",
                        "line": {"color": "#f4d44d"},
                        "name": column_name,
                    }
                ],
                "layout": {
                    "margin": dict(l=0, r=0, t=0, b=0, pad=0),
                    "xaxis": dict(showline=False, showgrid=False,
                                  zeroline=False, showticklabels=False),
                    "yaxis": dict(showline=False, showgrid=False,
                                  zeroline=False, showticklabels=False),
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                },
            }
        )

        return html.Div(
            className="row metric-row",
            children=[
                html.Div(
                    className="one column metric-row-button-text",
                    children=html.Button(
                        children=column_name,
                        id={'type': btn_type, 'index': id_suffix},
                        n_clicks=0,
                    ),

                ),
                html.Div(
                    className="two columns",
                    children=html.Div(
                        children=minutes_with_data_text,
                    ),
                ),
                html.Div(
                    className="two columns",
                    children=html.Div(
                        children=minutes_with_missing_data_text,
                    ),
                ),
                html.Div(
                    className="four columns",
                    children=dcc.Graph(
                        id=f"sparkline_{id_suffix}",
                        figure=sparkline_figure,
                        style={"width": "100%", "height": "50px"},
                        config={"staticPlot": True,   'scrollZoom': True ,
                                "displayModeBar": False},
                    ),
                ),
                html.Div(
                    className="four columns",
                    children=daq.GraduatedBar(
                        id=ooc_graph_id,
                        color={
                            "ranges": {
                                "#f45060": [0, 3],
                                "#f4d44d": [3, 7],
                                "#13aa13": [7, 10],
                            }
                        },
                        showCurrentValue=False,
                        max=10,
                        value=percentage_with_data / 10,
                        size=250,
                    ),
                ),
            ],
        )



    # Fonction pour diviser une liste en N parties égales
def split_list(lst, n):
        k, m = divmod(len(lst), n)
        return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

    # Organiser les données en sections avec trois colonnes
def create_section(title, data):
        items = [html.P([html.U(col), f": {mean:.2f}"]) for col, mean in data.items()]
        columns = split_list(items, 3)
        return html.Div([
            html.H5(title, style={'font-weight': 'bold'}),
            html.Div([html.Div(col, className='col') for col in columns], className='row')
        ])
