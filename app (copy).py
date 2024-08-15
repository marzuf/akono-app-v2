import dash_daq as daq
from settings import *
from utils_fcts import *
import plotly.express as px
from datetime import timedelta
import pandas as pd
import numpy as np
from dash import dash_table
import pandas as pd
from datetime import datetime, timedelta
from app_settings import *
from plotly.subplots import make_subplots
from dash.dependencies import ALL


from callbacks.common_callbacks import register_callbacks as register_dashboard_common


##################################### TODO IN PROCESS : dashboard
# https://dash.gallery/dash-manufacture-spc-dashboard/
# https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-manufacture-spc-dashboard/app.py


## prend les dates seulement dayP -> assume partt les mm !!

dayPdata_columns = get_daydata_columns("P")
dayIdata_columns = get_daydata_columns("I")
timedata_columns = get_timedata_columns()
timecols2show = [x for x in timedata_columns if not showcols_settings[x] == "NA"]
dayPcols2show = [x for x in dayPdata_columns if not x == db_daycol]
dayIcols2show = [x for x in dayIdata_columns if not x == db_daycol]

# Initialiser l'application Dash avec suppression des exceptions de callback
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
                suppress_callback_exceptions=True)

register_dashboard_common(app)

# Définir la mise en page de l'application

all_confirm_dialogs = [dcc.ConfirmDialog(id=x,message='')
                       for x in [
                                 'confirm-dialog-stat',
                                 'confirm-dialog-statgraph',
                                 'confirm-dialog-evotime',
                                 'confirm-dialog-evoDayIDBgraph',
                                 'confirm-dialog-evoTimeDBgraph',
                                 'confirm-dialog-evoDayPDBgraph',
                                 'confirm-dialog-analyseGraph',
                                 'confirm-dialog-subxtender',
                                'confirm-dialog-subvariotrack',
                                    'confirm-dialog-subbsp',
                                        'confirm-dialog-subbat',
'confirm-dialog-subminutes',
                    'confirm-dialog-subdayI'
                                 ]]

all_maxvar_dialogs = [dcc.ConfirmDialog(id=x,message=popupmsg_maxvar)
                       for x in ['confirm-dialog',
                                 'confirm-dialog-daydataP',
                                 'confirm-dialog-daydataI',
                                 ]]
all_range_pickers = [get_range_picker(x) for x in [
                    'range-picker-stat',
                        'range-picker-evotime',
                        'range-picker-analyseGraph',
                            'range-picker-subxtender',
                                        'range-picker-subvariotrack',
                                     'range-picker-subbsp',
                                'range-picker-subbat',
'range-picker-subminutes',
'range-picker-subdayI'
                            ]]




app.layout = html.Div([
    dcc.Tabs(id="tabs-example", value='tab-dashboard', children=[  # value ici définit l'onglet par défaut
        dcc.Tab(label='Dashboard', value='tab-dashboard',
                className='mytab', selected_className='mytab-slctd',
                children=[
                    dcc.Tabs(id="subtabs-dashboard", value='subtab-dayIdata', children=[
                        dcc.Tab(label='Données minutes', value='subtab-minutesdata',
                                className='mysubtab', selected_className='mysubtab-slctd'),
                        dcc.Tab(label='Données journalières', value='subtab-dayIdata',
                                className='mysubtab', selected_className='mysubtab-slctd'),

                    ]),                        dcc.Store(id='store-summary-minutes'),
                        dcc.Store(id='store-dbTime_df'),
                        dcc.Store(id='store-summary-dayI'),
                        dcc.Store(id='store-dbDayI_df')]),

        dcc.Tab(label='Evolution temporelle', value='tab-evotime',
                className='mytab', selected_className='mytab-slctd'),
        dcc.Tab(label='Statistiques', value='tab-stat',
                className='mytab', selected_className='mytab-slctd'),
        dcc.Tab(label='Analyse (graphes)', value='tab-analyseGraph',
                className='mytab', selected_className='mytab-slctd'),
        dcc.Tab(label='Par appareil', value='tab-appareils',
                className='mytab', selected_className='mytab-slctd',
             children=[
            dcc.Tabs(id="subtabs-appareils", value='subtab-bsp', children=[
                dcc.Tab(label='BSP', value='subtab-bsp',
                        className='mysubtab', selected_className='mysubtab-slctd'),
                dcc.Tab(label='VarioTrack', value='subtab-variotrack',
                            className='mysubtab', selected_className='mysubtab-slctd'),
                dcc.Tab(label='Xtender', value='subtab-xtender',
                                className='mysubtab', selected_className='mysubtab-slctd')
            ])]),
        dcc.Tab(label='Par fonction', value='tab-fonctions',
                className='mytab', selected_className='mytab-slctd',
                children=[
                    dcc.Tabs(id="subtabs-fonctions", value='subtab-batterie', children=[
                        dcc.Tab(label='Batterie', value='subtab-batterie',
                                className='mysubtab', selected_className='mysubtab-slctd')
                    ])]),
        dcc.Tab(label='Gérer les données', value='tab-updateDB',
                className='mytab', selected_className='mytab-slctd'),
        dcc.Tab(label='Base de données', value='tab-showDB',
                className='mytab', selected_className='mytab-slctd')
    ]),
    dcc.DatePickerSingle(
        id='date-picker-dbdata',
        date=None,
        display_format='DD.MM.YYYY',
        min_date_allowed=min(fetch_timedata_dates()),
        max_date_allowed=max(fetch_timedata_dates()),
        disabled_days=[pd.to_datetime(date).date() for date in
                       pd.date_range(start=min(fetch_timedata_dates()),
                                     end=max(fetch_timedata_dates())).
                       difference(pd.to_datetime(fetch_timedata_dates()))],
        style={'display': 'none'}  # Initialement caché
        # attention : pd.date_range(...).retourne un DatetimeIndex
        # pd.to_datetime pour convertir all_dates aussi en DatetimeIndex pr comparer
    )] +
                      all_range_pickers +
                      all_maxvar_dialogs +
                      all_confirm_dialogs+
    [html.Div(id='tabs-content')]

)

##################################################################################
######################################### CALL BACK tab analyse GRAPH
##################################################################################
@app.callback(
    [Output('confirm-dialog-daydataP', 'displayed'),
     Output('dayPdata-column-dropdown', 'value')],
    [Input('dayPdata-column-dropdown', 'value')]
)
def limit_selection_dayPdata(selected_columns):
    if len(selected_columns) > maxTimePlotVar:
        return True, selected_columns[:maxTimePlotVar]  # Afficher la pop-up et limiter la sélection à 2
    return False, selected_columns  # Ne pas afficher la pop-up
@app.callback(
    [Output('confirm-dialog-daydataI', 'displayed'),
     Output('dayIdata-column-dropdown', 'value')],
    [Input('dayIdata-column-dropdown', 'value')]
)
def limit_selection_dayPdata(selected_columns):
    if len(selected_columns) > maxTimePlotVar:
        return True, selected_columns[:maxTimePlotVar]  # Afficher la pop-up et limiter la sélection à 2
    return False, selected_columns  # Ne pas afficher la pop-up
@app.callback(
    Output('dayPdata-column-description', 'children'),
    [Input('dayPdata-column-dropdown', 'value')]
)
def update_dayP_description(selected_columns):
    if selected_columns:
        desc_txt = '<br>'.join(["<b>" + selcol + "</b> : " + \
                                dayPcols_settings[selcol]['description']
                                for selcol in selected_columns])
        return html.Div([dcc.Markdown(desc_txt,
                                      dangerously_allow_html=True)])
    return html.P('No column selected')
@app.callback(
    Output('dayIdata-column-description', 'children'),
    [Input('dayIdata-column-dropdown', 'value')]
)
def update_dayI_description(selected_columns):
    if selected_columns:
        # print(';'.join(showcols_settings.keys()))
        desc_txt = '<br>'.join(["<b>" + selcol + "</b> : " + \
                                dayIcols_settings[selcol]['description']
                                for selcol in selected_columns])
        return html.Div([dcc.Markdown(desc_txt,
                                      dangerously_allow_html=True)])
    return html.P('No column selected')
