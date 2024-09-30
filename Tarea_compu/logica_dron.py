list_april = []

def acumulador_list (x):
    if x not in list_april:
        list_april.append(x)
    else:
        pass

while True:
    num_april = int(input(" Agrega numero "))
    if num_april == 0:
        break
    else:
        acumulador_list(num_april)

print(list_april)