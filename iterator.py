import xl_to_csv
import cal_api


def iterate():
    for i, row in xl_to_csv.table2.iterrows():
        subject, start_date, start_time, end_date, end_time = row['Subject'], row['Start Date'], row['Start Time'], \
                                                              row['End Date'], row['End Time']
        # converting to string and removing '00:00:00' suffix
        start_date = str(start_date)[:10]
        end_date = str(end_date)[:10]
        # insert given row as a single event into calendar
        cal_api.import_df(subject, start_date, start_time, end_date, end_time)
