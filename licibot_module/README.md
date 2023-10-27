## Licibot
- **Technical Name**: licibot_module
- **Version**: 15.0.0.1.0
- **Author**: Ricardo Araya, Daniel Vásquez, Esteban Soto
- **License**: OPL-1
- **Application**: False

## Descripción
Este módulo permite realizar peticiones a la api de mercadopublico.cl 
e ingresar dicha información en la base de datos de odoo.

Adicionalmente se crea una vista interna que clasifica a las unidades de compra
en base a diversos criterios de análisis (20 posiciones en el ranking).

Posteriormente envía la información al CRM para que los agentes de ventas tengan 
una ventaja en sus gestiones comerciales.

## Dependencias
### Módulos Odoo
- 'crm'
- 'opens_licitacion_crm' v15

### Librerías de Python
- 'pandas'
- 'requests'
- 'scipy'
- 'numpy'
- 'scikit-learn'

## Dependencias externas
Dado que la información es recabada de la api de mercado público, cualquier 
falla o caída de esta puede afectar al correcto funcionamiento del módulo.

## Instrucciones de Instalación
- En construcción ...

## Credit(s)
### Icon
- Icon made by Daniel Vásquez 

### Contributor
- Nicolas Pinilla 
- Ricardo Araya ![Ricardo Araya LinkedIn](https://www.linkedin.com/in/ricardo-araya-calfio/)
- Daniel Vásquez ![Daniel Vásquez LinkedIn](https://www.linkedin.com/in/daniel-vasquez-r/)
- Esteban Soto ![Esteban Soto LinkedIn](https://www.linkedin.com/in/esteban-soto-valenzuela/)

![Licibot Logo](static/description/icon.png "Licibot")
