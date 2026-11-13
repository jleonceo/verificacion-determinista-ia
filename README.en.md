Versión en español: [README.md](README.md)

# verificacion-determinista-ia

[![ci](https://github.com/jleonceo/verificacion-determinista-ia/actions/workflows/ci.yml/badge.svg)](https://github.com/jleonceo/verificacion-determinista-ia/actions/workflows/ci.yml)

**The one that recounts after the AI has answered: coherence checks that do not depend on AI**

## The problem

When an ordinary program breaks, it says so: a message appears, everything stops and whoever looks at
it knows there is something to fix. We have lived with that way of failing for forty years.

A system running on artificial intelligence does not break like that. Say you ask it to fix the VAT
treatment of an invoice. It fixes the entry. And the entry comes out spotless, with what is recorded
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

## What is in this repository

A hundred-and-four-line program, its tests, two files of made-up data and the explanation of where
all this came from. The only thing the program does is read a set of books and answer with one word,
`SANO` or `ENFERMO` (healthy or sick).

To decide, it asks no artificial intelligence. It adds, subtracts and compares. It needs no internet
connection. No database. No piece of software beyond what Python ships with.

**Deterministic** means that with the same data it always gives the same answer, today and three
years from now, whether or not the model was swapped in between.

Inside the system, its place is behind the artificial intelligence: it does not stop the assistant
from making a mistake, it raises a flag once the mistake is there.

## The example

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
or "stop", so it can be hung off an automated process that halts by itself the moment something
stops adding up.

## The concepts

An **invariant** is a rule that always holds in correct data, with no exceptions allowed, which is
why it admits a one-word answer: either it holds, or something is broken. This repository has three
invariants. Each of them watches a different level.

- INV-1, the global balance. The whole ledger is added up and the left column is checked against
  the right one, 3,420.00 euros on each side in the sample data.
- INV-2, each entry balancing on its own. It is needed because an imbalance and its opposite
  cancel each other out, so from the total nobody sees them any more.
- INV-3, coherence between layers. This is the one that answers the cascading VAT failure.

In a data system, a **layer** is each level of processing the same information passes through, and
there are two here: the ledger, which holds the detail entry by entry, and the summary by account,
which holds each already-computed balance and feeds the reports. Since the summary comes entirely
out of the ledger, it has to match it.

A **negative control** means injecting an error on purpose to check that the alarm goes off. Without
it you know the detector is not firing, but you do not know whether it is silent because there is
nothing wrong or because it has broken. That is what the second of the repository's two tests does:
it takes the summary, adds a hundred euros to the first account and demands that INV-3 turn red. The
verdict arrives with the detail attached, `cuenta 600 (resumen=1100.00, real=1000.00)`, while the
ledger still balances and the other two invariants stay green. This is the textbook case. It balances
on its own and it is still incoherent.

A computer stores decimal numbers by default in a way that drags a tiny residue along, so if you ask
it for 0.1 plus 0.2 it answers 0.30000000000000004. Comparing two amounts that way to see whether
they are equal does not mean much. This program uses the other calculation mode Python offers, the
one with **exact decimal arithmetic**. That is what lets it issue a verdict with no tolerances and
no margins.

## Try it

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

## What has been measured

Executed on 22/07/2026 with Python 3.14.6, nothing copied from the documentation:

| Check | Result |
|---|---|
| `coherencia.py` on the sample data | `SANO`, the three invariants green |
| Total debits and total credits | 3,420.00 on each side |
| `test_coherencia.py`, two tests | both pass, in 0.01 seconds |
| The five balances recomputed by another route | they match the published summary |
| Negative control of a hundred euros on the summary | INV-1 and INV-2 green, INV-3 red, `ENFERMO` |

## The verifier is verified by one third

The most interesting part falls outside that table: a defect of this very repository.

A **mutation test** consists of breaking the program on purpose, one piece at a time, and watching
whether its own tests notice, which is the only way to know whether a green test suite protects
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

It is worth thinking about what that means. A repository that is precisely about verification has
carried the warning inside `.github/workflows/ci.yml` since 20/07/2026, dated and unfixed, so this
page would rather repeat it than show an "all green" that fails to tell the three rules apart.
Extending coverage to INV-1 and INV-2 is pending and matters more than anything else that could be
added here.

## When it is not the right tool

**The error copied into both layers gets through.** If the ledger and the summary are wrong in the
same way, they match, and matching is all that gets checked here. The only thing it looks at is
internal correspondence; about the outside world it knows nothing, neither whether the invoice
existed, nor whether the supplier is who they claim to be, nor whether the chosen account was the
right one.

**The entry inflated on both sides gets through.** Tested: the first ledger line was given five
hundred euros more on the left and five hundred more on the right, and the verdict stayed `SANO`. The
three invariants look at differences. Two figures growing at once leave the difference untouched.

**Corrupt data does not give `ENFERMO`, it gives a crash.** With an empty amount cell in the file,
the program stops with a message written for programmers, never reaching a verdict.

**Size weighs on it.** To check entry-by-entry balancing, the program walks the whole ledger once per
entry, so time grows with the square of the size. Measured: five hundred entries in 0.03 seconds, a
thousand in 0.11, two thousand in 0.45 and four thousand in 1.83. Twice the entries, four times the
wait. With the seven lines of the example this goes unnoticed, and with a full year of tens of
thousands of entries the wait turns into minutes.

## What to take away

**Plausible looks more like correct than suits us.** An artificial intelligence system does not fall
over: it keeps answering in good form while the substance quietly stops adding up. Somebody has to
count again. And whoever recounts has to be someone other than whoever counted.

**Arithmetic does not change its mind when you change model.** That is the value of a watchdog being
short and dumb, because a hundred and four lines of adding and comparing will be worth as much three
years from now as they are today, and they will outlive every model update around them.

**An alarm with no negative control is not yet an alarm.** And a green test suite proves little on
its own: two of the three rules in this repository switch off without their tests noticing.

## What to open and in what order

| Order | File | What you will find |
|---|---|---|
| 1 | `caso_real.md` | Where this came from: a cascading VAT correction |
| 2 | `datos_ejemplo/libro_sintetico.csv` | Seven made-up entries; opens in Excel |
| 3 | `datos_ejemplo/resumen_por_cuenta.csv` | The five balances being checked |
| 4 | `auditor/coherencia.py` | The whole verifier, with its three invariants |
| 5 | `auditor/test_coherencia.py` | Two tests, one of them the negative control |
| 6 | `.github/workflows/ci.yml` | The automated watchdog, with the coverage confession inside |

## Structure

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

## Privacy

The sample case uses a synthetic dataset; it contains no real or personal information.

## Ecosystem

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

*Synthetic data, no real or personal information.*
