# Buscar mensajes de buenos días

import re
import pandas as pd
from datetime import date

MENSAJES = [
    '¡Muy Buenos Días a Todos! Recuerden que para tener un día extraordinario es necesario hacer un gran esfuerzo ¡Que tengan una mañana tranquila y llena de oportunidades!',
    'Esta es la oportunidad para salir de tu zona de confort y tener un hermoso día, recuérdalo cuando las dificultades lleguen a ti y debas superarlas ¡Que tengan un buen día, amigos!',
    'Amigos míos, tengan presente que caemos para levantarnos, nunca se queden en el suelo ni se conformen con menos, este es un día para ser mejor que ayer. Que tengas el mejor día.',
    'Querida familia, oro para que este día sea asombroso para cada uno de ustedes, productivo y lleno de alegría y que en cada paso que den hoy nunca se apague la llama de sus sueños. Buenos días.',
    'Nos proponemos metas para cumplirlas, cada paso que damos es un nuevo objetivo, no dejes pasar un día sin trabajar por tus sueños. Es el amanecer de un nuevo día, reúne tus fuerzas para luchar, sonreír y experimentar la vida ¡Que tengas un gran día!',
    'Que tus sueños te mantengan fuerte y lleno de motivación, que sus metas hagan de esta una excelente mañana, no te olvides de celebrar y disfrutar de la vida, no te preocupes en exceso por el mañana, porque los cambios están a la orden del día.',
    'Cada nuevo día es una oportunidad para lograr más, para alcanzar nuevos sueños y perseguirlos sin cansancio. Mientras trabajas pueden practicar la gran sonrisa que tendrán en la cima ¡Disfruten de este día!',
    'Molt Bon dia a Tots! Recordin que per a tenir un dia extraordinari és necessari fer un gran esforç. Que tinguin un matí tranquil i ple d\'oportunitats!',
    'Aquesta és l\'oportunitat per a sortir de la teva zona de confort i tenir un bell dia, recorda\'l quan les dificultats arribin a tu i hagis de superar-les. Que tinguin un bon dia, amics!',
    'Amics meus, tinguin present que caiem per a aixecar-nos, mai es quedin en el sòl ni es conformin amb menys, aquest és un dia per a ser millor que ahir. Que tinguis el millor dia.',
    'Benvolguda família, or perquè aquest dia sigui sorprenent per a cadascun de vostès, productiu i ple d\'alegria i que en cada pas que donin avui mai s\'apagui la flama dels seus somnis. Bon dia.',
    'Ens proposem metes per a complir-les, cada pas que donem és un nou objectiu, no deixis passar un dia sense treballar pels teus somnis. És l\'alba d\'un nou dia, reuneix les teves forces per a lluitar, somriure i experimentar la vida. Que tinguis un gran dia!',
    'Que els teus somnis et mantinguin fort i ple de motivació, que les seves metes facin d\'aquesta un excel·lent matí, no t\'oblidis de celebrar i gaudir de la vida, no et preocupis en excés pel demà, perquè els canvis estan a l\'ordre del dia.',
    'Cada nou dia és una oportunitat per a aconseguir més, per a aconseguir nous somnis i perseguir-los sense cansament. Mentre treballes poden practicar el gran somriure que tindran en el cim. Gaudeixin d\'aquest dia!',
    'bondiarodalies😚😚\nA quina hora passa el tren de Sant Vicent de Calders🤨🤨 no puc esperar més😫😫\nNen, porto aquí mitja hora i això no ve saps😡😡'
]


def read_txt(profeta):
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

    message_string = '|'.join(MENSAJES)
    messages = re.findall(f'(\d+/\d+/\d+, \d+:\d+\d+) - ({profeta}): (' + message_string + ')', data)

    return messages

def make_dataframe():
    df = pd.DataFrame(read_txt(),columns=['Time', 'Name', 'Message'])

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

    df.columns = ['new_date', 'HORA_MBD', 'MBD_TIPO']

    df['new_date'] = pd.to_datetime(df.new_date, format='%Y/%m/%d')

    df = df.set_index('new_date').asfreq('D')

    return df

if __name__ == '__main__':
    print(read_txt())