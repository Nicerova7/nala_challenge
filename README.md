### Guia del repositorio


#### Notebooks

* Aqui encontraremos:
  - requeriments.txt para ejecutar los notebooks
  - EDA_1 : Análisis EDA.
  - Clasificación: Clasificación de **clientes**.
  - Detección de fraude: Modelo que detecta fraude de transacciones.

#### App

Aqui encontraremos
    - proyecto para desplegar nuestro modelo y usarlo con api


### Como ejecutar

#### Notebook:
    * Creando entorno virtual:

```
$ virtualenv nombre_entorno
$ pip install -r requirements.txt
$ jupyter notebook
- Abrir EDA_1
- Abrir Clasificacion_2
- Abrir Deteccion de fraude_3
```

#### App:
    * Creamos entorno virtual
```
$ virtualenv nombre_entorno
$ pip install -r requirements.txt
$ uvicorn main:app --reload 
- Nos ubicamos en http://127.0.0.1:8000/docs#/
- Nos ubicamos en el api post /files/
- Luego subimos usamos como input el archivo data_input.csv
- Considerar que este archivo solo tomara en cuenta un valor (el ultimo). Favor de usar solo uno.
- Considerar usar ese excel que ya tiene la estructura (body) del input
```

### Imágenes de app funcionando

Deploy locally

![](/images_md/fastapi1.PNG)
![](/images_md/fastapi2.PNG)
![](/images_md/fastapi3.PNG)
![](/images_md/fastapi4.PNG)


#### Deploy heroku
TODO

Nilton Rojas Vales
2021