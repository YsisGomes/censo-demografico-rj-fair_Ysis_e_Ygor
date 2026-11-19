"""
ETL Pipeline - Microdados da Amostra do Censo Demográfico 2022 (IBGE)
UF: Rio de Janeiro (33)
Projeto Final da Disciplina: Linguagem de Programação (Análise e Visualização de Dados)
Conformidade: FAIR Guiding Principles
"""

import os
import sys
import logging
import argparse
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ETL_CENSO2022_RJ")

# Salário mínimo de referência do Censo 2022 (vigente em 2022: R$ 1.212,00)
SALARIO_MINIMO_2022 = 1212.0

# Dicionários de mapeamento categórico oficial do IBGE (Microdados CD2022)
MAP_SITUACAO = {1: "Urbana", 2: "Rural"}

MAP_SEXO = {1: "Masculino", 2: "Feminino", 9: "Ignorado"}

MAP_RACA = {
    1: "Branca",
    2: "Preta",
    3: "Amarela",
    4: "Parda",
    5: "Indígena",
    9: "Ignorado"
}

MAP_INSTRUCAO = {
    1: "Sem instrução / Fundamental incompleto",
    2: "Fundamental completo / Médio incompleto",
    3: "Médio completo / Superior incompleto",
    4: "Superior completo"
}

MAP_TIPOLOGIA_FAMILIA = {
    1: "Casal sem filhos",
    2: "Casal sem filhos c/ parentes",
    3: "Casal com filhos",
    4: "Casal com filhos c/ parentes",
    5: "Monoparental feminina (mãe solo c/ filhos)",
    6: "Monoparental feminina c/ filhos e parentes",
    7: "Monoparental masculina (pai solo c/ filhos)",
    8: "Monoparental masculina c/ filhos e parentes",
    9: "Poliafetivo / Múltiplos cônjuges",
    10: "Outro arranjo familiar"
}

MAP_ESGOTAMENTO = {
    1: "Rede geral de esgoto / pluvial",
    2: "Fossa séptica/filtro ligada à rede",
    3: "Fossa séptica/filtro não ligada à rede",
    4: "Fossa rudimentar / buraco",
    5: "Vala a céu aberto",
    6: "Rio, lago, córrego ou mar",
    7: "Outra forma de esgotamento",
    9: "Sem banheiro nem sanitário"
}

MAP_ABASTECIMENTO_AGUA = {
    1: "Rede geral de distribuição",
    2: "Poço profundo ou artesiano",
    3: "Poço raso, freático ou cacimba",
    4: "Fonte, nascente ou mina",
    5: "Carro-pipa",
    6: "Água de chuva armazenada",
    7: "Rios, açudes, córregos ou lagos",
    8: "Outra forma"
}

MAP_DESTINO_LIXO = {
    1: "Coletado no domicílio por serviço de limpeza",
    2: "Depositado em caçamba de serviço de limpeza",
    3: "Queimado na propriedade",
    4: "Enterrado na propriedade",
    5: "Jogado em terreno baldio, encosta ou rio",
    6: "Outro destino"
}

MAP_ANO_OBITO = {
    1: 2019,
    2: 2020,
    3: 2021,
    4: 2022
}

MAP_FAIXA_ETARIA = {
    1: "0 a 4 anos",
    2: "5 a 9 anos",
    3: "10 a 14 anos",
    4: "15 a 19 anos",
    5: "20 a 24 anos",
    6: "25 a 29 anos",
    7: "30 a 34 anos",
    8: "35 a 39 anos",
    9: "40 a 44 anos",
    10: "45 a 49 anos",
    11: "50 a 54 anos",
    12: "55 a 59 anos",
    13: "60 a 64 anos",
    14: "65 a 69 anos",
    15: "70 a 74 anos",
    16: "75 a 79 anos",
    17: "80 anos ou mais",
    99: "Idade ignorada"
}

