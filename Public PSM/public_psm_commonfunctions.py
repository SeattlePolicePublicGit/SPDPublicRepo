import pandas as pd
import numpy as np
import datetime
import string

region = "us-gov-west-1"

        
weapon_conversion_key = {
    '-': 0,
    'None': 0,
    'None/Not Applicable': 0,
    'Knife/Cutting/Stabbing Instrument': 1,
    'Other Firearm': 1,
    'Blunt Object/Striking Implement': 1,
    'Fire/Incendiary Device': 1,
    'Handgun': 1,
    'Taser/Stun Gun': 1,
    'Firearm': 1,
    'Mace/Pepper Spray': 1,
    'Rifle': 1,
    'Personal Weapons (hands, feet, etc.)': 1,
    'Lethal Cutting Instrument': 1,
    'Firearm Other': 1,
    'Club, Blackjack, Brass Knuckles': 1,
    'Firearm (unk type)': 1,
    'Club': 1,
    'Automatic Handgun': 1,
    'Shotgun': 1,
    'Brass Knuckles': 1,
    'Blackjack': 1,
        np.nan: 0
}


def process_weapon (array_of_weapons):
    output = [i for i in array_of_weapons if i not in ('-', 'None')]
    output = sorted(list(set(output)))
    return output

def watch_from_squad_desc (input, timestamp):
    try:
        time = timestamp.time()
    except ValueError:
        print(f'Error processing time {timestamp}')
        time = None
    first_watch_start = datetime.time(3,0)
    second_watch_start = datetime.time(11,0)
    third_watch_start = datetime.time(19,0)
    watch = None
    input = str(input)
    if input:
        if '1ST' in input.upper():
            watch = '1ST' 
        elif '2ND' in input.upper():
            watch = '2ND'
        elif '3RD' in input.upper():
            watch = '3RD'

    if not watch and time:
        if time >= first_watch_start and time < second_watch_start:
            watch = '1ST'
        elif time >= second_watch_start and time < third_watch_start:
            watch = '2ND'
        elif time >= third_watch_start and time <= datetime.time(23,59,59):
            watch = '3RD'
        elif time >= datetime.time(0,0) and time < first_watch_start:
            watch = '3RD'
        else:
            watch = input.upper()
    return watch


def get_rolling_count(grp, freq, time_field='observation_datetime_d', count_field='Terry Stop ID'):
    return grp.rolling(freq, on=time_field, closed = 'left')[count_field].count()

def generate_features (df, group_by_key, feature_name, lookback_period):
    
    if lookback_period.endswith('M'):
        time_period = f'{30*int(lookback_period[:-1])}D'
    elif lookback_period.endswith('Y'):
        time_period = f'{365*int(lookback_period[:-1])}D'
    elif lookback_period.endswith('D'):
        time_period = f'{lookback_period}D'
    else:
        raise Exception ('Lookback_period not supported. Support input types are *D, *M, *Y.')

    df[f'{feature_name}_{lookback_period}'] = df.groupby(
        group_by_key, as_index=False, group_keys=False
    ).apply(get_rolling_count, time_period)

    return df

