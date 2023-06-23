# Buscar mensajes Drg
import re
import pandas as pd
from datetime import datetime

PROFETA = "Pablo"

def read_txt(profeta, all_dates=True, start_date="", end_date=""):
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
    data = data.replace('- Jaoquien:', '- Joaquín:')
    data = data.replace('- Joaquin:', '- Joaquín:')
    data = data.replace('- aitor:', '- Aitor:')

    messages = re.findall(f'(\d+/\d+/\d+, \d+:\d+\d+) - ({profeta}): (drg$|Drg$|drg 🙏$)', data, re.MULTILINE)

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
    df = pd.DataFrame(read_txt(profeta="Pablo"),columns=['Time', 'Name', 'Message'])

    df['Time'] = pd.to_datetime(df.Time, format='%d/%m/%y, %H:%M')

    #df.drop('Message', axis=1)

    #Dividir datetime a fecha y hora
    df['new_date'] = [d.date() for d in df['Time']]
    df['new_time'] = [d.time() for d in df['Time']]

    df = df.drop('Time', axis=1).drop('Name', axis=1)

    #Reordenar columnas
    cols = df.columns.tolist()

    cols = cols[-1:] + cols[:-1]
    cols = cols[-1:] + cols[:-1]

    df = df[cols] 

    df.columns = ['new_date', 'HORA_DRG', 'DRG']

    df['new_date'] = pd.to_datetime(df.new_date, format='%Y/%m/%d')

    df = df.drop_duplicates(subset='new_date', keep="first")
    df = df.set_index('new_date').asfreq('D')

    df = df.drop('DRG', axis=1)

    return df

df_mbd = make_dataframe()

if __name__ == '__main__':
    print(read_txt(profeta="Pablo", all_dates=False, start_date="23/1/1", end_date="23/1/2"))