def categorizar_grupo_etario(faixa_cod: int) -> str:
    """Classifica as faixas etárias censitárias em grandes grupos de ciclo de vida."""
    if faixa_cod in [1, 2, 3]:
        return "Crianças e Adolescentes (0 a 14 anos)"
    elif faixa_cod in [4, 5, 6]:
        return "Jovens (15 a 29 anos)"
    elif faixa_cod in [7, 8, 9, 10, 11, 12]:
        return "Adultos (30 a 59 anos)"
    elif faixa_cod in [13, 14, 15, 16, 17]:
        return "Idosos (60 anos ou mais)"
    return "Ignorado"


def classificar_faixa_renda(renda_pc: float) -> str:
    """Classifica a renda per capita em múltiplos do Salário Mínimo de 2022 (R$ 1.212)."""
    if pd.isna(renda_pc):
        return "Sem declaração"
    if renda_pc == 0:
        return "Renda zero"
    elif renda_pc <= 0.25 * SALARIO_MINIMO_2022:
        return "Extrema pobreza (Até 1/4 SM)"
    elif renda_pc <= 0.5 * SALARIO_MINIMO_2022:
        return "Pobreza (1/4 a 1/2 SM)"
    elif renda_pc <= 1.0 * SALARIO_MINIMO_2022:
        return "Baixa renda (1/2 a 1 SM)"
    elif renda_pc <= 2.0 * SALARIO_MINIMO_2022:
        return "Renda média-baixa (1 a 2 SM)"
    elif renda_pc <= 5.0 * SALARIO_MINIMO_2022:
        return "Renda média (2 a 5 SM)"
    else:
        return "Renda alta (> 5 SM)"


