from settings import *

from utils_fcts import *


conn = sqlite3.connect(db_file)
selected_period = "as_all"
dbname = dbTime_name
query = f"SELECT * FROM {dbname}"
query = get_query_extractInterval(dbTime_name, "2023-11-26", "2023-11-28")

all_df = pd.read_sql_query(query, conn)
conn.close()

dbTime_df = all_df
dbTime_df['time'] = pd.to_datetime(dbTime_df['time'])

# Définir la plage complète de temps en minutes
all_minutes = pd.date_range(start=dbTime_df['time'].min(),
                            end=dbTime_df['time'].max(), freq='min')

# Vérifier les minutes manquantes dans la colonne 'time'
missing_times = all_minutes.difference(dbTime_df['time'])

# Ajouter les minutes manquantes au DataFrame avec des valeurs NaN pour les autres colonnes
if not missing_times.empty:
    missing_data = pd.DataFrame(missing_times, columns=['time'])
    dbTime_df = pd.concat([dbTime_df, missing_data], ignore_index=True).sort_values(by='time')

# Calcul du nombre de minutes avec des données et des données manquantes pour chaque colonne
summary = pd.DataFrame({
    'Column': dbTime_df.columns[1:],  # Exclure la colonne 'time'
    'Minutes with Data': dbTime_df.iloc[:, 1:].notna().sum().values,
    'Minutes with Missing Data': (dbTime_df.iloc[:, 1:].isna().sum() + len(missing_times)).values
})

dbTime_df['day'] = dbTime_df['time'].dt.date

# Exclure les colonnes entièrement vides
df_filtered = dbTime_df.dropna(how='all', axis=1)

columns_to_check = df_filtered.columns.difference(['time', 'day'])

# Calcul des jours avec toutes les données manquantes
days_with_all_data_missing = df_filtered.groupby('day').apply(
                                            lambda x: x[columns_to_check].isna().all().all())

# Calcul des jours avec certaines données manquantes
days_with_partial_data_missing = df_filtered.groupby('day').apply(
                                lambda x: x[columns_to_check].isna().any().any() and not
                                            x[columns_to_check].isna().all().all())

# Tableau des jours avec aucune donnée
days_with_no_data = days_with_all_data_missing[days_with_all_data_missing].index.tolist()
days_with_no_data_df = pd.DataFrame(days_with_no_data, columns=['Days with No Data'])

# Tableau des jours avec certaines données manquantes
days_with_some_data_missing = days_with_partial_data_missing[days_with_partial_data_missing].index.tolist()
days_with_some_data_missing_df = pd.DataFrame(days_with_some_data_missing,
                                              columns=['Days with Some Data Missing'])

# Afficher les tableaux
print("Days with No Data:")
print(days_with_no_data_df)

print("\nDays with Some Data Missing:")
print(days_with_some_data_missing_df)













date_to_filter = pd.to_datetime('2023-11-27').date()
filtered_data = dbTime_df[dbTime_df['day'] == date_to_filter]

filtered_data.groupby('day').apply(lambda x: x.isna().all())












conn = sqlite3.connect(db_file)
selected_period = "as_all"
dbname = dbDayI_name
query = f"SELECT * FROM {dbname}"
all_df = pd.read_sql_query(query, conn)
conn.close()

dayI_df = all_df
dayI_df['day'] = pd.to_datetime(dayI_df['day'])

all_days = pd.date_range(start=dayI_df['day'].min(), end=dayI_df['day'].max())

missing_days = all_days.difference(dayI_df['day'])

if not missing_days.empty:
    missing_data = pd.DataFrame(missing_days, columns=['day'])
    dayI_df = pd.concat([dayI_df, missing_data], ignore_index=True).sort_values(by='day')

summary = pd.DataFrame({
    'Column': dayI_df.columns[1:],  # Exclure la colonne 'day'
    'Days with Data': dayI_df.iloc[:, 1:].notna().sum().values,
    'Days with Missing Data': (dayI_df.iloc[:, 1:].isna().sum() + len(missing_days)).values
})

# Affichage du tableau récapitulatif
print(summary)




























selected_period="as_all"
if selected_period == 'as_all':
    query = f"SELECT * FROM {dbname}"
    # interval_txt = " (tout)"
    # interval_txt = " Toutes les données"
