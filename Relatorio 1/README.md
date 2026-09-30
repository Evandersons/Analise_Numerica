# Análise Numérica e Cálculo Numérico

Repositório dedicado à implementação e análise de métodos numéricos para a disciplina de **Análise Numérica da Universidade Estadual de Santa Cruz (UESC)**.

O projeto abrange a implementação de métodos numéricos relacionados aos seguintes conteúdos:

* **Capítulo 3:** Resolução de zeros de funções;
* **Capítulo 4:** Sistemas lineares diretos e sistemas mal-condicionados;
* **Capítulo 5:** Métodos iterativos aplicados a EDPs e circuitos.

---

## 📂 Estrutura do Repositório

A organização do projeto está dividida em diretórios responsáveis pelo código-fonte, arquivos de entrada, resultados e testes automatizados.

```text
.
├── codigo/
│   ├── lista1/
│   │   ├── exe_3_3.py
│   │   ├── exe_4_1.py
│   │   └── exe_5_1.py
│   ├── metodos/
│   │   ├── raizes.py
│   │   └── matrizes.py
│   └── ferramentas.py
│
├── dados/
│   ├── entradas/
│   │   └── arquivos .txt de configuração
│   └── saida/
│       └── arquivos .csv e resumos
│
└── testes/
    └── testes unitários
```

### `codigo/`

Contém os scripts executáveis dos exercícios e os módulos responsáveis pela implementação dos métodos numéricos.

* `codigo/lista1/`: scripts correspondentes aos exercícios;
* `codigo/metodos/raizes.py`: métodos relacionados à resolução de zeros de funções;
* `codigo/metodos/matrizes.py`: métodos relacionados a matrizes e sistemas lineares;
* `codigo/ferramentas.py`: funções auxiliares utilizadas pelos demais módulos.

### `dados/entradas/`

Contém os arquivos `.txt` utilizados para configurar os parâmetros de execução dos métodos, como tolerâncias e quantidade máxima de iterações.

### `dados/saida/`

Armazena os resultados produzidos durante a execução dos programas, incluindo:

* históricos das iterações;
* resultados numéricos;
* arquivos `.csv`;
* resumos utilizados na geração de documentos em LaTeX.

### `testes/`

Contém a suíte de testes unitários utilizada para verificar o funcionamento das funções implementadas.

---

# 🚀 Tutorial Rápido

## 1. Configuração dos arquivos de entrada

Antes de executar os exercícios, verifique os arquivos de configuração localizados em:

```text
dados/entradas/
```

Esses arquivos contêm parâmetros necessários para a execução dos métodos, como:

* tolerância numérica;
* número máximo de iterações;
* outros parâmetros específicos de cada exercício.

Caso a pasta de entradas seja apagada ou um novo exercício seja executado sem possuir um arquivo de configuração correspondente, o programa poderá criar automaticamente um **template padrão**.

Esse arquivo poderá ser posteriormente editado de acordo com os parâmetros definidos no enunciado do exercício.

---

# 🧪 2. Executando os Testes Unitários

Os testes unitários permitem verificar se as principais funções matemáticas do projeto estão funcionando corretamente.

Para executar todos os testes, abra um terminal na raiz do repositório e utilize:

```bash
python -m unittest discover testes
```

O comando procura automaticamente os testes existentes dentro do diretório:

```text
testes/
```

e executa a suíte disponível.

Os testes abrangem as principais funcionalidades relacionadas a:

* métodos para encontrar raízes;
* operações com matrizes;
* resolução de sistemas lineares;
* técnicas de pivotamento;
* funções auxiliares.

---

# ▶️ 3. Executando os Exercícios

Cada exercício possui um script independente localizado no diretório:

```text
codigo/lista1/
```

Para executar um exercício, utilize o terminal a partir da **raiz do repositório**.

A estrutura geral do comando é:

```bash
python codigo/lista1/NOME_DO_ARQUIVO.py
```

---

## 📌 Capítulo 3 — Zeros de Funções

Para executar, por exemplo, o **Exercício 3.3**, utilize:

```bash
python codigo/lista1/exe_3_3.py
```

O programa executará o método numérico implementado para o exercício e produzirá os resultados correspondentes.

Os resultados gerados poderão ser armazenados no diretório:

```text
dados/saida/
```

---

## 📌 Capítulo 4 — Sistemas Lineares

Para executar o **Exercício 4.1**, utilize:

```bash
python codigo/lista1/exe_4_1.py
```

Esse conjunto de exercícios está relacionado à resolução de sistemas lineares e às técnicas numéricas utilizadas para esse tipo de problema.

---

## 📌 Capítulo 5 — Métodos Iterativos

Para executar o **Exercício 5.1**, utilize:

```bash
python codigo/lista1/exe_5_1.py
```

Os exercícios desse capítulo envolvem métodos iterativos aplicados a problemas como **Equações Diferenciais Parciais (EDPs)** e **circuitos**.

---

# 📊 4. Arquivos de Saída

Durante a execução dos exercícios, o projeto pode gerar arquivos de resultados no diretório:

```text
dados/saida/
```

Entre os arquivos gerados podem estar:

* arquivos `.csv` contendo o histórico das iterações;
* resultados finais dos métodos;
* informações utilizadas posteriormente na análise dos resultados;
* resumos destinados à utilização em documentos LaTeX.

Os arquivos `.csv` podem ser utilizados para analisar a evolução dos métodos numéricos ao longo das iterações.

---

# 🔢 5. Fluxo de Execução

De forma geral, a utilização do projeto segue o seguinte fluxo:

```text
1. Configurar os arquivos em dados/entradas/
                ↓
2. Executar os testes unitários
                ↓
3. Executar o exercício desejado
                ↓
4. O método numérico é processado
                ↓
5. Os resultados são gerados
                ↓
6. Os arquivos são armazenados em dados/saida/
                ↓
7. Os resultados podem ser analisados
   ou utilizados na documentação em LaTeX
```

---

# 🛠️ 6. Comandos Principais

### Executar todos os testes

```bash
python -m unittest discover testes
```

### Executar o Exercício 3.3

```bash
python codigo/lista1/exe_3_3.py
```

### Executar o Exercício 4.1

```bash
python codigo/lista1/exe_4_1.py
```

### Executar o Exercício 5.1

```bash
python codigo/lista1/exe_5_1.py
```

---

# 📚 Conteúdos Abrangidos

O projeto contempla diferentes técnicas de **Análise Numérica e Cálculo Numérico**, organizadas de acordo com os capítulos trabalhados na disciplina.

| Capítulo | Conteúdo                                               |
| -------- | ------------------------------------------------------ |
| **3**    | Zeros de funções                                       |
| **4**    | Sistemas lineares diretos e sistemas mal-condicionados |
| **5**    | Métodos iterativos aplicados a EDPs e circuitos        |

---

# 📝 Observações

Para garantir o funcionamento adequado dos exercícios:

1. Execute os comandos a partir da raiz do repositório.
2. Verifique os arquivos presentes em `dados/entradas/`.
3. Confira os parâmetros de tolerância e número máximo de iterações.
4. Execute os testes unitários antes de validar os resultados dos exercícios.
5. Consulte os arquivos gerados em `dados/saida/` após a execução.

---

# 📌 Resumo

Este repositório reúne as implementações desenvolvidas para a disciplina de **Análise Numérica**, organizando os códigos, configurações, testes e resultados de forma estruturada.

A separação entre código, dados de entrada, dados de saída e testes facilita a execução dos métodos, a validação das implementações e a análise dos resultados obtidos.