@app.callback(
    [
        Output('analyseGraph-pie-chart-global', 'children'),
        Output('analyseGraph-pie-chart-day', 'children'),
        Output('analyseGraph-pie-chart-night', 'children'),
        Output('analyseGraph-period-subtit', 'children'),
        Output('analyseGraph-pie-chart-tit', 'children'),
        Output('analyseGraph-tempbat-barplot', 'children'),
        Output('confirm-dialog-analyseGraph', 'displayed'),
        Output('confirm-dialog-analyseGraph', 'message')
    ],
    [Input('show-asGraph-btn', 'n_clicks')],
    [
        State('asGraphPeriod-dropdown', 'value'),
        State('asL-dropdown', 'value'),
        State('range-picker-analyseGraph', 'start_date'),
        State('range-picker-analyseGraph', 'end_date')
    ]
)
def update_analyse_pie_chart(n_clicks, selected_period, selected_L,
                             start_date, end_date):
    if n_clicks is None or n_clicks == 0:
        return [""] * 6 + [False, ""]
    if selected_period != 'stat_all' and (not start_date or not end_date):
        return [""] * 6 + [True, "Sélectionnez une période"]
    if selected_period != 'stat_all':
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return [""] * 6 + [True, "Choisir une seule date"]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return [""] * 6 + [True, "Choisir une date différente"]
    conn = sqlite3.connect(db_file)
    if selected_period == 'stat_all':
        query = f"SELECT * FROM {dbTime_name}"
        interval_txt = " Toutes les données"
    else:
        query = get_query_extractInterval(dbTime_name, start_date, end_date)
        interval_txt = ("Période : " + start_date.strftime('%d/%m/%Y') + " - " +
                        end_date.strftime('%d/%m/%Y'))
    df = pd.read_sql_query(query, conn)
    conn.close()
    if selected_L == "as_L1":
        df['calc_col'] = df[xtfincol + '_L1']
        calcol_txt = xtfincol + '_L1'
    elif selected_L == "as_L2":
        df['calc_col'] = df[xtfincol + '_L2']
        calcol_txt = xtfincol + '_L2'
    elif selected_L == "as_both":
        df['calc_col'] = df[xtfincol + '_L1'] + df[xtfincol + '_L2']
        calcol_txt = xtfincol + '_L1' + "+" + xtfincol + '_L2'
    else:
        exit(1)
    pie_chart_tit = html.Div([
        html.H4("Répartition fréquences (" + calcol_txt + ")"),
        html.H6("(génératrice si > " + str(xtfin_genThresh) +
                " ; ni gén. ni rés. si = " + str(xtfin_nosource) + ")")

    ])
    period_subtit = html.H6(interval_txt)
    df['freq_type'] = np.where(df['calc_col'] > xtfin_genThresh,
                               "génératrice", "réseau")
    df.loc[df['calc_col'] == xtfin_nosource, 'freq_type'] = "ni gén. ni rés."
    # ******* GLOBAL
    freq_counts = df['freq_type'].value_counts(normalize=True) * 100
    fig_global = px.pie(
        names=freq_counts.index,
        values=freq_counts.values,
        # title="Répartition des fréquences " + interval_txt + " (Global)"
        title="Global"
    )
    # ******* JOUR
    df_day = df[(pd.to_datetime(df[db_timecol]).dt.time >=
                 datetime.strptime("08:00", "%H:%M").time()) &
                (pd.to_datetime(df[db_timecol]).dt.time <
                 datetime.strptime("18:00", "%H:%M").time())]
    freq_counts_day = df_day['freq_type'].value_counts(normalize=True) * 100
    fig_day = px.pie(
        names=freq_counts_day.index,
        values=freq_counts_day.values,
        # title="Répartition des fréquences "  + interval_txt + " (Jour : 08:00 - 18:00)",
        title="Jour : 08:00 - 18:00"
    )
    # ******* NUIT
    df_night = df[(pd.to_datetime(df[db_timecol]).dt.time >=
                       datetime.strptime("18:00", "%H:%M").time()) |
                  (pd.to_datetime(df[db_timecol]).dt.time <
                    datetime.strptime("08:00", "%H:%M").time())]
    assert df.shape[0] == (df_night.shape[0] + df_day.shape[0])
    freq_counts_night = df_night['freq_type'].value_counts(normalize=True) * 100
    fig_night = px.pie(
        names=freq_counts_night.index,
        values=freq_counts_night.values,
        # title="Répartition des fréquences " +  interval_txt + " (Nuit : 18:00 - 08:00)"
        title="Nuit : 18:00 - 08:00"
    )
    #### calcul des moyennes températures batterie
    barplot_data = pd.DataFrame({
        'Période': ['Global', 'Jour', 'Nuit'],
        'Moyenne Temp': [df[tempTbatcol].mean(),
                         df_day[tempTbatcol].mean(),
                         df_night[tempTbatcol].mean()]
    })
    fig_barplot = px.bar(barplot_data, x='Période', y='Moyenne Temp', title='Moyenne de TempTbatcol')
    return [dcc.Graph(figure=fig_global),
            dcc.Graph(figure=fig_day),
            dcc.Graph(figure=fig_night),
            period_subtit,
            pie_chart_tit,
            dcc.Graph(figure=fig_barplot),
            False, ""]



################################################################################################
################################ CALLBACKS - TAB EVOTIME - VISUALISATIONS   tab-evotime
################################################################################################


@app.callback(
    Output('evotimeTimeDB-graph-varinfo', 'children'),
    [Input('evotimeTimeDB-graph-col', 'value')]
)
def update_evotimevarinfo(selected_col, selected_db=dbTime_name):
    if selected_col and selected_db:
        desc_txt = get_var_desc(selected_col, selected_db)
    else:
        return None
    return html.Div([dcc.Markdown(desc_txt,
                                  dangerously_allow_html=True)])

# Callback pour afficher le graphique en fonction de la sélection :
@app.callback(
    [Output('evotimeTimeDB-graph', 'figure'),
     Output('confirm-dialog-evoTimeDBgraph', 'displayed'),
     Output('confirm-dialog-evoTimeDBgraph', 'message'),
     Output('evotime-range-info', 'children')],
    [Input('show-evotimeTimeDBgraph-btn', 'n_clicks')],
    [
        State('evotimeTimeDB-graph-col', 'value'),
        State('evotimeTimeDB-graph-viz', 'value'),
        State('range-picker-evotime', 'start_date'),
        State('range-picker-evotime', 'end_date'),
        State('evotimeperiod-dropdown', 'value')]
)
def display_evoTimeDB_graph(n_clicks, selected_col, selected_viz,
                            start_date, end_date, selected_period):
    selected_db = dbTime_name
    if n_clicks is None or n_clicks == 0:
        return [go.Figure(), False, "", ""]
    if (not selected_db or not selected_col or not selected_viz) and (not start_date or not end_date):
        return [go.Figure(), True, "Sélectionnez des données et une période", "Sélectionnez des données et une période"]

    if not selected_db or not selected_col or not selected_viz:
        return [go.Figure(), True, "Sélectionnez des données","Sélectionnez des données"]

    if selected_period == "stat_all":
        date_info = f"Toutes les données disponibles"
        query = get_query_extractInterval(selected_db, None, None)
    else :
        if not start_date or not end_date:
            return [go.Figure(), True, "Sélectionnez une période", "Sélectionnez une période"]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date", ""]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return [go.Figure(), True, "Choisir une date différente", "Choisir une date différente"]

        date_info = f"Données du {start_date} au {end_date}"
        query = get_query_extractInterval(selected_db, start_date, end_date)

    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query, conn)
    conn.close()

    if selected_db == dbTime_name:
        xcol = db_timecol
    else:
        xcol = db_daycol
        if selected_db == dbDayI_name:
            for col in dayI_cols:
                df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)
    if selected_db == dbTime_name and selected_viz == 'boxplot':
        df['date'] = pd.to_datetime(df[xcol]).dt.date
        fig = px.box(df, x='date', y=selected_col, title=f'{selected_col} Box Plot par jour')
    else:
        if selected_viz == 'lineplot':
            shapes = []
            threshold = 56
            above_threshold = df[df[selected_col] > threshold]

            if not above_threshold.empty:
                segments = []
                start_idx = None

                for i in range(len(df)):
                    if df.iloc[i][selected_col] > threshold:
                        if start_idx is None:
                            start_idx = i
                    else:
                        if start_idx is not None:
                            segments.append((start_idx, i - 1))
                            start_idx = None
                if start_idx is not None:
                    segments.append((start_idx, len(df) - 1))
                for segment in segments:
                    shapes.append({
                        'type': 'rect',
                        'xref': 'x',
                        'yref': 'paper',
                        'x0': df.iloc[segment[0]][xcol],
                        'y0': 0,
                        'x1': df.iloc[segment[1]][xcol],
                        'y1': 1,
                        'fillcolor': 'red',
                        'opacity': 0.3,
                        'line': {
                            'width': 0,
                        }
                    })

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df[xcol], y=df[selected_col],
                                     mode='lines', name=f'{selected_col} Line Plot',
                                     line=dict(color='blue')))

            fig.update_layout(shapes=shapes, title=f'{selected_col} Line Plot')
        elif selected_viz == 'barplot':
            fig = px.bar(df, x=xcol, y=selected_col, title=f'{selected_col} Bar Plot')
        elif selected_viz == 'boxplot':
            fig = px.box(df, x=xcol, y=selected_col, title=f'{selected_col} Box Plot')
    if (selected_db == dbTime_name and selected_viz == 'boxplot') or (
            selected_db == dbDayP_name or selected_db == dbDayI_name):
        fig.update_layout(xaxis=dict(title='Date', tickformat='%Y-%m-%d', dtick="D1"))
    return [fig, False, "", date_info]


############################### ###############################
############################### CALL BACKS STAT tab-stat
############################### ###############################

@app.callback(
    [
        Output('stat-range-info', 'children'),
        Output('confirm-dialog-stat', 'displayed'),
        Output('confirm-dialog-stat', 'message'),
        Output('stat-means-info', 'children')
    ],
    [Input('show-stat-btn', 'n_clicks')],
    [
        State('statperiod-dropdown', 'value'),
        State('range-picker-stat', 'start_date'),
        State('range-picker-stat', 'end_date')
    ]
)
def update_stat_values(n_clicks, selected_period, start_date, end_date):
    if n_clicks is None or n_clicks == 0:
        return ["", False, "", ""]
    if selected_period == "stat_all":
        query_time = get_query_extractInterval(dbTime_name, None, None)
    else :
        if not start_date or not end_date:
            return ["", True, "Sélectionnez une période", ""]
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # query_time = f"SELECT * FROM {dbTime_name} WHERE DATE({db_timecol}) >= DATE('{start_date}') AND DATE({db_timecol}) <= DATE('{end_date}')"
        query_time = get_query_extractInterval(dbTime_name, start_date, end_date)

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date", ""]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return ["ERREUR", True, "Choisir une date différente", ""]

    # Extraire les données pour l'intervalle sélectionné
    conn = sqlite3.connect(db_file)

    df_time = pd.read_sql_query(query_time, conn)

    query_dayP = get_query_extractInterval(dbDayP_name, start_date, end_date)
    df_dayP = pd.read_sql_query(query_dayP, conn)

    query_dayI = get_query_extractInterval(dbDayI_name, start_date, end_date)
    df_dayI = pd.read_sql_query(query_dayI, conn)

    conn.close()

    means_html = html.Div([
        create_section("Moyennes des données minutes",
                       df_time.mean(numeric_only=True)),
        create_section("Moyennes des données journalières (P)",
                       df_dayP.mean(numeric_only=True)),
        create_section("Moyennes des données journalières (I)",
                       df_dayI.mean(numeric_only=True))
    ])
    date_info = f"Données du {start_date} au {end_date}"
    return [date_info, False, "", means_html]

################################ CALLBACKS - TAB STAT - VISUALISATION
# Callback pour mettre à jour les colonnes disponibles en fonction de la table sélectionnée :
@app.callback(
    Output('tabstatgraph-col', 'options'),
    [Input('tabstatgraph-db', 'value')]
)
def update_stat_columns(selected_db):
    if selected_db:
        if selected_db == dbTime_name:
            columns = [{'label': col, 'value': col} for col in timecols2show]
        elif selected_db == dbDayP_name:
            columns = [{'label': col, 'value': col} for col in dayPcols2show]
        elif selected_db == dbDayI_name:
            columns = [{'label': col, 'value': col} for col in dayI_cols + dayIcols2show]
        return columns
    return []


# Callback pour mettre à jour texte info var

