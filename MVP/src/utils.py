import pandas as pd

def validate_file_features(row: str, action: str):
    split = [[i.strip() for i in item.split(',')] for item in row.split('\n')]

    if 'Title' in split[0] and action=='test':
        df = pd.DataFrame(split[1:])
        df.columns = split[0]
        return df
    elif 'Title' in split[0] and 'Related' in split[0] and action=='train':
        df = pd.DataFrame(split[1:])
        df.columns = split[0]
        return df