# Buscar gepeos

import re
import pandas as pd
from datetime import datetime

def read_txt(start_date="", end_date="", all_dates=True):
    f = open("./chats/chat.txt", "r", encoding='utf-8')

    #Arreglar nombres
    data = f.read()
    data = data.replace('- antoni:', '- Anton:')
    data = data.replace('- Antoni:', '- Anton:')
    data = data.replace('- Sergowo Asterisco:', '- Sergio:')
    data = data.replace('- Sergio Acróbata:', '- Sergio:')
    data = data.replace('- Miden:', '- Miranda:')
    data = data.replace('- Netherlands:', '- Miranda:')
    data = data.replace('- Diego Smash:', '- Diego:')
    data = data.replace('- Paula Arcas:', '- Paula:')
    data = data.replace('- Laura Toro Diosdado:', '- Laura:')
    data = data.replace('- Jaoquien:', '- Joaquin:')
    data = data.replace('- Joaquin:', '- Joaquin:')
    data = data.replace('- aitor:', '- Aitor:')

    messages = re.findall('(\d+/\d+/\d+, \d+:\d+\d+) - (.*?): (gp$|Gp$|GP$)', data, re.MULTILINE)

    if all_dates:
        return messages
    else:
        start_date = datetime.strptime(start_date, "%y/%m/%d").date()
        end_date = datetime.strptime(end_date, "%y/%m/%d").date()

        filtered_messages = []
        for date_str, *rest in messages:
            date = datetime.strptime(date_str, "%d/%m/%y, %H:%M").date()
            if start_date <= date <= end_date:
                filtered_messages.append((date_str, *rest))

        return filtered_messages

def make_dataframe():
    df = pd.DataFrame(read_txt(),columns=['Time', 'Name', 'Message'])

    df['Time'] = pd.to_datetime(df.Time, format='%d/%m/%y, %H:%M')

    df.drop('Message', axis=1)

    #Dividir datetime a fecha y hora
    df['new_date'] = [d.date() for d in df['Time']]
    df['new_time'] = [d.time() for d in df['Time']]

    df = df.astype(str)

    df = df.pivot_table(
        values='new_time',
        index='new_date',
        columns='Name',
        aggfunc=lambda x: '; '.join(x)
    )

    df = df.reset_index()

    df['new_date'] = pd.to_datetime(df.new_date, format='%Y/%m/%d')

    df = df.set_index('new_date').asfreq('D')

    return df

#df_gp = make_dataframe()

if __name__ == '__main__':
    #print(df_gp.tail(60))
    print(read_txt(all_dates=False, start_date="23/1/1", end_date="23/2/1"))
