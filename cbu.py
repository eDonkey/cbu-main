from flask import Flask, request, jsonify, render_template_string
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
    <style>
        body { font-family: Arial; padding: 40px; background: #f4f4f4; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; }
        input[type=text] { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; }
        .error { color: red; }
        pre { background: #f1f1f1; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Decodificador de CBU</h1>
        <h3>ATENCION: Esta herramienta es solo para fines educativos y no debe usarse para realizar transacciones financieras.</h3>
        <h3>ATENCION 2: Esta herramienta no puede utilizarse con billeteras virtuales (CVU) como Mercado Pago, Ualá, etc.</h3>
        <h3>ATENCION 3: Esta herramienta no puede utilizarse con cuentas de criptomonedas.</h3>
        <h3>ATENCION 4: Esta herramienta no puede utilizarse con cuentas de bancos extranjeros (No Argentinos).</h3>
        <form method="POST">
            <input type="text" name="cbu" placeholder="Ingrese su CBU" required maxlength="22">
            <button type="submit">Decodificar</button>
        </form>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if resultado %}<div class="result"><h2>Resultado</h2><pre>{{ resultado }}</pre></div>{% endif %}
    </div>
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
            data = decodificar_cbu(cbu)
            resultado = json.dumps(data, indent=4, ensure_ascii=False)
        except ValueError as e:
            error = str(e)
    return render_template_string(HTML_TEMPLATE, error=error, resultado=resultado)

@app.route('/api/decodificar', methods=['POST'])
def api_decodificar():
    data = request.get_json()
    if not data or 'cbu' not in data:
        return jsonify({"error": "Se requiere el campo 'cbu'"}), 400
    try:
        resultado = decodificar_cbu(data['cbu'])
        return jsonify(resultado)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)