from chatgui import inizia

utente = ''
res = inizia(utente, charge=True)


while utente != 'esci':
    utente = str(input(""))
    res = inizia(utente)
    print('AI:' + res)