"""
Módulo de Visualização Científica e Geração de Figuras
Projeto: Censo Demográfico RJ 2022 (FAIR-Compliant)
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)


def gerar_graficos_rq1(df_dom: pd.DataFrame):
    """
    RQ1: Saneamento básico e conectividade digital (Urbano vs Rural e Renda).
    """
    print("[1/3] Gerando visualizações para RQ1 (Infraestrutura e Saneamento)...")

    taxa_rural_esgoto = (df_dom[df_dom['situacao_domicilio'] == 'Rural']['esgotamento_adequado'].mean()) * 100
    taxa_urbana_esgoto = (df_dom[df_dom['situacao_domicilio'] == 'Urbana']['esgotamento_adequado'].mean()) * 100
    
    taxa_rural_agua = (df_dom[df_dom['situacao_domicilio'] == 'Rural']['agua_rede_geral'].mean()) * 100
    taxa_urbana_agua = (df_dom[df_dom['situacao_domicilio'] == 'Urbana']['agua_rede_geral'].mean()) * 100
    
    taxa_rural_net = (df_dom[df_dom['situacao_domicilio'] == 'Rural']['possui_internet'].mean()) * 100
    taxa_urbana_net = (df_dom[df_dom['situacao_domicilio'] == 'Urbana']['possui_internet'].mean()) * 100
    
    indicadores = ['Esgotamento Adequado', 'Água por Rede Geral', 'Acesso à Internet']
    valores_urb = [taxa_urbana_esgoto, taxa_urbana_agua, taxa_urbana_net]
    valores_rur = [taxa_rural_esgoto, taxa_rural_agua, taxa_rural_net]
    
    x = np.arange(len(indicadores))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
    rects1 = ax.bar(x - width/2, valores_urb, width, label='Urbana (N=417.516)', color='#1f77b4', edgecolor='black', linewidth=0.5)
    rects2 = ax.bar(x + width/2, valores_rur, width, label='Rural (N=14.252)', color='#ff7f0e', edgecolor='black', linewidth=0.5)
    
    ax.set_ylabel('Percentual de Domicílios Atendidos (%)', fontsize=11, fontweight='bold')
    ax.set_title('Figura 1: Acesso a Serviços Essenciais segundo Situação Domiciliar no RJ', fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(indicadores, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    
    for r in rects1:
        h = r.get_height()
        ax.annotate(f'{h:.1f}%', xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
    for r in rects2:
        h = r.get_height()
        ax.annotate(f'{h:.1f}%', xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    static_path = os.path.join(ASSETS_DIR, "figura1_saneamento_rq1.png")
    fig.savefig(static_path, dpi=300)
    plt.close()

    ordem_renda = [
        "Renda zero",
        "Extrema pobreza (Até 1/4 SM)",
        "Pobreza (1/4 a 1/2 SM)",
        "Baixa renda (1/2 a 1 SM)",
        "Renda média-baixa (1 a 2 SM)",
        "Renda média (2 a 5 SM)",
        "Renda alta (> 5 SM)"
    ]
    df_renda = df_dom[df_dom['faixa_renda_sm'].isin(ordem_renda)].copy()
    taxas_renda = df_renda.groupby('faixa_renda_sm', observed=False).agg(
        taxa_esgoto=('esgotamento_adequado', lambda s: s.mean() * 100),
        taxa_internet=('possui_internet', lambda s: s.mean() * 100),
        taxa_pleno=('saneamento_basico_pleno', lambda s: s.mean() * 100),
        total_dom=('id_domicilio', 'count')
    ).reindex(ordem_renda).reset_index()
    
    fig_plotly = go.Figure()
    fig_plotly.add_trace(go.Bar(
        x=taxas_renda['faixa_renda_sm'],
        y=taxas_renda['taxa_esgoto'],
        name='Esgotamento Adequado (%)',
        marker_color='#2ca02c'
    ))
    fig_plotly.add_trace(go.Bar(
        x=taxas_renda['faixa_renda_sm'],
        y=taxas_renda['taxa_internet'],
        name='Acesso à Internet (%)',
        marker_color='#1f77b4'
    ))
    fig_plotly.add_trace(go.Scatter(
        x=taxas_renda['faixa_renda_sm'],
        y=taxas_renda['taxa_pleno'],
        name='Saneamento Pleno (%)',
        mode='lines+markers',
        line=dict(color='#d62728', width=3),
        marker=dict(size=8)
    ))
    fig_plotly.update_layout(
        title="<b>Taxa de Adequação Sanitária e Conectividade por Estrato de Renda (RJ)</b>",
        xaxis_title="Estrato de Rendimento Domiciliar per Capita (Salários Mínimos)",
        yaxis_title="Percentual (%)",
        barmode='group',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=100),
        height=500
    )
    fig_plotly.write_html(os.path.join(ASSETS_DIR, "interativo_rq1_saneamento.html"), include_plotlyjs='cdn')


def gerar_graficos_rq2(df_fam: pd.DataFrame):
    """
    RQ2: Disparidades de renda por gênero, raça e tipologia familiar.
    """
    print("[2/3] Gerando visualizações para RQ2 (Desigualdades na Chefia Familiar)...")

    df_valid = df_fam[
        df_fam['sexo_responsavel'].isin(['Masculino', 'Feminino']) &
        df_fam['raca_responsavel'].isin(['Branca', 'Preta', 'Parda']) &
        (df_fam['rendimento_familiar_per_capita'] >= 0)
    ].copy()
    
    medians = df_valid.groupby(['raca_responsavel', 'sexo_responsavel'])['rendimento_familiar_per_capita'].median().unstack()
    
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
    medians.plot(kind='bar', ax=ax, color=['#1f77b4', '#e377c2'], edgecolor='black', linewidth=0.5, width=0.6)
    
    ax.set_title('Figura 2: Mediana da Renda Familiar per Capita por Raça e Sexo do Chefe de Família (RJ)', fontsize=11, fontweight='bold', pad=15)
    ax.set_ylabel('Rendimento Familiar per Capita Mediano (R$)', fontsize=10, fontweight='bold')
    ax.set_xlabel('Cor ou Raça do Responsável', fontsize=10, fontweight='bold')
    ax.set_xticklabels(medians.index, rotation=0, fontsize=10)
    ax.legend(['Chefe Masculino', 'Chefe Feminino'], frameon=True)

    ax.axhline(1212.0, color='red', linestyle='--', linewidth=1, label='1 Salário Mínimo (2022: R$ 1.212)')
    
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(f'R$ {height:,.0f}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 3),
                        textcoords='offset points')
            
    plt.tight_layout()
    static_path = os.path.join(ASSETS_DIR, "figura2_renda_familia_rq2.png")
    fig.savefig(static_path, dpi=300)
    plt.close()

    df_tip = df_fam[df_fam['rendimento_familiar_per_capita'] >= 0].copy()
    top_tipologias = [
        "Casal sem filhos",
        "Casal com filhos",
        "Monoparental masculina (pai solo c/ filhos)",
        "Monoparental feminina (mãe solo c/ filhos)",
        "Casal com filhos c/ parentes",
        "Monoparental feminina c/ filhos e parentes"
    ]
    df_tip = df_tip[df_tip['tipologia_familiar'].isin(top_tipologias)]
    resumo_tip = df_tip.groupby('tipologia_familiar').agg(
        renda_mediana=('rendimento_familiar_per_capita', 'median'),
        taxa_extrema_pobreza=('em_extrema_pobreza', lambda s: s.mean() * 100),
        total_familias=('id_domicilio', 'count')
    ).sort_values('renda_mediana', ascending=True).reset_index()
    
    fig_plotly = px.bar(
        resumo_tip,
        x='renda_mediana',
        y='tipologia_familiar',
        orientation='h',
        color='taxa_extrema_pobreza',
        color_continuous_scale='Reds',
        labels={
            'renda_mediana': 'Renda Familiar per Capita Mediana (R$)',
            'tipologia_familiar': 'Tipologia do Núcleo Familiar',
            'taxa_extrema_pobreza': 'Taxa em Extrema Pobreza (%)'
        },
        title="<b>Vulnerabilidade Econômica e Renda Mediana por Tipologia Familiar (RJ)</b>"
    )
    fig_plotly.update_layout(
        template='plotly_white',
        margin=dict(l=40, r=40, t=60, b=40),
        height=450
    )
    fig_plotly.write_html(os.path.join(ASSETS_DIR, "interativo_rq2_familias.html"), include_plotlyjs='cdn')


def gerar_graficos_rq3(df_mort: pd.DataFrame):
    """
    RQ3: Dinâmica temporal e demográfica da mortalidade (2019-2022).
    """
    print("[3/3] Gerando visualizações para RQ3 (Dinâmica da Mortalidade)...")

    df_valid = df_mort[df_mort['sexo_falecido'].isin(['Masculino', 'Feminino'])].copy()
    obitos_ano_sexo = df_valid.groupby(['ano_obito', 'sexo_falecido']).size().unstack()
    
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    obitos_ano_sexo.plot(kind='bar', ax=ax, color=['#1f77b4', '#d62728'], edgecolor='black', linewidth=0.5, width=0.6)
    
    ax.set_title('Figura 3: Evolução dos Óbitos Registrados no RJ por Ano e Sexo (2019 a 2022)', fontsize=11, fontweight='bold', pad=15)
    ax.set_ylabel('Número de Óbitos Amostrais', fontsize=10, fontweight='bold')
    ax.set_xlabel('Ano de Ocorrência do Óbito', fontsize=10, fontweight='bold')
    ax.set_xticklabels(obitos_ano_sexo.index, rotation=0, fontsize=10)
    ax.legend(['Masculino', 'Feminino'], frameon=True)
    
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(f'{int(height):,}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 3),
                        textcoords='offset points')
            
    plt.tight_layout()
    static_path = os.path.join(ASSETS_DIR, "figura3_mortalidade_rq3.png")
    fig.savefig(static_path, dpi=300)
    plt.close()

    df_comp = df_mort[df_mort['ano_obito'].isin([2019, 2021]) & (df_mort['faixa_etaria_falecido'] != 'Idade ignorada')].copy()
    comp_etaria = df_comp.groupby(['faixa_etaria_falecido', 'ano_obito']).size().unstack().fillna(0).reset_index()
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=comp_etaria['faixa_etaria_falecido'],
        y=comp_etaria[2019],
        name='Ano Pré-pandêmico (2019)',
        marker_color='#4575b4'
    ))
    fig_comp.add_trace(go.Bar(
        x=comp_etaria['faixa_etaria_falecido'],
        y=comp_etaria[2021],
        name='Pico da Pandemia (2021)',
        marker_color='#d73027'
    ))
    fig_comp.update_layout(
        title="<b>Comparativo da Mortalidade por Faixa Etária: 2019 vs 2021 (RJ)</b>",
        xaxis_title="Faixa Etária do Falecido",
        yaxis_title="Volume de Óbitos Amostrais",
        barmode='group',
        template='plotly_white',
        margin=dict(l=40, r=40, t=60, b=80),
        height=480
    )
    fig_comp.write_html(os.path.join(ASSETS_DIR, "interativo_rq3_mortalidade.html"), include_plotlyjs='cdn')


def main():
    print("Iniciando geração de todas as figuras estáticas e interativas...")
    df_dom = pd.read_parquet(os.path.join(PROCESSED_DIR, "domicilios_rj_clean.parquet"))
    df_fam = pd.read_parquet(os.path.join(PROCESSED_DIR, "familias_rj_clean.parquet"))
    df_mort = pd.read_parquet(os.path.join(PROCESSED_DIR, "mortalidade_rj_clean.parquet"))
    
    gerar_graficos_rq1(df_dom)
    gerar_graficos_rq2(df_fam)
    gerar_graficos_rq3(df_mort)
    print("Visualizações geradas com sucesso em docs/assets/!")


if __name__ == "__main__":
    main()
