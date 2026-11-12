# Publicar no GitHub

O repositório está **preparado** (`.gitignore`, `README.md`, `LICENSE`,
`requirements.txt`), mas o **Git não está instalado** nesta máquina — e o
`winget install Git.Git` falhou (sem acesso de rede no ambiente atual).

São três passos: instalar o Git, criar o repositório vazio no GitHub, rodar o
`publicar.bat`.

---

## 1. Instalar o Git

Baixe em **https://git-scm.com/download/win** e instale com as opções padrão.

Depois de instalar, **feche e abra** o terminal (o PATH só atualiza em sessões
novas). Confirme:

```bash
git --version
```

## 2. Criar o repositório vazio no GitHub

1. Acesse **https://github.com/new**
2. **Repository name**: `gerador-relatorios-fiscais` (ou o nome que preferir)
3. **Não** marque "Add a README file", "Add .gitignore" nem "Choose a license" —
   eles já existem no projeto e causariam conflito no primeiro push
4. Clique em **Create repository**
5. Copie a URL, algo como `https://github.com/seuusuario/gerador-relatorios-fiscais.git`

## 3. Rodar o `publicar.bat`

Duplo clique em **`publicar.bat`** e cole a URL quando pedido.

Ele executa:

```bash
git init
git branch -M main
git add -A
git commit -m "Gerador de relatorios fiscais RREO/RGF a partir da MSC"
git remote add origin <URL>
git push -u origin main
```

---

## O que vai e o que não vai

O `.gitignore` bloqueia o que **não pode** ser publicado:

| Bloqueado | Motivo |
|---|---|
| `dados/` | matrizes contábeis do Estado — **118 MB** e dados sensíveis |
| `saida/` | relatórios gerados |
| `MDF_STN/` | acervo de manuais da STN |
| `__pycache__/`, `*.pyc` | artefatos |
| `*.zip` | pacotes das matrizes |

**49 arquivos, 0,35 MB** — só código e documentação.

---

## Se preferir pela linha de comando

```bash
cd RN_Fiscal

git init
git branch -M main
git add -A
git commit -m "Gerador de relatorios fiscais RREO/RGF a partir da MSC"
git remote add origin https://github.com/seuusuario/gerador-relatorios-fiscais.git
git push -u origin main
```

Se o push pedir credenciais, use um **Personal Access Token** (GitHub →
Settings → Developer settings → Personal access tokens → Tokens (classic) → scope
`repo`). Senha comum não funciona desde 2021.

---

## Antes de publicar — revise

1. **Dados sensíveis.** Confira que `dados/` não entrou:
   ```bash
   git status --short
   ```
   Não deve aparecer nenhum caminho começando com `dados/` ou `saida/`.

2. **Autoria do commit.** O `publicar.bat` usa `Victor <victor@localhost>`.
   Para usar seu e-mail do GitHub:
   ```bash
   git config --global user.name "Seu Nome"
   git config --global user.email "seu@email.com"
   ```
   O e-mail precisa estar associado à sua conta, senão o commit não aparece como
   seu no perfil.

3. **Licença.** O `LICENSE` está como MIT com o titular "Victor". Ajuste se
   quiser outro nome ou outra licença.

---

## Sugestões para o repositório

- **Descrição**: "Gerador de demonstrativos do RGF a partir da Matriz de Saldos
  Contábeis do Siconfi — MDF 14ª edição"
- **Topics**: `contabilidade-publica`, `siconfi`, `rgf`, `rreo`, `lrf`, `msc`,
  `tesouro-nacional`, `python`
- **About → Releases**: nenhum release ainda; o primeiro pode ser a versão com os
  seis anexos do RGF

---

## Se quiser publicar as matrizes de exemplo

Não publique as reais. Se quiser um exemplo funcional no repositório, crie um
`exemplos/` com uma matriz **sintética** (poucos lançamentos, dados fictícios) e
um teste que rode o pipeline sobre ela. Isso documenta o formato sem expor dado
do Estado.

O formato aceito é simples — a primeira linha é o cabeçalho e as demais são os
lançamentos:

```
24EX;2024-12
CONTA;IC1;TIPO1;IC2;TIPO2;IC3;TIPO3;IC4;TIPO4;IC5;TIPO5;IC6;TIPO6;Valor;Tipo_valor;Natureza_valor
622130400;10111;PO;1500;FR;31901100;ND;;;;;;;1000000,00;ending_balance;C
```
