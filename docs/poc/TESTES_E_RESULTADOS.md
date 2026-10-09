# Testes, respostas e evidências

## Instalação limpa concluída — rodada atual

Em 09/10/2026 às 11:08:55 UTC, os prints recebidos mostram setup concluído, dez Jobs PASS e os mesmos 16 critérios true, com 85 linhas de auditoria. A execução foi realizada em pasta nova após remoção dos clusters anteriores, sem intervenção corretiva registrada. Ver [evidências e transcrição](../../evidence/public/2026-10-09-instalacao-limpa/README.md). A matriz abaixo se aplica às duas rodadas; a nova evidência encerra a pendência de instalação limpa nesse ambiente. Arquivos de logs e JSON originais da nova rodada ainda não foram transferidos.

## Proveniência histórica — 08/10/2026

Execução informada pela autora: **08/10/2026 22:00:15 UTC (19:00:15 Brasília)**, depois de recuperação manual de configuração. Dez Jobs exibiram PASS; o JSON informado contém 16 critérios true e 91 linhas de auditoria. Ver [transcrição](../../evidence/public/RESULTADO_INFORMADO_USUARIA.json), [proveniência](../../evidence/public/VALIDACAO_AUTORA.md) e [prints recortados](../../evidence/public/Anexo_Prints_Validacao.pdf).

O arquivo original results.json e logs completos dos Jobs não foram transferidos para revisão independente. Os prints apoiam o relato, mas não substituem logs e código. Os testes locais deste pacote usam servidor HTTPS simulado e não executam Kubernetes.

## Matriz de aceite

Todos os critérios abaixo foram informados como true. True significa correspondência com a resposta esperada, inclusive quando a ação deve ser negada.

| Critério | Resposta esperada | O que demonstra e limite |
|---|---|---|
| baseline_connection | Autenticar e ler antes das políticas | Caminho A→B funcional; TLS/auth continuam ativos |
| baseline_unrestricted | Probe B alcança handshake TLS antes da política | Usa falha específica de CA como sinal de conectividade; não é leitura autorizada |
| authorized | Login e leitura permitidos; escrita/outro caminho negados; revogação funciona | Combinação de identidade, ACL e ciclo de token |
| wrong-sa | Login recusado | SA outsider não satisfaz role |
| wrong-audience | Login recusado | JWT com audience inadequada não é aceito |
| expired | Token de duração curta deixa de funcionar | Expiração de token OpenBao; não é teste completo de todas as credenciais |
| leaked-token | Próprio escopo ainda acessível, outro escopo negado e revogação aplicada | Vazamento residual realista; não prevenção absoluta de vazamento |
| attack-chain | Acesso próprio seguido de recusas à ampliação administrativa | Cadeia simulada; não exploração de CVE ou host |
| tls-ca | Falha de confiança na CA | Cliente recusa servidor sem CA confiável |
| network-denied | Probe local B não alcança serviço após política | Restrição local; sem comprovação de isolamento externo A/B |
| rbac-reader-get-secrets | no | reader sem leitura de Secrets Kubernetes |
| rbac-reviewer-create-tokenreviews.authentication.k8s.io | yes | reviewer pode criar TokenReview |
| rbac-reviewer-get-secrets | no | reviewer sem leitura de Secrets |
| rbac-reader-create-pods | no | reader não cria Pods |
| rbac-reader-create-clusterrolebindings.rbac.authorization.k8s.io | no | reader não cria vínculos globais |
| audit_present | Arquivo com conteúdo | Presença de auditoria; 91 linhas na rodada anterior e 85 na instalação limpa não provam completude ou imutabilidade |

## Cenários de ameaça

O cenário simples usa identidade errada, audience errada ou token expirado. O vazamento controlado reutiliza token válido do próprio laboratório: a leitura dentro do escopo continua possível. O cenário encadeado tenta ampliar o alcance para outro segredo e interfaces administrativas, incluindo mounts, auditoria e criação arbitrária de token. O sucesso do teste consiste em observar as recusas previstas, não em comprometer um sistema real.

## Resposta à pergunta do trabalho

Os resultados relatados sustentam a viabilidade de controlar um fluxo A→B por TLS, identidade Kubernetes e política OpenBao, com verificações RBAC e auditoria presente. Não sustentam a conclusão de que toda comunicação entre clusters está isolada ou que vazamentos são impossíveis. O modelo completo permanece sujeito à avaliação documental e operacional das 28 práticas.

## Testes adicionais aplicáveis, ainda pendentes

| Teste | Motivo | Evidência necessária |
|---|---|---|
| Workload não autorizado em A contra B | Validar o caminho intercluster negativo | Teste positivo de controle, origem observada, decisão do CNI e resultado negativo |
| Reinício/substituição e recuperação | Estado é efêmero | Ensaio com dados fictícios e procedimento de restauração |
| Rotação e expiração da CA/reviewer | Credenciais temporárias afetam operação | Antes/depois e testes de autenticidade/continuidade |
| Correlação de eventos de auditoria | Contagem não confirma cobertura | Eventos sanitizados por caso, retenção e controle de acesso |
| Compatibilidade e atualização | Dependências e APIs mudam | Matriz suportada, release notes e repetição da suíte |
| Desempenho e disponibilidade | Custos não foram medidos | Latência, erros, recursos e metodologia antes/depois |

Nenhum desses itens pendentes deve receber PASS com base na suíte já executada. O terceiro cluster não integra esta entrega.
