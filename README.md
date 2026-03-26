# PassGen

PassGen é um gerador de senhas local desenvolvido em Python. A aplicação utiliza a biblioteca `customtkinter` para prover uma interface gráfica (GUI) moderna e responsiva. O núcleo de geração de senhas baseia-se no módulo `secrets` da biblioteca padrão do Python, garantindo a utilização de um Gerador de Números Pseudoaleatórios Criptograficamente Seguro (CSPRNG) para a seleção dos caracteres, o que protege contra ataques de previsibilidade.

## Detalhes de Implementação e Funcionalidades
- **Algoritmo de Geração Seguro:** Quando o usuário seleciona os pools de caracteres disponíveis (maiúsculas, minúsculas, números, símbolos), o algoritmo garante a inclusão estrita de pelo menos um caractere de cada pool selecionado. O restante do comprimento alvo (configurável através de um slider, de 6 a 64) é preenchido de forma estocástica através de `secrets.choice()`. Por fim, o array resultante sofre um embaralhamento in-place via `secrets.SystemRandom().shuffle()` para evitar padrões posicionais determinísticos.
- **Análise de Entropia (zxcvbn):** A força da senha em tempo real é avaliada utilizando a implementação em Python da biblioteca `zxcvbn`. Em vez de executar verificações ingênuas baseadas apenas em complexidade (ex: "tem que conter 1 símbolo"), ela testa contra dicionários, substituições comuns (1337 sP3@k), repetições estruturais e vazamentos conhecidos de bancos de dados. Esta estimativa de entropia resulta na classificação de segurança e preenche a barra de feedback em tela.
- **Gerenciamento de Área de Transferência:** A integração com `pyperclip` permite transferir de forma rápida e segura a string final para o clipboard do sistema operacional.
- **Interface Gráfica UI/UX:** A aplicação é construída sobre o mainloop do framework tkinter, com a utilização do `customtkinter` para forçar componentes em modo escuro (Dark Mode) nativo e renderizar a exibição.

## Como rodar o projeto

1. Certifique-se de ter o Python 3.x instalado e adicionado às variáveis de ambiente (PATH).
2. Clone este repositório para sua máquina local e navegue até a pasta:
   ```bash
   git clone https://github.com/luisfelypehoffmanndev/PassGen.git
   cd PassGen
   ```
3. Crie e ative um ambiente virtual isolado para suportar as dependências do projeto:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # No Windows (PowerShell/CMD)
   source .venv/bin/activate  # No Linux/macOS
   ```
4. Instale as bibliotecas necessárias declaradas (`customtkinter`, `pyperclip`, `zxcvbn`) usando o requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
5. Execute o script principal e inicie a janela da aplicação:
   ```bash
   python app.py
   ```

---

# PassGen (English)

PassGen is a local desktop password generator built natively in Python. The application makes use of the `customtkinter` library to deliver a modern, fully responsive Graphical User Interface (GUI). Down to its core, the password generation engine relies strictly on the standard library module `secrets`, ensuring the application uses a Cryptographically Secure Pseudorandom Number Generator (CSPRNG) for character selection—thus effectively defending against potential predictability or unseeding attacks.

## Implementation Details & Technical Features
- **Secure Generation Algorithm:** Upon selecting the desired character pools (uppercase, lowercase, numerals, symbols), the application enforces that at least one character from each active pool is selected. The remaining characters needed to reach the target length (controllable via a UI slider, ranging from 6 to 64) are chosen by `secrets.choice()`. Afterwards, the algorithm uses an in-place array shuffle (`secrets.SystemRandom().shuffle()`) to guarantee there are no deterministic positional trends or clustering of character pools.
- **Real-Time Entropy Analysis (zxcvbn):** Instant feedback regarding password strength is evaluated through the `zxcvbn` library parser. Rather than validating strength through naive rule-based conditionals (e.g., "must contain special character"), it tests permutations against thousands of common dictionary words, well-known database leaks, usual spatial substitutions (leet speak), and repetitive structural patterns. The parsed result provides an entropy score which manipulates the on-screen progress bar seamlessly.
- **Clipboard Management:** Integration via the `pyperclip` external library facilitates frictionless dumping of generated strings directly to the host's system clipboard without invoking insecure subprocesses.
- **UI Architecture:** The front-end renders asynchronously by locking the process into standard tkinter's mainloop event cycle, overriding standard styles via the modern `customtkinter` engine to enforce a system-wide Dark Mode design.

## How to setup and run

1. Ensure a working Python 3.x environment is properly installed and active in your system PATH.
2. Clone the repository and move to its root directory via the command line:
   ```bash
   git clone https://github.com/luisfelypehoffmanndev/PassGen.git
   cd PassGen
   ```
3. Deploy and activate an isolated virtual environment to manage software dependencies locally:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # On Windows (PowerShell/CMD)
   source .venv/bin/activate  # On Linux/macOS
   ```
4. Bulk-install the exact required dependencies listed inside `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
5. Dispatch the Python interpreter on the main file to execute the software:
   ```bash
   python app.py
   ```
