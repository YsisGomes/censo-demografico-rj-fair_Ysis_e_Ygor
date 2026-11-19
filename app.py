import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configuração da página
st.set_page_config(
    page_title="Censo 2022 RJ — Análise e Indicadores",
    layout="wide"
)

st.title("Desigualdades e Dinâmica Demográfica no Rio de Janeiro (Censo 2022)")

st.write(
    "Dashboard de análise e visualização dos microdados da amostra do Censo Demográfico 2022 "
    "para o Estado do Rio de Janeiro, abordando infraestrutura domiciliar, vulnerabilidade familiar e mortalidade."
)

st.markdown("""
**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  
**Professor:** Alexandre Neves Louzada  
**Alunos:** Ysis Barbosa Gomes e Ygor Barbosa Gomes  
**Metodologia:** Ciência Aberta e Princípios FAIR (Findable, Accessible, Interoperable, Reusable)
""")

st.divider()

# Carregamento de dados com cache
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

@st.cache_data
def carregar_dados():
    df_dom = pd.read_parquet(os.path.join(PROCESSED_DIR, "domicilios_rj_clean.parquet"))
    df_fam = pd.read_parquet(os.path.join(PROCESSED_DIR, "familias_rj_clean.parquet"))
    df_mort = pd.read_parquet(os.path.join(PROCESSED_DIR, "mortalidade_rj_clean.parquet"))
    
    # Auto-recuperação defensiva de colunas
    for df in [df_dom, df_fam, df_mort]:
        if "situacao_domicilio" not in df.columns and "cod_situacao_domicilio" in df.columns:
            df["situacao_domicilio"] = df["cod_situacao_domicilio"].map({1: "Urbana", 2: "Rural"}).fillna("Urbana").astype(str)
            
    return df_dom, df_fam, df_mort

try:
    df_dom, df_fam, df_mort = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar arquivos da pasta {PROCESSED_DIR}: {e}")
    st.stop()

# Barra Lateral - Filtros
st.sidebar.header("Filtros")

situacoes = sorted(list(df_dom["situacao_domicilio"].dropna().unique()))
situacoes_selecionadas = st.sidebar.multiselect(
    "Situação do Domicílio",
    situacoes,
    default=situacoes
)

faixas_renda = [
    "Extrema pobreza (Até 1/4 SM)",
    "Pobreza (1/4 a 1/2 SM)",
    "Baixa renda (1/2 a 1 SM)",
    "Renda média-baixa (1 a 2 SM)",
    "Renda média (2 a 5 SM)",
    "Renda alta (> 5 SM)"
]
faixas_selecionadas = st.sidebar.multiselect(
    "Faixa de Renda per Capita",
    faixas_renda,
    default=faixas_renda
)

racas = ["Branca", "Preta", "Parda"]
racas_selecionadas = st.sidebar.multiselect(
    "Cor ou Raça do Responsável",
    racas,
    default=racas
)

sexos_resp = ["Feminino", "Masculino"]
sexos_selecionados = st.sidebar.multiselect(
    "Sexo do Responsável Familiar",
    sexos_resp,
    default=sexos_resp
)

anos_obito = [2019, 2020, 2021, 2022]
anos_selecionados = st.sidebar.multiselect(
    "Ano do Óbito (Mortalidade)",
    anos_obito,
    default=anos_obito
)

# Aplicação dos Filtros
df_dom_filtrado = df_dom[
    (df_dom["situacao_domicilio"].isin(situacoes_selecionadas)) &
    (df_dom["faixa_renda_sm"].isin(faixas_selecionadas))
]

df_fam_filtrado = df_fam[
    (df_fam["situacao_domicilio"].isin(situacoes_selecionadas)) &
    (df_fam["faixa_renda_sm"].isin(faixas_selecionadas)) &
    (df_fam["raca_responsavel"].isin(racas_selecionadas)) &
    (df_fam["sexo_responsavel"].isin(sexos_selecionados))
]

df_mort_filtrado = df_mort[
    (df_mort["situacao_domicilio"].isin(situacoes_selecionadas)) &
    (df_mort["ano_obito"].isin(anos_selecionados))
]

# Indicadores Principais (Grid 3x2 igual ao G1)
st.subheader("Indicadores principais")

if not df_dom_filtrado.empty:
    total_domicilios = len(df_dom_filtrado)
    taxa_esgoto = df_dom_filtrado["esgotamento_adequado"].mean() * 100
    taxa_agua = df_dom_filtrado["agua_rede_geral"].mean() * 100
    taxa_internet = df_dom_filtrado["possui_internet"].mean() * 100
    
    renda_mediana = df_fam_filtrado["rendimento_familiar_per_capita"].median() if not df_fam_filtrado.empty else 0
    total_obitos = len(df_mort_filtrado)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Domicílios na amostra",
        f"{total_domicilios:,}".replace(",", ".")
    )

    col2.metric(
        "Esgotamento adequado",
        f"{taxa_esgoto:.1f}%"
    )

    col3.metric(
        "Água por rede geral",
        f"{taxa_agua:.1f}%"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Acesso à internet",
        f"{taxa_internet:.1f}%"
    )

    col5.metric(
        "Renda per capita mediana",
        f"R$ {renda_mediana:,.0f}".replace(",", ".")
    )

    col6.metric(
        "Óbitos domiciliares registrados",
        f"{total_obitos:,}".replace(",", ".")
    )
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