@app.callback(
    Output('tabstatgraph-varinfo', 'children'),
    [Input('tabstatgraph-col', 'value')],
    [State('tabstatgraph-db', 'value')]
)
def update_statvarinfo(selected_col, selected_db):
    if selected_col and selected_db:
        if selected_db == dbTime_name:
            desc_txt = "<b>" + selected_col + "</b> : " + \
                       showcols_settings[selected_col]['description']
        elif selected_db == dbDayP_name:
            desc_txt = "<b>" + selected_col + "</b> : " + \
                       dayPcols_settings[selected_col]['description']
        elif selected_db == dbDayI_name:
            desc_txt = "<b>" + selected_col + "</b> : " + \
                       dayIcols_settings[selected_col]['description']
        else:
            return None
        return html.Div([dcc.Markdown(desc_txt,
                                      dangerously_allow_html=True)])
    return None

# Callback pour afficher le graphique en fonction de la sélection :
@app.callback(
    [Output('stat-graph', 'figure'),
     Output('confirm-dialog-statgraph', 'displayed'),
     Output('confirm-dialog-statgraph', 'message')],
    [Input('show-statgraph-btn', 'n_clicks')],
    [State('tabstatgraph-db', 'value'),
     State('tabstatgraph-col', 'value'),
     State('tabstatgraph-viz', 'value'),
State('statperiod-dropdown', 'value'),
     State('range-picker-stat', 'start_date'),
     State('range-picker-stat', 'end_date')]
)
def display_stat_graph(n_clicks, selected_db, selected_col, selected_viz,
                  selected_period, start_date, end_date):
    if n_clicks is None or n_clicks == 0:
        return [go.Figure(), False, ""]
    if selected_period == "stat_all":
        query_time = get_query_extractInterval(dbTime_name, None, None)
    else :
        if ((not selected_db or not selected_col or not selected_viz) and
                        (not start_date or not end_date)):
            return [go.Figure(), True, "Sélectionnez des données et une période"]

        if not selected_db or not selected_col or not selected_viz:
            return [go.Figure(), True, "Sélectionnez des données"]

        if not start_date or not end_date:
            return [go.Figure(), True, "Sélectionnez une période"]

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return [go.Figure(), True, "Choisir une seule date"]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return [go.Figure(), True, "Choisir une date différente"]

        query_time = get_query_extractInterval(selected_db, start_date, end_date)

    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query_time, conn)
    conn.close()

    if selected_db == dbTime_name:
        xcol = db_timecol
    else:
        xcol = db_daycol
        if selected_db == dbDayI_name:
            for col in dayI_cols:
                df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)

    if selected_db == dbTime_name and selected_viz == 'boxplot':
        df['date'] = pd.to_datetime(df[xcol]).dt.date
        fig = px.box(df, x='date', y=selected_col, title=f'{selected_col} Box Plot par jour')
    else:
        if selected_viz == 'lineplot':
            fig = px.line(df, x=xcol, y=selected_col, title=f'{selected_col} Line Plot')
        elif selected_viz == 'barplot':
            fig = px.bar(df, x=xcol, y=selected_col, title=f'{selected_col} Bar Plot')
        elif selected_viz == 'boxplot':
            fig = px.box(df, x=xcol, y=selected_col, title=f'{selected_col} Box Plot')

    if (selected_db == dbTime_name and selected_viz == 'boxplot') or (
            selected_db == dbDayP_name or selected_db == dbDayI_name):
        fig.update_layout(xaxis=dict(title='Date', tickformat='%Y-%m-%d', dtick="D1"))

    fig.update_layout(xaxis=dict(
        title='Date TEST SCROLL',
        rangeslider=dict(visible=True),  # Add a range slider to the x-axis
        type="date"  # Set the x-axis type to date
    ))

    # # Configuration pour permettre le zoom avec la molette de la souris
    # graph_config = {
    #     'scrollZoom': True  # Activer le zoom avec la molette
    # }
    #
    # # Créer le composant dcc.Graph avec la figure et la configuration
    # dcc.Graph(
    #     id='graph',
    #     figure=fig,
    #     config=graph_config  # Passer la configuration à dcc.Graph
    # )

    return [fig, False, ""]

@app.callback(
    Output('tabstatgraph-viz', 'options'),
    [Input('tabstatgraph-db', 'value')]
)
def update_viz_options(selected_db):
    if selected_db == dbTime_name:
        return [
            {'label': 'Line Plot', 'value': 'lineplot'},
            {'label': 'Bar Plot', 'value': 'barplot'},
            {'label': 'Box Plot', 'value': 'boxplot'}
        ]
    else:
        return [
            {'label': 'Line Plot', 'value': 'lineplot'},
            {'label': 'Bar Plot', 'value': 'barplot'}
        ]

################################################################################################
################################ CALLBACKS SUBTAB DAHSBOARD
################################################################################################
# Définir les callbacks pour mettre à jour le contenu des sous-onglets
@app.callback(Output('subtabs-dashboard-content', 'children'),
              [Input('subtabs-dashboard', 'value')])
def render_subtab_dashboard_content(subtab):
    if subtab == 'subtab-minutesdata':
        return html.Div([
            html.H4("Données minutes"),
            get_period_dropdown('subminutesdashb-period-dropdown'),
            html.Button('Afficher', id='show-minutesdashb-btn', n_clicks=0),
            html.Div(id='subminutesdashb-range-info', style={'marginTop': '20px'}),
            html.Div(id='subtab-minutesdashb-content', style={'marginTop': '20px'}),
            get_modal_dashboard(id_mainDiv="graph-modal-minutesdashb",
                                id_childDiv="modal-content-minutesdashb",
                                id_closeBtn="close-modal-minutesdashb",
                                id_graph="modal-graph-minutesdashb")
        ])
    elif subtab == 'subtab-dayIdata':
        return html.Div([
            html.H4("Données journalières I"),
            get_period_dropdown('subdayIdashb-period-dropdown'),
            html.Button('Afficher', id='show-dayIdashb-btn', n_clicks=0),
            html.Div(id='subdayIdashb-range-info', style={'marginTop': '20px'}),
            html.Div(id='subtab-dayIdashb-content', style={'marginTop': '20px'}),
            get_modal_dashboard(id_mainDiv="graph-modal-dayIdashb",
                                id_childDiv="modal-content-dayIdashb",
                                id_closeBtn="close-modal-dayIdashb",
                                id_graph="modal-graph-dayIdashb")

        ])

################################################################################################
################################ CALLBACKS SUBTAB PAR APPAREIL
################################################################################################
# Définir les callbacks pour mettre à jour le contenu des sous-onglets
@app.callback(Output('subtabs-appareils-content', 'children'),
              [Input('subtabs-appareils', 'value')])
def render_subtab_appareils_content(subtab):
    if subtab == 'subtab-variotrack':
        return html.Div([
            html.H4("Données de l'appareil VarioTrack"),
            get_period_dropdown('subvariotrack-period-dropdown'),
            html.Button('Afficher', id='show-variotrack-btn', n_clicks=0),
            html.Div(id='subvariotrack-range-info', style={'marginTop': '20px'}),
            html.Div(id='subtab-variotrack-content', style={'marginTop': '20px'}),
        ])
    elif subtab == 'subtab-xtender':
        return html.Div([
            html.H4("Données de l'appareil XTender"),
            get_period_dropdown('subxtender-period-dropdown'),
            html.Button('Afficher', id='show-xtender-btn', n_clicks=0),
            html.Div(id='subxtender-range-info', style={'marginTop': '20px'}),
            html.Div(id='subtab-xtender-content', style={'marginTop': '20px'}),
        ])
    elif subtab == 'subtab-bsp':
        return html.Div([
            html.H4("Données de l'appareil BSP"),
            get_period_dropdown('subbsp-period-dropdown'),
            html.Button('Afficher', id='show-bsp-btn', n_clicks=0),
            html.Div(id='subbsp-range-info', style={'marginTop': '20px'}),
            html.Div(id='subtab-bsp-content', style={'marginTop': '20px'}),
        ])



################################################################################################
################################ CALLBACKS SUBTAB PAR APPAREIL
################################################################################################
# Définir les callbacks pour mettre à jour le contenu des sous-onglets
@app.callback(Output('subtabs-fonctions-content', 'children'),
              [Input('subtabs-fonctions', 'value')])
def render_subtab_fonctions_content(subtab):
    if subtab == 'subtab-batterie':
        return html.Div([
            html.H4("Données sur la batterie"),
            get_period_dropdown('subbat-period-dropdown'),
            html.Button('Afficher', id='show-batterie-btn', n_clicks=0),
            html.Div(id='subbat-range-info', style={'marginTop': '20px'}),
            html.Div(id='subtab-batterie-content', style={'marginTop': '20px'}),
        ])


######################################################################
# NEW DASHBOARD minutesdata
######################################################################



@app.callback(
    [Output('graph-modal-minutesdashb', 'style'),
     Output('modal-graph-minutesdashb', 'figure')],
    [Input({'type': 'dynamic-button', 'index': ALL}, 'n_clicks'),
     Input('close-modal-minutesdashb', 'n_clicks')],
    [State('graph-modal-minutesdashb', 'style'),
     State('store-summary-minutes', 'data'),
     State('store-dbTime_df', 'data')]
)
def toggle_modal_minutes(button_clicks, close_click, modal_style, summary_data_minutes, dbTime_df_data):
    print("BUTTON CLICKED******\n")

    ctx = dash.callback_context

    if not ctx.triggered:
        return {"display": "none"}, go.Figure()

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if 'dynamic-button' in triggered_id:
        # Trouver l'index du bouton qui a été cliqué
        triggered_index = eval(triggered_id)['index']
        column_name = summary_data_minutes[triggered_index]['Column']

        df = pd.DataFrame(dbTime_df_data)
        fig = go.Figure(
            data=[
                go.Scatter(x=df['time'], y=df[column_name], mode='lines')
            ],
            layout=go.Layout(
                title=f"Courbe de {column_name} en fonction du temps",
                xaxis_title="Time",
                yaxis_title=column_name
            )
        )
        return {"display": "block"}, fig

    elif 'close-modal-minutesdashb' in triggered_id:
        return {"display": "none"}, go.Figure()

    return {"display": "none"}, go.Figure()

