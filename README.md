<h2 align="center">
  <p align="center">Licibot</p>
  <p align="center"><img src="licibot_module/static/banner.png" width="1200"></p>
</h2>

- **Technical Name**: licibot_module
- **Version**: 15.0.0.1.0
- **Author**: Ricardo Araya, Daniel Vásquez, Esteban Soto, Nicolas Pinilla
- **License**: Sin especificar.
- **Application**: False

## Descripción
Este módulo permite realizar peticiones a la api de mercadopublico.cl 
e ingresar dicha información en la base de datos de odoo.

Adicionalmente se crea una vista interna que clasifica a las unidades de compra
en base a diversos criterios de análisis (20 posiciones en el ranking por defecto).

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
- 🚧 En construcción ...

## Creditos

### Icono
- Icono hecho por Daniel Vásquez 

### Contribuidores
- Nicolas Pinilla 
- [![LinkedIn Logo](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ricardo-araya-calfio/ "Perfil de Ricardo Araya C.") Ricardo Araya C.
- [![LinkedIn Logo](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daniel-vasquez-r/ "Perfil de Daniel Vásquez R.") Daniel Vásquez R. 
- [![LinkedIn Logo](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/esteban-soto-valenzuela/ "Perfil de Esteban Soto V.") Esteban Soto V.

  <p align="center"><img src="licibot_module/static/banner.png" width="400"></p>

