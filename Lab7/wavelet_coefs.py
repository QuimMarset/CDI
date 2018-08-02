



def definir_wavelet(coeficientes):
    suma = 0
    suma_cuadrados = 0
    for coef in coeficientes:
        suma += coef
        suma_cuadrados += coef**2
    print("Condicion 1:", suma)
    print("Condicion 2:", suma_cuadrados)



coeficientes = [0.46, 0.8421, 0.2471, -0.135]
coeficientes2 = [0.06, 1.242, -0.1529, 0.265]
definir_wavelet(coeficientes)