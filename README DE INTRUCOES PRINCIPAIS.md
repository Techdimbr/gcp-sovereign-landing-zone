# 🏛️ README DE INSTRUÇÕES PRINCIPAIS — GCP Sovereign Landing Zone

**Repositório Oficial:** `https://github.com/Techdimbr/gcp-sovereign-landing-zone`  
**Classificação:** Projeto de Referência Técnica Corporativa (Padrão Open-Core)  
**Doutrina de Engenharia:** Kether_1 · Central de Tecnologia TECHDIM  
**Status Atual:** Base Canônica Homologada — Pronto para Expansão de Funções  
**Website Institucional:** https://techdimbr.github.io/techdimbr/  
**Licença:** MIT Corporate  

---

## 1. Identificação e Propósito do Projeto
- **Nome Comercial:** GCP Sovereign Landing Zone
- **Identificador (Slug):** `gcp-sovereign-landing-zone`
- **Categoria:** Arquitetura Cloud (Google Cloud Platform) & Infraestrutura como Código
- **Stack Tecnológica:** Terraform 1.6+ / OpenTofu, Google Cloud Provider, Cloud KMS, Cloud NAT, Cloud Armor, IAP
- **Objetivo Central:** Entregar módulos Terraform declarativos e testados para provisionar um ambiente fundacional (Landing Zone) soberano no Google Cloud, garantindo isolamento de rede, Zero Public IPs e conformidade regulatória.

### Casos de Uso Reais
1. **Onboarding de Novos Ambientes Cloud:** Criação rápida de projetos em conformidade com o framework de arquitetura segura da Google Cloud.
2. **Eliminação de Jump Hosts:** Acesso administrativo seguro via IAP sem necessidade de servidores intermediários.
3. **Criptografia Mandatória (CMEK):** Rotação automática de chaves e bloqueio de criação de buckets ou discos sem chave KMS vinculada.

---

## 2. Estrutura dos Módulos em `03_APLICACAO/src/`

```text
03_APLICACAO/src/
├── versions.tf                        # Restrições de versão do Terraform e provedor google/google-beta
├── variables.tf                       # Variáveis de entrada (project_id, region, subnets, etc.)
├── main.tf                            # Módulo raiz orquestrando VPC, NAT, IAP e KMS
├── outputs.tf                         # Saídas do módulo (network_id, nat_ips, kms_key_id)
└── validator.py                       # Script Python para validação estática de segurança
```

---

## 3. Guia Operacional para o Desenvolvedor

1. **Bootstrap do Ambiente:**
   ```bash
   ./iniciar.sh
   ```
2. **Executar Testes de Validação Estática:**
   ```bash
   python3 -m unittest discover 03_APLICACAO/tests
   ```
3. **Auditar Integridade Criptográfica dos Arquivos:**
   ```bash
   ./00_AUDITORIA/verificar_integridade.sh --gerar
   ```

---

## 4. Diretrizes e Regras de Negócio da Função (Para Preenchimento)
<!-- ÁREA DESTINADA À ESPECIFICAÇÃO DE NOVOS MÓDULOS TERRAFORM -->
- [x] Módulo base de VPC com `auto_create_subnetworks = false`;
- [x] Módulo Cloud Router e Cloud NAT com alocação estática de IPs;
- [x] Regra de firewall para permitir tráfego IAP (`35.235.240.0/20`);
- [ ] Módulo Cloud KMS com Key Ring e CryptoKey configuradas para rotação de 90 dias;
- [ ] Regras customizadas de Cloud Armor contra injeções SQL e ataques de bots L7.
