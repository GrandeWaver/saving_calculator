import pandas as pd

#importuj dane historyczne indexu S&P500
def import_df(days_range):
    #https://pl.investing.com/indices/us-spx-500-historical-data
    df = pd.read_csv(r"https://github.com/GrandeWaver/saving_calculator/blob/main/Dane%20historyczne%20dla%20S%26P%20500%20(0).csv")
    df = df.head(days_range)
    #przygotowanie danych
    df['Ostatnio'] = df['Ostatnio'].str.replace('.', '')
    df['Ostatnio'] = df['Ostatnio'].str.replace(',', '.')
    df['Cena'] = df['Ostatnio'].astype(float)
    #odwróć kolejność -> od najstarszych danych w lewo na wykresie
    df = df.reindex(index=df.index[::-1])
    df = df.reset_index()
    df['index'] = df.index
    #wyrzucenie niepotrzebnych danych ze zbioru
    df.drop(['Wol.', 'Otwarcie', 'Max.', 'Min.'], axis=1, inplace=True)
    #Daty
    df['Data'] = df['Data'].str.replace('.', '')
    df['Data'] = pd.to_datetime(df['Data'],format='%d%m%Y')
    return df