def processar_domicilios(input_path: str, output_parquet: str, output_csv_gz: str) -> pd.DataFrame:
    """
    Ingere, limpa, normaliza e enriquece os microdados de Domicílios (RJ).
    """
    logger.info(f"Iniciando ingestão de Domicílios: {input_path}")
    
    usecols = [
        'D0100', 'D0110', 'D0120', 'D0140', 'D0150', 'D0160', 'D0170', 'D0180',
        'D0190', 'D0200', 'D0220', 'D0230', 'D0250', 'D0260', 'D0300', 'D0310',
        'D0330', 'D0340', 'D0350', 'D0360', 'D0370', 'D0380'
    ]
    
    df = pd.read_csv(input_path, sep=';', usecols=usecols, low_memory=False)
    logger.info(f"Registros brutos lidos (Domicílios): {len(df):,}")
    
    # Renomeação semântica padronizada
    rename_dict = {
        'D0100': 'id_domicilio',
        'D0110': 'peso_amostral',
        'D0120': 'cod_situacao_setor',
        'D0140': 'cod_situacao_domicilio',
        'D0150': 'total_moradores',
        'D0160': 'total_criancas',
        'D0170': 'sexo_responsavel_domicilio',
        'D0180': 'faixa_etaria_responsavel_domicilio',
        'D0190': 'cod_condicao_ocupacao',
        'D0200': 'cod_tipo_especie',
        'D0220': 'total_comodos',
        'D0230': 'comodos_dormitorio',
        'D0250': 'cod_esgotamento_sanitario',
        'D0260': 'cod_abastecimento_agua',
        'D0300': 'cod_agua_canalizada',
        'D0310': 'cod_destino_lixo',
        'D0330': 'cod_acesso_internet',
        'D0340': 'ocorrencia_obito_domicilio',
        'D0350': 'rendimento_domiciliar_total',
        'D0360': 'rendimento_domiciliar_per_capita',
        'D0370': 'total_homens',
        'D0380': 'total_mulheres'
    }
    df = df.rename(columns=rename_dict)
    
    # Conversões e Tipagens
    df['id_domicilio'] = df['id_domicilio'].astype(np.int64)
    df['peso_amostral'] = pd.to_numeric(df['peso_amostral'], errors='coerce').fillna(1.0)
    
    # Decodificação e mapeamento categórico
    df['situacao_domicilio'] = df['cod_situacao_domicilio'].map(MAP_SITUACAO).astype('category')
    df['esgotamento_descricao'] = df['cod_esgotamento_sanitario'].map(MAP_ESGOTAMENTO).fillna("Não informado")
    df['abastecimento_agua_descricao'] = df['cod_abastecimento_agua'].map(MAP_ABASTECIMENTO_AGUA).fillna("Não informado")
    df['destino_lixo_descricao'] = df['cod_destino_lixo'].map(MAP_DESTINO_LIXO).fillna("Não informado")
    df['acesso_internet_descricao'] = df['cod_acesso_internet'].map({1: "Com Acesso", 2: "Sem Acesso"}).fillna("Não informado")
    df['obito_recente_descricao'] = df['ocorrencia_obito_domicilio'].map({1: "Com Óbito (2019-2022)", 2: "Sem Óbito"}).fillna("Não informado")
    
    # Indicadores Derivados de Negócio / Pesquisa (RQ1)
    # Esgotamento adequado: Rede geral ou fossa séptica/filtro ligada à rede (Conceito IBGE/PNSB)
    df['esgotamento_adequado'] = df['cod_esgotamento_sanitario'].isin([1, 2])
    
    # Abastecimento adequado: Rede geral de distribuição
    df['agua_rede_geral'] = df['cod_abastecimento_agua'] == 1
    
    # Destino do lixo adequado: Coletado no domicílio ou caçamba
    df['lixo_coletado_adequado'] = df['cod_destino_lixo'].isin([1, 2])
    
    # Conectividade digital
    df['possui_internet'] = df['cod_acesso_internet'] == 1
    
    # Saneamento Básico Pleno (Água por rede + Esgoto adequado + Lixo coletado)
    df['saneamento_basico_pleno'] = (
        df['esgotamento_adequado'] & 
        df['agua_rede_geral'] & 
        df['lixo_coletado_adequado']
    )
    
    # Classificação de Renda
    df['faixa_renda_sm'] = df['rendimento_domiciliar_per_capita'].apply(classificar_faixa_renda)
    
    # Exportação em formato aberto otimizado (Parquet) e CSV comprimido
    logger.info(f"Salvando Domicílios tratados em: {output_parquet}")
    df.to_parquet(output_parquet, index=False, engine='pyarrow', compression='snappy')
    
    logger.info(f"Salvando Domicílios tratados em: {output_csv_gz}")
    df.to_csv(output_csv_gz, index=False, compression='gzip')
    
    return df


