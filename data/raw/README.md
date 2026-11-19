# Repositório de Dados Brutos (Raw Data) - Censo Demográfico 2022 (IBGE)

Este diretório é destinado ao armazenamento dos arquivos brutos originais referentes aos microdados da amostra do Censo Demográfico 2022 para o Estado do **Rio de Janeiro (UF 33)**.

Em estrita consonância com os **Princípios FAIR** e com as boas práticas de versionamento no GitHub:
- Arquivos com tamanho superior a 50 MB (como `Pessoas_33_publico.csv` com ~377 MB e `Domicilios_33_publico.csv` com ~61 MB) são ignorados pelo `.gitignore` para evitar exceder os limites rígidos do GitHub (100 MB por arquivo).
- Para assegurar a **acessibilidade universal (Pilar Accessible)** e **reprodutibilidade (Pilar Reusable)**, disponibiliza-se neste diretório o script automatizado `download_raw_data.py`.

---

## 📋 Inventário das Fontes de Dados Primárias

| Arquivo Bruto | Dimensão Aproximada | Registros (UF 33) | Fonte Oficial | Descrição |
| :--- | :---: | :---: | :--- | :--- |
| `Domicilios_33_publico.csv` | ~61,2 MB | 431.768 | IBGE (FTP Oficial) | Características das habitações, saneamento, água, energia, internet e renda domiciliar. |
| `Familia_33_publico.csv` | ~26,8 MB | 345.752 | IBGE (FTP Oficial) | Estrutura de convivência, tipologia de família, chefia familiar e renda per capita. |
| `Mortalidade_33_publico.csv` | ~1,5 MB | 26.594 | IBGE (FTP Oficial) | Registro dos óbitos ocorridos entre janeiro de 2019 e julho de 2022 (impacto pandêmico). |
| `Pessoas_33_publico.csv` | ~377,4 MB | 1.129.665 | IBGE (FTP Oficial) | Perfil demográfico completo, sexo, raça/cor, idade, alfabetização, educação e trabalho. |

---

## 🚀 Como Obter os Dados Brutos Automaticamente

Para baixar todos os arquivos diretamente do repositório FTP oficial do IBGE para esta pasta, execute no terminal:

```bash
python download_raw_data.py
```

Ou, caso prefira o download manual direto pelo navegador:
- **Portal de Microdados do IBGE:** [https://www.ibge.gov.br/estatisticas/portais-de-dados/portal-de-microdados](https://www.ibge.gov.br/estatisticas/portais-de-dados/portal-de-microdados)
- **Repositório FTP Direto:** [ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Microdados_e_Areas_de_Ponderacao/Microdados_de_acesso_Publico/](ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Microdados_e_Areas_de_Ponderacao/Microdados_de_acesso_Publico/)

---

## 🔒 Licença dos Dados Originais
Os dados abertos governamentais do Censo Demográfico são de domínio público, regidos pela Lei Federal nº 12.527/2011 (Lei de Acesso à Informação - LAI) e licenciados pelo Instituto Brasileiro de Geografia e Estatística (IBGE) sob termos compatíveis com **Creative Commons Atribuição 4.0 Internacional (CC-BY 4.0)**.
