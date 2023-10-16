# Descripción
Este módulo permite realizar peticiones a la api de mercadopublico.cl 
e ingresar dicha información en la base de datos de odoo.

Adicionalmente se crea una vista interna que clasifica a las unidades de compra
en base a diversos criterios de análisis (20 posiciones en el ranking).

Posteriormente envía la información al CRM para que los agentes de ventas tengan 
una ventaja en sus gestiones comerciales.

# Dependencias
## Módulos Odoo
- 'crm'
- 'opens_licitacion_crm'
## Librerías de Python
- 'pandas'
- 'requests'

# Dependencias externas
Dado que la información es recabada de la api de mercado público, cualquier 
falla o caída de esta puede afectar al correcto funcionamiento del módulo.

# Instrucciones de Instalación
- En construcción ...