def processar_familias(input_path: str, output_parquet: str, output_csv_gz: str) -> pd.DataFrame:
    """
    Ingere, limpa, normaliza e enriquece os microdados de Famílias (RJ).
    """
    logger.info(f"Iniciando ingestão de Famílias: {input_path}")
    
    usecols = [
        'F0100', 'F0101', 'F0110', 'F0120', 'F0140', 'F0150', 'F0160', 'F0170',
        'F0180', 'F0190', 'F0200', 'F0210', 'F0230', 'F0240', 'F0250', 'F0260'
    ]
    
    df = pd.read_csv(input_path, sep=';', usecols=usecols, low_memory=False)
    logger.info(f"Registros brutos lidos (Famílias): {len(df):,}")
    
    rename_dict = {
        'F0100': 'id_domicilio',
        'F0101': 'id_ordem_familia',
        'F0110': 'peso_amostral',
        'F0120': 'cod_situacao_setor',
        'F0140': 'cod_situacao_domicilio',
        'F0150': 'cod_identificacao_familia',
        'F0160': 'total_pessoas_familia',
        'F0170': 'cod_sexo_responsavel',
        'F0180': 'cod_faixa_etaria_responsavel',
        'F0190': 'cod_instrucao_responsavel',
        'F0200': 'cod_raca_responsavel',
        'F0210': 'cod_tipologia_familiar',
        'F0230': 'filhos_menores_10_anos',
        'F0240': 'integrantes_homens',
        'F0250': 'integrantes_mulheres',
        'F0260': 'rendimento_familiar_per_capita'
    }
    df = df.rename(columns=rename_dict)
    
    df['id_domicilio'] = df['id_domicilio'].astype(np.int64)
    df['peso_amostral'] = pd.to_numeric(df['peso_amostral'], errors='coerce').fillna(1.0)
    
    # Decodificação
    df['situacao_domicilio'] = df['cod_situacao_domicilio'].map(MAP_SITUACAO).astype('category')
    df['sexo_responsavel'] = df['cod_sexo_responsavel'].map(MAP_SEXO).fillna("Não aplicável / Família secundária")
    df['raca_responsavel'] = df['cod_raca_responsavel'].map(MAP_RACA).fillna("Não informado")
    df['instrucao_responsavel'] = df['cod_instrucao_responsavel'].map(MAP_INSTRUCAO).fillna("Não informado")
    df['tipologia_familiar'] = df['cod_tipologia_familiar'].map(MAP_TIPOLOGIA_FAMILIA).fillna("Outra tipologia")
    
    # Métricas derivadas (RQ2)
    df['is_chefiada_por_mulher'] = df['cod_sexo_responsavel'] == 2
    df['is_monoparental_feminina'] = df['cod_tipologia_familiar'].isin([5, 6])
    df['faixa_renda_sm'] = df['rendimento_familiar_per_capita'].apply(classificar_faixa_renda)
    df['em_extrema_pobreza'] = df['rendimento_familiar_per_capita'] <= (0.25 * SALARIO_MINIMO_2022)
    
    logger.info(f"Salvando Famílias tratadas em: {output_parquet}")
    df.to_parquet(output_parquet, index=False, engine='pyarrow', compression='snappy')
    
    logger.info(f"Salvando Famílias tratadas em: {output_csv_gz}")
    df.to_csv(output_csv_gz, index=False, compression='gzip')
    
    return df


def processar_mortalidade(input_path: str, output_parquet: str, output_csv_gz: str) -> pd.DataFrame:
    """
    Ingere, limpa, normaliza e enriquece os microdados de Mortalidade (RJ).
    """
    logger.info(f"Iniciando ingestão de Mortalidade: {input_path}")
    
    usecols = ['M0010', 'M0020', 'M0100', 'M0101', 'M0110', 'M0120', 'M0130', 'M0140', 'M0150', 'M0160', 'M0170']
    df = pd.read_csv(input_path, sep=';', usecols=usecols, low_memory=False)
    logger.info(f"Registros brutos lidos (Mortalidade): {len(df):,}")
    
    rename_dict = {
        'M0100': 'id_domicilio',
        'M0101': 'id_ordem_falecido',
        'M0110': 'peso_amostral',
        'M0120': 'cod_situacao_setor',
        'M0140': 'cod_situacao_domicilio',
        'M0150': 'cod_ano_obito',
        'M0160': 'cod_sexo_falecido',
        'M0170': 'cod_faixa_etaria_falecido'
    }
    df = df.rename(columns=rename_dict)
    
    df['id_domicilio'] = df['id_domicilio'].astype(np.int64)
    df['peso_amostral'] = pd.to_numeric(df['peso_amostral'], errors='coerce').fillna(1.0)
    
    # Mapeamento do ano de óbito
    df['ano_obito'] = df['cod_ano_obito'].map(MAP_ANO_OBITO)
    df = df[df['ano_obito'].notna()].copy()
    df['ano_obito'] = df['ano_obito'].astype(int)
    
    # Decodificação
    df['situacao_domicilio'] = df['cod_situacao_domicilio'].map(MAP_SITUACAO).astype('category')
    df['sexo_falecido'] = df['cod_sexo_falecido'].map(MAP_SEXO).fillna("Ignorado")
    df['faixa_etaria_falecido'] = df['cod_faixa_etaria_falecido'].map(MAP_FAIXA_ETARIA).fillna("Ignorado")
    df['grupo_etario_falecido'] = df['cod_faixa_etaria_falecido'].apply(categorizar_grupo_etario)
    
    # Flag do período crítico pandêmico
    df['periodo_pandemico'] = df['ano_obito'].isin([2020, 2021])
    
    logger.info(f"Salvando Mortalidade tratada em: {output_parquet}")
    df.to_parquet(output_parquet, index=False, engine='pyarrow', compression='snappy')
    
    logger.info(f"Salvando Mortalidade tratada em: {output_csv_gz}")
    df.to_csv(output_csv_gz, index=False, compression='gzip')
    
    return df


