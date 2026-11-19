"""
Script de Download Automatizado dos Dados Brutos do Censo Demográfico 2022 (IBGE)
UF: Rio de Janeiro (33)
Conformidade: FAIR Guiding Principles (Pilar Accessible & Reusable)

Este script permite a qualquer pesquisador ou aluno reproduzir o download dos
microdados públicos oficiais diretamente dos servidores FTP do IBGE.
"""

import os
import sys
import logging
from ftplib import FTP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DOWNLOAD_CENSO_2022")

# Configurações do FTP do IBGE
FTP_HOST = "ftp.ibge.gov.br"
FTP_DIR = "Censos/Censo_Demografico_2022/Microdados_e_Areas_de_Ponderacao/Microdados_de_acesso_Publico"

# Arquivos de microdados para a UF 33 (Rio de Janeiro)
ARQUIVOS_RJ = [
    "Domicilios_33_publico.csv",
    "Familia_33_publico.csv",
    "Mortalidade_33_publico.csv",
    "Pessoas_33_publico.csv"
]


def baixar_dados(destino_dir: str = "."):
    os.makedirs(destino_dir, exist_ok=True)
    logger.info(f"Conectando ao FTP do IBGE: {FTP_HOST}...")
    
    try:
        ftp = FTP(FTP_HOST, timeout=60)
        ftp.login()
        logger.info(f"Navegando para o diretório: {FTP_DIR}")
        ftp.cwd(FTP_DIR)
        
        # Lista arquivos disponíveis
        arquivos_disponiveis = ftp.nlst()
        logger.info(f"Arquivos encontrados no servidor: {len(arquivos_disponiveis)}")
        
        for arq in ARQUIVOS_RJ:
            caminho_local = os.path.join(destino_dir, arq)
            if os.path.exists(caminho_local):
                logger.info(f"Arquivo já existe localmente: {arq} ({os.path.getsize(caminho_local):,} bytes). Pulando.")
                continue
            
            # Se o arquivo estiver compactado como .zip no FTP, tenta encontrar
            match_arq = [f for f in arquivos_disponiveis if arq.lower() in f.lower() or f.lower().startswith("33_")]
            alvo = arq if arq in arquivos_disponiveis else (match_arq[0] if match_arq else arq)
            
            logger.info(f"Iniciando download de {alvo}...")
            with open(caminho_local, "wb") as f_out:
                ftp.retrbinary(f"RETR {alvo}", f_out.write)
            logger.info(f"Download concluído: {arq} ({os.path.getsize(caminho_local):,} bytes).")
            
        ftp.quit()
        logger.info("Todos os downloads foram concluídos com sucesso.")
    except Exception as e:
        logger.error(f"Erro durante a conexão ou transferência FTP: {e}")
        logger.info("Caso a rede universitária bloqueie a porta FTP (21), os microdados também podem ser baixados manualmente pelo portal: https://www.ibge.gov.br/estatisticas/portais-de-dados/portal-de-microdados")


if __name__ == "__main__":
    destino = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    baixar_dados(destino)
