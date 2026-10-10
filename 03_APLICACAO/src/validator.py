#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador Estático de Políticas de Segurança para GCP Sovereign Landing Zone
Verifica conformidade de regras em arquivos Terraform (.tf).
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

def validar_arquivo_terraform(caminho: Path) -> List[Tuple[str, bool, str]]:
    """Aplica verificações de segurança em um arquivo Terraform."""
    conteudo = caminho.read_text(encoding="utf-8")
    resultados = []
    
    # 1. Checar se auto_create_subnetworks é false
    if "google_compute_network" in conteudo:
        valido = "auto_create_subnetworks = false" in conteudo
        resultados.append(("VPC sem sub-redes automáticas", valido, "auto_create_subnetworks deve ser false"))

    # 2. Checar se o acesso IAP usa o range correto (35.235.240.0/20) e não 0.0.0.0/0
    if "35.235.240.0/20" in conteudo:
        resultados.append(("Range de Ingress IAP Seguro", True, "Usa range oficial do Google Cloud IAP"))
        
    if "0.0.0.0/0" in conteudo and ('"22"' in conteudo or '"3389"' in conteudo):
        resultados.append(("SSH/RDP sem exposição pública direta", False, "Portas 22 ou 3389 abertas para 0.0.0.0/0 detectadas!"))
    else:
        resultados.append(("SSH/RDP sem exposição pública direta", True, "Nenhuma porta administrativa aberta para 0.0.0.0/0"))

    return resultados

def main():
    pasta_src = Path(__file__).resolve().parent
    arquivos_tf = list(pasta_src.glob("*.tf"))
    
    print("=" * 65)
    print("☁️  TECHDIM GCP SOVEREIGN LANDING ZONE - VALIDADOR DE SEGURANÇA")
    print("=" * 65)
    
    falhas = 0
    total = 0
    for tf in arquivos_tf:
        print(f"\n📄 Analisando: {tf.name}")
        cheques = validar_arquivo_terraform(tf)
        for regra, sucesso, msg in cheques:
            total += 1
            icone = "✅" if sucesso else "❌"
            print(f"  {icone} {regra:<40} : {msg}")
            if not sucesso:
                falhas += 1
                
    print("\n" + "-" * 65)
    if falhas == 0:
        print(f"🎉 Todas as {total} verificações de segurança foram APROVADAS com louvor!")
        sys.exit(0)
    else:
        print(f"⚠️  {falhas} inconsistências de conformidade detectadas.")
        sys.exit(1)

if __name__ == "__main__":
    main()