@app.callback(
    [Output('subtab-minutesdashb-content', 'children'),
     Output('confirm-dialog-subminutes', 'displayed'),
     Output('confirm-dialog-subminutes', 'message'),
     Output('subminutesdashb-range-info', 'children'),
     Output('store-summary-minutes', 'data'),
     Output('store-dbTime_df', 'data')
     ],
    [Input('show-minutesdashb-btn', 'n_clicks')],
    [
     State('range-picker-subminutes', 'start_date'),
     State('range-picker-subminutes', 'end_date'),
        State('subminutesdashb-period-dropdown', 'value')]
)
def display_minutesdata_dashboard(n_clicks,start_date, end_date, selected_period):
    selected_db = dbTime_name
    selected_col = "FOO"
    if n_clicks is None or n_clicks == 0:
        return ["", False, "", "", None, None]
    if selected_period == "stat_all":
        query = get_query_extractInterval(selected_db, None, None)
    else :
        if (not selected_db or not selected_col) and (not start_date or not end_date):
            return ["", True, "Sélectionnez des données et une période", "",None, None]
        if not selected_db or not selected_col :
            return [ "", True, "Sélectionnez des données", "",None, None]
        if not start_date or not end_date:
            return ["", True, "Sélectionnez une période", "",None, None]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date de début et fin", "",None, None]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return ["ERREUR", True, "Choisir une date différente", "",None, None]

        query = get_query_extractInterval(selected_db, start_date, end_date)

    date_info = f"Données du {start_date} au {end_date}"

    conn = sqlite3.connect(db_file)

    dbTime_df = pd.read_sql_query(query, conn)
    conn.close()

    dbTime_df[db_timecol] = pd.to_datetime(dbTime_df[db_timecol])

    # Définir la plage complète de temps en minutes
    ## pour avoir de start date 00 et end date 2359
    start_date_minute = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_minute = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(minutes=1)
    all_minutes = pd.date_range(start=start_date_minute,
                                end=end_date_minute, freq='min')
    missing_times = all_minutes.difference(dbTime_df[db_timecol])
    if not missing_times.empty:
        missing_data = pd.DataFrame(missing_times, columns=[db_timecol])
        dbTime_df = pd.concat([dbTime_df, missing_data],
                              ignore_index=True).sort_values(by=db_timecol)
    ## assurer que c'est bien la colonne 'time' en position 0
    assert dbTime_df.columns[0] == db_timecol
    summary = pd.DataFrame({
        'Column': dbTime_df.columns[1:],  # Exclure la colonne 'time'
        'Minutes with Data': dbTime_df.iloc[:, 1:].notna().sum().values,
        'Minutes with Missing Data': (dbTime_df.iloc[:, 1:].isna().sum() +
                                      len(missing_times)).values
    })
    summary['Percentage Data'] = summary['Minutes with Data'] / (
                summary['Minutes with Data'] + summary['Minutes with Missing Data']) * 100

    summary_data_minutes = summary.to_dict('records')
    dbTime_df_data = dbTime_df.to_dict('records')

    dbTime_df[db_timecol] = pd.to_datetime(dbTime_df[db_timecol])
    time_data = dbTime_df[db_timecol]

    div_container = [generate_header_row("minutes")]
    for i, row in summary.iterrows():
        sparkline_data = dbTime_df[row['Column']]
        div_container.append(
            generate_summary_row(
                i,
                row['Column'],
                row['Minutes with Data'],
                row['Minutes with Missing Data'],
                sparkline_data,
                time_data,
                'dynamic-button'
            )
        )

    dbTime_df['day'] = dbTime_df[db_timecol].dt.date

    df_filtered = dbTime_df.dropna(how='all', axis=1)

    columns_to_check = df_filtered.columns.difference(['day',db_timecol])

    days_with_all_data_missing = df_filtered.groupby('day').apply(
        lambda x: x[columns_to_check].isna().all().all())

    days_with_partial_data_missing = df_filtered.groupby('day').apply(
        lambda x: x[columns_to_check].isna().any().any() and not
        x[columns_to_check].isna().all().all())

    days_with_no_data = days_with_all_data_missing[days_with_all_data_missing].index.tolist()
    days_with_no_data_df = pd.DataFrame(days_with_no_data, columns=['Days with No Data'])

    days_with_some_data_missing = days_with_partial_data_missing[days_with_partial_data_missing].index.tolist()
    days_with_some_data_missing_df = pd.DataFrame(days_with_some_data_missing,
                                                  columns=['Days with Some Data Missing'])

    div_container.append(html.H3("Days with No Data"))
    div_container.append(dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in days_with_no_data_df.columns],
        data=days_with_no_data_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'}
    ))
    div_container.append(html.H3("Days with Some Data Missing"))
    div_container.append(dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in days_with_some_data_missing_df.columns],
        data=days_with_some_data_missing_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'}
    ))
    return [div_container, False, "", date_info,summary_data_minutes, dbTime_df_data]

######################################################################
# NEW DASHBOARD dayI data
######################################################################

@app.callback(
    [Output('graph-modal-dayIdashb', 'style'),
     Output('modal-graph-dayIdashb', 'figure')],
    [Input({'type': 'dynamic-button-dayI', 'index': ALL}, 'n_clicks'),
     Input('close-modal-dayIdashb', 'n_clicks')],
    [State('graph-modal-dayIdashb', 'style'),
     State('store-summary-dayI', 'data'),
     State('store-dbDayI_df', 'data')]
)
def toggle_modal_dayI(button_clicks, close_click, modal_style, summary_data_dayI, dayI_df_data):

    print("BUTTON CLICKED dayI******\n")

    ctx = dash.callback_context

    if not ctx.triggered:
        return {"display": "none"}, go.Figure()

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if 'dynamic-button-dayI' in triggered_id:
        # Trouver l'index du bouton qui a été cliqué
        triggered_index = eval(triggered_id)['index']
        column_name = summary_data_dayI[triggered_index]['Column']
        print("column name = " + column_name)

        df = pd.DataFrame(dayI_df_data)
        print("all cols = " + ','.join(df.columns))
        fig = go.Figure(
            data=[
                go.Scatter(x=df[db_daycol], y=df[column_name], mode='lines')
            ],
            layout=go.Layout(
                title=f"Courbe de {column_name} en fonction du temps",
                xaxis_title="Time",
                yaxis_title=column_name
            )
        )
        return {"display": "block"}, fig

    elif 'close-modal-dayIdashb' in triggered_id:
        return {"display": "none"}, go.Figure()

    return {"display": "none"}, go.Figure()

@app.callback(
    [Output('subtab-dayIdashb-content', 'children'),
     Output('confirm-dialog-subdayI', 'displayed'),
     Output('confirm-dialog-subdayI', 'message'),
     Output('subdayIdashb-range-info', 'children'),
     Output('store-summary-dayI', 'data'),
     Output('store-dbDayI_df', 'data')
     ],
    [Input('show-dayIdashb-btn', 'n_clicks')],
    [
     State('range-picker-subdayI', 'start_date'),
     State('range-picker-subdayI', 'end_date'),
        State('subdayIdashb-period-dropdown', 'value')]
)
def display_dayIdata_dashboard(n_clicks,start_date, end_date, selected_period):
    selected_db = dbDayI_name
    selected_col = "FOO"
    if n_clicks is None or n_clicks == 0:
        return ["", False, "", "", None, None]
    if selected_period == "stat_all":
        query = get_query_extractInterval(selected_db, None, None)
    else :
        if (not selected_db or not selected_col) and (not start_date or not end_date):
            return ["", True, "Sélectionnez des données et une période", "",None, None]
        if not selected_db or not selected_col :
            return [ "", True, "Sélectionnez des données", "",None, None]
        if not start_date or not end_date:
            return ["", True, "Sélectionnez une période", "",None, None]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date de début et fin", "",None, None]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return ["ERREUR", True, "Choisir une date différente", "",None, None]

        query = get_query_extractInterval(selected_db, start_date, end_date)

    date_info = f"Données du {start_date} au {end_date}"

    conn = sqlite3.connect(db_file)

    dbDayI_df = pd.read_sql_query(query, conn)
    conn.close()

    dbDayI_df[db_daycol] = pd.to_datetime(dbDayI_df[db_daycol])
    all_days = pd.date_range(start=start_date,
                             end=end_date)
    missing_days = all_days.difference(dbDayI_df[db_daycol])
    if not missing_days.empty:
        missing_data = pd.DataFrame(missing_days, columns=[db_daycol])
        dbDayI_df = pd.concat([dbDayI_df, missing_data],
                              ignore_index=True).sort_values(by=db_daycol)

    ## assurer que c'est bien la colonne 'time' en position 0
    assert dbDayI_df.columns[0] == db_daycol
    # Calcul du nombre de minutes avec des données et des données manquantes pour chaque colonne
    summary = pd.DataFrame({
        'Column': dbDayI_df.columns[1:],  # Exclure la colonne 'day'
        'Jours avec données': dbDayI_df.iloc[:, 1:].notna().sum().values,
        'Jours sans données': (dbDayI_df.iloc[:, 1:].isna().sum() +
                                      len(missing_days)).values
    })

    summary['Pourcentage Data'] = summary['Jours avec données'] / (
                summary['Jours avec données'] + summary['Jours sans données']) * 100

    summary_data_dayI = summary.to_dict('records')
    dbDayI_df_data = dbDayI_df.to_dict('records')

    dbDayI_df[db_daycol] = pd.to_datetime(dbDayI_df[db_daycol])
    time_data = dbDayI_df[db_daycol]

    div_container = [generate_header_row("jours")]
    for i, row in summary.iterrows():
        sparkline_data = dbDayI_df[row['Column']]
        div_container.append(
            generate_summary_row(
                i,
                row['Column'],
                row['Jours avec données'],
                row['Jours sans données'],
                sparkline_data,
                time_data,
                'dynamic-button-dayI'
            )
        )

    dbDayI_df['day'] = dbDayI_df[db_daycol].dt.date

    df_filtered = dbDayI_df.dropna(how='all', axis=1)
    columns_to_check = df_filtered.columns.difference(['day',db_daycol])
    days_with_all_data_missing = df_filtered.groupby('day').apply(
        lambda x: x[columns_to_check].isna().all().all())
    days_with_partial_data_missing = df_filtered.groupby('day').apply(
        lambda x: x[columns_to_check].isna().any().any() and not
        x[columns_to_check].isna().all().all())

    days_with_no_data = days_with_all_data_missing[days_with_all_data_missing].index.tolist()
    days_with_no_data_df = pd.DataFrame(days_with_no_data, columns=['Jours sans données'])

    days_with_some_data_missing = days_with_partial_data_missing[days_with_partial_data_missing].index.tolist()
    days_with_some_data_missing_df = pd.DataFrame(days_with_some_data_missing,
                                                  columns=['Jours avec données partielles'])

    div_container.append(html.H3("Jours sans données"))
    div_container.append(dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in days_with_no_data_df.columns],
        data=days_with_no_data_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'}
    ))
    div_container.append(html.H3("Jours avec données partielles"))
    div_container.append(dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in days_with_some_data_missing_df.columns],
        data=days_with_some_data_missing_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'}
    ))
    return [div_container, False, "", date_info,summary_data_dayI, dbDayI_df_data]

