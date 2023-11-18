<h2 align="center">
  <p align="center">Licibot</p>
  <p align="center"><img src="static/banner.png" width="1200"></p>
</h2>

- **Nombre Técnico**: licibot_module
- **Versión**: 15.0.1.0.0
- **Autor**: Ricardo Araya, Daniel Vásquez, Esteban Soto, Nicolas Pinilla
- **Licencia**: Sin especificar.
- **Aplicación**: False
<p align="center">
   <img src="https://img.shields.io/badge/ESTADO-FINALIZADO-green">
</p>

## Descripción
Este módulo permite realizar peticiones a la api de mercadopublico.cl e ingresar dicha información en la base de datos de odoo.

Adicionalmente se crea una vista interna en la base de datos que clasifica a las unidades de compra según su comportamiento en el mercado gracias técnicas de ML, concretamente un módelo K-Means, que primero separará a las unidades de compra en diferentes cluster y posteriormente asignara las posiciones en el ranking (50 posiciones cómo máximo, sin embargo, este valor se puede cambiar en las configuraciones de odoo).
Finalmente, envía la información de estas unidades de compra rankeadas al CRM de Odoo para que los distintos agentes comerciales puedan comenzar sus gestiones.

## Funcionamiento
Una vez instalado el módulo se recomienda activar el modo desarrollador y dirigirse a Ajustes > Técnico > Parámetros del sistema.
En este menú se podrá configurar los siguientes parámetros del código:

|Parámetro|Descripción|
|:-------:|:---------:|
|licibot_module.days_gone|Cantidad de días que deben transcurrir para que una unidad de compra pueda volver a ser enviada al CRM. Por defecto son 180 días (6 meses aprox.)|
|licibot_module.ranking_length|Cantidad de posiciones que considerará el ranking al momento de calcularse.|
|licibot_module.ranking_ml_length|Cantidad de posiciones que considerará el ranking al momento de calcularse. Versión Machine Learning|
|licibot_module.ip|IP del servidor en el cual operará el módulo. Misma IP del servidor en el que se aloja el sistema Odoo. Parámetro obligatorio.|
|licibot_module.token_mp|Token otorgado por mercadopubico, el cual permite tener acceso a los endpoints de la api de mercadopublico. Parámetro obligatorio.|

Una vez configure estos parametros dirijase al menú Ajustes > Técnico > Acciones planificadas y busque la palabra "Licibot".
Se mostraran todos los crones que permiten automatizar las funciones incluidas en el módulo.
Active los siguientes y configure la frecuencia a su criterio y/o necesidad:
- CRON Licibot: Extracción Licitaciones Diarias, el cuál permite que se vayan recolectando licitaciones. Se recomienda seleccionar una hora en la que el ambiente no este siendo utilizado por ejemplo 1am.
- CRON Licibot: Calcular Ranking ML, el cuál calcula las posiciones de las distintas unidades de compra en base a la información que sea recopilada.
- CRON Licibot: Enviar al CRM, que envia al CRM aquellas unidades de compra que esten en el ranking. Cabe mencionar que si una unidad de compra ya se encuentra en el CRM y sigue estando en el ranking, esta no volvera a ser enviada a menos que hayan transcurrido la cantidad de días configurada (licibot_module.days_gone) entre la fecha de la última oportunidad ingresada y la fecha actual.

Con estas configuraciones el módulo esta listo para funcionar de forma automatizada, recolectando día tras día nueva información directamente desde las licitaciones adjudicadas de mercado publico.

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
Para no sobreextender el archivo README.md se solicita que visite el <a href="static/Manual%20de%20Instalación.docx">Manual de Instalación</a> para conocer más sobre el paso a paso a seguir.

## Creditos

### Contribuidores
- Nicolas Pinilla 
- [![LinkedIn Logo](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ricardo-araya-calfio/ "Perfil de Ricardo Araya C.") Ricardo Araya C.
- [![LinkedIn Logo](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daniel-vasquez-r/ "Perfil de Daniel Vásquez R.") Daniel Vásquez R. 
- [![LinkedIn Logo](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/esteban-soto-valenzuela/ "Perfil de Esteban Soto V.") Esteban Soto V.

### Logo
- Imagen realizada por Daniel Vásquez
  
<p align="center"><img src="static/banner.png" width="400"></p>

