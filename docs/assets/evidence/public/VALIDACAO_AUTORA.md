# Registro histórico: validação no laboratório da autora — 08/10/2026

Nota de atualização: a pendência de instalação limpa descrita abaixo era válida em 08/10 e foi encerrada na [rodada de 09/10/2026](2026-10-09-instalacao-limpa/README.md). O relato histórico foi preservado.

Origem: resultado de terminal e conteúdo de evidence/results.json fornecidos pela autora nesta conversa. Este arquivo reconstrói os campos informados; não é uma coleta independente nem o arquivo original transferido. Horário informado: 22:00:15 UTC, 19:00:15 de Brasília.

Os 16 critérios retornaram true, com 91 linhas de auditoria. Dez Jobs exibiram PASS. Os controles RBAC e a presença de auditoria também foram aprovados no relatório informado.

Interpretação: os campos RBAC true indicam que a resposta correspondeu ao esperado. O reader NÃO ganhou acesso a Secrets, criação de Pods ou ClusterRoleBindings. O reviewer pode criar TokenReviews e NÃO ler Secrets.

O cenário leaked-token aprovado demonstra que um token válido comprometido continua permitindo leitura dentro do próprio escopo; o teste aprova os limites de alcance e a revogação, não a ausência de vazamento. attack-chain verifica tentativas controladas de expansão, não exploração de vulnerabilidades ou comprometimento do host.

Correções realizadas durante a execução: armazenamento file removido no OpenBao 2.7 foi substituído por pebbledb; disable_mlock foi retirado; auditoria criada pela API foi substituída por audit declarativo em server.hcl, carregado com SIGHUP. A configuração restante foi concluída por bloco de recuperação na conversa.

O pacote foi corrigido para conter essas configurações. A instalação limpa usando o pacote corrigido ainda não foi repetida: os testes informados foram executados após as correções e a recuperação manual.

Limites: NodePort pode mascarar origem, exigindo revisão de SNAT/CNI. Bloqueio foi demonstrado com Pod local no cluster B; não prova isolamento de todos os workloads entre clusters. Não foram medidos desempenho, DoS, alta disponibilidade, recuperação de desastre, vulnerabilidades de imagens nem conformidade dos 28 itens. Regra de único administrador humano, MFA e estado de produção institucional não foram certificados.

Pendência de evidência: preservar na máquina da autora results.json original e logs dos Jobs; revisão linha a linha desses logs ainda não realizada aqui. Resultado: demonstração técnica aprovada no escopo informado do laboratório; modelo completo e produção não certificados.

Fontes das correções:
https://openbao.org/community/release-notes/2-7-0/
https://openbao.org/docs/configuration/audit/
https://openbao.org/docs/next/configuration/storage/pebbledb/
