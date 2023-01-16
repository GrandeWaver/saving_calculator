import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math


class Symulation:
    def __init__(self, df, amount, every_x_days, moving_average, wait):
        self.df = df
        self.amount = amount
        self.every_x_days = every_x_days
        self.moving_average = moving_average
        self.wait = wait
    

    #ŚREDNIA KROCZĄCA
    def calc_moving_average(self):
        _values = []
        _averages = []

        for n, a in enumerate(self.df['Cena']):
            _values.append(a)
            if n >= self.every_x_days:
                _values.pop(0)
                avg = sum(_values) / len(_values)
                _averages.append(avg)
            else:
                _averages.append(self.df['Cena'].iloc[0])
        self.df["Srednia"] = _averages
    

    #STRATEGIA 
    def strategy(self):
        self.df['Kupno'] = np.nan
        counter = 0
        waiter = 0

        for index, row in self.df.iterrows():
            #pierwszy zakup
            if counter == 0:
                self.df.loc[index, 'Kupno'] = row['Cena']
            #aby nie czekać w nieskończoność przy niesutannej hossie
            elif counter == 2*self.every_x_days-1:
                self.df.loc[index, 'Kupno'] = row['Cena']
                counter -= self.every_x_days
            #lokalny dołek
            elif counter >= self.every_x_days:
                if row['Cena'] < row['Srednia']:
                    if waiter == self.wait:
                        self.df.loc[index, 'Kupno'] = row['Cena']
                        counter = 0
                        waiter = 0
                    else:
                        waiter += 1
                else:
                    row['Kupno'] = None
            counter += 1

    #WYKRES
    def build_plot(self):
        fig, ax = plt.subplots(figsize=(32, 9))
        ax.plot(self.df['Data'], self.df['Cena'], label='cena')
        ax.plot(self.df['Data'], self.df['Srednia'], label=f'średnia cena z {self.every_x_days} dni')
        ax.plot(self.df['Data'], self.df['Kupno'], "s", label='moment kupna')
        ax.legend()
        fig.autofmt_xdate()
        return fig

            
    # OBLICZANIE ZYSKÓW
    def calc_profits(self):
        wallet = 0
        transactions = 0

        # print("\nObliczanie zysków:")

        for index, row in self.df.iterrows():
            if not math.isnan(row['Kupno']):
                _transaction = self.amount/row['Kupno']
                transactions += 1
                wallet += _transaction
                # print(f"kupno po cenie: {row['Kupno']}, zakupiono: {_transaction}, stan portfela: {wallet}")

        # print(f"ostatecznie: {wallet}")
        payment = transactions * self.amount
        value = round(wallet * self.df['Cena'].iloc[-1], 2)
        profit = value - payment
        return payment, value, profit

    
    
