# verificacion-determinista-ia

**El que recuenta cuando la IA ya ha contestado: comprobaciones de coherencia que no dependen de la IA**
**The one that recounts after the AI has answered: coherence checks that do not depend on AI**

[Español](#español) · [English](#english)

---

## Español

### El problema

Cuando un programa corriente se rompe, avisa: salta un mensaje en la pantalla, se para todo y quien
lo mira sabe que hay algo que arreglar. Con esa manera de fallar llevamos conviviendo cuarenta años.

Un sistema que trabaja con inteligencia artificial no se rompe así. Imagina que le pides corregir el
tratamiento del IVA de una factura. Corrige el apunte, y el apunte queda impecable, con lo anotado a
la izquierda sumando lo mismo que lo anotado a la derecha. No salta ningún aviso en la pantalla,
porque no hay nada de qué avisar.

Pero esa corrección tenía que llegar además al cierre del ejercicio, a la apertura del siguiente, a
la declaración del trimestre y al cuadro de mando de dirección. Cuatro sitios más. Si uno se queda
sin tocar, la pieza que se quedó atrás sigue estando cuadrada y correcta por dentro, y lo único que
pasa es que deja de corresponder con las demás. Eso se descubre meses después, cuando un total no
encaja con otro total y ya nadie recuerda qué se cambió aquel día.

Hay una segunda avería igual de callada. Cada pocos meses los modelos de inteligencia artificial se
actualizan, y al actualizarse cambian de comportamiento, de manera que una vigilancia montada sobre
un modelo tampoco piensa igual de un mes para otro. De ese cambio de criterio no avisa nadie.

### Qué hay en este repositorio

Un programa de ciento cuatro líneas, sus pruebas, dos ficheros de datos inventados y la explicación
de dónde salió todo. Lo único que hace el programa es leer unas cuentas y contestar con una palabra,
`SANO` o `ENFERMO`.

Para decidirlo no le pregunta a ninguna inteligencia artificial: suma, resta y compara. Tampoco
necesita conexión a internet, ni base de datos, ni ninguna pieza de software añadida a las que
Python trae de fábrica.

**Determinista** quiere decir que con los mismos datos da siempre la misma respuesta, hoy y dentro de
tres años, se haya cambiado de modelo por medio o no se haya cambiado.

Dentro del sistema, su sitio está detrás de la inteligencia artificial: no evita que el ayudante se
equivoque, avisa cuando ya lo ha hecho.

### El ejemplo

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

### Los conceptos

Una **invariante** es una regla que en unos datos correctos se cumple siempre y sin excepción que
valga, y que por eso admite una respuesta de una sola palabra: o se cumple, o hay algo estropeado.
En este repositorio las invariantes son tres, y cada una vigila un nivel distinto.

- **INV-1, el cuadre global.** Se suma el libro entero y se comprueba que la columna de la izquierda
  da lo mismo que la de la derecha, 3.420,00 euros por cada lado en los datos de ejemplo.
- **INV-2, el cuadre de cada asiento por separado.** Hace falta porque un descuadre y su contrario
  se anulan entre ellos, y desde el total ya nadie los ve.
- **INV-3, la coherencia entre capas.** Es la que responde a la avería del IVA en cascada.

En un sistema de datos, una **capa** es cada nivel de elaboración por el que pasa la misma
información. Aquí hay dos: el libro, que guarda el detalle apunte por apunte, y el resumen por
cuenta, que guarda el saldo ya calculado de cada una y alimenta los informes. Como el resumen sale
enteramente del libro, tiene que corresponder con él.

Un **control negativo** es meter un error a propósito para comprobar que la alarma suena. Sin él
sabes que el detector no está avisando, pero no sabes si calla porque no hay nada o porque se ha
estropeado. Eso hace la segunda de las dos pruebas del repositorio: coge el resumen, le suma cien
euros a la primera cuenta y exige que INV-3 se ponga roja. El veredicto llega con el detalle puesto,
`cuenta 600 (resumen=1100.00, real=1000.00)`, mientras el libro sigue cuadrando y las otras dos
invariantes siguen en verde. Es el caso de manual: cuadra por sí mismo y es incoherente.

Un ordenador guarda por defecto los números con decimales de una forma que arrastra un residuo
minúsculo, de modo que si le pides 0,1 más 0,2 te contesta 0,30000000000000004. Comparar dos
importes así para ver si son iguales no significa gran cosa. Este programa usa el otro modo de
cálculo que ofrece Python, el de la **aritmética exacta** con decimales, y por eso se permite un
veredicto sin tolerancias ni márgenes.

### Pruébalo

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

### Qué está medido

Ejecutado el 22/07/2026 con Python 3.14.6, sin copiar nada de la documentación:

| Comprobación | Resultado |
|---|---|
| `coherencia.py` sobre los datos de ejemplo | `SANO`, las tres invariantes en verde |
| Total del debe y total del haber | 3.420,00 por cada lado |
| `test_coherencia.py`, dos pruebas | pasan las dos, en 0,01 segundos |
| Los cinco saldos recalculados por otra vía | coinciden con el resumen publicado |
| Control negativo de cien euros al resumen | INV-1 e INV-2 verdes, INV-3 roja, `ENFERMO` |

### El verificador está verificado en un tercio

Lo más interesante queda fuera de esa tabla, y es un defecto de este mismo repositorio.

Una **prueba de mutación** consiste en estropear el programa a propósito, una pieza cada vez, y mirar
si sus propias pruebas se dan cuenta. Es la única manera de saber si unas pruebas en verde protegen
algo o solo lo parecen. Aplicada a este repositorio el 22/07/2026, desactivando una invariante cada
vez, el resultado es este:

| Avería plantada | Las pruebas |
|---|---|
| INV-1 declarada siempre en verde | pasan igual |
| INV-2 declarada siempre en verde | pasan igual |
| INV-3 declarada siempre en verde | fallan; queda cazada |

Dos de las tres reglas se pueden desactivar del todo sin que las pruebas se enteren. La razón está en
el propio control negativo, que planta su error en el resumen, la única capa de la que se ocupa
INV-3. A nadie se le ocurrió plantar además un descuadre en el libro, así que INV-1 e INV-2 se
quedaron sin quien las examine.

Conviene pensar en lo que eso significa dentro de un repositorio que va precisamente de verificar. El
aviso lleva escrito desde el 20/07/2026 dentro de `.github/workflows/ci.yml`, con fecha y sin
arreglar. Esta portada prefiere repetirlo antes que enseñar un «todo verde» que no distinga entre
las tres reglas. Ampliar la cobertura a INV-1 e INV-2 está pendiente y vale más que cualquier otra
cosa que se pueda añadir aquí.

### Cuándo no sirve

**El error copiado en las dos capas pasa.** Si el libro y el resumen se equivocan de la misma manera,
coinciden, y coincidir es todo lo que aquí se comprueba. Lo único que mira son correspondencias
internas; de la realidad de fuera no sabe nada, ni de si la factura existió, ni de si el proveedor es
quien dice ser, ni de si la cuenta elegida era la que tocaba.

**El apunte inflado por los dos lados pasa.** Probado: a la primera línea del libro se le pusieron
quinientos euros de más a la izquierda y quinientos de más a la derecha, y el veredicto siguió siendo
`SANO`. Las tres invariantes miran diferencias, y a una diferencia le da igual que las dos cifras
hayan crecido a la vez.

**Un dato corrupto no da `ENFERMO`, da un plantón.** Con una casilla de importe vacía en el fichero,
el programa se para con un mensaje escrito para programadores, sin llegar a dictar veredicto.

**El tamaño le pesa.** Para comprobar el cuadre asiento por asiento, el programa recorre el libro
entero una vez por cada asiento, de manera que el tiempo crece con el cuadrado del tamaño. Medido:
quinientos asientos en 0,03 segundos, mil en 0,11, dos mil en 0,45 y cuatro mil en 1,83. Al doble de
asientos, cuatro veces de espera. Con las siete líneas del ejemplo esto no se nota, y con un libro de
un año de decenas de miles de apuntes la espera se convierte en minutos.

### Qué llevarse

**Lo verosímil se parece a lo correcto más de lo que nos conviene.** Un sistema de inteligencia
artificial no se cae: sigue contestando con buena forma mientras el fondo se le descuadra por dentro.
Alguien tiene que volver a contar, y quien recuenta ha de ser distinto de quien contó.

**La aritmética no cambia de opinión cuando cambias de modelo.** Ahí está el valor de que la
vigilancia sea corta y tonta, porque ciento cuatro líneas de sumar y comparar valdrán dentro de tres
años lo mismo que valen hoy, y ninguna actualización se las llevará por delante.

**Una alarma sin control negativo todavía no es una alarma.** Y un banco de pruebas en verde tampoco
demuestra gran cosa por sí solo: dos de las tres reglas de este repositorio se apagan sin que sus
pruebas se enteren.

### Qué abrir y en qué orden

| Orden | Fichero | Qué encontrarás |
|---|---|---|
| 1 | `caso_real.md` | De dónde salió esto: una corrección de IVA en cascada |
| 2 | `datos_ejemplo/libro_sintetico.csv` | Siete apuntes inventados; se abre con Excel |
| 3 | `datos_ejemplo/resumen_por_cuenta.csv` | Los cinco saldos que se contrastan |
| 4 | `auditor/coherencia.py` | El verificador entero, con sus tres invariantes |
| 5 | `auditor/test_coherencia.py` | Dos pruebas, una de ellas el control negativo |
| 6 | `.github/workflows/ci.yml` | El vigilante automático, con la confesión de cobertura dentro |

### Estructura

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

### Privacidad

El caso de ejemplo utiliza un conjunto de datos sintético; no contiene información real ni personal.

### Ecosistema

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

## English

### The problem

When an ordinary program breaks, it says so: a message appears, everything stops and whoever looks at
it knows there is something to fix. We have lived with that way of failing for forty years.

A system running on artificial intelligence does not break like that. Say you ask it to fix the VAT
treatment of an invoice. It fixes the entry, and the entry comes out spotless, with what is recorded
on the left adding up to the same as what is recorded on the right. No warning appears on screen,
because there is nothing to warn about.

That correction, though, also had to reach the year-end close, the opening of the following year, the
quarterly tax return and the management dashboard. Four more places. If one of them goes untouched,
the piece left behind is still balanced and correct inside itself, and the only thing that happens is
that it stops matching the others. You find out months later, when one total does not fit another
total and nobody remembers what was changed that day.

There is a second failure just as quiet. Every few months the artificial intelligence models are
updated, and updating them changes how they behave, so a watchdog built on top of a model does not
think the same from one month to the next either. Nobody warns you about that change of judgement.

### What is in this repository

A hundred-and-four-line program, its tests, two files of made-up data and the explanation of where
all this came from. The only thing the program does is read a set of books and answer with one word,
`SANO` or `ENFERMO` (healthy or sick).

To decide, it asks no artificial intelligence: it adds, subtracts and compares. It needs no internet
connection, no database and no piece of software beyond what Python ships with.

**Deterministic** means that with the same data it always gives the same answer, today and three
years from now, whether or not the model was swapped in between.

Inside the system, its place is behind the artificial intelligence: it does not stop the assistant
from making a mistake, it raises a flag once the mistake is there.

### The example

The sample data is seven entries from a double-entry ledger and the five account balances that come
out of them. Account 600, purchases, gets a single entry of 1,000.00 euros in the ledger, and the
balances file declares exactly those 1,000.00 euros for it. They match.

The day somebody touches one of the two files without touching the other they will stop matching.
That is precisely the slip described above. To catch it, the program recomputes each account balance
from the detail and puts it against the declared one.

This is how a ledger line comes in:

```
2,2026-01-10,430,Cliente,1210.00,0.00
```

Entry number 2 of 10 January, account 430 (customers), one thousand two hundred and ten euros on the
left and nothing on the right. From that line, its route through the program takes five steps.

1. **It loads.** The seven ledger lines and the five summary lines go from text to exact numbers.
2. **It adds up both columns.** 3,420.00 against 3,420.00.
3. **It groups by entry.** The three entries each balance on their own.
4. **It recomputes the five balances** from the detail and puts them one by one against the written
   summary.
5. **It issues the verdict.** Three rules green gives `SANO`; a single red one gives `ENFERMO`.

On finishing, the program returns a zero or a one, which is how one program tells another "all good"
or "stop". That is what lets you hang it off an automated process that halts by itself the moment
something stops adding up.

### The concepts

An **invariant** is a rule that always holds in correct data, with no exceptions allowed, which is
why it admits a one-word answer: either it holds, or something is broken. This repository has three
invariants, each of them watching a different level.

- **INV-1, the global balance.** The whole ledger is added up and the left column is checked against
  the right one, 3,420.00 euros on each side in the sample data.
- **INV-2, each entry balancing on its own.** It is needed because an imbalance and its opposite
  cancel each other out, so from the total nobody sees them any more.
- **INV-3, coherence between layers.** This is the one that answers the cascading VAT failure.

In a data system, a **layer** is each level of processing the same information passes through. There
are two here: the ledger, which holds the detail entry by entry, and the summary by account, which
holds each already-computed balance and feeds the reports. Since the summary comes entirely out of
the ledger, it has to match it.

A **negative control** means injecting an error on purpose to check that the alarm goes off. Without
it you know the detector is not firing, but you do not know whether it is silent because there is
nothing wrong or because it has broken. That is what the second of the repository's two tests does:
it takes the summary, adds a hundred euros to the first account and demands that INV-3 turn red. The
verdict arrives with the detail attached, `cuenta 600 (resumen=1100.00, real=1000.00)`, while the
ledger still balances and the other two invariants stay green. This is the textbook case: balanced on
its own and still incoherent.

A computer stores decimal numbers by default in a way that drags a tiny residue along, so if you ask
it for 0.1 plus 0.2 it answers 0.30000000000000004. Comparing two amounts that way to see whether
they are equal does not mean much. This program uses the other calculation mode Python offers, the
one with **exact decimal arithmetic**, which is what lets it issue a verdict with no tolerances and
no margins.

### Try it

```bash
python auditor/coherencia.py        # report on the sample data
python auditor/test_coherencia.py   # the tests, including the negative control
```

Output on the sample data, abbreviated; the program also prints its own header:

```
[OK   ] INV-1 - Cuadre global (total del debe = total del haber)
         debe=3420.00  haber=3420.00  diferencia=0.00
[OK   ] INV-2 - Cuadre por asiento (cada asiento cuadra solo)
         todos los asientos cuadran
[OK   ] INV-3 - Coherencia entre capas (resumen = recalculo desde el libro)
         el resumen corresponde con el libro
VEREDICTO: SANO
```

It takes less than a second.

### What has been measured

Executed on 22/07/2026 with Python 3.14.6, nothing copied from the documentation:

| Check | Result |
|---|---|
| `coherencia.py` on the sample data | `SANO`, the three invariants green |
| Total debits and total credits | 3,420.00 on each side |
| `test_coherencia.py`, two tests | both pass, in 0.01 seconds |
| The five balances recomputed by another route | they match the published summary |
| Negative control of a hundred euros on the summary | INV-1 and INV-2 green, INV-3 red, `ENFERMO` |

### The verifier is verified by one third

The most interesting part falls outside that table: a defect of this very repository.

A **mutation test** consists of breaking the program on purpose, one piece at a time, and watching
whether its own tests notice. It is the only way to know whether a green test suite protects
something or merely looks as if it did. Applied to this repository on 22/07/2026, disabling one
invariant at a time, the result is this:

| Failure planted | The tests |
|---|---|
| INV-1 always declared green | still pass |
| INV-2 always declared green | still pass |
| INV-3 always declared green | fail; caught |

Two of the three rules can be switched off entirely without the tests noticing. The reason lies in
the negative control itself, which plants its error in the summary, the only layer INV-3 deals with.
Nobody thought to plant an imbalance in the ledger as well, so INV-1 and INV-2 were left with no one
to examine them.

It is worth thinking about what that means inside a repository that is precisely about verification.
The warning has been written down since 20/07/2026 inside `.github/workflows/ci.yml`, dated and
unfixed. This page would rather repeat it than show an "all green" that fails to tell the three
rules apart. Extending coverage to INV-1 and INV-2 is pending and matters more than anything else
that could be added here.

### When it is not the right tool

**The error copied into both layers gets through.** If the ledger and the summary are wrong in the
same way, they match, and matching is all that gets checked here. The only thing it looks at is
internal correspondence; about the outside world it knows nothing, neither whether the invoice
existed, nor whether the supplier is who they claim to be, nor whether the chosen account was the
right one.

**The entry inflated on both sides gets through.** Tested: the first ledger line was given five
hundred euros more on the left and five hundred more on the right, and the verdict stayed `SANO`. The
three invariants look at differences, so two figures growing at once leave the difference untouched.

**Corrupt data does not give `ENFERMO`, it gives a crash.** With an empty amount cell in the file,
the program stops with a message written for programmers, never reaching a verdict.

**Size weighs on it.** To check entry-by-entry balancing, the program walks the whole ledger once per
entry, so time grows with the square of the size. Measured: five hundred entries in 0.03 seconds, a
thousand in 0.11, two thousand in 0.45 and four thousand in 1.83. Twice the entries, four times the
wait. With the seven lines of the example this goes unnoticed, and with a full year of tens of
thousands of entries the wait turns into minutes.

### What to take away

**Plausible looks more like correct than suits us.** An artificial intelligence system does not fall
over: it keeps answering in good form while the substance quietly stops adding up. Somebody has to
count again, and whoever recounts has to be someone other than whoever counted.

**Arithmetic does not change its mind when you change model.** That is the value of a watchdog being
short and dumb, because a hundred and four lines of adding and comparing will be worth as much three
years from now as they are today, and they will outlive every model update around them.

**An alarm with no negative control is not yet an alarm.** And a green test suite proves little on
its own: two of the three rules in this repository switch off without their tests noticing.

### What to open and in what order

| Order | File | What you will find |
|---|---|---|
| 1 | `caso_real.md` | Where this came from: a cascading VAT correction |
| 2 | `datos_ejemplo/libro_sintetico.csv` | Seven made-up entries; opens in Excel |
| 3 | `datos_ejemplo/resumen_por_cuenta.csv` | The five balances being checked |
| 4 | `auditor/coherencia.py` | The whole verifier, with its three invariants |
| 5 | `auditor/test_coherencia.py` | Two tests, one of them the negative control |
| 6 | `.github/workflows/ci.yml` | The automated watchdog, with the coverage confession inside |

### Structure

```
verificacion-determinista-ia/
├── auditor/
│   ├── coherencia.py          the verifier (arithmetic only, no AI, no database)
│   └── test_coherencia.py     tests + negative control
├── datos_ejemplo/
│   ├── libro_sintetico.csv        double-entry ledger (made-up data)
│   └── resumen_por_cuenta.csv     derived summary (the "layer" being checked)
├── .github/workflows/ci.yml   runs the tests on every push
├── caso_real.md               where this comes from (no real data)
├── requirements.txt · LICENSE · .gitignore
```

### Privacy

The sample case uses a synthetic dataset; it contains no real or personal information.

### Ecosystem

This repository is the **verification** piece of a set of projects on AI agent systems:

- **[gobernanza-skills-analiticas](https://github.com/jleonceo/gobernanza-skills-analiticas)**, the governance method told in prose. This repo is the code of one of its pieces: the verification that rechecks the state without AI.
- **[accounting-agent-swarm](https://github.com/jleonceo/accounting-agent-swarm)**, the agent swarm that produces the accounting. These checks are the guardrail that keeps it balanced.
- **[audience-analyst-swarm](https://github.com/jleonceo/audience-analyst-swarm)**, the same swarm pattern carried over to audience analytics in a matter of days.
- **[agent-memory-governance](https://github.com/jleonceo/agent-memory-governance)**, the governance of the agent's memory. Its sibling: there you govern what the agent *remembers*; here, the coherence of the *data*.
- **[claude-code-context-management](https://github.com/jleonceo/claude-code-context-management)**, managing the Claude Code context files so CLAUDE.md and MEMORY.md do not bloat the context.
- **[llm-eval-contable](https://github.com/jleonceo/llm-eval-contable)**, the exam that measures whether the skill *gets it right*. Complementary: that one verifies *answers*; this one, that the *data* matches across layers.
- **[orquestacion-enjambres-ia](https://github.com/jleonceo/orquestacion-enjambres-ia)**, multi-agent routing. That one verifies which agent each request goes to; this one, that the data adds up.
- **[tu-primer-asistente-ia-web](https://github.com/jleonceo/tu-primer-asistente-ia-web)**, the plain-language entry point: what an AI assistant is, for someone starting from zero.
- **[tesoreria-forecast-ia](https://github.com/jleonceo/tesoreria-forecast-ia)**, cash-flow forecasting by decomposition with backtesting, plus ratios and aging.
- **[control-interno-fraude-ia](https://github.com/jleonceo/control-interno-fraude-ia)**, accounting fraud detection with arithmetic, inside an internal-control framework.

---

*Datos sintéticos · sin información real ni personal · synthetic data, no real or personal information.*
