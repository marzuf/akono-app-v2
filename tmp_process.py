datafolder='../LOG_300524'
datafile=datafolder+"/LG231126.CSV"
file_path=datafile=datafolder+"/LG231210.CSV"

datafile=datafolder+"/LG240415.CSV"

from settings import *
import pandas as pd
import re
def clean_cols(myl):
    #  myl = [re.sub(r'\[.*\]', '', x) for x in myl]
    myl = [re.sub(r'[-\[\]\+ \(\)°%]', '_', x.strip()) for x in myl]
    myl = [re.sub(r'_+', '_', x) for x in myl]
    myl = [x.strip("_") for x in myl]
    return myl

def getheadercols(r1, r2, r3):
    # les headers ont un champ de moins que les valeurs
    l1 = r1.split(';') #+ ["missing"]
    l2 = r2.split(';') #+ [""]
    l3 = r3.split(';') #+ [""]
    assert len(l1) == len(l2)
    assert len(l1) == len(l3)
    for i in range(1, len(l1)):
        if l1[i] == '':
            l1[i] = l1[i - 1]
    # enlever caractères spéciaux et unité
    l1 = clean_cols(l1)
    # Concatenate the first three rows to form new column names
    new_columns = [f'{l1[i]}_{l2[i]}_{l3[i]}' for i in range(len(l1))]
    new_columns = [re.sub(r'_+', '_', x) for x in new_columns]
    new_columns[0] = db_timecol
    return clean_cols(new_columns)

# def process_file(file_path):
time_pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$')
dayP_pattern = re.compile(r'^P\d.+')
dayI_pattern = re.compile(r'^I\d.+')



with open(file_path, encoding='latin1') as f:
    # Lire les 3 lignes du header
    header_lines = [f.readline().strip().rstrip(";") for _ in range(3)]
    new_columns = getheadercols(header_lines[0], header_lines[1], header_lines[2])
    time_lines_init = [f.readline().strip().rstrip(";").split(";") for _ in
                                                        range(60*24)]
    curr_day =  time_lines_init[0][0].split(' ')[0]
    # pas nécessaire de mettre range(3, 3 + 60 * 24)] ! _ est le pointeur
    time_lines = [x for x in time_lines_init if len(x)== len(new_columns) and
                                                time_pattern.match(x[0]) and
                  re.compile(curr_day).match(x[0])]
    maxTime_idx = max(i for i, x in enumerate(time_lines_init) if len(x) ==
                                len(new_columns) and time_pattern.match(x[0]))
    dayPstart_idx = maxTime_idx+nHeaderSkip+1
    # repositionner le pointeur
    f.seek(0)
    for _ in range(dayPstart_idx):
        f.readline()

    dayP_lines_init = [f.readline().strip().rstrip(";").split(";") for _ in
                            range(nRowsDayP)]
    # pas nécessaire dayPstart_idx,(dayPstart_idx+nRowsDayP))
    dayP_lines = [x for x in dayP_lines_init if  dayP_pattern.match(x[0])]
    maxDayP_idx = max(i for i, x in enumerate(dayP_lines_init) if
                                                dayP_pattern.match(x[0]))

    dayIstart_idx = maxDayP_idx+dayPstart_idx+1

    # repositionner le pointeur
    f.seek(0)
    for _ in range(dayIstart_idx):
        f.readline()

    dayI_lines_init = [f.readline().strip().rstrip(";").split(";") for _ in
                            range(nRowsDayI)]
    # pas nécessaire range(dayIstart_idx,(dayIstart_idx+nRowsDayI)
    dayI_lines = [x for x in dayI_lines_init if  dayI_pattern.match(x[0])]




# s il y avait toutes les données temps, alors max_idx vaut 1439 (60*24+1)
time_data = pd.DataFrame(time_lines, columns=new_columns)
# assert time_data.columns.isin(time_real_cols + time_txt_cols).all()

dayP_dataL = pd.DataFrame(dayP_lines)

dayP_datam = dayP_dataL.melt(id_vars=[0],
                             value_vars=list(dayP_dataL.columns),
                             var_name='variable',
                             value_name='value')
dayP_datam.iloc[:, 0] = dayP_datam.iloc[:, 0] + "_" + dayP_datam.iloc[:, 1].astype(str)
dayP_datam.drop(columns=['variable'], inplace=True)
dayP_data = dayP_datam.T
dayP_data.columns = dayP_data.iloc[0]
dayP_data = dayP_data[1:]
dayP_data.insert(0, day_txt_cols[0], curr_day)

ndayP, ndayPcols = dayP_data.shape
assert ndayP == 1

dayI_data = pd.DataFrame(dayI_lines)


return time_data, dayP_data, dayI_data


# Exemple d'utilisation
file_path = "path_to_your_file.txt"
time_data, dayP_data, dayI_data = process_file(file_path)
