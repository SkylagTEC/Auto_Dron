import math


def main():
    opciones = [1,2,3,4,5,6,0]
    a = [1, 2, 3]
    while True:
        print('Actividad colaborativa con Listas'.center(50))
        print(('Equipo #' + str(numero_equipo) ).center(50))
        print("Selecciona una opcion")
        print()
        print("   ,  ".join(map(str,opciones)))
        print("Para salir es 0")
        opcion = int(input('Opción: '))
        if opcion == 0:
            break
        else:
            opciones_fun(opcion)
        print('\n')

def opciones_fun(x):
    if x == 1:
        print('Realizar la opción 1')
        print(positives([-21, -31]))
        print(positives([-48, -2, 0, -47, 45]))
        print(positives([-9, -38, 49, -49, 32, 6, 4, 26, -8, 45]))
        print(positives([-27, 48, 13, 5, 27, 5, -48, -42, -35, 49,
                     -41, -24, 11, 29, 33, -8, 45, -44, 12, 46]))
        print(positives([-2, 0, 27, 47, -13, -23, 8, -28, 23, 7,
                     -29, -24, -30, -6, -21, -17, -35, -8, -30,
                     -7, -48, -18, -2, 1, -1, 18, 35, -32, -42,
                     -5, 46, 8, 0, -31, -23, -47, -4, 37, -5,
                     -45, -17, -5, -29, -35, -2, 40, 9, 25, -11,
                     -32]))

    elif x == 2:
        print('Realizar la opción 2')
        print(dotproduct([], []))
        print(dotproduct([1, 2, 3], [4, 5, 6]))
        print(dotproduct([1.3, 3.4, 5.7, 9.5, 10.4],[-4.5, 3.0, 1.5, 0.9, 0.0]))
        print(dotproduct([92, -39, 82, 16, -64, -1, -16, -45, -7,39, 45, 0, 34, -3, -51, 71, 23, -8, 41, -40],[-50, -81, 94, -84, 47, 86, 52, 19, -57, 36,
                      -20, 11, -42, 48, 14, 13, 9, -67, 92, 96]))

    elif x == 3:
        print('Realizar la opción 3')
        print(replicate(7, []))
        print(replicate(0, ['a', 'b', 'c']))
        print(replicate(3, ['a']))
        print(replicate(3, ['a', 'b', 'c']))
        print(replicate(4, [1, 2, 3, 4]))
    elif x == 4:
        print('Realizar la opción 4')
        print(fibo(0))
        print(fibo(1))
        print(fibo(2))
        print(fibo(5))
        print(fibo(10))
        print(fibo(20))
        print(fibo(30))
        print(fibo(100))

    elif x == 5:
        print('Realizar la opción 5')
        print(deviation([42]))
        print(deviation([10, 20]))
        print(deviation([1, 2, 3, 4, 5]))
        print(deviation([7, 7, 7, 7, 7, 7, 7]))
        print(deviation([32, 88, 20, 26, 14, 24, 26, 44, 14, 94, 94, 72, 
                     8, 46, 92, 50, 38, 56, 60, 84]))

    elif x == 6:
        print(compress(['a', 'a', 'a', 'a', 'b', 'c', 'c', 'a', 'a', 'd',
                    'e', 'e', 'e', 'e']))
        print(compress(['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']))
        print(compress(['a', 'b', 'c', 'd']))
        print(compress([]))
        
    else:
        print('Opción no válida, intenta de nuevo')

def positives(x):
    numeros_correjidos = []
    for i in x:
        if i >=  0:
            numeros_correjidos.append(i)
    print("  ")
    return (f"Lista nueva {numeros_correjidos}")
    
def  dotproduct(a, b):
    contador = 0
    for i in range(len(b)):
        contador = (a[i] * b[i]) + contador
    return (contador)
    
def replicate(n,x):
    lista_nueva = []
    if n> 0:
        lista_nueva = x*n
    return(sorted(lista_nueva))

def fibo(n):
    fibonacci_sequence = []
    if n >= 1:
        fibonacci_sequence.append(0)
    if n >= 2:
        fibonacci_sequence.append(1)
    
    while len(fibonacci_sequence) < n:
        next_number = fibonacci_sequence[-1] + fibonacci_sequence[-2]
        fibonacci_sequence.append(next_number)
    
    return fibonacci_sequence

def deviation(d):
    cantidad = len(d)
    m = sum(d)/cantidad
    sum_squared_diff = 0
    for xi in d:
        diff = xi - m      
        squared_diff = diff ** 2  
        sum_squared_diff += squared_diff 
    standard_deviation = math.sqrt(sum_squared_diff / cantidad)
    return standard_deviation
        
def compress(x):
    if not x:
        return []
    lista_nueva = [x[0]]    
    for i in range(1, len(x)):  
        if x[i] != x[i - 1]:  
            lista_nueva.append(x[i])
                    
    return lista_nueva        
    
numero_equipo = 7

main()