######################################################################
# graphes batterie
######################################################################
@app.callback(
    [Output('subtab-batterie-content', 'children'),
     Output('confirm-dialog-subbat', 'displayed'),
     Output('confirm-dialog-subbat', 'message'),
     Output('subbat-range-info', 'children')],
    [Input('show-batterie-btn', 'n_clicks')],
    [
     State('range-picker-subbat', 'start_date'),
     State('range-picker-subbat', 'end_date'),
        State('subbat-period-dropdown', 'value')]
)
def display_batterie_graph(n_clicks,start_date, end_date, selected_period):
    selected_db = dbTime_name
    selected_col = "FOO"

    if n_clicks is None or n_clicks == 0:
        return ["", False, "", ""]

    if selected_period == "stat_all":
        query = get_query_extractInterval(selected_db, None, None)
    else :
        if (not selected_db or not selected_col) and (not start_date or not end_date):
            return ["", True, "Sélectionnez des données et une période", ""]

        if not selected_db or not selected_col :
            return [ "", True, "Sélectionnez des données", ""]

        if not start_date or not end_date:
            return ["", True, "Sélectionnez une période", ""]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date de début et fin", ""]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return ["ERREUR", True, "Choisir une date différente", ""]

        query = get_query_extractInterval(selected_db, start_date, end_date)

    date_info = f"Données du {start_date} au {end_date}"


    conn = sqlite3.connect(db_file)

    # query = f"SELECT {db_daycol}, {selected_col} FROM {selected_db} WHERE {db_daycol} >= '{start_date}' AND {db_daycol} <= '{end_date}'"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if selected_db == dbTime_name:
        xcol = db_timecol
    else:
        xcol = db_daycol
        if selected_db == dbDayI_name:
            for col in dayI_cols:
                df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)


    div_container = []
    ##** GRAPHE 1 - minute

    plot1 = get_dbTime_2vargraph(df=df, xcol=db_timecol,col1="XT_Ubat_Vdc_I3092_L1_1",
                                 col2="XT_Ubat_Vdc_I3092_L2_2",
                                 dbName = dbTime_name,
                                 settingsdict=showcols_settings)
    div_container.append(dcc.Graph(id='graph-battrie-XTubat', figure=plot1[0]))
    div_container.append(dcc.Markdown(plot1[1],
                                      dangerously_allow_html=True))

    ##** GRAPHE 2 - jours
    selected_db = dbDayI_name
    queryI = get_query_extractInterval(selected_db, start_date, end_date)
    conn = sqlite3.connect(db_file)
    print(queryI)
    dayI_df = pd.read_sql_query(queryI, conn)
    conn.close()
    print(" nrow " + str(dayI_df.shape[0]))
    print('show first days dayI: ' + ','.join(dayI_df['day']))
    IvarsVT_toplot = ["I7007_1","I7008_1"]
    dayI_df = dayI_df[[db_daycol]+IvarsVT_toplot]

    plot3= get_dbTime_2vargraph(dayI_df, db_daycol,col1=IvarsVT_toplot[0],
                                col2 = IvarsVT_toplot[1],
                                dbName = dbDayI_name)
    div_container.append(dcc.Graph(id='graph-batterie_dayI', figure=plot3[0]))
    div_container.append(dcc.Markdown(plot3[1],
                                      dangerously_allow_html=True))

    return [div_container, False, "", date_info]



######################################################################
# graphes variotrack
######################################################################
@app.callback(
    [Output('subtab-variotrack-content', 'children'),
     Output('confirm-dialog-subvariotrack', 'displayed'),
     Output('confirm-dialog-subvariotrack', 'message'),
     Output('subvariotrack-range-info', 'children')],
    [Input('show-variotrack-btn', 'n_clicks')],
    [
     State('range-picker-subvariotrack', 'start_date'),
     State('range-picker-subvariotrack', 'end_date'),
        State('subvariotrack-period-dropdown', 'value')]
)
def display_variotrack_graph(n_clicks,start_date, end_date, selected_period):
    selected_db = dbTime_name
    selected_col = "FOO"

    if n_clicks is None or n_clicks == 0:
        return ["", False, "", ""]

    if selected_period == "stat_all":
        query = get_query_extractInterval(selected_db, None, None)
    else :
        if (not selected_db or not selected_col) and (not start_date or not end_date):
            return ["", True, "Sélectionnez des données et une période", ""]

        if not selected_db or not selected_col :
            return [ "", True, "Sélectionnez des données", ""]

        if not start_date or not end_date:
            return ["", True, "Sélectionnez une période", ""]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date de début et fin", ""]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return ["ERREUR", True, "Choisir une date différente", ""]

        query = get_query_extractInterval(selected_db, start_date, end_date)

    date_info = f"Données du {start_date} au {end_date}"


    conn = sqlite3.connect(db_file)

    # query = f"SELECT {db_daycol}, {selected_col} FROM {selected_db} WHERE {db_daycol} >= '{start_date}' AND {db_daycol} <= '{end_date}'"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if selected_db == dbTime_name:
        xcol = db_timecol
    else:
        xcol = db_daycol
        if selected_db == dbDayI_name:
            for col in dayI_cols:
                df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)


    div_container = []
    ##** GRAPHE 1 - VT PSo
    plot1 = get_dbTime_2vargraph(df, xcol,"VT_PsoM_kW_I11043_1", "VT_PsoM_kW_I11043_ALL")
    div_container.append(dcc.Graph(id='graph-VT_PsoM', figure=plot1[0]))
    div_container.append(dcc.Markdown(plot1[1],
                                      dangerously_allow_html=True))
    # ##** GRAPHE 2 - XT Uin
    plot2 = get_dbTime_2vargraph(df, xcol,"VT_IbaM_Adc_I11040_1")
    div_container.append(dcc.Graph(id='graph-VT_IbaM', figure=plot2[0]))
    div_container.append(dcc.Markdown(plot2[1],
                                      dangerously_allow_html=True))
#### ajouter les variables I
    selected_db = dbDayI_name
    queryI = get_query_extractInterval(selected_db, start_date, end_date)

    conn = sqlite3.connect(db_file)
    print(queryI)
    dayI_df = pd.read_sql_query(queryI, conn)
    conn.close()
    print(" nrow " + str(dayI_df.shape[0]))
    print('show first days dayI: ' + ','.join(dayI_df['day']))

    IvarsVT = [x for x in dayIcols_settings.keys() if
                    dayIcols_settings[x]["source"] == "VarioTrack" and
                                x in dayI_df.columns ]
    ### I11006 et I11007 ; seulement valeur dans colonne 1
    emptycols = [x for x in IvarsVT if "_2" in x]
    assert dayI_df[emptycols].isna().all().all()
    IvarsVT_toplot = [x for x in IvarsVT if "_1" in x]
    dayI_df = dayI_df[[db_daycol]+IvarsVT_toplot]

    # # Reshape le DataFrame en long format
    dayI_df_long = dayI_df.melt(id_vars=['day'],
                                value_vars=IvarsVT_toplot,
                                var_name='variable', value_name='value')
    assert len(IvarsVT_toplot)==2#
    colors = {'green': IvarsVT_toplot[0], 'red': IvarsVT_toplot[1]}

    ## grpahe 3
    plot3= get_dbTime_2vargraph(dayI_df, db_daycol,col1=IvarsVT_toplot[0],
                                col2 = IvarsVT_toplot[1],
                                dbName = dbDayI_name)
    div_container.append(dcc.Graph(id='graph-VT_dayIprod', figure=plot3[0]))
    div_container.append(dcc.Markdown(plot3[1],
                                      dangerously_allow_html=True))

    return [div_container, False, "", date_info]

######################################################################
# graphes BSP
######################################################################
@app.callback(
    [Output('subtab-bsp-content', 'children'),
     Output('confirm-dialog-subbsp', 'displayed'),
     Output('confirm-dialog-subbsp', 'message'),
     Output('subbsp-range-info', 'children')],
    [Input('show-bsp-btn', 'n_clicks')],
    [
     State('range-picker-subbsp', 'start_date'),
     State('range-picker-subbsp', 'end_date'),
        State('subbsp-period-dropdown', 'value')]
)
def display_bsp_graph(n_clicks,start_date, end_date, selected_period):
    selected_db = dbTime_name
    selected_col = "FOO"

    if n_clicks is None or n_clicks == 0:
        return ["", False, "", ""]

    if selected_period == "stat_all":
        query = get_query_extractInterval(selected_db, None, None)
    else :
        if (not selected_db or not selected_col) and (not start_date or not end_date):
            return ["", True, "Sélectionnez des données et une période", ""]

        if not selected_db or not selected_col :
            return [ "", True, "Sélectionnez des données", ""]

        if not start_date or not end_date:
            return ["", True, "Sélectionnez une période", ""]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date de début et fin", ""]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return ["ERREUR", True, "Choisir une date différente", ""]

        query = get_query_extractInterval(selected_db, start_date, end_date)

    date_info = f"Données du {start_date} au {end_date}"

    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query, conn)
    conn.close()

    if selected_db == dbTime_name:
        xcol = db_timecol
    else:
        xcol = db_daycol
        if selected_db == dbDayI_name:
            for col in dayI_cols:
                df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)
    div_container = []

    ##** GRAPHE 1 - ubat
    plot1 = get_dbTime_2vargraph(df, xcol,"BSP_Ubat_Vdc_I7030_1")
    div_container.append(dcc.Graph(id='graph-BSP_ubat', figure=plot1[0]))
    div_container.append(dcc.Markdown(plot1[1],
                                      dangerously_allow_html=True))
    # ##** GRAPHE 2 - ibat
    plot2 = get_dbTime_2vargraph(df, xcol,"BSP_Ibat_Adc_I7031_1")
    div_container.append(dcc.Graph(id='graph-BSP_ibat', figure=plot2[0]))
    div_container.append(dcc.Markdown(plot2[1],
                                      dangerously_allow_html=True))

    # ##** GRAPHE 3 - tbat ### température moyenne  !!!
    ### ajouter une colonne -> ou je remplacer chaque valeur par al moyenne
    df[db_timecol] = pd.to_datetime(df[db_timecol])
    curr_var = 'BSP_Tbat_C_I7033_1'
    func = "mean"
    new_var = curr_var+'_day'+func.title()
    df[new_var] = df.groupby(df[db_timecol].dt.date)[curr_var].transform(func)
