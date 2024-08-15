
from dash.dependencies import Input, Output
from app_settings import *

all_pickers = ['date-picker-dbdata'] + all_range_pickers

def register_callbacks(app):

    ##################################################################################
    ######################################### DATE PICKER HANDLING
    ##################################################################################
    @app.callback(
        [Output(picker_id, 'style') for picker_id in all_pickers],

        # [
        #     Output('date-picker-dbdata', 'style'),
        #     Output('range-picker-evotime', 'style'),
        #     Output('range-picker-stat', 'style'),
        #     Output('range-picker-analyseGraph', 'style'),
        #     Output('range-picker-subxtender', 'style'),
        #     Output('range-picker-subvariotrack', 'style'),
        #     Output('range-picker-subbsp', 'style'),
        #     Output('range-picker-subbat', 'style'),
        #     Output('range-picker-subminutes', 'style'),
        #     Output('range-picker-subdayI', 'style'),
        #     Output('range-picker-exportdata', 'style')
        # ],
        [
            Input('tabs-example', 'value'),
            Input('subtabs-appareils', 'value'),
            Input('subtabs-fonctions', 'value'),
            Input('subtabs-dashboard', 'value'),
            Input('subtabs-data', 'value')        ]
    )
    def show_hide_datepickers(tab, subtab_appareils, subtab_fonctions,
                              subtab_dashboard, subtab_data):
        # styles = {
        #     'date-picker-dbdata': {'display': 'none'},
        #     'range-picker-evotime': {'display': 'none'},
        #     'range-picker-stat': {'display': 'none'},
        #     'range-picker-analyseGraph': {'display': 'none'},
        #     'range-picker-subxtender': {'display': 'none'},
        #     'range-picker-subvariotrack': {'display': 'none'},
        #     'range-picker-subbsp': {'display': 'none'},
        #     'range-picker-subbat': {'display': 'none'},
        #     'range-picker-subminutes': {'display': 'none'},
        #     'range-picker-subdayI': {'display': 'none'},
        #     'range-picker-exportdata': {'display': 'none'}
        # }

        styles = {picker: {'display': 'none'} for picker in all_pickers}

        if tab == "tab-data" :
            if subtab_data == 'subtab-showDB':
                styles['date-picker-dbdata'] = {'display': 'block', 'margin': '20px 0'}
            elif subtab_data == 'subtab-exportDB':
                styles['range-picker-exportdata'] = {'display': 'block', 'margin': '20px 0'}
        elif tab == 'tab-evotime':
            styles['range-picker-evotime'] = {'display': 'block', 'margin': '20px 0'}
        elif tab == 'tab-stat':
            styles['range-picker-stat'] = {'display': 'block', 'margin': '20px 0'}
        elif tab == 'tab-analyseGraph':
            styles['range-picker-analyseGraph'] = {'display': 'block', 'margin': '20px 0'}
        elif tab == 'tab-appareils':
            if subtab_appareils == "subtab-xtender":
                styles['range-picker-subxtender'] = {'display': 'block', 'margin': '20px 0'}
            elif subtab_appareils == "subtab-variotrack":
                styles['range-picker-subvariotrack'] = {'display': 'block', 'margin': '20px 0'}
            elif subtab_appareils == "subtab-bsp":
                styles['range-picker-subbsp'] = {'display': 'block', 'margin': '20px 0'}
        elif tab == 'tab-fonctions':
            if subtab_fonctions == "subtab-batterie":
                styles['range-picker-subbat'] = {'display': 'block', 'margin': '20px 0'}
        elif tab == 'tab-dashboard':
            if subtab_dashboard == "subtab-minutesdata":
                styles['range-picker-subminutes'] = {'display': 'block', 'margin': '20px 0'}
            elif subtab_dashboard == "subtab-dayIdata":
                styles['range-picker-subdayI'] = {'display': 'block', 'margin': '20px 0'}

        return [styles[key] for key in styles]
