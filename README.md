# Entrenamiento paralelo de MLP — Proyecto final CPD 2026-II

Proyecto 7 (Redes Neuronales) del curso Computación Paralela y Distribuida, UTEC. Se entrenan q perceptrones multicapa con semillas distintas repartidas entre p procesos (Map) y se elige el de mayor exactitud con una reducción en árbol de log p niveles (Reduce), siguiendo un modelo CREW PRAM.

**Integrantes:** Juan Carlos Ticlia Maqui, Paulo Isael Miranda Barrientos, Joseph Anderson Cose Rojas.

## Estructura

| Carpeta | Contenido |
|---|---|
| `informe/` | Informe final en LaTeX (`main.tex`) y PDF compilado (`main.pdf`) |
| `codigo/` | Implementación, benchmark, análisis y scripts de Slurm |
| `codigo/dev/` | Versiones beta del desarrollo (beta 1, beta 2, beta 3 y final) |
| `codigo/docs/` | Enunciado y metodología de experimentación |
| `resultados/datos/` | CSV crudos de Khipu (una fila por ejecución) |
| `resultados/figuras/` | Resúmenes por configuración, ajuste del modelo y figuras |
| `resultados/*.out` | Logs de los jobs de Slurm |

## Experimentos

Ejecutados en Khipu, nodo `n005` (2 sockets × 16 núcleos × 2 hilos), con 32 CPUs de Slurm (16 núcleos físicos). Cada configuración se repitió 6 veces; se descarta la primera y se promedian las 5 restantes.

| Caso | Configuración | Job |
|---|---|---|
| Escalabilidad | n = 2000 fijo, q ∈ {8, 16, 32, 64, 128, 256} × p ∈ {1, 2, 4, 8, 16, 32} (q múltiplo de p) | 62094 |
| Impacto de n | q = 32 fijo, n ∈ {500, 1000, 2000, 5000, 10000, 20000, 40000} × p | 62095 |
| Análisis | Ajuste del modelo y figuras | 62132 |

## Resultados principales

- Speedup máximo de 9.3 con p = 16 (q = 256). La reducción en árbol tarda como máximo 4 ms.
- La eficiencia depende de p y casi no de q: 0.92, 0.76, 0.64 y 0.54 para p = 2, 4, 8 y 16. Con p = 32 (hyperthreading) cae a ~0.25.
- La eficiencia no se mantiene constante con q ∝ p, y aumentar n solo la mejora hasta n ≈ 5000.
- Un modelo con contención multiplicativa, T_p = a·⌈q/p⌉·n·(1 + γ·log₂p) + c, ajusta mejor que el modelo con término aditivo log p (γ = 0.127, R² = 0.999 con p ≤ 16).

El análisis completo está en `informe/main.pdf`, sección 3.

## Uso

```bash
cd codigo
pip install -r requirements.txt

# Prueba local
python3 mlp_paralelo.py --n 5000 --q 8 --p 4 --E 50

# En Khipu (desde codigo/)
sbatch slurm/escalabilidad.slurm
sbatch slurm/impacto_n.slurm
sbatch slurm/analisis.slurm

# Figura de escalabilidad débil
python3 figuras_extra.py
```

Compilar el informe:

```bash
cd informe
latexmk -pdf main.tex
```