# La température moyenne de la batterie (I7033 BSP) (plutôt graph colonnes)
    varsettingsdict = {}
    varsettingsdict[curr_var] = {'description' : showcols_settings[curr_var]['description']}
    varsettingsdict[new_var] = {'description' : "moyenne journalière de " + curr_var}
    plot3 = get_dbTime_2vargraph(df, xcol, curr_var,
                                 col2=new_var,
                                 settingsdict=varsettingsdict)
    div_container.append(dcc.Graph(id='graph-BSP_tbat', figure=plot3[0]))
    div_container.append(dcc.Markdown(plot3[1],
                                      dangerously_allow_html=True))

    #### ajouter les variables I
    ### TODO : LOADER LA TABLE
    ## FILTER LES IVARS_TOPLOT QUI SONT DANS COLNAMES
    selected_db = dbDayI_name
    if selected_period == "stat_all":
        queryI = get_query_extractInterval(selected_db, None, None)
    else:
        queryI = get_query_extractInterval(selected_db, start_date, end_date)

    conn = sqlite3.connect(db_file)
    print(queryI)
    dayI_df = pd.read_sql_query(queryI, conn)
    conn.close()
    print(" nrow " + str(dayI_df.shape[0]))
    print('show first days dayI: ' + ','.join(dayI_df['day']))
    print(dayI_df['I7008_1'])
    print(dayI_df['I7007_1'])
    ##  le "throughput energy" journalier I7007 [AH]  BSP
    # Le bilan des Ah chargé et déchargé du jour I7008-I7007 BSP
    # 	Pour la Batterie : champs fixe sans lien avec le segment temporel affiché
    #  le "throughput energy" total: Somme I7007 [AH] BSP
    # Rendement de batterie:( I7008/I7007) *100 BSP
    # Nombre de cycle (à 50%) tot I7007/90 arrondi 0BSP
    IvarBSP = [x for x in dayIcols_settings.keys() if
                    dayIcols_settings[x]["source"] == "BSP" and
                                x in dayI_df.columns ]
    ### I7007 et I7008 ; seulement valeur dans colonne 1
    emptycols = [x for x in IvarBSP if "_2" in x]
    assert dayI_df[emptycols].isna().all().all()
    IvarBSP_toplot = [x for x in IvarBSP if "_1" in x]
    assert len(IvarBSP_toplot) == 2

    dayI_df = dayI_df[[db_daycol]+IvarBSP_toplot]

    ## grpahe 5 différence entre 7007 et 7008
    # Calcul des zones colorées
    df=dayI_df.copy()
    df['day'] = pd.to_datetime(df['day'])
    df.set_index('day', inplace=True)
    plot5 = get_intersectLines_plot(df, db_daycol,
                                    col1=IvarBSP_toplot[0],
                                    col2=IvarBSP_toplot[1])
    div_container.append(dcc.Graph(id = "ivarbsp_intersectarea",figure=plot5))
    plot5_desc = get_plotdesc(IvarBSP_toplot[0], col2=IvarBSP_toplot[1], db=dbDayI_name)
    div_container.append(dcc.Markdown(plot5_desc,
                                      dangerously_allow_html=True))
    df = dayI_df.copy()
    plot6 = get_stacked_cmpgraph(df, db_daycol, IvarBSP_toplot[0],IvarBSP_toplot[1],
                                 settingsdict=dayIcols_settings)

    fig6 = plot6[0]
    fig6.update_layout(
        title = "Bilan des Ah chargés et déchargés " +
                                f'(<b>{IvarBSP_toplot[0]}</b> et <b>{IvarBSP_toplot[1]}</b>)',
        yaxis_title="Valeur"
    )

    div_container.append(dcc.Graph(id='ivarbsp_area', figure=fig6))
    div_container.append(dcc.Markdown(plot6[1],
                                      dangerously_allow_html=True))

# # Rendement de batterie:( I7008/I7007) *100 BSP
    df=dayI_df.copy()
    df['delta'] = df["I7008_1"] - df["I7007_1"]
    df['rendement'] = (df["I7008_1"] / df["I7007_1"]) * 100
    df['rendement_pos'] = df['rendement'] - 100
    df['rendement_neg'] = df['rendement'] - 100

    # Créer les sous-graphiques
    figRel = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Delta", "Rendement"))

    # Tracer 'delta' (graphique du haut)
    figRel.add_trace(go.Scatter(x=df.index, y=df['delta'],
                             mode='lines', name='Delta',
                             line=dict(color='black')), row=1, col=1)

    # Ajouter les zones de fond pour 'delta'
    figRel.add_shape(type="rect", xref="x", yref="y",
                  x0=df.index.min(), y0=0, x1=df.index.max(), y1=df['delta'].max(),
                  fillcolor="rgba(255, 0, 0, 0.2)", layer="below", row=1, col=1)
    figRel.add_shape(type="rect", xref="x", yref="y",
                  x0=df.index.min(), y0=df['delta'].min(), x1=df.index.max(), y1=0,
                  fillcolor="rgba(0, 0, 255, 0.2)", layer="below", row=1, col=1)

    # Tracer les barres de 'rendement' (graphique du bas)
    figRel.add_trace(go.Bar(x=df.index, y=np.where(df['rendement'] >= 100, df['rendement_pos'], 0),
                         name='Rendement > 100', marker=dict(color='red')), row=2, col=1)
    figRel.add_trace(go.Bar(x=df.index, y=np.where(df['rendement'] < 100, df['rendement_neg'], 0),
                         name='Rendement < 100', marker=dict(color='blue')), row=2, col=1)

    # Mise à jour de la mise en page
    figRel.update_layout(
        title_text="<b>Delta (I7008_1-I7007_1) et Rendement (100*I7008_1/I7007_1)</b>",
        height=600,
        xaxis=dict(title=db_daycol.title()),
        yaxis=dict(title='Delta', zerolinecolor='gray'),
        yaxis2=dict(title='Rendement', zerolinecolor='gray', zerolinewidth=2),
        barmode='overlay'  # Superposer les barres
    )

    figRel_desc = get_plotdesc("I7007_1" ,"I7008_1",db=dbDayI_name)
    # Ajouter le graphique à l'application Dash
    div_container.append(dcc.Graph(id='ivarbsp_rendement', figure=figRel))
    div_container.append(dcc.Markdown(figRel_desc,
                                      dangerously_allow_html=True))

    # Nombre de cycle (à 50%) tot I7007/90 arrondi 0BSP
    df=dayI_df.copy()
    df['cycles'] = round(df["I7007_1"]/90)

    figCycles = go.Figure()

    figCycles.add_trace(go.Bar(x=df[db_daycol], y=df['cycles'],
                          name='Cycles', marker=dict(color='darkblue')))

    figCycles.update_layout(
    title="<b>Nombre de cycles à 50% I7007_1/90</b>",
    title_font=dict(size=20),
        xaxis_title=db_daycol.title(),
        yaxis_title="I7007_1/90")

    figCycles_desc = get_plotdesc("I7007_1" ,db=dbDayI_name)
    # Ajouter le graphique à l'application Dash
    div_container.append(dcc.Graph(id='ivarbsp_nbcycles', figure=figCycles))
    div_container.append(dcc.Markdown(figCycles_desc,
                                      dangerously_allow_html=True))


    return [div_container, False, "", date_info]

