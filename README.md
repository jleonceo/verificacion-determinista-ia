# verificacion-determinista-ia

**Verificación determinista para sistemas de IA: comprobaciones de coherencia que no dependen de la IA.**
**Deterministic verification for AI systems: coherence checks that do not depend on AI.**

---

## Español

### Qué resuelve
Los sistemas de IA generan respuestas verosímiles. Y lo verosímil no es lo correcto. Un conjunto de datos puede ser coherente consigo mismo y no reflejar la realidad.

Este proyecto pone una capa de verificación determinista: código que recomprueba la coherencia por aritmética, sin preguntar a ningún modelo. Su trabajo es señalar dónde no cuadran entre sí las distintas capas del sistema.

### Un ejemplo concreto
Un asiento contable puede cuadrar por sí mismo, debe igual a haber, y no corresponder con el saldo real de su grupo en el ejercicio. La validación individual lo da por bueno. Solo el cruce entre capas descubre la incoherencia. Esa es la clase de error que estas comprobaciones cazan.

### Cómo funciona y por qué es fiable
El verificador comprueba un conjunto de reglas que, en unas cuentas correctas, siempre deben cumplirse:
- el total del debe coincide con el total del haber;
- cada asiento cuadra por sí mismo;
- los totales ya calculados que alimentan los informes (el «resumen») coinciden con los datos de origen de los que salen.

Cada regla se responde con un sí o un no: o se cumple, o salta la alarma. Y cada comprobación se hace con una operación aritmética, no preguntándole a una IA.

Ahí está la clave. Los modelos se actualizan y se sustituyen a menudo, y al cambiar se comportan distinto. Una verificación que dependiera de la IA daría hoy un resultado y mañana otro.

Esta no. Al ser pura aritmética, responde siempre igual, use el modelo que use. Y no arrastra los errores del sistema que revisa.

Incluye una prueba de control. Mete a propósito un error en los datos y comprueba que el verificador lo caza. Si no saltara, sabríamos que la verificación ha dejado de servir.

### Pruébalo
```bash
python auditor/coherencia.py        # informe sobre los datos de ejemplo
python auditor/test_coherencia.py   # las pruebas, incluido el control negativo
```
Salida sobre los datos de ejemplo (abreviada; el script imprime además su cabecera):
```
[OK   ] INV-1 - Cuadre global (total del debe = total del haber)
         debe=3420.00  haber=3420.00  diferencia=0.00
[OK   ] INV-2 - Cuadre por asiento (cada asiento cuadra solo)
         todos los asientos cuadran
[OK   ] INV-3 - Coherencia entre capas (resumen = recalculo desde el libro)
         el resumen corresponde con el libro
VEREDICTO: SANO
```
El control negativo toca **solo el resumen**. El libro sigue cuadrando, con INV-1 e INV-2 en verde, y aun así INV-3 detecta que el resumen ya no corresponde con sus datos. Es el caso de manual: cuadra por sí mismo y es incoherente.

### Estructura
```
verificacion-determinista-ia/
├── auditor/
│   ├── coherencia.py          # el verificador (solo aritmética, sin IA ni base de datos)
│   └── test_coherencia.py     # pruebas + control negativo
├── datos_ejemplo/
│   ├── libro_sintetico.csv        # libro de doble partida (datos inventados)
│   └── resumen_por_cuenta.csv     # resumen derivado (la «capa» que se contrasta)
├── caso_real.md               # de dónde viene esto (sin datos reales)
├── requirements.txt · LICENSE · .gitignore
```

### Privacidad
El caso de ejemplo utiliza un conjunto de datos sintético; no contiene información real ni personal.

