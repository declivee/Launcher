# Passo a Passo para Executar o Launcher 

Este guia explica como preparar o ambiente, instalar dependências e executar o *Launcher* baseado no código fornecido.

<img width="582" height="273" alt="Screenshot_6" src="https://github.com/user-attachments/assets/45269ffe-87fe-4e29-9b42-316733ea0383" />



---

## 📌 1. Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* **Python 3.10+**

---

## 📥 2. Instalar dependências

O launcher utiliza diversas bibliotecas como **PyQt6**, **requests**, entre outras.

No cmd, execute:

```
py -m pip install Nuitka PyQt6 requests
```

---

## 📁 3. Preparar a Estrutura de Pastas

Crie a seguinte estrutura na mesma pasta do script:

```
/launcher
 ├── data/
 │    ├── icon.ico
 │    └── background.png
 └── launcher.py
```

> A pasta **data** é obrigatória para que o launcher carregue o ícone e o fundo.

---

## 🌐 4. Configurar URLs Importantes

Para que o launcher consiga baixar atualizações automaticamente, você precisa publicar releases no GitHub acompanhadas do arquivo ZIP com o jogo atualizado e da versão correspondente. Portanto no main do github precisa conter o version.txt e no release os upload seguido das versões.

O script acessa:

* versão no GitHub
* zip do cliente (release)
* site do jogo
* convite do Discord

Verifique se todos os links estão funcionando corretamente.
 

### ✔ Passo a passo para criar uma release

1. **Acesse seu repositório no GitHub**
2. No menu superior, clique em **Releases**


<img width="581" height="360" alt="Screenshot_1" src="https://github.com/user-attachments/assets/70c26f8a-ae65-4dff-b3b9-e20890f54972" />


3. Clique no botão **Draft a new release**

### ✔ 1. Escolher a tag da versão

* No campo **Tag version**, coloque a versão no formato:

  ```
  v1.0.0
  ```
* Se a tag ainda não existir, clique em **Create new tag**
* Em **Target**, deixe como `main` (a menos que deseje outra branch)

### ✔ 2. Título e descrição da release

* No campo **Release title**, coloque algo como:

  ```
  Client v1.0.0
  ```
* Na descrição, você pode listar mudanças, mas é opcional.

### ✔ 3. Enviar o ZIP da nova versão do cliente

O launcher espera encontrar um arquivo ZIP para baixar.

⚠ Importante:

* O ZIP deve conter **exatamente** os arquivos do cliente (não uma pasta dentro de outra pasta).
* O nome do ZIP pode ser algo como:

  ```
  client.zip
  ```
* Clique em **Attach binaries…** e selecione o arquivo.

>Dica: Utilize sequencia de versões como = V1.0.0, V1.0.1, V1.0.2 e assim vai...

### ✔ 4. Publicar

* Clique em **Publish release**.

### ❗ MUITO IMPORTANTE

A versão definida na release **deve ser idêntica** à versão dentro do arquivo:

```
version.txt (branch main)
```

Por exemplo:

* Release: `v1.0.0`
* Conteúdo do `version.txt`:

  ```
  v1.0.0
  ```

Se forem diferentes, o launcher **sempre tentará atualizar novamente**.

---

## 🔑 5. Configurar Token do GitHub

No topo do código existe:

```
TOKEN = "seu_token_aqui"
```

O token deve ter permissões de leitura.

Para criar um token:

1. Acesse **GitHub → Settings**


<img width="564" height="755" alt="Screenshot_2" src="https://github.com/user-attachments/assets/ce0fdab6-ec6c-4af0-9ddc-c27eb2420753" />

2. Vá em **Developer settings → Personal access tokens**
3. Crie um **Classic Token** com:

   * `repo:public_repo`

Cole o token no campo correspondente.

> ⚠ *Nunca publique seu token em repositórios públicos.*

---

## ▶️ 6. Executar o Launcher

Para iniciar o launcher, no cmd digite:

```
launcher.py
```

Se tudo estiver correto, a interface gráfica será exibida.

---

## 🔄 7. Funcionamento do Atualizador

O launcher faz automaticamente:

1. Verifica versão local
2. Baixa a versão remota
3. Compara versões
4. Caso haja atualização:

   * baixa o `.zip`
   * extrai (incluindo ZIPs internos)
   * remove versão antiga
   * move nova versão para `client/`
5. Executa o jogo

---

## 🧹 8. Remover Dados do Cliente

O botão **Remove Client** apaga completamente a pasta `client/`.

Útil caso ocorra algum erro na instalação.

---

## 🔍 9. Como funciona a verificação de versão

O launcher utiliza um sistema duplo de verificação de versão, garantindo que o cliente esteja sempre atualizado.

### ✔ Onde são verificadas as versões

O código consulta dois lugares:

1. **version.txt no GitHub (branch main)**

   * Caminho: `https://raw.githubusercontent.com/<repo>/main/version.txt`
   * Esse arquivo define a versão "oficial" esperada pelo launcher.

2. **Último release no GitHub**

   * O launcher baixa o arquivo `client.zip` da release mais recente.
   * O conteúdo dessa release deve corresponder à mesma versão definida no `version.txt`.

### ✔ Regra de decisão

O processo funciona assim:

* O launcher lê a versão salva localmente em:

  ```
  client/version.txt
  ```

* Lê a versão remota do arquivo:

  ```
  version.txt (no branch main do GitHub)
  ```

* **Se forem iguais → não atualiza**

  * Ele pula o download e inicia o jogo diretamente.

* **Se forem diferentes → atualiza**

  * Faz download do último release.
  * Extrai e substitui todo o conteúdo.
  * Salva a nova versão em `client/version.txt`.

### ❗ Importante

Para evitar atualizações desnecessárias, o valor dentro de:

* `version.txt` no GitHub
* **e o conteúdo da release (ZIP) que você subiu**

**DEVEM sempre corresponder.**

Exemplo:

* Release publicada: **v1.0.0**
* Então o arquivo `version.txt` precisa conter:

  ```
  v1.0.0
  ```

Se isso não for igual, o launcher vai interpretar como atualização disponível e fará o download novamente.

---

## 🛠️ 10. Como compilar o launcher com Nuitka


### 📌 2. Gerar o executável

Use o comando abaixo na raiz do projeto:

```
py -m nuitka launcher.py ^
 --onefile ^
 --windows-console-mode=disable ^
 --enable-plugin=pyqt6 ^
 --windows-icon-from-ico="data\icon.ico" ^
 --include-data-dir="data=data"
```

O executável será gerado na pasta atual do projeto.

---

## ✔ Concluído

O launcher está pronto para uso!
