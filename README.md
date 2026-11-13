English version: [README.en.md](README.en.md)

# verificacion-determinista-ia

[![ci](https://github.com/jleonceo/verificacion-determinista-ia/actions/workflows/ci.yml/badge.svg)](https://github.com/jleonceo/verificacion-determinista-ia/actions/workflows/ci.yml)

**El que recuenta cuando la IA ya ha contestado: comprobaciones de coherencia que no dependen de la IA**

## El problema

Cuando un programa corriente se rompe, avisa: salta un mensaje en la pantalla, se para todo y quien
lo mira sabe que hay algo que arreglar. Con esa manera de fallar llevamos conviviendo cuarenta años.

Un sistema que trabaja con inteligencia artificial no se rompe así. Imagina que le pides corregir el
tratamiento del IVA de una factura. Corrige el apunte. Y el apunte queda impecable, con lo anotado a
la izquierda sumando lo mismo que lo anotado a la derecha. No salta ningún aviso en la pantalla,
porque no hay nada de qué avisar.

Pero esa corrección tenía que llegar además al cierre del ejercicio, a la apertura del siguiente, a
la declaración del trimestre y al cuadro de mando de dirección. Cuatro sitios más. Si uno se queda
sin tocar, la pieza que se quedó atrás sigue estando cuadrada y correcta por dentro. Lo único que
pasa es que deja de corresponder con las demás. Eso se descubre meses después, cuando un total no
encaja con otro total y ya nadie recuerda qué se cambió aquel día.

Hay una segunda avería igual de callada. Cada pocos meses los modelos de inteligencia artificial se
actualizan y al actualizarse cambian de comportamiento, de manera que una vigilancia montada sobre
un modelo tampoco piensa igual de un mes para otro. De ese cambio de criterio no avisa nadie.

## Qué hay en este repositorio

Un programa de ciento cuatro líneas, sus pruebas, dos ficheros de datos inventados y la explicación
de dónde salió todo. Lo único que hace el programa es leer unas cuentas y contestar con una palabra,
`SANO` o `ENFERMO`.

Para decidirlo no le pregunta a ninguna inteligencia artificial. Suma, resta y compara. Tampoco
necesita conexión a internet. Ni base de datos. Ni ninguna pieza de software añadida a las que
Python trae de fábrica.

**Determinista** quiere decir que con los mismos datos da siempre la misma respuesta, hoy y dentro de
tres años, se haya cambiado de modelo por medio o no se haya cambiado.

Dentro del sistema, su sitio está detrás de la inteligencia artificial: no evita que el ayudante se
equivoque, avisa cuando ya lo ha hecho.

## El ejemplo

Los datos de ejemplo son siete apuntes de un libro de contabilidad de doble partida y los cinco
saldos que salen de ellos. La cuenta 600, la de compras, recibe un solo apunte de 1.000,00 euros en
el libro, y el fichero de saldos declara para ella esos mismos 1.000,00 euros. Cuadran.

El día que alguien toque uno de los dos ficheros sin tocar el otro dejarán de cuadrar. Ese es
exactamente el descuido del apartado anterior. Para cazarlo, el programa vuelve a calcular el saldo
de cada cuenta desde el detalle y lo enfrenta con el saldo declarado.

Así entra una línea del libro:

```
2,2026-01-10,430,Cliente,1210.00,0.00
```

Asiento número 2 del 10 de enero, cuenta 430 (clientes), mil doscientos diez euros a la izquierda y
nada a la derecha. Desde esa línea, el recorrido dentro del programa tiene cinco pasos.

1. **Se carga.** Las siete líneas del libro y las cinco del resumen pasan de texto a números
   exactos.
2. **Se suman las dos columnas.** 3.420,00 contra 3.420,00.
3. **Se agrupa por asiento.** Los tres asientos cuadran cada uno por su cuenta.
4. **Se recalculan los cinco saldos** desde el detalle y se enfrentan uno a uno con el resumen
   escrito.
5. **Se dicta el veredicto.** Las tres reglas en verde dan `SANO`; una sola en rojo da `ENFERMO`.

Al terminar, el programa devuelve un cero o un uno, que es como un programa le dice a otro «todo
bien» o «para». Con eso se cuelga de un proceso automático que se detenga solo en cuanto algo deje
de cuadrar.

## Los conceptos

Una **invariante** es una regla que en unos datos correctos se cumple siempre y sin excepción que
valga. Por eso admite una respuesta de una sola palabra: o se cumple, o hay algo estropeado.
En este repositorio las invariantes son tres. Cada una vigila un nivel distinto.

- INV-1, el cuadre global. Se suma el libro entero y se comprueba que la columna de la izquierda
  da lo mismo que la de la derecha, 3.420,00 euros por cada lado en los datos de ejemplo.
- INV-2, el cuadre de cada asiento por separado. Hace falta porque un descuadre y su contrario
  se anulan entre ellos, y desde el total ya nadie los ve.
- INV-3, la coherencia entre capas. Es la que responde a la avería del IVA en cascada.

En un sistema de datos, una **capa** es cada nivel de elaboración por el que pasa la misma
información. Aquí hay dos: el libro, que guarda el detalle apunte por apunte, y el resumen por
cuenta, que guarda el saldo ya calculado de cada una y alimenta los informes. Como el resumen sale
enteramente del libro, tiene que corresponder con él.

Un **control negativo** es meter un error a propósito para comprobar que la alarma suena. Sin él
sabes que el detector no está avisando, pero no sabes si calla porque no hay nada o porque se ha
estropeado. Eso hace la segunda de las dos pruebas del repositorio: coge el resumen, le suma cien
euros a la primera cuenta y exige que INV-3 se ponga roja. El veredicto llega con el detalle puesto,
`cuenta 600 (resumen=1100.00, real=1000.00)`, mientras el libro sigue cuadrando y las otras dos
invariantes siguen en verde. Es el caso de manual. Cuadra por sí mismo y es incoherente.

Un ordenador guarda por defecto los números con decimales de una forma que arrastra un residuo
minúsculo, de modo que si le pides 0,1 más 0,2 te contesta 0,30000000000000004. Comparar dos
importes así para ver si son iguales no significa gran cosa. Este programa usa el otro modo de
cálculo que ofrece Python, el de la **aritmética exacta** con decimales. Por eso se permite un
veredicto sin tolerancias ni márgenes.

## Pruébalo

```bash
python auditor/coherencia.py        # informe sobre los datos de ejemplo
python auditor/test_coherencia.py   # las pruebas, incluido el control negativo
```

Salida sobre los datos de ejemplo, abreviada; el programa imprime además su cabecera:

```
[OK   ] INV-1 - Cuadre global (total del debe = total del haber)
         debe=3420.00  haber=3420.00  diferencia=0.00
[OK   ] INV-2 - Cuadre por asiento (cada asiento cuadra solo)
         todos los asientos cuadran
[OK   ] INV-3 - Coherencia entre capas (resumen = recalculo desde el libro)
         el resumen corresponde con el libro
VEREDICTO: SANO
```

Tarda menos de un segundo.

## Qué está medido

Ejecutado el 22/07/2026 con Python 3.14.6, sin copiar nada de la documentación:

| Comprobación | Resultado |
|---|---|
| `coherencia.py` sobre los datos de ejemplo | `SANO`, las tres invariantes en verde |
| Total del debe y total del haber | 3.420,00 por cada lado |
| `test_coherencia.py`, dos pruebas | pasan las dos, en 0,01 segundos |
| Los cinco saldos recalculados por otra vía | coinciden con el resumen publicado |
| Control negativo de cien euros al resumen | INV-1 e INV-2 verdes, INV-3 roja, `ENFERMO` |

## El verificador está verificado en un tercio

Lo más interesante queda fuera de esa tabla y es un defecto de este mismo repositorio.

Una **prueba de mutación** consiste en estropear el programa a propósito, una pieza cada vez, y mirar
si sus propias pruebas se dan cuenta, que es la única manera de saber si unas pruebas en verde
protegen algo o solo lo parecen. Aplicada a este repositorio el 22/07/2026, desactivando una
invariante cada vez, el resultado es este:

| Avería plantada | Las pruebas |
|---|---|
| INV-1 declarada siempre en verde | pasan igual |
| INV-2 declarada siempre en verde | pasan igual |
| INV-3 declarada siempre en verde | fallan; queda cazada |

Dos de las tres reglas se pueden desactivar del todo sin que las pruebas se enteren. La razón está en
el propio control negativo, que planta su error en el resumen, la única capa de la que se ocupa
INV-3. A nadie se le ocurrió plantar además un descuadre en el libro, así que INV-1 e INV-2 se
quedaron sin quien las examine.

Conviene pensar en lo que eso significa. Un repositorio que va precisamente de verificar lleva el
aviso escrito desde el 20/07/2026 dentro de `.github/workflows/ci.yml`, con fecha y sin arreglar,
así que esta portada prefiere repetirlo antes que enseñar un «todo verde» que no distinga entre las
tres reglas. Ampliar la cobertura a INV-1 e INV-2 está pendiente y vale más que cualquier otra cosa que
se pueda añadir aquí.

## Cuándo no sirve

**El error copiado en las dos capas pasa.** Si el libro y el resumen se equivocan de la misma manera,
coinciden, y coincidir es todo lo que aquí se comprueba. Lo único que mira son correspondencias
internas; de la realidad de fuera no sabe nada, ni de si la factura existió, ni de si el proveedor es
quien dice ser, ni de si la cuenta elegida era la que tocaba.

**El apunte inflado por los dos lados pasa.** Probado: a la primera línea del libro se le pusieron
quinientos euros de más a la izquierda y quinientos de más a la derecha, y el veredicto siguió siendo
`SANO`. Las tres invariantes miran diferencias. A una diferencia le da igual que las dos cifras
hayan crecido a la vez.

**Un dato corrupto no da `ENFERMO`, da un plantón.** Con una casilla de importe vacía en el fichero,
el programa se para con un mensaje escrito para programadores, sin llegar a dictar veredicto.

**El tamaño le pesa.** Para comprobar el cuadre asiento por asiento, el programa recorre el libro
entero una vez por cada asiento, de manera que el tiempo crece con el cuadrado del tamaño. Medido:
quinientos asientos en 0,03 segundos, mil en 0,11, dos mil en 0,45 y cuatro mil en 1,83. Al doble de
asientos, cuatro veces de espera. Con las siete líneas del ejemplo esto no se nota, y con un libro de
un año de decenas de miles de apuntes la espera se convierte en minutos.

## Qué llevarse

**Lo verosímil se parece a lo correcto más de lo que nos conviene.** Un sistema de inteligencia
artificial no se cae: sigue contestando con buena forma mientras el fondo se le descuadra por dentro.
Alguien tiene que volver a contar. Y quien recuenta ha de ser distinto de quien contó.

**La aritmética no cambia de opinión cuando cambias de modelo.** Ahí está el valor de que la
vigilancia sea corta y tonta, porque ciento cuatro líneas de sumar y comparar valdrán dentro de tres
años lo mismo que valen hoy, y ninguna actualización se las llevará por delante.

**Una alarma sin control negativo todavía no es una alarma.** Y un banco de pruebas en verde tampoco
demuestra gran cosa por sí solo: dos de las tres reglas de este repositorio se apagan sin que sus
pruebas se enteren.

## Qué abrir y en qué orden

| Orden | Fichero | Qué encontrarás |
|---|---|---|
| 1 | `caso_real.md` | De dónde salió esto: una corrección de IVA en cascada |
| 2 | `datos_ejemplo/libro_sintetico.csv` | Siete apuntes inventados; se abre con Excel |
| 3 | `datos_ejemplo/resumen_por_cuenta.csv` | Los cinco saldos que se contrastan |
| 4 | `auditor/coherencia.py` | El verificador entero, con sus tres invariantes |
| 5 | `auditor/test_coherencia.py` | Dos pruebas, una de ellas el control negativo |
| 6 | `.github/workflows/ci.yml` | El vigilante automático, con la confesión de cobertura dentro |

## Estructura

```
verificacion-determinista-ia/
├── auditor/
│   ├── coherencia.py          el verificador (solo aritmética, sin IA ni base de datos)
│   └── test_coherencia.py     pruebas + control negativo
├── datos_ejemplo/
│   ├── libro_sintetico.csv        libro de doble partida (datos inventados)
│   └── resumen_por_cuenta.csv     resumen derivado (la «capa» que se contrasta)
├── .github/workflows/ci.yml   ejecuta las pruebas en cada push
├── caso_real.md               de dónde viene esto (sin datos reales)
├── requirements.txt · LICENSE · .gitignore
```

## Privacidad

El caso de ejemplo utiliza un conjunto de datos sintético; no contiene información real ni personal.

## Ecosistema

Este repositorio es la pieza de **verificación** de un conjunto de proyectos sobre sistemas de
agentes de IA:

- **[gobernanza-skills-analiticas](https://github.com/jleonceo/gobernanza-skills-analiticas)**, el método de gobernanza contado en prosa. Este repo es el código de una de sus piezas: la verificación que recomprueba el estado sin IA.
- **[accounting-agent-swarm](https://github.com/jleonceo/accounting-agent-swarm)**, el enjambre de agentes que genera la contabilidad. Estas comprobaciones son el guardarraíl que lo mantiene cuadrado.
- **[audience-analyst-swarm](https://github.com/jleonceo/audience-analyst-swarm)**, el mismo patrón de enjambre llevado a la analítica de audiencias en cuestión de días.
- **[agent-memory-governance](https://github.com/jleonceo/agent-memory-governance)**, la gobernanza de la memoria del agente. Su hermano: allí se gobierna lo que el agente *recuerda*; aquí, la coherencia de los *datos*.
- **[claude-code-context-management](https://github.com/jleonceo/claude-code-context-management)**, la gestión de los ficheros de contexto de Claude Code, para que CLAUDE.md y MEMORY.md no saturen el contexto.
- **[llm-eval-contable](https://github.com/jleonceo/llm-eval-contable)**, el examen que mide si la skill *acierta*. Complementario: aquel verifica las *respuestas*; este, que los *datos* cuadren entre capas.
- **[orquestacion-enjambres-ia](https://github.com/jleonceo/orquestacion-enjambres-ia)**, el enrutado multi-agente. Aquel verifica a qué agente va cada petición; este, que los datos cuadren.
- **[tu-primer-asistente-ia-web](https://github.com/jleonceo/tu-primer-asistente-ia-web)**, la entrada sin tecnicismos: qué es un asistente de IA, para quien empieza de cero.
- **[tesoreria-forecast-ia](https://github.com/jleonceo/tesoreria-forecast-ia)**, previsión de caja por descomposición con backtesting, más ratios y aging.
- **[control-interno-fraude-ia](https://github.com/jleonceo/control-interno-fraude-ia)**, detección de fraude contable con aritmética, dentro de un marco de control interno.

---

*Datos sintéticos · sin información real ni personal.*
