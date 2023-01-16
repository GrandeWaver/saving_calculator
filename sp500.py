import time
import streamlit as st
from symulation import *
from import_df import *
from best import best


st.set_page_config(layout="wide")

st.title("Oszczędzanie")

col1,col2, col3 = st.columns([1,2,1])

#COLUMN 2
col2.subheader("Konfiguracja")

DAYS = col2.slider("Zakres dni", min_value=30, max_value=5000, value=70)
AMOUNT = col2.number_input("Kwota", value=200)
BUY_SPACE = col2.number_input("Co ile dni kupujemy", value=30)

with col2.expander("więcej"):
    DAYS_AVG = st.number_input("średnia krocząca", value=30)
    WAITER = st.number_input("poczekaj (po ilu dodatkowych dniach od spadku kupić)", value=5)

#COLUMN 1
col1.subheader("Informacje")
with col1.expander("Strategia oszczędzania", expanded=True):
    st.write(f"Co **{BUY_SPACE} dni** odłóż **{AMOUNT} $** na zakup indeksu, poczekaj **{DAYS} dni** i ciesz się wynikami. W tym konkretnym modelu **dodatkowo** algorytm 'kupuje' indeks **{WAITER} dni** po tym jak **obecna cena jest niższa ze średniej ceny z {DAYS_AVG} dni**. Ten prosty sposób na kupowanie jest zastosowany przez bota, jednak wdrożenie go w życie nie jest czymś niemożliwym. Wystarczy co jakiś czas sprawdzać kurs indeksu i dokupować na lokalnych dołkach.")
with col1.expander("Czym jest S&P500"):
    st.write("S&P 500 – indeks giełdowy, w skład którego wchodzi 500 przedsiębiorstw o największej kapitalizacji, notowanych na New York Stock Exchange i NASDAQ. Są to głównie przedsiębiorstwa amerykańskie.")
with col1.expander("Jak oszczędzać"):
    st.video('https://www.youtube.com/embed/6H3Bc5nQig0?start=74')
with col1.expander("Czym jest fundusz inwestycyjny"):
    st.write('To forma wspólnego inwestowania polegająca na zbiorowym lokowaniu środków pieniężnych wpłaconych przez uczestników funduszu.')
with col1.expander("Co zamiast indeksu lub funduszu?"):
    st.write('**Kupując akcje**, inwestor staje się współwłaścicielem spółki, zarabia na wzroście kursu lub na wypłacanej dywidendzie. **W przypadku obligacji** zyskiem są odsetki od pożyczonej emitentowi kwoty — mogą być one wypłacane cyklicznie lub w momencie, gdy upłynie czas trwania umowy.')


#WYKONYWANIE SKRYPTU
if col2.button('Przetestuj'):
    progress_bar = col2.progress(0)
    for perc_completed in range(100):
        time.sleep(0.0001)
        progress_bar.progress(perc_completed+1) 
    
    #BACKEND
    df = import_df(days_range=DAYS)
    model = Symulation(
        df=df, 
        amount=AMOUNT, 
        every_x_days=BUY_SPACE, 
        moving_average=DAYS_AVG, 
        wait=WAITER
        )
    model.calc_moving_average()
    model.strategy()
    fig = model.build_plot()
    payment, value, profit = model.calc_profits()

    col2.pyplot(fig)
    progress_bar.empty()
    
    #COLUMN 3
    col3.metric(label="Zainwestowano", value=f"{payment} $", delta=f"{round(value/payment*100-100, 2)}%")
    col3.metric(label="Obecna wartość", value=f'{value} $', delta=f"{round(profit, 2)} $ zysku")


#SZUKANIE NAJLEPSZYCH PARAMETRÓW
if col3.button('Znajdź najlepszą konfigurację'):
    progress_bar = col3.progress(0)
    info = col3.empty()

    for perc_completed in range(DAYS):
        time.sleep(0.01)
        info.empty()
        progress_bar.progress(round(perc_completed/DAYS*100)) 

    best_parameters, for_parameters, search_list = best(DAYS, AMOUNT, BUY_SPACE, DAYS_AVG, WAITER)

    progress_bar.empty()
    time.sleep(0.1)

    for perc_completed, element in enumerate(search_list):
        info.info(element, icon="⚠️")
        time.sleep(0.03)
        info.empty()
        progress_bar.progress(round(perc_completed/len(search_list)*100)) 

    time.sleep(2)
    col3.write(f'dla:')
    col3.write(for_parameters)
    col3.write(f'najlepsze parametry to:')
    col3.write(best_parameters)

    progress_bar.empty()






