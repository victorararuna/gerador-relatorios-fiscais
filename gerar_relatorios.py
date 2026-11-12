# -*- coding: utf-8 -*-
"""Gera os demonstrativos do RGF a partir das Matrizes de Saldos Contábeis.

Uso:
    python gerar_relatorios.py --entrada "C:\\caminho\\das\\matrizes"
    python gerar_relatorios.py --entrada ... --saida ... --exercicio 2024
    python gerar_relatorios.py --ui          (abre a janela)

A pasta de entrada pode ter as matrizes em qualquer organização: o programa lê
a primeira linha de cada arquivo (`24EX;2024-12`) e identifica o exercício e o
mês. Basta apontar para a pasta onde elas estão.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "app"))


def _cli() -> int:
    import argparse
    import pipeline

    ap = argparse.ArgumentParser(
        description="Gera os demonstrativos do RGF a partir das matrizes MSC.")
    ap.add_argument("--entrada", help="pasta com as matrizes (instancia.csv)")
    ap.add_argument("--saida", help="pasta de destino (padrão: ./saida)")
    ap.add_argument("--exercicio", type=int, help="exercício (padrão: o mais recente)")
    ap.add_argument("--quadrimestre", type=int, default=3)
    ap.add_argument("--ui", action="store_true", help="abre a interface gráfica")
    args = ap.parse_args()

    if args.ui or not args.entrada:
        return _ui()

    saida = args.saida or os.path.join(AQUI, "saida")
    try:
        r = pipeline.gerar(args.entrada, saida, args.exercicio, args.quadrimestre)
    except SystemExit as e:
        print(f"ERRO: {e}")
        return 1
    print()
    print("=" * 60)
    print(f"Relatório gerado: {r['rgf']}")
    print("=" * 60)
    return 0


def _ui() -> int:
    """Janela simples: escolher a pasta, gerar e abrir o resultado."""
    import threading
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    raiz = tk.Tk()
    raiz.title("Gerador de Relatórios Fiscais — RGF")
    raiz.geometry("640x420")
    raiz.configure(bg="#f4f6f8")

    titulo = tk.Label(raiz, text="Gerador de Relatórios Fiscais",
                      font=("Segoe UI", 15, "bold"), bg="#f4f6f8")
    titulo.pack(pady=(18, 2))
    sub = tk.Label(raiz, text="Aponte a pasta com as Matrizes de Saldos Contábeis "
                              "e o programa gera o RGF completo.",
                   font=("Segoe UI", 9), bg="#f4f6f8", fg="#555")
    sub.pack(pady=(0, 14))

    quadro = tk.Frame(raiz, bg="#f4f6f8")
    quadro.pack(fill="x", padx=24)

    tk.Label(quadro, text="Pasta das matrizes:", font=("Segoe UI", 9, "bold"),
             bg="#f4f6f8").grid(row=0, column=0, sticky="w")
    var_entrada = tk.StringVar()
    tk.Entry(quadro, textvariable=var_entrada, font=("Segoe UI", 9),
             width=52).grid(row=1, column=0, pady=4, sticky="we")

    def escolher() -> None:
        p = filedialog.askdirectory(title="Selecione a pasta com as matrizes")
        if p:
            var_entrada.set(p)

    tk.Button(quadro, text="Procurar…", command=escolher,
              font=("Segoe UI", 8)).grid(row=1, column=1, padx=(6, 0))

    tk.Label(quadro, text="Pasta de saída:", font=("Segoe UI", 9, "bold"),
             bg="#f4f6f8").grid(row=2, column=0, sticky="w", pady=(10, 0))
    var_saida = tk.StringVar(value=os.path.join(AQUI, "saida"))
    tk.Entry(quadro, textvariable=var_saida, font=("Segoe UI", 9),
             width=52).grid(row=3, column=0, pady=4, sticky="we")

    def escolher_saida() -> None:
        p = filedialog.askdirectory(title="Selecione a pasta de saída")
        if p:
            var_saida.set(p)

    tk.Button(quadro, text="Procurar…", command=escolher_saida,
              font=("Segoe UI", 8)).grid(row=3, column=1, padx=(6, 0))
    quadro.columnconfigure(0, weight=1)

    log = tk.Text(raiz, height=10, font=("Consolas", 8), bg="#ffffff",
                  relief="solid", bd=1)
    log.pack(fill="both", expand=True, padx=24, pady=14)

    barra = ttk.Progressbar(raiz, mode="indeterminate")

    def escrever(msg: str) -> None:
        log.insert("end", msg + "\n")
        log.see("end")
        raiz.update_idletasks()

    def executar() -> None:
        entrada = var_entrada.get().strip()
        if not entrada or not os.path.isdir(entrada):
            messagebox.showwarning("Atenção", "Escolha a pasta com as matrizes.")
            return
        saida = var_saida.get().strip() or os.path.join(AQUI, "saida")
        botao.config(state="disabled")
        barra.pack(fill="x", padx=24, pady=(0, 10))
        barra.start(12)
        log.delete("1.0", "end")

        def tarefa() -> None:
            import pipeline
            try:
                r = pipeline.gerar(entrada, saida, None, 3, verbose=False)
                # reexecuta mostrando o log
                escrever(f"{r['matrizes']} matrizes encontradas (exercício {r['exercicio']})")
                escrever("Gerando o RGF …")
                escrever("")
                escrever(f"Pronto: {r['rgf']}")
                messagebox.showinfo("Concluído", f"Relatório gerado:\n{r['rgf']}")
            except SystemExit as e:
                escrever(f"ERRO: {e}")
                messagebox.showerror("Erro", str(e))
            except Exception as e:  # noqa: BLE001
                escrever(f"ERRO: {type(e).__name__}: {e}")
                messagebox.showerror("Erro", f"{type(e).__name__}: {e}")
            finally:
                barra.stop()
                barra.pack_forget()
                botao.config(state="normal")

        threading.Thread(target=tarefa, daemon=True).start()

    botao = tk.Button(raiz, text="Gerar relatórios", command=executar,
                      font=("Segoe UI", 10, "bold"), bg="#1f6feb", fg="white",
                      activebackground="#1858c4", activeforeground="white",
                      relief="flat", padx=20, pady=8)
    botao.pack(pady=(0, 18))

    raiz.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
