import pandas as pd
import numpy as np
from datetime import timedelta


def convert(name, schedule):
    # shift start/end times
    t1 = '15:30'
    t2 = '16:30'
    t3 = '08:00'
    t4 = '20:00'
    t5 = '20:30'

    # reading the schedule
    table1 = pd.read_excel(schedule)

    # arranging for comfort
    table1.rename(columns={'Unnamed: 3': 'morningStart',
                           'משמרת בוקר': 'morningPerson',
                           'משמרת ערב - ראשונה': 'eveningPerson',
                           'משמרת לילה - שניה': 'nightPerson',
                           'Unnamed: 7': 'nightStart',
                           'Unnamed: 5': 'eveningStart',
                           'יום': 'day',
                           'תאריך': 'date',
                           }, inplace=True)
    table1 = table1.drop(columns=['הערות'])  # or inplace = True

    # for strange date formats
    # misha['date'] = pd.to_datetime(misha['date'])

    # filtering rows that don't have your name
    table1 = table1[(table1.morningPerson.str.contains(name)) |
                    (table1.nightPerson.str.contains(name)) |
                    (table1.eveningPerson.str.contains(name))]

    # creating the google calendar format
    table2 = pd.DataFrame(columns=['Subject', 'Start Date',
                                   'Start Time', 'End Date',
                                   'End Time'])

    # inserting shift dates
    table2['Start Date'] = table1['date']
    table2['End Date'] = np.where(table1['nightPerson'] == name,
                                  table1['date'] + timedelta(days=1), table1['date'])

    # inserting shift types to 'Subject' column
    conditions = [table1['morningPerson'] == name,
                  (table1['nightPerson'] == name),
                  (table1['eveningPerson'] == name)]
    choices = ['Morning shift', 'Night shift', 'Evening shift']
    table2['Subject'] = np.select(conditions, choices, default=np.nan)

    # inserting shift start and end times
    conditions = [(table1['day'] == 'שלישי') & (table1['eveningPerson'] == name),
                  (table1['day'] != 'שלישי') & (table1['eveningPerson'] == name),
                  ((table1['day'] == 'שישי') | (table1['day'] == 'שבת')) & (table1['nightPerson'] == name),
                  ((table1['day'] != 'שישי') | (table1['day'] != 'שבת')) & (table1['nightPerson'] == name),
                  (table1['morningPerson'] == name)]
    choices_start = [t1, t2, t4, t5, t3]
    choices_end = [t5, t5, t3, t3, t4]
    table2['Start Time'] = np.select(conditions, choices_start, default=np.nan)
    table2['End Time'] = np.select(conditions, choices_end, default=np.nan)

    # exporting to csv
    table2.set_index('Subject').to_csv("shifts.csv", encoding='iso8859_8')
