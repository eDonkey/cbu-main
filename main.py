from flask import Flask, redirect, request, jsonify, render_template_string, url_for
from flask_restx import Api, Resource, fields
import json

app = Flask(__name__)

CODIGOS_ENTIDAD = {
    '005': 'The Royal Bank of Scotland N.V.',
    '007': 'Banco de Galicia y Buenos Aires S.A.',
    '011': 'Banco de la Nación Argentina',
    '014': 'Banco de la Provincia de Buenos Aires',
    '015': 'Industrial and Commercial Bank of China S.A.',
    '016': 'Citibank N.A.',
    '017': 'BBVA Banco Francés S.A.',
    '018': 'The Bank of Tokyo-Mitsubishi UFJ, LTD.',
    '020': 'Banco de la Provincia de Córdoba S.A.',
    '027': 'Banco Supervielle S.A.',
    '029': 'Banco de la Ciudad de Buenos Aires',
    '030': 'Banco Central de la República Argentina',
    '034': 'Banco Patagonia S.A.',
    '044': 'Banco Hipotecario S.A.',
    '045': 'Banco de San Juan S.A.',
    '046': 'Banco do Brasil S.A.',
    '060': 'Banco de Tucumán S.A.',
    '065': 'Banco Municipal de Rosario',
    '072': 'Banco Santander Río S.A.',
    '083': 'Banco del Chubut S.A.',
    '086': 'Banco de Santa Cruz S.A.',
    '093': 'Banco de La Pampa Sociedad de Economía Mixta',
    '094': 'Banco de Corrientes S.A.',
    '097': 'Banco Provincia del Neuquén S.A.',
    '143': 'Brubank S.A.U.',
    '147': 'Banco Interfinanzas S.A.',
    '150': 'HSBC Bank Argentina S.A.',
    '158': 'Openbank',
    '165': 'JP Morgan Chase Bank N.A. (Sucursal Buenos Aires)',
    '191': 'Banco Credicoop Cooperativo Limitado',
    '198': 'Banco de Valores S.A.',
    '247': 'Banco Roela S.A.',
    '254': 'Banco Mariva S.A.',
    '259': 'Banco Itaú Argentina S.A.',
    '262': 'Bank of America National Association',
    '266': 'BNP Paribas',
    '268': 'Banco Provincia de Tierra del Fuego',
    '269': 'Banco de la República Oriental del Uruguay',
    '277': 'Banco Sáenz S.A.',
    '281': 'Banco Meridian S.A.',
    '285': 'Banco Macro S.A.',
    '295': 'American Express Bank LTD. S.A.',
    '299': 'Banco Comafi S.A.',
    '300': 'Banco de Inversión y Comercio Exterior S.A.',
    '301': 'Banco Piano S.A.',
    '305': 'Banco Julio S.A.',
    '309': 'Nuevo Banco de La Rioja S.A.',
    '310': 'Banco del Sol S.A.',
    '311': 'Nuevo Banco del Chaco S.A.',
    '312': 'MBA Lazard Banco de Inversiones S.A.',
    '315': 'Banco de Formosa S.A.',
    '319': 'Banco CMF S.A.',
    '321': 'Banco de Santiago del Estero S.A.',
    '322': 'Banco Industrial S.A.',
    '325': 'Deutsche Bank S.A.',
    '330': 'Nuevo Banco de Santa Fe S.A.',
    '331': 'Banco Cetelem Argentina S.A.',
    '332': 'Banco de Servicios Financieros S.A.',
    '336': 'Banco Bradesco Argentina S.A.',
    '338': 'Banco de Servicios y Transacciones S.A.',
    '339': 'RCI Banque S.A.',
    '340': 'BACS Banco de Crédito y Securitización S.A.',
    '341': 'Más Ventas S.A.',
    '384': 'Wilobank S.A.',
    '386': 'Nuevo Banco de Entre Ríos S.A.',
    '389': 'Banco Columbia S.A.',
    '405': 'Ford Credit Compañía Financiera S.A.',
    '406': 'Metrópolis Compañía Financiera S.A.',
    '408': 'Compañía Financiera Argentina S.A.',
    '413': 'Montemar Compañía Financiera S.A.',
    '415': 'Transatlántica Compañía Financiera S.A.',
    '428': 'Caja de Crédito Coop. La Capital del Plata LTDA.',
    '431': 'Banco Coinag S.A.',
    '432': 'Banco de Comercio S.A.',
    '434': 'Caja de Crédito Cuenca Coop. LTDA.',
    '437': 'Volkswagen Credit Compañía Financiera S.A.',
    '438': 'Cordial Compañía Financiera S.A.',
    '440': 'Fiat Crédito Compañía Financiera S.A.',
    '441': 'GPAT Compañía Financiera S.A.',
    '442': 'Mercedes-Benz Compañía Financiera Argentina S.A.',
    '443': 'Rombo Compañía Financiera S.A.',
    '444': 'John Deere Credit Compañía Financiera S.A.',
    '445': 'PSA Finance Argentina Compañía Financiera S.A.',
    '446': 'Toyota Compañía Financiera de Argentina S.A.',
    '448': 'Finandino Compañía Financiera S.A.',
    '453': 'Naranja X',
    '992': 'Provincanje S.A.'
}


