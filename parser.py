'''
Source: https://github.com/rljacobson/PillowData
'''
from collections import OrderedDict
import datetime
import pytz
import pandas as pd

tables = [
    'ZPILLOWUSER', 'ZSLEEPNOTE', 'Z_2SLEEPSESSION', 'ZSLEEPSESSION',
    'ZSLEEPSTAGEDATAPOINT', 'ZSNOOZELAB', 'ZSOUNDDATAPOINT', 'Z_PRIMARYKEY',
    'Z_METADATA', 'Z_MODELCACHE', 'Y_UBMETA', 'Y_UBRANGE', 'Y_UBKVS'
]


def getDictFromString(string):
    tokens = string.split()
    # tokens.reverse()
    row = OrderedDict()

    while tokens:
        # Values may be multiple words. We build up a value until we reach a
        # separator. The value is then the concatenation of the reverse of the list.
        value_parts = [tokens.pop()]
        value_part_or_sep = tokens.pop()  # ' -> '
        while value_part_or_sep != '->':
            value_parts.append(value_part_or_sep)
            value_part_or_sep = tokens.pop()
        value_parts.reverse()

        # Keys are one word.
        key = tokens.pop()
        row[key] = ' '.join(value_parts)

    return row


filename = 'data-raw/PillowData.txt'

reading_table = None
dataframes = {}
rows = []
count = 0

with open(filename) as file:
    for line in file:
        #         count += 1
        #         if count >2:
        #             break

        line = line.strip()

        # if we are at a new table heading
        if line in tables:
            # If we are finished reading the last table
            if reading_table:
                dataframes[reading_table] = pd.DataFrame(rows)

            # record which table we are reading.
            reading_table = line
            # Init the list of rows.
            rows = []
            continue

        elif line == '':
            # EOF has extra newline, conveniently signalling that we need to
            # make the dataframe for the last table.
            dataframes[reading_table] = pd.DataFrame(rows)
            del rows
            break

        rows.append(getDictFromString(line))

# Reverse the order of the columns in each dataframe.
for k, v in dataframes.items():
    dataframes[k] = v.iloc[:, ::-1]

# Convert each column to numeric datatype if possible.
for df in dataframes.values():
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

df_sessions = dataframes['ZSLEEPSESSION']
df_stages = dataframes['ZSLEEPSTAGEDATAPOINT']
df_audio = dataframes['ZSOUNDDATAPOINT']
df_session_notes = dataframes['Z_2SLEEPSESSION']
df_notes = dataframes['ZSLEEPNOTE']


def makeDateTime(timestamp):
    reference_time = 978264000 + 3600 * 9  # Asia/Tokyo
    return datetime.datetime.fromtimestamp(
        timestamp + reference_time).strftime('%Y-%m-%d %H:%M:%S')


df_stages.sort_values('ZTIMESTAMP', inplace=True)
df_stages['ZTIMESTAMP'] = df_stages['ZTIMESTAMP'].apply(makeDateTime)
df_sessions['ZSTARTTIME'] = df_sessions['ZSTARTTIME'].apply(makeDateTime)
df_sessions['ZENDTIME'] = df_sessions['ZENDTIME'].apply(makeDateTime)
if df_audio.empty is not True:
    df_audio.sort_values('ZTIMESTAMP', inplace=True)
    df_audio['ZTIMESTAMP'] = df_audio['ZTIMESTAMP'].apply(makeDateTime)

# Remove invalid rows
df_stages = df_stages.loc[df_stages['ZSLEEPSESSION'] != '(null)']


def save_to_csv(dataframe, file_name):
    dataframe = dataframe.drop(columns=['ZUNIQUEIDENTIFIER'])
    dataframe['TIMEZONE'] = "Asia/Tokyo"
    dataframe.to_csv(file_name, index=False)


save_to_csv(df_stages, 'stages.csv')
save_to_csv(df_sessions, 'sessions.csv')
