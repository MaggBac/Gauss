import numpy
import time

def norma(xx):
    return (sum(x ** 2 for x in xx)) ** 0.5


def wyznacz_blad_spelnienia_url(a, x, b):
    n = a.shape[0]
    r = numpy.zeros((n,), 'd')
    for i in range(n):
        t = 0.0
        for j in range(n):
            t += a[i, j] * x[j]
        r[i] = b[i] - t
    return norma(r)


def czytaj(nazwa):
    with open(nazwa) as f:
        dane = f.readlines()
    n = len(dane)
    a = numpy.zeros((n, n), 'd')
    b = numpy.zeros((n,))
    i = 0
    for x in dane:
        x = x.split()
        for j in range(n):
            a[i, j] = float(x[j])
        b[i] = float(x[n])
        i += 1
    return n, a, b


def czy_rozwiazanie(a, x, b, tol=1e-10):
    res = wyznacz_blad_spelnienia_url(a, x, b)
    return norma(res) < tol


def czyGTr(a):
    n = a.shape
    for i in range(1, n[0]):
        for j in range(0, i):
            if (a[i, j] != 0):
                return False
    return True


def rozwiaz_uklad_trojkatny(a, b):
    # czy a jest m kw
    n = a.shape[0]
    assert a.shape == (n, n)
    assert b.shape == (n,)

    for i in range(n):
        if a[i, i] == 0.0: #element 0 na przekątnej
            return None

    x = numpy.zeros((n,))
    # przeglądamy równania od ostatniego do pierwszego
    for i in range(n - 1, -1, -1):
        # z i-tego równania wyznaczyć x[i]
        suma = 0.0
        for j in range(i + 1, n):
            suma += a[i, j] * x[j]
        x[i] = (b[i] - suma) / a[i, i]
    return x

def do_postaci_trojkatnej(a, b):
    # czy a jest m kw
    n = a.shape[0]
    assert a.shape == (n, n)
    assert b.shape == (n,)
    for i in range(0, n - 1):
        print('*')
        # i ty wiersz służy do wyzerowania element ów w i-tej kolumnie pod przekątną
        for j in range(i + 1, n):
            # za pomocą wiersza nr i modyfikujemny wiersz nr j
            # tak by wyzerować w j-tym wierszu elem z itej kolumny
            if a[i, i] != 0.:
                wsp = - a[j, i] / a[i, i]
                for k in range(i, n):
                    a[j, k] += wsp * a[i, k]
                b[j] += wsp * b[i]
            else:
                print('katastrofa!')

def do_post_troj_bez_zamiany(a,b):
    n = a.shape[0]
    assert a.shape == (n, n)
    assert b.shape == (n,)
    for i in range(n):
        m = a[i, i]
        if m == 0.0:
            return False, a, b
        for j in range(i+1, n):
            wsp = -a[j,i]/m
            for k in range(i,n):
                a[j,k] += wsp*a[i,k]
            b[j] += wsp*b[i]
    return True, a, b

def do_post_troj_z_zamiana(a,b):
    n = a.shape[0]
    assert a.shape == (n, n)
    assert b.shape == (n,)
    for i in range(n):
        m = a[i,i]
        if m ==0.0:
            j = i+1
            while (j<n):
                if a[j,i] != 0:
                    break
                j+=1
            if j<n:
                a[i], a[j] = a[j], a[i]
                b[i],b[j] = b[j], b[i]
            else:
                return False, a, b
        print('***', i, a[i,i])
        print(a)
        m=a[i,i] #OLa m = a[i]
        for j in range(i+1, n):
            wsp=-a[j,i]/m
            for k in range(i,n):
                a[j,k]+= wsp*a[i,k]
            b[j] += wsp*b[i]
    print(a)
    return True, a, b


def eliminacja_gaussa(a,b):
    w,a,b = do_post_troj_bez_zamiany(a,b)
    if w:
        return rozwiaz_uklad_trojkatny(a,b)
    else:
        return None




plik = 'trza'
n, m, r = czytaj(plik)
print(m, m.shape)
print(r, r.shape)
print("przed")
print(m)
print(r)
time1 = time.process_time()
x=eliminacja_gaussa(m,r)
print("Eliminacja Gaussa:")
print(x)
print("po")
print(m)
print(r)
time2 = time.process_time()
timeval = time2 - time1
print("Czas bez zmiany:")
print(timeval)

if x is not None:
    bladdd = wyznacz_blad_spelnienia_url(m, x, r)
    print(bladdd)
    n, m, r = czytaj(plik)
    bladdd = wyznacz_blad_spelnienia_url(m, x, r)
    print(bladdd)