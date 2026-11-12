# -*- coding: utf-8 -*-
"""Interface grafica (Tkinter) da aplicacao de demonstrativos fiscais.

Tres abas:
  Entradas       - arquivos carregados e periodos reconhecidos
  Conferencia    - achados das regras (erros e alertas)
  Demonstrativos - geracao e abertura dos arquivos produzidos

A interface nao contem regra de negocio: apenas orquestra app.rascunho,
app.validacao e app.gerador.
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Optional

import anexos as cat
import gerador
import rascunho
import validacao
from modelo import Documento

TITULO = "Demonstrativos Fiscais — MDF/Siconfi"
COR_ERRO = "#b00020"
COR_ALERTA = "#b26a00"
COR_OK = "#1b5e20"


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TITULO)
        self.geometry("1180x720")
        self.minsize(960, 600)
        self.docs: List[Documento] = []
        self.achados: List[validacao.Achado] = []
        self.resultados: List[Dict] = []
        self.pasta_saida = tk.StringVar(value=os.path.join(os.getcwd(), "saida"))
        self.status = tk.StringVar(value="Pronto. Adicione os rascunhos do Siconfi (.xls).")

        self._estilo()
        self._montar()

    # ------------------------------------------------------------------ visual
    def _estilo(self) -> None:
        st = ttk.Style(self)
        try:
            st.theme_use("vista")
        except tk.TclError:
            pass
        st.configure("Titulo.TLabel", font=("Segoe UI", 14, "bold"))
        st.configure("Sub.TLabel", font=("Segoe UI", 9), foreground="#444")
        st.configure("Treeview", font=("Segoe UI", 9), rowheight=22)
        st.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        st.configure("Acao.TButton", font=("Segoe UI", 9, "bold"))

    def _montar(self) -> None:
        topo = ttk.Frame(self, padding=(12, 10, 12, 4))
        topo.pack(fill="x")
        ttk.Label(topo, text="Gerador de demonstrativos fiscais", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(topo, text="Entrada: rascunhos do Siconfi (.xls) · Saída: XLSX e HTML para PDF · "
                             "Conferência automática pelas regras do MDF",
                  style="Sub.TLabel").pack(anchor="w")

        barra = ttk.Frame(self, padding=(12, 6))
        barra.pack(fill="x")
        ttk.Button(barra, text="Adicionar arquivos…", command=self.adicionar_arquivos).pack(side="left")
        ttk.Button(barra, text="Adicionar pasta…", command=self.adicionar_pasta).pack(side="left", padx=(6, 0))
        ttk.Button(barra, text="Limpar", command=self.limpar).pack(side="left", padx=(6, 0))
        ttk.Separator(barra, orient="vertical").pack(side="left", fill="y", padx=10)
        ttk.Label(barra, text="Saída:").pack(side="left")
        ttk.Entry(barra, textvariable=self.pasta_saida, width=52).pack(side="left", padx=6)
        ttk.Button(barra, text="…", width=3, command=self.escolher_saida).pack(side="left")

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=12, pady=6)
        self._aba_entradas()
        self._aba_conferencia()
        self._aba_demonstrativos()

        rodape = ttk.Frame(self, padding=(12, 4, 12, 10))
        rodape.pack(fill="x")
        ttk.Label(rodape, textvariable=self.status, style="Sub.TLabel").pack(side="left")
        self.progresso = ttk.Progressbar(rodape, mode="indeterminate", length=160)
        self.progresso.pack(side="right")

    def _aba_entradas(self) -> None:
        f = ttk.Frame(self.nb, padding=8)
        self.nb.add(f, text="  Entradas  ")
        cols = ("tipo", "exercicio", "periodo", "anexos", "layout", "arquivo")
        self.tv_docs = ttk.Treeview(f, columns=cols, show="headings", height=14)
        for c, t, w, a in [("tipo", "Documento", 90, "center"), ("exercicio", "Exercício", 80, "center"),
                           ("periodo", "Período", 130, "center"), ("anexos", "Anexos", 200, "w"),
                           ("layout", "Layout", 90, "center"), ("arquivo", "Arquivo de origem", 380, "w")]:
            self.tv_docs.heading(c, text=t)
            self.tv_docs.column(c, width=w, anchor=a)
        self.tv_docs.pack(fill="both", expand=True)
        self.lbl_entradas = ttk.Label(f, text="Nenhum arquivo carregado.", style="Sub.TLabel")
        self.lbl_entradas.pack(anchor="w", pady=(6, 0))

    def _aba_conferencia(self) -> None:
        f = ttk.Frame(self.nb, padding=8)
        self.nb.add(f, text="  Conferência  ")
        topo = ttk.Frame(f)
        topo.pack(fill="x", pady=(0, 6))
        self.lbl_resumo = ttk.Label(topo, text="Sem conferência.", style="Sub.TLabel")
        self.lbl_resumo.pack(side="left")
        ttk.Button(topo, text="Validar novamente", command=self.validar).pack(side="right")
        self.var_so_erros = tk.BooleanVar(value=False)
        ttk.Checkbutton(topo, text="somente erros", variable=self.var_so_erros,
                        command=self._repreencher_achados).pack(side="right", padx=8)

        cols = ("sev", "anexo", "bloco", "linha", "regra", "mensagem", "esperado", "encontrado")
        self.tv_ach = ttk.Treeview(f, columns=cols, show="headings", height=16)
        for c, t, w, a in [("sev", "Sev.", 70, "center"), ("anexo", "Anexo", 110, "w"),
                           ("bloco", "Bloco", 150, "w"), ("linha", "Linha", 230, "w"),
                           ("regra", "Regra", 110, "w"), ("mensagem", "Mensagem", 300, "w"),
                           ("esperado", "Esperado", 110, "e"), ("encontrado", "Encontrado", 110, "e")]:
            self.tv_ach.heading(c, text=t)
            self.tv_ach.column(c, width=w, anchor=a)
        self.tv_ach.tag_configure("erro", foreground=COR_ERRO)
        self.tv_ach.tag_configure("alerta", foreground=COR_ALERTA)
        self.tv_ach.pack(fill="both", expand=True)

    def _aba_demonstrativos(self) -> None:
        f = ttk.Frame(self.nb, padding=8)
        self.nb.add(f, text="  Demonstrativos  ")
        topo = ttk.Frame(f)
        topo.pack(fill="x", pady=(0, 6))
        ttk.Button(topo, text="Gerar demonstrativos", style="Acao.TButton",
                   command=self.gerar).pack(side="left")
        ttk.Button(topo, text="Abrir pasta de saída", command=self.abrir_saida).pack(side="left", padx=6)
        ttk.Label(topo, text="(XLSX para edição/publicação e HTML para imprimir em PDF)",
                  style="Sub.TLabel").pack(side="left", padx=10)

        cols = ("anexo", "status", "arquivos")
        self.tv_saida = ttk.Treeview(f, columns=cols, show="headings", height=16)
        for c, t, w, a in [("anexo", "Anexo", 130, "w"), ("status", "Situação", 180, "w"),
                           ("arquivos", "Arquivos gerados", 780, "w")]:
            self.tv_saida.heading(c, text=t)
            self.tv_saida.column(c, width=w, anchor=a)
        self.tv_saida.tag_configure("pendente", foreground=COR_ALERTA)
        self.tv_saida.tag_configure("ok", foreground=COR_OK)
        self.tv_saida.pack(fill="both", expand=True)

    # ------------------------------------------------------------------ acoes
    def escolher_saida(self) -> None:
        pasta = filedialog.askdirectory(initialdir=self.pasta_saida.get() or os.getcwd())
        if pasta:
            self.pasta_saida.set(pasta)

    def adicionar_arquivos(self) -> None:
        arquivos = filedialog.askopenfilenames(
            title="Selecione os rascunhos (.xls) ou conferências (.xls)",
            filetypes=[("Planilhas", "*.xls *.xlsx"), ("Todos", "*.*")])
        if arquivos:
            self._carregar(list(arquivos))

    def adicionar_pasta(self) -> None:
        pasta = filedialog.askdirectory(title="Pasta com os rascunhos")
        if not pasta:
            return
        arquivos = [os.path.join(pasta, n) for n in sorted(os.listdir(pasta))
                    if n.lower().endswith((".xls", ".xlsx"))]
        if arquivos:
            self._carregar(arquivos)

    def limpar(self) -> None:
        self.docs.clear()
        self.achados.clear()
        self.resultados.clear()
        for tv in (self.tv_docs, self.tv_ach, self.tv_saida):
            tv.delete(*tv.get_children())
        self.lbl_entradas.config(text="Nenhum arquivo carregado.")
        self.lbl_resumo.config(text="Sem conferência.")
        self.status.set("Pronto.")

    def _carregar(self, caminhos: List[str]) -> None:
        self._ocupado(True, f"Lendo {len(caminhos)} arquivo(s)…")
        erros = []
        for caminho in caminhos:
            try:
                doc = rascunho.ler_rascunho(caminho)
                self.docs.append(doc)
            except Exception as e:                     # noqa: BLE001
                erros.append(f"{os.path.basename(caminho)}: {e}")
        self._repreencher_docs()
        self._ocupado(False)
        if erros:
            messagebox.showwarning("Alguns arquivos não puderam ser lidos", "\n".join(erros[:8]))
        self.validar()

    def _repreencher_docs(self) -> None:
        self.tv_docs.delete(*self.tv_docs.get_children())
        for d in self.docs:
            nums = ", ".join(f"{a.numero:02d}" for a in d.anexos)
            self.tv_docs.insert("", "end", values=(
                d.tipo, d.periodo.exercicio if d.periodo else "?", str(d.periodo) if d.periodo else "?",
                nums, d.versao_layout or "-", d.arquivo_origem))
        self.lbl_entradas.config(
            text=f"{len(self.docs)} documento(s) · {sum(len(d.anexos) for d in self.docs)} anexo(s)")

    def validar(self) -> None:
        if not self.docs:
            return
        self._ocupado(True, "Conferindo…")
        self.achados.clear()
        for d in self.docs:
            self.achados.extend(validacao.validar_documento(d))
        self._repreencher_achados()
        self._ocupado(False)

    def _repreencher_achados(self) -> None:
        self.tv_ach.delete(*self.tv_ach.get_children())
        so_erros = self.var_so_erros.get()
        for a in self.achados:
            if so_erros and a.severidade != "erro":
                continue
            self.tv_ach.insert("", "end", tags=(a.severidade,), values=(
                a.severidade.upper(), a.anexo, a.bloco[:40], a.linha[:60], a.regra,
                a.mensagem, gerador.fmt_moeda(a.esperado), gerador.fmt_moeda(a.encontrado)))
        r = validacao.resumo(self.achados)
        self.lbl_resumo.config(
            text=f"{r['erro']} erro(s) · {r['alerta']} alerta(s) · {len(self.achados)} achado(s)")

    def gerar(self) -> None:
        if not self.docs:
            messagebox.showinfo("Nada para gerar", "Adicione ao menos um rascunho.")
            return
        pasta = self.pasta_saida.get().strip() or os.path.join(os.getcwd(), "saida")
        self._ocupado(True, "Gerando demonstrativos…")
        self.resultados.clear()
        self.tv_saida.delete(*self.tv_saida.get_children())
        try:
            for d in self.docs:
                self.resultados.extend(gerador.gerar_documento(d, pasta))
        except Exception as e:                         # noqa: BLE001
            self._ocupado(False)
            messagebox.showerror("Falha ao gerar", str(e))
            return
        for r in self.resultados:
            status = "gerado" if r.get("status") == "ok" else r.get("status", "?")
            arquivos = "\n".join(os.path.basename(x) for x in r.get("arquivos", [])) or r.get("mensagem", "")
            self.tv_saida.insert("", "end", tags=(("ok",) if status == "gerado" else ("pendente",)),
                                 values=(r.get("anexo"), status, arquivos))
        self._ocupado(False)
        self.status.set(f"Concluído: {sum(1 for r in self.resultados if r.get('status') == 'ok')} "
                        f"anexo(s) gerado(s) em {pasta}")
        self.nb.select(2)

    def abrir_saida(self) -> None:
        pasta = self.pasta_saida.get().strip()
        if not os.path.isdir(pasta):
            messagebox.showinfo("Pasta inexistente", "Gere os demonstrativos primeiro.")
            return
        if sys.platform.startswith("win"):
            os.startfile(pasta)                        # noqa: S606
        else:
            subprocess.Popen(["xdg-open", pasta])      # noqa: S603,S607

    # ------------------------------------------------------------------ util
    def _ocupado(self, ativo: bool, msg: Optional[str] = None) -> None:
        if ativo:
            self.progresso.start(12)
            self.configure(cursor="watch")
            if msg:
                self.status.set(msg)
        else:
            self.progresso.stop()
            self.configure(cursor="")
        self.update_idletasks()


def rodar() -> None:
    App().mainloop()


if __name__ == "__main__":
    rodar()
