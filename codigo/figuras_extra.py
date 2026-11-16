import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resumen", default="../resultados/figuras/resumen_escalabilidad.csv")
    ap.add_argument("--out", default="../resultados/figuras")
    a = ap.parse_args()
    e = pd.read_csv(a.resumen)
    e["k"] = e.q // e.p
    n = int(e.n.iloc[0])

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for k in (1, 2, 4, 8):
        g = e[e.k == k].sort_values("p")
        ax.plot(g.p, g.E, "o-", label=f"$q/p={k}$")
    ax.axhline(1, color="k", ls="--", alpha=0.5)
    ax.set_xscale("log", base=2)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("$p$ — procesos")
    ax.set_ylabel("$E_f = S_p/p$")
    ax.set_title(f"$E_f$ vs $p$ con $q \propto p$ ($n={n}$)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(a.out, "escalabilidad_debil.png"), dpi=160)


if __name__ == "__main__":
    main()
