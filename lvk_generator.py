#!/usr/bin/env python3
"""
LVK Generator aus EULUMDAT/LDT-Dateien.
Erzeugt eine LVK-Grafik als PNG und PDF.

Beispiel:
    python lvk_generator.py example_spotlight.ldt --out output
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class LDTData:
    manufacturer: str
    product: str
    article: str
    file_name: str
    n_c: int
    n_g: int
    c_angles: np.ndarray
    gamma_angles: np.ndarray
    values_cd_klm: np.ndarray
    lumens: float | None
    watt: float | None
    color_temp: str | None
    cri: str | None


def _to_float(s: str) -> float | None:
    try:
        return float(s.strip().replace(",", "."))
    except Exception:
        return None


def read_ldt(path: str | Path) -> LDTData:
    path = Path(path)
    raw_lines = path.read_text(encoding="latin-1").splitlines()
    lines = [line.strip() for line in raw_lines]

    manufacturer = lines[0] if len(lines) > 0 else ""
    product = lines[8] if len(lines) > 8 else path.stem
    article = lines[9] if len(lines) > 9 else ""
    file_name = lines[10] if len(lines) > 10 else path.name

    n_c = int(float(lines[3].replace(",", ".")))
    n_g = int(float(lines[5].replace(",", ".")))

    numeric_positions: list[tuple[int, float]] = []

    for idx, line in enumerate(lines):
        val = _to_float(line)
        if val is not None:
            numeric_positions.append((idx, val))

    start_pos = None

    for i in range(len(numeric_positions) - n_c - n_g):
        c_candidate = [v for _, v in numeric_positions[i:i + n_c]]
        g_candidate = [v for _, v in numeric_positions[i + n_c:i + n_c + n_g]]

        c_ok = all(
            abs(c_candidate[j] - c_candidate[0] - j * (360 / n_c)) < 0.2
            for j in range(n_c)
        )

        g_ok = (
            abs(g_candidate[0]) < 0.2
            and all(g_candidate[j] >= g_candidate[j - 1] for j in range(1, n_g))
        )

        if c_ok and g_ok:
            start_pos = i
            break

    if start_pos is None:
        raise ValueError(
            "C-/Gamma-Winkel konnten in der LDT-Datei nicht automatisch gefunden werden."
        )

    c_angles = np.array(
        [v for _, v in numeric_positions[start_pos:start_pos + n_c]],
        dtype=float
    )

    gamma_angles = np.array(
        [v for _, v in numeric_positions[start_pos + n_c:start_pos + n_c + n_g]],
        dtype=float
    )

    vals = [
        v for _, v in numeric_positions[
            start_pos + n_c + n_g:
            start_pos + n_c + n_g + n_c * n_g
        ]
    ]

    if len(vals) < n_c * n_g:
        raise ValueError("Nicht genug Lichtstärke-Werte in der LDT-Datei gefunden.")

    values = np.array(vals, dtype=float).reshape((n_c, n_g))

    lumens = _to_float(lines[28]) if len(lines) > 28 else None
    color_temp = lines[29] if len(lines) > 29 else None
    cri = lines[30] if len(lines) > 30 else None
    watt = _to_float(lines[31]) if len(lines) > 31 else None

    return LDTData(
        manufacturer=manufacturer,
        product=product,
        article=article,
        file_name=file_name,
        n_c=n_c,
        n_g=n_g,
        c_angles=c_angles,
        gamma_angles=gamma_angles,
        values_cd_klm=values,
        lumens=lumens,
        watt=watt,
        color_temp=color_temp,
        cri=cri
    )


def make_lvk_plot(
    data: LDTData,
    out_png: Path,
    out_pdf: Path | None = None,
    c_plane: float | None = None
) -> None:
    if c_plane is None:
        intensity = data.values_cd_klm.mean(axis=0)
        plane_label = "Mittelwert aller C-Ebenen"
    else:
        idx = int(np.argmin(np.abs(data.c_angles - c_plane)))
        intensity = data.values_cd_klm[idx]
        plane_label = f"C{data.c_angles[idx]:.0f}"

    gamma = data.gamma_angles
    max_i = float(np.nanmax(intensity))
    grid_max = math.ceil(max_i / 500) * 500

    x_right = gamma
    y_right = intensity

    x_left = -gamma[::-1]
    y_left = intensity[::-1]

    x_poly = np.concatenate([x_left, x_right])
    y_poly = np.concatenate([y_left, y_right])

    fig, ax = plt.subplots(figsize=(7.2, 5.4))

    ax.plot(x_poly, y_poly, linewidth=2)
    ax.fill(x_poly, y_poly, alpha=0.25)

    for ang in [-90, -60, -30, 0, 30, 60, 90]:
        ax.plot([0, ang], [0, grid_max], linewidth=0.8, alpha=0.35)

        if ang != 0:
            ax.text(
                ang,
                grid_max * 1.03,
                f"{abs(ang)}°",
                ha="center",
                va="bottom",
                fontsize=10
            )

    for r in np.linspace(grid_max / 4, grid_max, 4):
        xs = np.linspace(-90, 90, 361)
        ys = r * np.cos(np.radians(xs))

        ax.plot(xs, ys, linewidth=0.8, alpha=0.35)
        ax.text(
            0,
            r,
            f"{int(round(r))}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    ax.set_xlim(-95, 95)
    ax.set_ylim(0, grid_max * 1.1)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    title = f"LVK {data.product} | Art.-Nr. {data.article}"
    subtitle = f"{plane_label} | max. {max_i:.0f} cd/klm"

    if data.lumens:
        subtitle += f" | {data.lumens:.0f} lm"

    if data.watt:
        subtitle += f" | {data.watt:.0f} W"

    ax.set_title(title + "\n" + subtitle, fontsize=12, pad=20)

    ax.text(
        0,
        grid_max * 1.08,
        "cd/klm",
        ha="center",
        va="top",
        fontsize=10
    )

    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")

    if out_pdf:
        fig.savefig(out_pdf, bbox_inches="tight")

    plt.close(fig)


def generate_lvk(ldt_file, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = read_ldt(ldt_file)

    base = Path(ldt_file).stem
    png_path = output_dir / f"{base}_LVK.png"
    pdf_path = output_dir / f"{base}_LVK.pdf"

    make_lvk_plot(data, png_path, pdf_path)

    return png_path, pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LVK-Grafik aus LDT/EULUMDAT erzeugen"
    )

    parser.add_argument("ldt_file", help="Pfad zur .ldt Datei")
    parser.add_argument("--out", default="output", help="Ausgabeordner")
    parser.add_argument(
        "--c-plane",
        type=float,
        default=None,
        help="Optional: bestimmte C-Ebene, z. B. 0, 90, 180"
    )

    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    data = read_ldt(args.ldt_file)

    base = Path(args.ldt_file).stem
    png = out_dir / f"{base}_LVK.png"
    pdf = out_dir / f"{base}_LVK.pdf"

    make_lvk_plot(data, png, pdf, args.c_plane)

    print("Fertig.")
    print(f"Produkt: {data.product}")
    print(f"Artikel: {data.article}")
    print(f"C-Ebenen: {data.n_c}, Gamma-Winkel: {data.n_g}")
    print(f"Max: {np.max(data.values_cd_klm):.1f} cd/klm")
    print(f"PNG: {png}")
    print(f"PDF: {pdf}")


if __name__ == "__main__":
    main()