def calcular_digito_verificador(numero, multiplicadores):
    suma = sum(int(d) * m for d, m in zip(numero, multiplicadores))
    resto = suma % 10
    return (10 - resto) % 10

def decodificar_cbu(cbu):
    if len(cbu) != 22 or not cbu.isdigit():
        raise ValueError("La CBU debe tener exactamente 22 dígitos numéricos.")

    entidad = cbu[0:3]
    sucursal = cbu[3:7]
    digito_verificador_1 = int(cbu[7])
    bloque1 = cbu[0:7]
    multiplicadores_bloque1 = [7, 1, 3, 9, 7, 1, 3]
    dv1_calculado = calcular_digito_verificador(bloque1, multiplicadores_bloque1)

    cuenta = cbu[8:21]
    digito_verificador_2 = int(cbu[21])
    bloque2 = cbu[8:21]
    multiplicadores_bloque2 = [3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3]
    dv2_calculado = calcular_digito_verificador(bloque2, multiplicadores_bloque2)

    if digito_verificador_1 != dv1_calculado or digito_verificador_2 != dv2_calculado:
        raise ValueError("Los dígitos verificadores son incorrectos.")

    nombre_banco = CODIGOS_ENTIDAD.get(entidad, "Entidad desconocida")

    return {
        "entidad": {
            "codigo": entidad,
            "nombre": nombre_banco
        },
        "sucursal": sucursal,
        "cuenta": cuenta,
        "digitos_verificadores": {
            "bloque1": digito_verificador_1,
            "bloque2": digito_verificador_2
        }
    }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Decodificador de CBU</title>
    <link rel="icon" type="image/png" href="/static/images/logo.png"> <!-- Favicon -->
    <style>
        body { font-family: Arial; padding: 40px; background: #f4f4f4; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; }
        .logo { display: block; margin: 0 auto 20px; max-width: 230px; }
        input[type=text] { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; }
        .error { color: red; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        table, th, td { border: 1px solid #ccc; }
        th, td { padding: 10px; text-align: left; }
        th { background-color: #f4f4f4; }
        .alert { padding: 15px; margin-bottom: 20px; border: 1px solid transparent; border-radius: 5px; }
        .alert-info { background-color: #e9f7fd; border-color: #bce8f1; color: #31708f; }
        footer { text-align: center; margin-top: 20px; font-size: 0.9em; color: #555; }
        footer a { color: #007bff; text-decoration: none; }
        footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <img src="/static/images/logo.png" alt="Logo InfoCBU" class="logo"> <!-- Logo -->
        <h1>Decodificador de CBU</h1>
        <div class="alert alert-info">
            <strong>ATENCIÓN:</strong> Esta herramienta es solo para fines educativos y no debe usarse para realizar transacciones financieras.
        </div>
        <div class="alert alert-info">
            <strong>ATENCIÓN:</strong> Este sitio no utiliza cookies ni guarda ningún dato. Es un sitio de solo lectura.
        </div>
        <form method="POST">
            <input type="text" name="cbu" placeholder="Ingrese su CBU" required maxlength="22">
            <button type="submit">Decodificar</button>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        {% if resultado %}
        <div class="result">
            <h2>Resultado</h2>
            <table>
                <tr>
                    <th>Campo</th>
                    <th>Valor</th>
                </tr>
                <tr>
                    <td>Entidad</td>
                    <td>{{ resultado['entidad']['nombre'] }} ({{ resultado['entidad']['codigo'] }})</td>
                </tr>
                <tr>
                    <td>Sucursal</td>
                    <td>{{ resultado['sucursal'] }}</td>
                </tr>
                <tr>
                    <td>Cuenta</td>
                    <td>{{ resultado['cuenta'] }}</td>
                </tr>
                <tr>
                    <td>Dígito Verificador Bloque 1</td>
                    <td>{{ resultado['digitos_verificadores']['bloque1'] }}</td>
                </tr>
                <tr>
                    <td>Dígito Verificador Bloque 2</td>
                    <td>{{ resultado['digitos_verificadores']['bloque2'] }}</td>
                </tr>
            </table>
        </div>
        {% endif %}
    </div>
    <footer>
        <p>Copyleft &copy; 2025 - v1.1.0 Este proyecto es de uso libre. <a href="https://github.com/eDonkey/cbu-main/issues">Feedback</a> - <a href="https://github.com/eDonkey/cbu-main/blob/main/README.md">Github Readme</a></p>
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    resultado = None
    if request.method == 'POST':
        cbu = request.form.get('cbu', '').strip()
        try:
            resultado = decodificar_cbu(cbu)  # Pass the dictionary directly
        except ValueError as e:
            error = str(e)
    return render_template_string(HTML_TEMPLATE, error=error, resultado=resultado)

@app.route('/api/decodificar', methods=['POST'])
def decode():
    try:
        # Parse JSON request
        data = request.get_json()
        if not data or 'cbu' not in data:
            return jsonify({"error": "Se requiere el campo 'cbu' en el cuerpo de la solicitud"}), 400

        cbu = data['cbu'].strip()
        if not cbu.isdigit() or len(cbu) != 22:
            return jsonify({"error": "La CBU debe tener exactamente 22 dígitos numéricos"}), 400

        # Decode the CBU
        resultado = decodificar_cbu(cbu)
        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500



if __name__ == '__main__':
    app.run(debug=False)