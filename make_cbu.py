def calcular_digito_verificador(numero, multiplicadores):
    suma = sum(int(d) * m for d, m in zip(numero, multiplicadores))
    resto = suma % 10
    return (10 - resto) % 10

def construir_cbu(codigo_banco, codigo_sucursal, numero_cuenta):
    # Normalizar entradas
    banco = str(codigo_banco).zfill(3)
    sucursal = str(codigo_sucursal).zfill(4)
    cuenta = str(numero_cuenta).zfill(13)

    if len(banco) != 3 or len(sucursal) != 4 or len(cuenta) != 13:
        raise ValueError("Los datos ingresados no tienen el largo correcto.")

    # Calcular primer dígito verificador (DV1)
    bloque1 = banco + sucursal
    multiplicadores_bloque1 = [7, 1, 3, 9, 7, 1, 3]
    dv1 = calcular_digito_verificador(bloque1, multiplicadores_bloque1)

    # Calcular segundo dígito verificador (DV2)
    multiplicadores_bloque2 = [3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3]
    dv2 = calcular_digito_verificador(cuenta, multiplicadores_bloque2)

    # Armar CBU completo
    cbu = banco + sucursal + str(dv1) + cuenta + str(dv2)
    return cbu

# Ejemplo de uso
codigo_banco = '017'       # Banco Macro
codigo_sucursal = '0332'   # Ejemplo de sucursal
numero_cuenta = '4000003174267'  # 13 dígitos o menos (se rellena)

cbu_resultante = construir_cbu(codigo_banco, codigo_sucursal, numero_cuenta)
print(f"CBU generado: {cbu_resultante}")