######################################################################
# graphes xtender
######################################################################
# Callback pour afficher le graphique en fonction de la sélection :
@app.callback(
    [Output('subtab-xtender-content', 'children'),
     Output('confirm-dialog-subxtender', 'displayed'),
     Output('confirm-dialog-subxtender', 'message'),
     Output('subxtender-range-info', 'children'),],
    [Input('show-xtender-btn', 'n_clicks')],
    [
     State('range-picker-subxtender', 'start_date'),
     State('range-picker-subxtender', 'end_date'),
    State('subxtender-period-dropdown', 'value')]
)
def display_xtender_graph(n_clicks,start_date, end_date, selected_period):
    selected_db = dbTime_name
    selected_col = "FOO"

    if n_clicks is None or n_clicks == 0:
        return ["", False, "", ""]

    if selected_period == "stat_all":
        query = get_query_extractInterval(selected_db, None, None)
    else :
        if (not selected_db or not selected_col) and (not start_date or not end_date):
            return ["", True, "Sélectionnez des données et une période", ""]

        if not selected_db or not selected_col :
            return [ "", True, "Sélectionnez des données", ""]

        if not start_date or not end_date:
            return ["", True, "Sélectionnez une période", ""]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date de début et fin", ""]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return ["ERREUR", True, "Choisir une date différente", ""]

        query = get_query_extractInterval(selected_db, start_date, end_date)

    date_info = f"Données du {start_date} au {end_date}"

    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query, conn)
    conn.close()

    if selected_db == dbTime_name:
        xcol = db_timecol
    else:
        xcol = db_daycol
        if selected_db == dbDayI_name:
            for col in dayI_cols:
                df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)
    # xt fin discriminer Fréquence du réseau ou de la génératrice.
    # Les 2 sources peuvent être disciminée par leurs valeur:
    # Le réseau à une fréquence très stable <49,5Hz-50,5Hz>.
    # La generatrice est moin stable est a une fréquence généralement supérieure a 51Hz.
    # Une valeur nule indique l''absence de la source réseau/génératrice
    # XT-Phase []
    # Phase de charge de batterie.Dan ce système seule 3 phase devraient apparaitre:
    # Charge de masse,(1 rouge), Absorbtion, (2 orange), et Mintient (4 Jaune)
    # XT-Transfert []
    # Cette info pourrait être exploitée pour signaler la présence du réseau su les entrées.
    # Elle Vaut 1 lorsqu'une source est présente et 0 lorsque la source est absent est que les
    # 2 appareix foncctionnet en mode onduleur
    div_container = []
    ##** GRAPHE 1 - XT UBAT
    plot1 = get_dbTime_2vargraph(df, xcol,"XT_Ubat_MIN_Vdc_I3090_L1", "XT_Ubat_MIN_Vdc_I3090_L2")
    div_container.append(dcc.Graph(id='graph-XT_Ubat', figure=plot1[0]))
    div_container.append(dcc.Markdown(plot1[1],
                                      dangerously_allow_html=True))
    ##** GRAPHE 2 - XT Uin
    plot2 = get_dbTime_2vargraph(df, xcol,"XT_Uin_Vac_I3113_L1", "XT_Uin_Vac_I3113_L2")
    div_container.append(dcc.Graph(id='graph-XT_Uin', figure=plot2[0]))
    div_container.append(dcc.Markdown(plot2[1],
                                      dangerously_allow_html=True))

    ##** GRAPHE 3 - XT-Pout
    plot3 = get_dbTime_2vargraph(df, xcol,"XT_Pout_kVA_I3097_L1", "XT_Pout_kVA_I3097_L1",
                                 withQtLines = False, stacked = True)
    div_container.append(dcc.Graph(id='graph-XT_Pout', figure=plot3[0]))
    div_container.append(dcc.Markdown(plot3[1],
                                      dangerously_allow_html=True))
    ##** GRAPHE 4 - XT-Iin
    plot4 = get_dbTime_2vargraph(df, xcol,"XT_Iin_Aac_I3116_L1", "XT_Iin_Aac_I3116_L2",
                                 withQtLines = False, stacked = True)
    div_container.append(dcc.Graph(id='graph-XT_Iin', figure=plot4[0]))
    div_container.append(dcc.Markdown(plot4[1],
                                      dangerously_allow_html=True))

    ###** graphe 5 : XT Fin - a) valeurs minutes
    # Rescaler les valeurs pour que l'axe des x soit à y=51
    col1 = "XT_Fin_Hz_I3122_L1"
    col2 = "XT_Fin_Hz_I3122_L2"
    df['source'] = np.where(df[col1] == 0, 'Absence de source',
                            np.where(df[col1].between(49.5, 50.5), 'Réseau',
                                     np.where(df[col1] > 51, 'Génératrice', 'Incertain')))

    df['source2'] = np.where(df[col2] == 0, 'Absence de source',
                            np.where(df[col2].between(49.5, 50.5), 'Réseau',
                                     np.where(df[col2] > 51, 'Génératrice', 'Incertain')))

    colors = freq_colors
    unique_sources = set(df['source'].unique()).union(df['source2'].unique())
    figBarMin = make_subplots(rows=len(unique_sources), cols=1,
                        shared_xaxes=True, vertical_spacing=0.02)
    source_list = list(unique_sources)
    inosource = None
    for i, source in enumerate(source_list):
        source_df1 = df[df['source'] == source]
        source_df2 = df[df['source2'] == source]

        if source == "Absence de source":
            inosource = i
            assert np.all(source_df1[col1] == 0)
            assert np.all(source_df2[col2] == 0)
            source_df1[col1] = 1
            source_df1[col2] = 1

        figBarMin.add_trace(go.Bar(
            x=source_df1[db_timecol],
            y=source_df1[col1],
            name=f'{source} {col1}',
            marker_color=colors.get(source, 'grey'),
            showlegend=True if i == 0 else False
        ), row=i + 1, col=1)

        figBarMin.add_trace(go.Bar(
            x=source_df2[db_timecol],
            y=source_df2[col2],
            name=f'{source} {col2}',
            marker_color=colors.get(source, 'grey'),
            showlegend=True if i == 0 else False
        ), row=i + 1, col=1)

    figBarMin.update_layout(
        title='<b>Répartition des sources par jour</b>',
        yaxis=dict(title='Valeurs'),
        barmode='group',
        legend_title='Source',
        hovermode='x unified'
    )
    # enlever les yaxis labels pour aucune source = 0
    # fig.update_yaxes(showticklabels=False, row=3, col=1)
    # ou :
    if inosource:
        figBarMin.update_yaxes(tickvals=[0, 0.5, 1], ticktext=["","0", ""],
                     row=inosource+1, col=1)

    # Mise à jour des axes y de chaque subplot
    for i in range(1, len(unique_sources) + 1):
        figBarMin.update_yaxes(title_text="Valeurs", row=i, col=1)
        if i != len(unique_sources):  # Remove x-axis labels for all but the bottom subplot
            figBarMin.update_xaxes(showticklabels=False, row=i, col=1)

    div_container.append(dcc.Graph(id='graph-XT_FinMin', figure=figBarMin))
    div_container.append(dcc.Markdown(get_plotdesc(col1, col2),
                                      dangerously_allow_html=True))

    ###** graphe 5 : XT Fin - b) valeurs journalières

    df['day'] = pd.to_datetime(df[db_timecol]).dt.date
    #### barplot idem précédent mais par jour
    agg_df = df.groupby(['day', 'source']).size()
    wagg_df = agg_df.unstack(fill_value=0)
    pct_df = wagg_df.div(wagg_df.sum(axis=1), axis=0) * 100

    figBarDay = make_subplots(rows=2, cols=1, vertical_spacing=0.04)

    max_mean_col = pct_df.mean().idxmax()

    # s il n'y a qu un type -> np.min ne va pas marcher
    cut_int = [10,np.min(pct_df[max_mean_col]) - 0.5]
    # pour assurer qu elle soit plot en premier
    othercols = [x for x in colors.keys() if not x== max_mean_col]

    # Traces pour le second graphe (à partir de np.min(pct_df['Réseau']) - 10)
    for source in [max_mean_col]+othercols:
        if source in pct_df.columns:
            figBarDay.add_trace(go.Bar(
                x=pct_df.index,
                y=pct_df[source],
                name=source,
                marker_color=colors[source],
                showlegend=False #if source == 'Réseau' else True
            ), row=2, col=1)
            figBarDay.add_trace(go.Bar(
                x=pct_df.index,
                y=pct_df[source],
                name=source,
                marker_color=colors[source],
                showlegend=True# if source == 'Réseau' else True
            ), row=1, col=1)
    figBarDay.update_layout(
        title='<b>Répartition des sources par jour</b>',
        xaxis=dict(title='Jour'),
        barmode='stack',
        legend_title='Source',
        hovermode='x unified'
    )
    figBarDay.update_yaxes(range=[cut_int[1], 100], row=1, col=1)
    figBarDay.update_xaxes(visible=False, row=1, col=1)
    figBarDay.update_yaxes(range=[0, cut_int[0]], row=2, col=1)

    div_container.append(dcc.Graph(id='graph-XT_FinDay', figure=figBarDay))
    div_container.append(dcc.Markdown(get_plotdesc(col1, col2),
                                      dangerously_allow_html=True))


#### ajouter les variables I
    selected_db = dbDayI_name
    queryI = get_query_extractInterval(selected_db, start_date, end_date)
    conn = sqlite3.connect(db_file)
    dayI_df = pd.read_sql_query(queryI, conn)
    conn.close()
    print(" nrow " + str(dayI_df.shape[0]))
    print('show first days dayI: ' + ','.join(dayI_df['day']))


    Ivars_toplot = [x for x in dayIcols_settings.keys() if
                    dayIcols_settings[x]["source"] == "XTender" and
                                x in dayI_df.columns and
                            re.sub("_1|_2","" ,x) in IvarsOfInterset]

    dayI_df = dayI_df[[db_daycol] +Ivars_toplot]
    togroup = set([re.sub("_1|_2", "", x) for x in
                   dayI_df.columns if not x ==db_daycol])


    sumI_df = dayI_df[[db_daycol]].copy()
    for prefix in togroup:
        columns_to_sum = dayI_df.filter(like=prefix).columns
        sumI_df[prefix] = dayI_df[columns_to_sum].sum(axis=1)
    # Energie (bilan) sur l'entrée des 2 XT  (somme L1 * L2 I3081)
    # Energie (bilan) sur les sorties des 2 XT (somme L1 * L2 I3083)
    assert set(sumI_df.columns) == set( ['day', 'I3081', 'I3083'])
    data=sumI_df
    # Reshape le DataFrame en long format
    sumI_df_long = sumI_df.melt(id_vars=['day'], value_vars=['I3081', 'I3083'], var_name='variable', value_name='value')

    sumI_df_long['color'] = sumI_df_long['variable'].map(I_colors)

    # Créer le barplot
    fig = px.bar(sumI_df_long, x='day', y='value',
                 color='variable', barmode='group',
                 color_discrete_map=I_colors)

    fig.update_layout(
        title='<b>Comparaison des valeurs I3081 et I3083 par jour</b>',
        xaxis_title='Jour',
        yaxis_title='Valeurs (somme L1+L2)',
        hovermode='x unified'
    )

    text_desc81 = get_plotdesc('I3081_1', col2='I3081_2',
                             db=dbDayI_name, htmlFormat=True)
    text_desc83 = get_plotdesc('I3083_1', col2='I3083_2',
                             db=dbDayI_name, htmlFormat=True)

    div_container.append(dcc.Graph(id='graph-XT_Ivars', figure=fig))
    div_container.append(dcc.Markdown(text_desc81,
                                      dangerously_allow_html=True))
    div_container.append(dcc.Markdown(text_desc83,
                                      dangerously_allow_html=True))

    return [div_container, False, "", date_info]


################################################################################################################################
################################ CALLBACKS - TAB update & show DB - màj datepicker upload/delete
################################################################################################################################
# Callback pour mettre à jour la liste des dates après l'upload
# ou la suppression de données
@app.callback(
    [
        Output('date-picker-dbdata', 'min_date_allowed'),
        Output('date-picker-dbdata', 'max_date_allowed'),
        Output('date-picker-dbdata', 'disabled_days'),
        Output('date-picker-delete', 'min_date_allowed'),
        Output('date-picker-delete', 'max_date_allowed'),
        Output('date-picker-delete', 'disabled_days'),
    ],
    [Input('output-upload', 'children'),
     Input('output-delete', 'children')]
)
# *_ : convention pour indiquer que la fonction peut accepter un nombre arbitraire
# d'arguments, mais que ces arguments ne seront pas utilisés dans la fonction.
# comme *args pour ombre variable d'arguments positionnels (ici nom de variable _)

