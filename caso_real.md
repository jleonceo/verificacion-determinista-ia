# De dónde viene esto

Esta capa de verificación nació de un caso real en un sistema de contabilidad asistido por IA. En este repositorio los datos se han sustituido por datos sintéticos; lo que se conserva es el mecanismo y la lección.

Al corregir un tratamiento de IVA, el cambio tenía efecto en **cascada**: afectaba al libro diario, al cierre del ejercicio, a la apertura del siguiente, a las liquidaciones de impuestos y al cuadro de mando. Cada uno de esos saltos es fácil de olvidar al hacer la corrección a mano.

El detalle importante: un asiento puede quedar perfectamente cuadrado por sí mismo y, aun así, dejar de corresponder con el resto del sistema. **Cuadra solo y aun así es incoherente.** La validación individual («este asiento cuadra») no garantiza la coherencia entre capas.

La conclusión fue que hacía falta un mecanismo que recompruebe esas correspondencias al momento y de forma determinista, para que ningún salto de la cascada se quedara a medias. Como es pura aritmética, no depende de qué modelo de IA esté en uso ni hereda sus errores.

Este repositorio es ese mecanismo, reducido a un ejemplo mínimo. La invariante **INV-3** (el resumen debe coincidir con el recálculo desde el libro) es la que habría detectado el caso original: el resumen dejaba de corresponder con los datos aunque cada asiento siguiera cuadrando.

> Nota: los importes, las cuentas y cualquier dato de este repositorio son sintéticos. No representan información real ni personal.
