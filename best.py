from symulation import *
from import_df import *

def best(DAYS, AMOUNT, BUY_SPACE, DAYS_AVG, WAITER):
    search_list = []
    parameters = {
        "zakres dni": DAYS,
        "kwota": AMOUNT,
        "co ile dni kupno": BUY_SPACE
    }
    best = {
        "średnia_krocząca": int,
        "poczekaj": int,
        "wynik": -99999999
    }
    df = import_df(days_range=DAYS)

    #szukanie parametrów z przedziału:
    list_of_moving_average = np.array(range(7, 40, 3))
    list_of_wait = np.array(range(1, 15, 3))

    for y in list_of_moving_average:
        for z in list_of_wait:
            model = Symulation(
                df=df, 
                amount=AMOUNT, 
                every_x_days=BUY_SPACE, 
                moving_average=y, 
                wait=z
                )
            model.calc_moving_average()
            model.strategy()
            payment, value, profit = model.calc_profits()
            res = round(value/payment*100-100, 2)

            search_list.append(f'"średnia_krocząca": {y} "poczekaj": {z} "wynik": {res}')

            if res > best["wynik"]:
                best["wynik"] = res
                best["średnia_krocząca"] = y
                best["poczekaj"] = z

    return best, parameters, search_list