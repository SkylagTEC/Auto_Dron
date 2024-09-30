s = "Esta es una prueba"
vocales = 0
consonantes = 0
s =s.lower()
for i in range(len(s)):
    print(s[i],end=" ")
    if s[i] in ["a","e","i","o","u"]:
        vocales += 1
    else:
        consonantes += 1
print()
print()


v = 0
for c in s:
    print(c,end=" ")
    if c in "aeiou":
        v+= 1

print()
print(f"Numero de vocales {vocales}")
print(f"Numero de consonantes {consonantes}")
print(f"segundas palabras {v}")

lista = []
for i in range(0,11,2):
    lista.insert(0,i)
    
for (x) in lista:
    print(x,end=" ")
