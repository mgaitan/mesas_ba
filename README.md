# Relevamiento de carga de datos sospechosa en las elecciones de Provincia de Buenos Aires

Por Martín Gaitán

- Ir al [paper](https://github.com/mgaitan/mesas_ba/tree/master/mesas_ba/mesas_sospechosas.ipynb)


## Abstract

Este trabajo es un intento de hacer el trabajo de chequeo manual de telegramas de las PASO 2017 en la provincia de Buenos Aires de una más eficientemente, detectando aquellas mesas estádisticamente raras (no quiere decir que todas las mesas listadas estén incorrectas).

Para esto realizé un programa que obtiene los datos digitalizados oficiales de cada una de las mesas desde el sitio http://www.resultados.gob.ar/inicio.htm  y los estructuré en una base de datos para hacer agregaciones y consultas.

Por ejemplo, basado en la idea de que los resultados en una mesa son similares en un circuito, se pueden detectar aquellas mesas que tienen resultados muy distintos.

Las tablas resultantes muestran algunos datos e incluyen el link para ver el telegrama en el sitio oficial para que revisemos entre tod@s.

**Gracias por difundir**

- Martín Gaitán [`@tin_nqn_`](https://twitter.com/tin_nqn_)