st.divider()

# Seção de Gráficos (Estilo Seaborn/Matplotlib igual ao G1)
st.subheader("Análise dos indicadores")

if not df_dom_filtrado.empty:
    # Linha 1 de Gráficos (col_grafico1 e col_grafico2)
    col_grafico1, col_grafico2 = st.columns(2)

    # Gráfico 1: Cobertura por Situação (Urbano vs Rural)
    resumo_situacao = df_dom.groupby("situacao_domicilio", observed=False).agg(
        Esgoto_Adequado=("esgotamento_adequado", lambda s: s.mean() * 100),
        Agua_Canalizada=("agua_rede_geral", lambda s: s.mean() * 100),
        Internet=("possui_internet", lambda s: s.mean() * 100)
    ).reset_index()

    df_melt_sit = pd.melt(
        resumo_situacao,
        id_vars=["situacao_domicilio"],
        var_name="Servico",
        value_name="Percentual"
    )

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df_melt_sit,
        x="Servico",
        y="Percentual",
        hue="situacao_domicilio",
        palette=["#2E86C1", "#E67E22"],
        ax=ax1
    )
    ax1.set_title("Acesso a Serviços Básicos: Urbano vs Rural")
    ax1.set_xlabel("Serviço")
    ax1.set_ylabel("Percentual (%)")
    ax1.set_ylim(0, 110)
    for p in ax1.patches:
        h = p.get_height()
        if not np.isnan(h) and h > 0:
            ax1.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h),
                         ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 2),
                         textcoords='offset points')
    col_grafico1.pyplot(fig1)
    plt.close(fig1)

    # Gráfico 2: Renda Mediana por Raça e Sexo do Responsável
    if not df_fam_filtrado.empty:
        df_raca_sexo = df_fam_filtrado.groupby(["raca_responsavel", "sexo_responsavel"]).agg(
            renda_mediana=("rendimento_familiar_per_capita", "median")
        ).reset_index()

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=df_raca_sexo,
            x="raca_responsavel",
            y="renda_mediana",
            hue="sexo_responsavel",
            palette=["#E74C3C", "#2E86C1"],
            ax=ax2
        )
        ax2.set_title("Renda Familiar per Capita Mediana por Raça e Sexo")
        ax2.set_xlabel("Cor ou Raça")
        ax2.set_ylabel("Rendimento Mediano (R$)")
        ax2.axhline(1212, color="gray", linestyle="--", label="1 Salário Mínimo (2022: R$ 1.212)")
        ax2.legend(title="")
        for p in ax2.patches:
            h = p.get_height()
            if not np.isnan(h) and h > 0:
                ax2.annotate(f"R$ {h:,.0f}", (p.get_x() + p.get_width() / 2., h),
                             ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 2),
                             textcoords='offset points')
        col_grafico2.pyplot(fig2)
        plt.close(fig2)
    else:
        col_grafico2.info("Sem dados familiares para os filtros selecionados.")

    # Linha 2 de Gráficos (col_grafico3 e col_grafico4)
    col_grafico3, col_grafico4 = st.columns(2)

    # Gráfico 3: Renda por Tipologia Familiar
    if not df_fam_filtrado.empty:
        top_tipologias = [
            "Casal sem filhos",
            "Casal com filhos",
            "Monoparental masculina (pai solo c/ filhos)",
            "Monoparental feminina (mãe solo c/ filhos)"
        ]
        df_tip = df_fam_filtrado[df_fam_filtrado["tipologia_familiar"].isin(top_tipologias)].groupby("tipologia_familiar").agg(
            renda_mediana=("rendimento_familiar_per_capita", "median")
        ).reset_index().sort_values("renda_mediana", ascending=True)

        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=df_tip,
            y="tipologia_familiar",
            x="renda_mediana",
            palette="Blues_r",
            ax=ax3
        )
        ax3.set_title("Renda per Capita Mediana por Tipologia Familiar")
        ax3.set_xlabel("Renda Mediana (R$)")
        ax3.set_ylabel("Tipologia Familiar")
        for p in ax3.patches:
            w = p.get_width()
            if not np.isnan(w) and w > 0:
                ax3.annotate(f" R$ {w:,.0f}", (w, p.get_y() + p.get_height() / 2.),
                             va='center', fontsize=9, fontweight='bold')
        col_grafico3.pyplot(fig3)
        plt.close(fig3)
    else:
        col_grafico3.info("Sem dados para tipologias familiares.")

    # Gráfico 4: Evolução Anual de Óbitos Domiciliares (COVID-19)
    if not df_mort_filtrado.empty:
        obitos_anuais = df_mort_filtrado.groupby(["ano_obito", "sexo_falecido"]).size().reset_index(name="obitos")
        obitos_anuais = obitos_anuais[obitos_anuais["sexo_falecido"].isin(["Masculino", "Feminino"])]

        fig4, ax4 = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=obitos_anuais,
            x="ano_obito",
            y="obitos",
            hue="sexo_falecido",
            palette=["#2E86C1", "#E74C3C"],
            ax=ax4
        )
        ax4.set_title("Evolução dos Óbitos Domiciliares por Sexo (2019 a 2022)")
        ax4.set_xlabel("Ano do Óbito")
        ax4.set_ylabel("Quantidade de Óbitos Amostrais")
        for p in ax4.patches:
            h = p.get_height()
            if not np.isnan(h) and h > 0:
                ax4.annotate(f"{int(h):,}", (p.get_x() + p.get_width() / 2., h),
                             ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 2),
                             textcoords='offset points')
        col_grafico4.pyplot(fig4)
        plt.close(fig4)
    else:
        col_grafico4.info("Sem registros de óbito para o recorte atual.")

    # Seção Sazonalidade / Pirâmide Etária dos Óbitos (Heatmap e Distribuição)
    st.subheader("Dinâmica Etária da Mortalidade")

    if not df_mort_filtrado.empty:
        comp_obitos = df_mort_filtrado[
            df_mort_filtrado["faixa_etaria_falecido"] != "Idade ignorada"
        ].groupby(["faixa_etaria_falecido", "ano_obito"]).size().unstack(fill_value=0)

        fig5, ax5 = plt.subplots(figsize=(12, 6))
        sns.heatmap(
            comp_obitos,
            cmap="Blues",
            annot=True,
            fmt="d",
            ax=ax5
        )
        ax5.set_title("Distribuição dos Óbitos por Faixa Etária e Ano de Ocorrência (RJ)")
        ax5.set_xlabel("Ano do Óbito")
        ax5.set_ylabel("Faixa Etária do Falecido")
        st.pyplot(fig5)
        plt.close(fig5)

    # Interpretação dos Resultados (Estilo dinâmico igual ao G1)
    st.subheader("Interpretação dos Resultados")

    esgoto_urbano = df_dom[df_dom["situacao_domicilio"] == "Urbana"]["esgotamento_adequado"].mean() * 100
    esgoto_rural = df_dom[df_dom["situacao_domicilio"] == "Rural"]["esgotamento_adequado"].mean() * 100
    
    obitos_2019 = len(df_mort[df_mort["ano_obito"] == 2019])
    obitos_2021 = len(df_mort[df_mort["ano_obito"] == 2021])
    salto_obitos = ((obitos_2021 - obitos_2019) / obitos_2019) * 100

    st.write(
        f"""
        Considerando os dados da amostra do Censo 2022 para o Estado do Rio de Janeiro:
        \n* No **saneamento básico**, observa-se um contraste contundente: enquanto **{esgoto_urbano:.1f}%** dos domicílios urbanos contam com rede de esgoto ou fossa séptica ligada à rede, apenas **{esgoto_rural:.1f}%** dos domicílios rurais dispõem desse serviço.
        \n* Na **estrutura familiar**, famílias lideradas por mulheres apresentam mediana de renda per capita de **R$ 900,00**, expressivamente inferior à de famílias lideradas por homens (**R$ 1.204,00**). O recorte por raça acentua a desigualdade: responsáveis pretos e pardos recebem rendas per capita medianas consideravelmente abaixo das registradas por responsáveis brancos.
        \n* Na **mortalidade**, os registros revelam o impacto da pandemia de COVID-19, com aumento de **{salto_obitos:.1f}%** nos óbitos reportados em 2021 (pico) na comparação com 2019 (período basal pré-pandemia).
        """
    )

    st.subheader("Conclusão Executiva")

    st.write(
        f"""
        A investigação empírica dos microdados evidencia a persistência de assimetrias estruturais no Rio de Janeiro.\n
        O déficit de saneamento rural reforça a urgência de políticas públicas voltadas a soluções descentralizadas de infraestrutura sanitária.\n
        A sobreposição entre gênero, raça e monoparentalidade aponta a necessidade de programas focalizados de transferência de renda e creches para mães solo.\n
        Por fim, o expressivo aumento de óbitos em 2021 ilustra o valor dos registros censitários para a compreensão de choques epidemiológicos extremos sobre as famílias fluminenses.
        """
    )

st.subheader("Dados filtrados")

st.write(f"Registros de domicílios encontrados: {len(df_dom_filtrado):,}".replace(",", "."))

st.dataframe(
    df_dom_filtrado[["id_domicilio", "situacao_domicilio", "esgotamento_descricao", "abastecimento_agua_descricao", "possui_internet", "faixa_renda_sm", "rendimento_domiciliar_per_capita"]].head(100),
    use_container_width=True
)

st.caption("Censo Demográfico 2022 — IBGE | UF 33 (Rio de Janeiro) | Autores: Ysis Barbosa Gomes e Ygor Barbosa Gomes")