### Ecosistema, cómo encaja con los demás repositorios
Este repositorio es la pieza de **verificación** de un conjunto de proyectos sobre sistemas de agentes de IA:
- **[gobernanza-skills-analiticas](https://github.com/jleonceo/gobernanza-skills-analiticas)**, el método de gobernanza contado en prosa. Este repo es el código de una de sus piezas: la verificación que recomprueba el estado sin IA.
- **[accounting-agent-swarm](https://github.com/jleonceo/accounting-agent-swarm)**, el enjambre de agentes que genera la contabilidad. Estas comprobaciones son el guardarraíl que lo mantiene cuadrado.
- **[agent-memory-governance](https://github.com/jleonceo/agent-memory-governance)**, la gobernanza de la memoria del agente. Su hermano: allí se gobierna lo que el agente *recuerda*; aquí, la coherencia de los *datos*.
- **[claude-code-context-management](https://github.com/jleonceo/claude-code-context-management)**, la gestión de los ficheros de contexto de Claude Code, para que CLAUDE.md y MEMORY.md no saturen el contexto.
- **[llm-eval-contable](https://github.com/jleonceo/llm-eval-contable)**, el examen que mide si la skill *acierta*. Complementario: aquel verifica las *respuestas*; este, que los *datos* cuadren entre capas.
- **[orquestacion-enjambres-ia](https://github.com/jleonceo/orquestacion-enjambres-ia)**, el enrutado multi-agente. Aquel verifica a qué agente va cada petición; este, que los datos cuadren.
- **[tu-primer-asistente-ia-web](https://github.com/jleonceo/tu-primer-asistente-ia-web)**, la entrada sin tecnicismos: qué es un asistente de IA, para quien empieza de cero.
- **[tesoreria-forecast-ia](https://github.com/jleonceo/tesoreria-forecast-ia)**, previsión de caja por descomposición con backtesting, más ratios y aging.
- **[control-interno-fraude-ia](https://github.com/jleonceo/control-interno-fraude-ia)**, detección de fraude contable con aritmética, dentro de un marco de control interno.

---

## English

### What it solves
AI systems produce plausible answers. Plausible is not correct. A dataset can be consistent with itself and still fail to reflect reality.

This project adds a deterministic verification layer: code that re-checks coherence with plain arithmetic, without asking any model. Its job is to flag where the layers of the system stop matching each other.

### A concrete example
A double-entry record can be balanced on its own (debits = credits) and yet not match the actual balance of its account across the whole period. Individual validation accepts it; only the cross-layer check reveals the inconsistency. That is the kind of error these checks catch.

### How it works and why it is reliable
The verifier evaluates a set of rules that must always hold in correct books:
- total debits equal total credits;
- every entry balances on its own;
- the precomputed totals that feed the reports (the "summary") match the source data they come from.

Each rule yields a yes or a no: it holds, or the alarm fires. And every check is a plain arithmetic operation, not a query to an AI.

That is the core of its reliability. Models are updated and replaced often, and their behaviour shifts when they change. An AI-based verification would return one result today and another tomorrow.

This one does not. Being pure arithmetic, it always returns the same answer, whichever model is in use. And it does not inherit the errors of the system it checks.

It also includes a control test: it deliberately injects an error into the data and confirms that the verifier detects it. If it did not fire, we would know the verification had stopped working.

### Try it
```bash
python auditor/coherencia.py        # report on the sample data
python auditor/test_coherencia.py   # the tests, including the negative control
```
The negative control tampers with the **summary only**: the ledger still balances (INV-1 and INV-2 green) and yet INV-3 detects that the summary no longer matches its data. This is the "balanced on its own and still incoherent" case.

### Privacy
The sample case uses a synthetic dataset; it contains no real or personal information.

### Ecosystem
This repository is the **verification** piece of a set of projects on AI agent systems: it provides the deterministic guardrail for [gobernanza-skills-analiticas](https://github.com/jleonceo/gobernanza-skills-analiticas) (the governance method), [accounting-agent-swarm](https://github.com/jleonceo/accounting-agent-swarm) (the agent swarm it keeps balanced), [agent-memory-governance](https://github.com/jleonceo/agent-memory-governance) (its sibling: memory vs. data coherence), [claude-code-context-management](https://github.com/jleonceo/claude-code-context-management) (keeping the context files CLAUDE.md and MEMORY.md from bloating the context), [llm-eval-contable](https://github.com/jleonceo/llm-eval-contable) (which checks answers, while this checks cross-layer coherence), [orquestacion-enjambres-ia](https://github.com/jleonceo/orquestacion-enjambres-ia) (which routes each request to the right agent) and [tu-primer-asistente-ia-web](https://github.com/jleonceo/tu-primer-asistente-ia-web) (the plain-language entry point for beginners), plus [tesoreria-forecast-ia](https://github.com/jleonceo/tesoreria-forecast-ia) (cash-flow forecasting with backtesting, ratios and aging) and [control-interno-fraude-ia](https://github.com/jleonceo/control-interno-fraude-ia) (accounting fraud detection with arithmetic, inside an internal-control framework).

---

*Datos sintéticos · sin información real ni personal · synthetic data, no real or personal information.*