def update_all_dates(*_):
    all_dates = fetch_timedata_dates()
    min_date_allowed = min(all_dates)
    max_date_allowed = max(all_dates)
    disabled_days = [pd.to_datetime(date).date() for date in
                     pd.date_range(start=min_date_allowed, end=max_date_allowed).
                     difference(pd.to_datetime(all_dates))]
    return (min_date_allowed, max_date_allowed,
            disabled_days, min_date_allowed,
            max_date_allowed, disabled_days)

################################ CALLBACKS - TAB 3 - GESTION DES DONNÉEs
### callback pour l'upload de nouvelles données
@app.callback(
    Output('output-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children


# callback pour supprimer les données en fonction de la date
@app.callback(
    Output('output-delete', 'children'),
    [Input('delete-button', 'n_clicks')],
    [State('date-picker-delete', 'date')]
)
def delete_data(n_clicks, date):
    if n_clicks and date:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("DELETE FROM " + dbTime_name + " WHERE " + db_timecol + f" LIKE '{date}%'")
        conn.commit()
        conn.close()
        return html.Div(['Successfully deleted data for date: {}'.format(date)])
    return html.Div()
################################ CALLBACKS - TAB TIMEDATA - GRAPHIQUES TEMPORELS DONNEES HORAIRES
@app.callback(
    Output('time-series-graph', 'figure'),
    [Input('timedata-column-dropdown', 'value')]
)
def update_graph(selected_columns):
    if not selected_columns:
        return go.Figure()

    # Lire toutes les données de la base de données
    df = fetch_timedata()
    fig = go.Figure()
    for i, col in enumerate(selected_columns):
        # Ajout de chaque variable sur un axe y différent
        fig.add_trace(
            go.Scatter(
                x=df[db_timecol],
                y=df[col],
                mode='lines',
                name=col,
                yaxis=f'y{i + 1}'
            )
        )
    update_layout_cols(selected_columns)
    fig.update_layout(
        xaxis=dict(domain=[0.25, 0.75], showline=True, linewidth=2, linecolor='black'),
        yaxis=yaxis_layout,
        yaxis2=yaxis2_layout,
        yaxis3=yaxis3_layout,
        yaxis4=yaxis4_layout,
        title_text="",  ## titre en-haut à gauche
        margin=dict(l=40, r=40, t=40, b=30)
    )
    return fig

# callback pour vérifier le nombre de variables sélectionnées et afficher la pop-up :
@app.callback(
    [Output('confirm-dialog', 'displayed'),
     Output('timedata-column-dropdown', 'value')],
    [Input('timedata-column-dropdown', 'value')]
)
def limit_selection_timedata(selected_columns):
    if len(selected_columns) > maxTimePlotVar:
        return True, selected_columns[:maxTimePlotVar]  # Afficher la pop-up et limiter la sélection à 2
    return False, selected_columns  # Ne pas afficher la pop-up
# Ajouter un callback pour mettre à jour la description
@app.callback(
    Output('timedata-column-description', 'children'),
    [Input('timedata-column-dropdown', 'value')]
)
def update_description(selected_columns):
    if selected_columns:
        desc_txt = '<br>'.join(["<b>" + selcol + "</b> : " + showcols_settings[selcol]['description']
                                for selcol in selected_columns])
        return html.Div([dcc.Markdown(desc_txt,
                                      dangerously_allow_html=True)])
    return html.P('No column selected')

############################################## MAIN CALLBACK RENDER_CONTENT

# Callback pour mettre à jour le contenu des onglets
# NB : component_property ne peut pas être choisi librement !!
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs-example', 'value'),
     Input('date-picker-dbdata', 'date')
     ]
)
def render_content(tab, picked_date):
    if tab == 'tab-dashboard':
        return html.Div([
            html.Div(id='subtabs-dashboard-content')
        ])
    elif tab == 'tab-evotime':
        return html.Div([
            html.H3('Aperçu dans le temps'),
            html.H4(dbTime_name + ' database'),
            get_period_dropdown('evotimeperiod-dropdown'),
            html.Button('Afficher', id='show-evotime-btn', n_clicks=0),
            html.Div(id='evotime-range-info', style={'marginTop': '20px'}),

            dcc.Dropdown(
                id='evotimeTimeDB-graph-col',
                placeholder="Choisissez la colonne de données",
                options=[{'label': col, 'value': col} for col in timecols2show]
            ),
            html.Div(id='evotimeTimeDB-graph-varinfo', style={'marginTop': '20px'}),
            dcc.Dropdown(
                id='evotimeTimeDB-graph-viz',
                options=[
                    {'label': 'Line Plot', 'value': 'lineplot'},
                    {'label': 'Bar Plot', 'value': 'barplot'},
                    {'label': 'Box Plot', 'value': 'boxplot'}
                ],
                placeholder="Choisissez le type de visualisation"
            ),
            html.Button('Visualiser', id='show-evotimeTimeDBgraph-btn',
                        n_clicks=0),
            dcc.Graph(id='evotimeTimeDB-graph',config= {
                                    'scrollZoom': True  # Activer le zoom avec la molette
                                })
        ])
    elif tab == 'tab-stat':
        return html.Div([
            html.H3('Valeur moyenne de chacune des variables'),
            get_period_dropdown('statperiod-dropdown'),
            html.Button('Afficher', id='show-stat-btn', n_clicks=0),
            html.Div(id='stat-range-info', style={'marginTop': '20px'}),
            html.Div(id='stat-means-info', style={'marginTop': '20px'}),
            html.H3('Visualisation des données'),
            dcc.Dropdown(
                id='tabstatgraph-db',
                options=[
                    {'label': 'Données horaires', 'value': dbTime_name},
                    {'label': 'Données journalières P', 'value': dbDayP_name},
                    {'label': 'Données journalières I', 'value': dbDayI_name}
                ],
                placeholder="Choisissez la table de données"
            ),
            dcc.Dropdown(
                id='tabstatgraph-col',
                placeholder="Choisissez la colonne de données"
            ),
            html.Div(id='tabstatgraph-varinfo', style={'marginTop': '20px'}),
            dcc.Dropdown(
                id='tabstatgraph-viz',
                options=[
                    {'label': 'Line Plot', 'value': 'lineplot'},
                    {'label': 'Bar Plot', 'value': 'barplot'},
                    {'label': 'Box Plot', 'value': 'boxplot'}
                ],
                placeholder="Choisissez le type de visualisation"
            ),
            html.Button('Visualiser', id='show-statgraph-btn', n_clicks=0),
            dcc.Graph(id='stat-graph', config= {
                                    'scrollZoom': True  # Activer le zoom avec la molette
                                })
        ])
    elif tab == 'tab-analyseGraph':
        return html.Div([
            html.H3('Analyse (graphiques)'),
            get_period_dropdown('asGraphPeriod-dropdown'),
            html.Div(id='analyseGraph-period-subtit', children=""),
            html.H4('Répartition des fréquences '),
            dcc.Dropdown(
                id='asL-dropdown',
                options=[
                    {'label': 'L1', 'value': 'as_L1'},
                    {'label': 'L2', 'value': 'as_L2'},
                    {'label': 'L1+L2', 'value': 'as_both'}
                ],
                value='as_L1',
                placeholder="Source"
            ),
            html.Button('Afficher', id='show-asGraph-btn', n_clicks=0),
            html.Div(id='analyseGraph-pie-chart-tit', children=""),
            html.Div([
                html.Div(id='analyseGraph-pie-chart-global', children="", className="col"),
                html.Div(id='analyseGraph-pie-chart-day', children="", className="col"),
                html.Div(id='analyseGraph-pie-chart-night', children="", className="col")
            ], className='row'),
            html.H4('Température batterie'),
            html.Div([
                html.Div(id='analyseGraph-tempbat-barplot', children="", className="col")
            ], className='row')
        ])
    elif tab == 'tab-appareils':
        return html.Div([
            html.Div(id='subtabs-appareils-content')
        ])
    elif tab == 'tab-fonctions':
        return html.Div([
            html.Div(id='subtabs-fonctions-content')
        ])
    elif tab == 'tab-updateDB':
        return html.Div([
            html.H3('Gérer les données'),
            html.H4('Ajout de données à partir de fichier(s)'),
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload Files'),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True  # Allow multiple files to be uploaded
            ),
            html.Div(id='output-upload'),
            html.H4('Suppression de données'),
            dcc.DatePickerSingle(
                id='date-picker-delete',
                date=None,
                display_format='DD.MM.YYYY',
                min_date_allowed=min(fetch_timedata_dates()),
                max_date_allowed=max(fetch_timedata_dates()),
                disabled_days=[pd.to_datetime(date).date() for date in
                               pd.date_range(start=min(fetch_timedata_dates()),
                                             end=max(fetch_timedata_dates())).
                               difference(pd.to_datetime(fetch_timedata_dates()))]
            ),
            html.Button('Supprimer les données', id='delete-button', n_clicks=0),
            html.Div(id='output-delete')
        ])
    elif tab == 'tab-showDB':
        df = fetch_timedata()
        if picked_date:
            picked_df = fetch_timedata(picked_date)
        else:
            picked_df = pd.DataFrame(columns=["Aucun jour sélectionné"])
        # Convertir les données en tableau interactif DataTable
        data_table_all = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
        data_table_selected = dash_table.DataTable(
            data=picked_df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in picked_df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
        # Nouvelle section pour afficher le nombre de jours disponibles
        all_entries = fetch_timedata_dates()
        num_entries = len(all_entries)
        print(all_entries[0])
        all_days = set([datetime.strptime(x,
                                          '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') for
                        x in all_entries])

        num_days = len(all_days)
        nb_entries = html.Div([
            html.H6(f'Nombre d\'entrées dans la base de données : {num_entries}')
        ])
        nb_days = html.Div([
            html.H6(f'Nombre de jours dans la base de données : {num_days}')
        ])
        return html.Div([
            html.Div(id='datepicker-container'),
            html.H3('Données pour le jour sélectionné'),
            data_table_selected,
            html.H3('Aperçu de la base de données'),
            data_table_all,
            nb_entries,
            nb_days
        ])
# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
