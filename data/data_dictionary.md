# 📖 Dicionário de Metadados e Variáveis (FAIR Data Dictionary)

**Projeto:** Desigualdades Socioterritoriais, Estrutura Familiar e Mortalidade no Estado do Rio de Janeiro: Análise Multidimensional dos Microdados do Censo 2022  
**Autores:** Ysis Barbosa Gomes & Ygor Barbosa Gomes  
**Docente / Orientador:** Prof. Alexandre Neves Louzada  
**Instituição:** Bacharelado em Sistemas de Informação — 6º Período  
**Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python)  
**Fonte Primária:** Instituto Brasileiro de Geografia e Estatística (IBGE) — Censo Demográfico 2022: Microdados da Amostra (Acesso Público, UF 33 - RJ)  
**Padrão de Conformidade:** Princípios FAIR (Pilar Interoperable & Reusable)  
**Formato de Persistência:** Apache Parquet (colunar, compressão Snappy) e CSV Comprimido (GZIP, codificação UTF-8)  

---

## 📑 Sumário
1. [Convenções Gerais e Chaves de Relacionamento](#1-convenções-gerais-e-chaves-de-relacionamento)
2. [Tabela 1: Domicílios (`domicilios_rj_clean.parquet`)](#2-tabela-1-domicílios-domicilios_rj_cleanparquet)
3. [Tabela 2: Famílias (`familias_rj_clean.parquet`)](#3-tabela-2-famílias-familias_rj_cleanparquet)
4. [Tabela 3: Mortalidade (`mortalidade_rj_clean.parquet`)](#4-tabela-3-mortalidade-mortalidade_rj_cleanparquet)
5. [Tabela 4: Pessoas (`pessoas_amostra_rj_clean.parquet`)](#5-tabela-4-pessoas-pessoas_amostra_rj_cleanparquet)
6. [Tabela 5: Dataset Integrado (`domicilios_obitos_integrados.parquet`)](#6-tabela-5-dataset-integrado-domicilios_obitos_integradosparquet)

---

## 1. Convenções Gerais e Chaves de Relacionamento

- **Chave Primária do Domicílio:** `id_domicilio` (código original `D0100` / `F0100` / `M0100` / `P0100`). Permite a linkagem relacional determinística 1:N entre o domicílio e seus respectivos residentes, núcleos familiares e registros de óbito.
- **Fator de Expansão Amostral:** `peso_amostral` (códigos originais `D0110`, `F0110`, `M0110`, `P0110`). Peso calibrado pelo IBGE para projeção populacional na UF do Rio de Janeiro.
- **Valores Ausentes / Não Declarados:** Dados nulos representam não-aplicabilidade normativa do quesito (ex.: perguntas sobre trabalho restritas a maiores de 14 anos) ou resposta não informada.
- **Moeda de Referência:** Real Brasileiro (BRL / R$), com o Salário Mínimo de 2022 estipulado em **R$ 1.212,00**.

---

## 2. Tabela 1: Domicílios (`domicilios_rj_clean.parquet`)

Contém 431.768 observações sobre as características físicas, infraestrutura sanitária e rendimentos das unidades habitacionais do Rio de Janeiro.

| Campo Tratado | Código Original IBGE | Tipo Primitivo | Descrição Semântica / Pesquisa | Domínio / Valores Válidos |
| :--- | :--- | :--- | :--- | :--- |
| `id_domicilio` | `D0100` | `int64` | Identificador único de controle do domicílio | Inteiro positivo |
| `peso_amostral` | `D0110` | `float64` | Peso de calibração amostral do domicílio | Contínuo positivo |
| `cod_situacao_setor` | `D0120` | `int64` | Tipologia de adensamento do setor censitário | `1`: Urbano alta densidade; `2`: Urbano baixa densidade; `3`: Núcleo urbano; `5`: Povoado; `6`: Núcleo rural; `7`: Lugarejo; `8`: Rural exclusivo |
| `cod_situacao_domicilio` | `D0140` | `int64` | Código de localização territorial | `1`: Urbana; `2`: Rural |
| `situacao_domicilio` | Derivado de `D0140` | `category` | Situação geográfica decodificada | `'Urbana'`, `'Rural'` |
| `total_moradores` | `D0150` | `int64` | Quantidade total de moradores no domicílio | Inteiro (1 a 30) |
| `total_criancas` | `D0160` | `int64` | Quantidade de crianças residentes | Inteiro (0 a 15) |
| `sexo_responsavel_domicilio` | `D0170` | `int64` | Sexo da pessoa de referência da habitação | `1`: Masculino; `2`: Feminino; `9`: Ignorado |
| `cod_condicao_ocupacao` | `D0190` | `float64` | Condição de posse do imóvel | `1`: Próprio pago; `2`: Próprio pagando; `3`: Alugado; `4`: Cedido empregador; `5`: Cedido familiar; `6`: Cedido outro; `7`: Outro |
| `cod_esgotamento_sanitario` | `D0250` | `float64` | Forma de escoamento dos dejetos sanitários | `1`: Rede geral; `2`: Fossa ligada rede; `3`: Fossa não ligada; `4`: Fossa rudimentar; `5`: Vala céu aberto; `6`: Rio/mar; `7`: Outro; `9`: Sem sanitário |
| `esgotamento_descricao` | Derivado de `D0250` | `object` | Descrição textual da condição sanitária | Nomes categóricos das opções |
| `cod_abastecimento_agua` | `D0260` | `float64` | Principal forma de abastecimento hídrico | `1`: Rede geral; `2`: Poço profundo; `3`: Poço raso; `4`: Fonte/mina; `5`: Carro-pipa; `6`: Chuva; `7`: Rios/lagos; `8`: Outra |
| `abastecimento_agua_descricao` | Derivado de `D0260` | `object` | Descrição textual da fonte de água | Nomes categóricos das opções |
| `cod_destino_lixo` | `D0310` | `float64` | Destino final dos resíduos sólidos | `1`: Coletado serviço limpeza; `2`: Caçamba; `3`: Queimado; `4`: Enterrado; `5`: Jogado terreno/rio; `6`: Outro |
| `destino_lixo_descricao` | Derivado de `D0310` | `object` | Descrição textual do destino de resíduos | Nomes categóricos das opções |
| `cod_acesso_internet` | `D0330` | `float64` | Existência de conexão de internet no local | `1`: Sim; `2`: Não |
| `acesso_internet_descricao` | Derivado de `D0330` | `object` | Status de inclusão digital | `'Com Acesso'`, `'Sem Acesso'` |
| `rendimento_domiciliar_total` | `D0350` | `float64` | Soma dos rendimentos de todos os residentes | Valor em R$ (0,00 a contínuo) |
| `rendimento_domiciliar_per_capita` | `D0360` | `float64` | Rendimento médio por morador (R$) | Valor em R$ (0,00 a contínuo) |
| `esgotamento_adequado` | Derivado de `D0250` | `bool` | Critério IBGE/PNSB de esgotamento adequado | `True`: Códigos 1 ou 2; `False`: Demais |
| `agua_rede_geral` | Derivado de `D0260` | `bool` | Acesso à rede pública encanada | `True`: Código 1; `False`: Demais |
| `lixo_coletado_adequado` | Derivado de `D0310` | `bool` | Coleta regular de resíduos sólidos | `True`: Códigos 1 ou 2; `False`: Demais |
| `saneamento_basico_pleno` | Derivado | `bool` | Atendimento simultâneo de água, esgoto e lixo | `True`: Atende aos 3 requisitos; `False`: Déficit |
| `possui_internet` | Derivado de `D0330` | `bool` | Conectividade digital domiciliar ativa | `True`: Sim; `False`: Não |
| `faixa_renda_sm` | Derivado de `D0360` | `object` | Estrato social por Salários Mínimos (2022) | Extrema pobreza, Pobreza, Baixa renda, Renda média-baixa, Renda média, Renda alta |

---

## 3. Tabela 2: Famílias (`familias_rj_clean.parquet`)

Contém 345.752 registros de arranjos de convivência familiar no Rio de Janeiro.

| Campo Tratado | Código Original IBGE | Tipo Primitivo | Descrição Semântica / Pesquisa | Domínio / Valores Válidos |
| :--- | :--- | :--- | :--- | :--- |
| `id_domicilio` | `F0100` | `int64` | Identificador de controle do domicílio | Inteiro positivo |
| `id_ordem_familia` | `F0101` | `object` | Ordem da família na habitação (`F001`, etc.) | Alfanumérico |
| `peso_amostral` | `F0110` | `float64` | Fator de calibração populacional da família | Contínuo positivo |
| `situacao_domicilio` | Derivado de `F0140` | `category` | Situação de localização territorial | `'Urbana'`, `'Rural'` |
| `total_pessoas_familia`| `F0160` | `int64` | Quantidade de membros do núcleo familiar | Inteiro (1 a 20) |
| `cod_sexo_responsavel` | `F0170` | `float64` | Sexo da pessoa de referência familiar | `1`: Masculino; `2`: Feminino |
| `sexo_responsavel` | Derivado de `F0170` | `object` | Sexo decodificado | `'Masculino'`, `'Feminino'` |
| `cod_raca_responsavel` | `F0200` | `float64` | Cor/raça da pessoa responsável | `1`: Branca; `2`: Preta; `3`: Amarela; `4`: Parda; `5`: Indígena |
| `raca_responsavel` | Derivado de `F0200` | `object` | Cor/raça decodificada | `'Branca'`, `'Preta'`, `'Parda'`, etc. |
| `cod_instrucao_responsavel` | `F0190` | `float64` | Escolaridade máxima do responsável | `1`: Sem instr./Fund. inc.; `2`: Fund. compl./Médio inc.; `3`: Médio compl./Sup. inc.; `4`: Superior completo |
| `instrucao_responsavel` | Derivado de `F0190` | `object` | Escolaridade decodificada | Nomes formais dos estratos de ensino |
| `cod_tipologia_familiar` | `F0210` | `float64` | Arranjo de parentalidade e convivência | `1`: Casal s/ filhos; `3`: Casal c/ filhos; `5`: Monoparental feminina; `7`: Monoparental masculina; etc. |
| `tipologia_familiar` | Derivado de `F0210` | `object` | Descrição formal da tipologia familiar | Classes de núcleos familiares |
| `rendimento_familiar_per_capita` | `F0260` | `float64` | Rendimento médio por componente familiar | Valor contínuo em R$ |
| `is_chefiada_por_mulher` | Derivado de `F0170`| `bool` | Identificador de liderança familiar feminina | `True`: Feminino; `False`: Masculino |
| `is_monoparental_feminina` | Derivado de `F0210`| `bool` | Família liderada por mãe solo com filhos | `True`: Códigos 5 ou 6; `False`: Demais |
| `em_extrema_pobreza` | Derivado de `F0260`| `bool` | Condição de rendimento per capita <= 1/4 SM | `True`: Até R$ 303,00; `False`: Acima |

---

## 4. Tabela 3: Mortalidade (`mortalidade_rj_clean.parquet`)

Contém 26.594 eventos de mortalidade domiciliar informados no estado entre janeiro de 2019 e julho de 2022.

| Campo Tratado | Código Original IBGE | Tipo Primitivo | Descrição Semântica / Pesquisa | Domínio / Valores Válidos |
| :--- | :--- | :--- | :--- | :--- |
| `id_domicilio` | `M0100` | `int64` | Identificador do domicílio de ocorrência | Inteiro positivo |
| `id_ordem_falecido` | `M0101` | `object` | Sequencial do óbito na habitação | `M001`, `M002`, etc. |
| `peso_amostral` | `M0110` | `float64` | Fator de calibração amostral do evento | Contínuo positivo |
| `situacao_domicilio` | Derivado de `M0140` | `category` | Situação geográfica de residência | `'Urbana'`, `'Rural'` |
| `ano_obito` | Derivado de `M0150` | `int64` | Ano civil do falecimento | `2019`, `2020`, `2021`, `2022` |
| `sexo_falecido` | Derivado de `M0160` | `object` | Sexo da pessoa que veio a óbito | `'Masculino'`, `'Feminino'` |
| `faixa_etaria_falecido` | Derivado de `M0170` | `object` | Intervalo etário quinquenal ao falecer | `'0 a 4 anos'`, ..., `'80 anos ou mais'` |
| `grupo_etario_falecido` | Derivado | `object` | Macrociclo de vida ao falecer | Crianças (0-14), Jovens (15-29), Adultos (30-59), Idosos (60+) |
| `periodo_pandemico` | Derivado | `bool` | Marcação dos anos de pico da COVID-19 | `True`: Anos 2020 e 2021; `False`: 2019 e 2022 |

---

## 5. Tabela 4: Pessoas (`pessoas_amostra_rj_clean.parquet`)

Amostra contendo 1.129.665 pessoas recenseadas com recortes de educação e renda.

| Campo Tratado | Código Original IBGE | Tipo Primitivo | Descrição Semântica / Pesquisa | Domínio / Valores Válidos |
| :--- | :--- | :--- | :--- | :--- |
| `id_domicilio` | `P0100` | `int64` | Chave de ligação com a habitação | Inteiro positivo |
| `peso_amostral` | `P0110` | `float64` | Fator de expansão individual | Contínuo positivo |
| `situacao_domicilio` | Derivado de `P0140` | `category` | Recorte espacial de moradia | `'Urbana'`, `'Rural'` |
| `sexo` | Derivado de `P0150` | `object` | Identificação de sexo biológico | `'Masculino'`, `'Feminino'` |
| `raca` | Derivado de `P0210` | `object` | Autodeclaração de cor ou raça | `'Branca'`, `'Preta'`, `'Parda'`, etc. |
| `faixa_etaria` | Derivado de `P0180` | `object` | Faixa etária do morador | Estratos de 5 em 5 anos |
| `alfabetizado` | Derivado de `P0640` | `object` | Habilidade de ler e escrever bilhete simples | `'Sim'`, `'Não'` |
| `nivel_instrucao` | Derivado de `P0760` | `object` | Grau máximo de escolaridade atingido | Sem instrução até Superior completo |
| `rendimento_trabalho_habitual` | `P1080` | `float64` | Remuneração mensal do trabalho habitual | Valor em R$ |
| `possui_deficiencia` | Derivado de `P0470` | `bool` | Indicador de presença de deficiência | `True`: Sim; `False`: Não |

---

## 6. Tabela 5: Dataset Integrado (`domicilios_obitos_integrados.parquet`)

Resultado da união relacional (*linkage*) entre `Domicílios` e métricas acumuladas de `Mortalidade`, permitindo cruzar condições de moradia e renda com a mortalidade observada na habitação.

| Campo Integrado | Tipo Primitivo | Descrição Semântica / Pesquisa |
| :--- | :--- | :--- |
| `id_domicilio` | `int64` | Chave primária do domicílio |
| Atributos de Domicílio | `mixed` | Todos os atributos sanitários e socioeconômicos da Tabela 1 |
| `total_obitos` | `int64` | Quantidade total de óbitos reportados naquele domicílio entre 2019 e 2022 |
| `teve_obito_2021` | `bool` | Indicador se o domicílio sofreu luto no ano de ápice da COVID-19 (2021) |
| `obitos_homens` | `int64` | Total de pessoas do sexo masculino falecidas no domicílio |
| `obitos_mulheres` | `int64` | Total de pessoas do sexo feminino falecidas no domicílio |
| `obitos_idosos` | `int64` | Total de residentes idosos (60+ anos) falecidos no domicílio |