def processar_pessoas_amostra(input_path: str, output_parquet: str, output_csv_gz: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Ingere, filtra e sintetiza atributos demográficos e educacionais das Pessoas (RJ).
    """
    logger.info(f"Iniciando ingestão de Pessoas (Amostra curada): {input_path}")
    
    usecols = [
        'P0100', 'P0110', 'P0140', 'P0150', 'P0180', 'P0210', 'P0470',
        'P0640', 'P0760', 'P0930', 'P1000', 'P1080', 'P1110'
    ]
    
    df = pd.read_csv(input_path, sep=';', usecols=usecols, nrows=nrows, low_memory=False)
    logger.info(f"Registros brutos lidos (Pessoas): {len(df):,}")
    
    rename_dict = {
        'P0100': 'id_domicilio',
        'P0110': 'peso_amostral',
        'P0140': 'cod_situacao_domicilio',
        'P0150': 'cod_sexo',
        'P0180': 'cod_faixa_etaria',
        'P0210': 'cod_raca',
        'P0470': 'cod_indicador_deficiencia',
        'P0640': 'cod_alfabetizacao',
        'P0760': 'cod_nivel_instrucao',
        'P0930': 'cod_condicao_forca_trabalho',
        'P1000': 'cod_carteira_assinada',
        'P1080': 'rendimento_trabalho_habitual',
        'P1110': 'rendimento_todas_fontes'
    }
    df = df.rename(columns=rename_dict)
    
    df['id_domicilio'] = df['id_domicilio'].astype(np.int64)
    df['peso_amostral'] = pd.to_numeric(df['peso_amostral'], errors='coerce').fillna(1.0)
    
    df['situacao_domicilio'] = df['cod_situacao_domicilio'].map(MAP_SITUACAO).astype('category')
    df['sexo'] = df['cod_sexo'].map(MAP_SEXO).fillna("Ignorado")
    df['raca'] = df['cod_raca'].map(MAP_RACA).fillna("Ignorado")
    df['faixa_etaria'] = df['cod_faixa_etaria'].map(MAP_FAIXA_ETARIA).fillna("Ignorado")
    df['alfabetizado'] = df['cod_alfabetizacao'].map({1: "Sim", 2: "Não"}).fillna("Não informado")
    df['nivel_instrucao'] = df['cod_nivel_instrucao'].map(MAP_INSTRUCAO).fillna("Não determinado")
    df['possui_deficiencia'] = df['cod_indicador_deficiencia'] == 1
    
    logger.info(f"Salvando Pessoas tratadas em: {output_parquet}")
    df.to_parquet(output_parquet, index=False, engine='pyarrow', compression='snappy')
    
    logger.info(f"Salvando Pessoas tratadas em: {output_csv_gz}")
    df.to_csv(output_csv_gz, index=False, compression='gzip')
    
    return df


def gerar_indicadores_integrados(
    df_dom: pd.DataFrame, 
    df_fam: pd.DataFrame, 
    df_mort: pd.DataFrame,
    output_parquet: str
) -> pd.DataFrame:
    """
    Executa linkage relacional na chave id_domicilio para correlacionar
    infraestrutura residencial com óbitos domiciliares e tipologia familiar.
    """
    logger.info("Executando linkage relacional entre Domicílios, Mortalidade e Famílias...")
    
    # Agregação de óbitos por domicílio
    obitos_por_dom = df_mort.groupby('id_domicilio').agg(
        total_obitos=('id_ordem_falecido', 'count'),
        teve_obito_2021=('ano_obito', lambda s: (s == 2021).any()),
        obitos_homens=('cod_sexo_falecido', lambda s: (s == 1).sum()),
        obitos_mulheres=('cod_sexo_falecido', lambda s: (s == 2).sum()),
        obitos_idosos=('grupo_etario_falecido', lambda s: (s == "Idosos (60 anos ou mais)").sum())
    ).reset_index()
    
    # Merge com Domicílios
    df_integrado = df_dom.merge(obitos_por_dom, on='id_domicilio', how='left')
    df_integrado['total_obitos'] = df_integrado['total_obitos'].fillna(0).astype(int)
    df_integrado['teve_obito_2021'] = df_integrado['teve_obito_2021'].fillna(False).astype(bool)
    df_integrado['obitos_homens'] = df_integrado['obitos_homens'].fillna(0).astype(int)
    df_integrado['obitos_mulheres'] = df_integrado['obitos_mulheres'].fillna(0).astype(int)
    df_integrado['obitos_idosos'] = df_integrado['obitos_idosos'].fillna(0).astype(int)
    
    logger.info(f"Dataset integrado gerado com {len(df_integrado):,} domicílios.")
    df_integrado.to_parquet(output_parquet, index=False, engine='pyarrow', compression='snappy')
    return df_integrado


def main():
    parser = argparse.ArgumentParser(description="Pipeline ETL Censo 2022 RJ")
    parser.add_argument("--raw-dir", default=r"c:\Users\Desktop\Downloads", help="Diretório dos dados brutos")
    parser.add_argument("--out-dir", default=r"C:\Users\Desktop\.gemini\antigravity\scratch\censo-demografico-rj-fair\data\processed", help="Diretório de saída")
    args = parser.parse_args()
    
    raw_dir = args.raw_dir
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    
    # Caminhos de entrada
    path_dom = os.path.join(raw_dir, "Domicilios_33_publico.csv")
    path_fam = os.path.join(raw_dir, "Familia_33_publico.csv")
    path_mort = os.path.join(raw_dir, "Mortalidade_33_publico.csv")
    path_pess = os.path.join(raw_dir, "Pessoas_33_publico.csv")
    
    # Processamento sequencial auditável
    df_dom = processar_domicilios(
        path_dom, 
        os.path.join(out_dir, "domicilios_rj_clean.parquet"),
        os.path.join(out_dir, "domicilios_rj_clean.csv.gz")
    )
    
    df_fam = processar_familias(
        path_fam,
        os.path.join(out_dir, "familias_rj_clean.parquet"),
        os.path.join(out_dir, "familias_rj_clean.csv.gz")
    )
    
    df_mort = processar_mortalidade(
        path_mort,
        os.path.join(out_dir, "mortalidade_rj_clean.parquet"),
        os.path.join(out_dir, "mortalidade_rj_clean.csv.gz")
    )
    
    df_pess = processar_pessoas_amostra(
        path_pess,
        os.path.join(out_dir, "pessoas_amostra_rj_clean.parquet"),
        os.path.join(out_dir, "pessoas_amostra_rj_clean.csv.gz")
    )
    
    gerar_indicadores_integrados(
        df_dom,
        df_fam,
        df_mort,
        os.path.join(out_dir, "domicilios_obitos_integrados.parquet")
    )
    
    logger.info("Pipeline ETL concluído com sucesso e total reprodutibilidade!")


if __name__ == "__main__":
    main()
