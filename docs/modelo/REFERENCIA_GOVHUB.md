# Referência real e aplicação na POC

Repositório: https://github.com/GovHub-br/data-application-mgi
Commit: 9f9d94761a8867bcdd392a4b10c70b56f2e8c8da
Consulta: 08/10/2026. Leitura da árvore por checkout Git somente para inspeção.

| Evidência observada | Caminho | Uso na POC | Limite da conclusão |
|---|---|---|---|
| Airflow e dbt executam pipelines e transformações | README.md | Workload consumidor representa pipeline lendo configuração | Não executa as DAGs reais |
| Compose é infraestrutura local | infra/README.md | Cenário isolado, descartável | Não descreve segurança de produção |
| PostgreSQL, Superset e MinIO presentes | infra/docker-compose.yml | Motiva credenciais separadas por sistema | Não prova integração OpenBao existente |
| Portas de serviços publicadas no Compose | infra/docker-compose.yml | Motiva inventário e restrição de fluxos | Firewall real não foi inspecionado |
| Valores padrão de desenvolvimento | infra/docker-compose.yml | Motiva retirar credenciais reais do código e limitar acesso | Não afirmar que produção usa esses valores |
| MCP com parâmetro de leitura configurável | infra/docker-compose.yml | Motiva revisão de privilégios e ações permitidas | Não conecta IA/MCP ao laboratório |
| AGENTS.md ausente nesse commit | Árvore completa do checkout | Fornecido AGENTS.md próprio da POC | Não reconstruir regras anteriores sem fonte |

Separar o que foi observado do que foi proposto: a referência consultada não
mostra uma topologia Kubernetes/OpenBao nesses arquivos. A arquitetura da POC
é uma hipótese de laboratório para estudar comunicação segura, não uma descrição
da infraestrutura deles. Não foram usados dados pessoais, credenciais reais ou
serviços conectados à produção.

Para integração posterior: confirmar namespaces, CNI, endpoint, autoridade CA,
modelo de identidade e fluxos efetivos com responsáveis pelo ambiente; mapear
políticas por pipeline; executar testes de compatibilidade do provider de secrets
do Airflow; registrar versões e evidências antes de propor aplicação institucional.


## Contexto institucional e comparação

A página oficial [Quem somos](https://gov-hub.io/govhub/quem-somos/) descreve o GovHub como iniciativa de integração e qualificação de dados governamentais, originada da parceria Ipea/Lab Livre-UnB em 2024. O repositório público consultado contém pipelines vinculados ao contexto MGI. Essa associação não demonstra que o MGI opera Kubernetes/OpenBao na topologia proposta.

| Dimensão | Referência pública consultada | Proposta deste trabalho |
|---|---|---|
| Objetivo | Integrar e transformar dados governamentais | Avaliar controles da comunicação entre clusters |
| Aplicação | Airflow/dbt e integrações de dados | Job sintético representando consumidor |
| Infraestrutura inspecionada | Arquivos de desenvolvimento local e código público | Dois clusters kind no mesmo host |
| Segredos | Necessidade de credenciais nas integrações | OpenBao com identidade e escopo por consumidor |
| Evidência | Código/documentação públicos | Testes controlados e resultados informados |
| Adoção institucional | Não verificada por acesso ao ambiente real | Não implantada ou homologada institucionalmente |

A mudança proposta é tornar explícitas as fronteiras, permissões e verificações de um fluxo. Não é possível afirmar melhoria percentual de segurança, superioridade sobre a produção atual ou substituição recomendada da arquitetura institucional sem avaliação do ambiente real.

O modelo foi elaborado para este trabalho; a inspiração funcional vem do cenário de integração GovHub e os mecanismos vêm das documentações originais. Não houve cópia de um AGENTS.md institucional. O repositório de referência não é incluído no pacote.

## Exemplo público de uso da tecnologia

A documentação administrativa do [GitLab Secrets Manager](https://docs.gitlab.com/administration/secrets_manager/) descreve uso de OpenBao. É exemplo de adoção da tecnologia, não prova de que esta POC reproduz o desenho ou atende aos requisitos do GitLab. A existência de outros usuários não substitui nossos testes.

Consulta das páginas de contexto: 09/10/2026. Consulta do checkout de referência: 08/10/2026; commit fixado acima.