else:
    query = get_query_extractInterval(dbname, start_date, end_date)
    print(query)
    # interval_txt = ("Période : " + start_date.strftime('%d/%m/%Y') + " - " +
    #                 end_date.strftime('%d/%m/%Y'))
all_df = pd.read_sql_query(query, conn)
conn.close()
puicol_tot = xtpuicol_L1 + "+" + xtpuicol_L2
all_df[puicol_tot] = all_df[xtpuicol_L1] + all_df[xtpuicol_L2]
import numpy as np

df = all_df[[db_timecol, puicol_tot, xtpuicol_L1, xtpuicol_L2]].copy()
df.loc[:, 'catTime'] = np.where(
    (pd.to_datetime(df[db_timecol]).dt.time >=
     datetime.strptime("08:00", "%H:%M").time()) &
    (pd.to_datetime(df[db_timecol]).dt.time <
     datetime.strptime("18:00", "%H:%M").time()),
    "Jour",
    "Nuit"
)
time_df = df[['catTime', puicol_tot, xtpuicol_L1, xtpuicol_L2]].copy()
tot_df = df[[puicol_tot, xtpuicol_L1, xtpuicol_L2]].copy()

catTime_counts = time_df['catTime'].value_counts().reset_index()
# VRAI si 1 jour sélectionné
if selected_period == 'as_day':
    assert (catTime_counts.loc[catTime_counts['catTime'] == 'Nuit', 'count'] == 840).all()
    assert (catTime_counts.loc[catTime_counts['catTime'] == 'Jour', 'count'] == 600).all()

all_df['time'] = pd.to_datetime(all_df['time'])
all_df['BSP_Tbat_C_I7033_1_dayMean'] = all_df.groupby(all_df['time'].dt.date)['BSP_Tbat_C_I7033_1'].transform('mean')

# Calcul des zones colorées
df = dayI_df
df['day'] = pd.to_datetime(df['day'])


# Fonction pour trouver les points d'intersection exacts
def find_intersections(df):
    intersections = []
    for i in range(len(df) - 1):
        if (df['I7007_1'][i] - df['I7008_1'][i]) * (df['I7007_1'][i + 1] - df['I7008_1'][i + 1]) < 0:
            x1, x2 = df['day'][i], df['day'][i + 1]
            y1_1, y2_1 = df['I7007_1'][i], df['I7007_1'][i + 1]
            y1_2, y2_2 = df['I7008_1'][i], df['I7008_1'][i + 1]

            # Calcul de l'intersection linéaire
            slope_1 = (y2_1 - y1_1) / (x2 - x1).days
            slope_2 = (y2_2 - y1_2) / (x2 - x1).days
            intersect_day = x1 + pd.Timedelta(days=(y1_2 - y1_1) / (slope_1 - slope_2))
            intersect_value = y1_1 + slope_1 * (intersect_day - x1).days
            intersections.append((intersect_day, intersect_value))
    return intersections


# Trouver les points d'intersection
intersections = find_intersections(df)

# Ajouter les points d'intersection aux données en utilisant pd.concat
intersect_df = pd.DataFrame(intersections, columns=['day', 'I7007_1'])
intersect_df['I7008_1'] = intersect_df['I7007_1']

df = pd.concat([df, intersect_df], ignore_index=True)

# Trier les données par jour
df=all_df
# df = df.sort_values('day').reset_index(drop=True)
df.set_index('day', inplace=True)
import matplotlib
matplotlib.use('TkAgg')  ### poru voir plots dans paycharm
import matplotlib.pyplot as plt
x = df.index
y1 = df['I7007_1']
y2 = df['I7008_1']

# Création de la figure
fig, ax = plt.subplots(figsize=(10, 6))

# Tracer les lignes
ax.plot(x, y1, label='I7007_1', color='blue')
ax.plot(x, y2, label='I7008_1', color='red')

# Remplir les zones entre les courbes
ax.fill_between(x, y1, y2, where=(y2 >= y1), facecolor='green', alpha=0.3, interpolate=True)
ax.fill_between(x, y1, y2, where=(y2 <= y1), facecolor='red', alpha=0.3, interpolate=True)

# Ajouter le titre et les légendes
ax.set_title('Fill Between with Interpolation')
ax.legend(loc='upper left')

# Afficher le graphique
plt.show()