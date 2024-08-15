from dash.dependencies import Input, Output
from settings import *
from utils_fcts import *
import plotly.express as px

def register_callbacks(app):

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
