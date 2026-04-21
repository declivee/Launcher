import os

def carregar_ultima_versao(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return None
    
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linha = f.read().strip()
        return linha if linha else None


def incrementar_versao(versao):
    versao_num = versao.replace("V.", "")
    major, minor, patch = map(int, versao_num.split("."))

    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
    if minor > 9:
        minor = 0
        major += 1

    return f"V.{major}.{minor}.{patch}"


def gerar_versao(nome_arquivo="version.txt"):
    ultima = carregar_ultima_versao(nome_arquivo)

    if ultima is None:
        nova_versao = "V.1.0.0"
    else:
        nova_versao = incrementar_versao(ultima)

    # Sobrescreve mantendo só a nova versão
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(nova_versao)

    print(f"Nova versão criada: {nova_versao}")
    return nova_versao


if __name__ == "__main__":
    gerar_versao("version.txt")
