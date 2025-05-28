# Decodificador de CBU API

## Descripción
Este proyecto proporciona una API y una interfaz web para decodificar el CBU (Clave Bancaria Uniforme) argentino. Valida el formato del CBU, calcula los dígitos verificadores y proporciona información sobre el banco, la sucursal y la cuenta.

## Características
- Decodificar y validar números de CBU.
- Obtener información sobre el banco y la sucursal.
- Interfaz web para ingreso manual.
- Documentación Swagger para el uso de la API.

---

## Instalación

### Requisitos
- Python 3.13 o superior.
- `pip` (administrador de paquetes de Python).
- Heroku CLI (si se despliega en Heroku).

### Clonar el repositorio
```bash
git clone https://github.com/eDonkey/cbu-main.git
cd cbu-decoder
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## Uso

### Ejecutar localmente
Para ejecutar la aplicación localmente:
```bash
python main.py
```
Visita `http://127.0.0.1:5000` en tu navegador.

---

## Documentación de la API
```

### Endpoints

#### `POST /api/decodificar`
Decodifica un CBU y obtiene sus detalles.

**Cuerpo de la solicitud**:
```json
{
  "cbu": "1234567890123456789012"
}
```

**Respuesta**:
```json
{
  "entidad": {
    "codigo": "123",
    "nombre": "Banco Ejemplo"
  },
  "sucursal": "4567",
  "cuenta": "8901234567890",
  "digitos_verificadores": {
    "bloque1": 8,
    "bloque2": 2
  }
}
```

**Respuesta de error**:
```json
{
  "error": "La CBU debe tener exactamente 22 dígitos numéricos."
}
```

---


## Estructura del proyecto
```
cbu-decoder/
├── main.py              # Archivo principal de la aplicación
├── requirements.txt     # Dependencias del proyecto
├── Procfile             # Configuración para despliegue en Heroku
└── README.md            # Documentación del proyecto
```

---

## Licencia
Copyleft &copy; 2025 - Este proyecto es de uso libre.

---

## Soporte
Para problemas o preguntas, abre un issue en el repositorio o contacta al mantenedor del proyecto.