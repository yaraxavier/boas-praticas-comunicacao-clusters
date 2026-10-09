# O que foi revisado e corrigido

| Problema observado | Decisão/correção | Evidência e situação |
|---|---|---|
| OpenBao encerrava com `unknown storage type file` | Substituir backend file por pebbledb | Logs fornecidos; servidor iniciou e storage_type retornou pebbledb |
| Aviso de campo disable_mlock desconhecido | Remover configuração obsoleta | Configuração atual não contém o campo |
| Habilitação de auditoria via API retornou HTTP 400 | Declarar audit em server.hcl | API indicou configuração declarativa; autora confirmou auditoria após atualização/SIGHUP |
| Setup interrompido após inicialização | Recuperar configuração restante mantendo clusters | Autora informou initialized=true, sealed=false; depois suíte aprovada |
| Necessidade de preservar dados durante correção | Evitar recriar Pod com emptyDir | Estado atual efêmero explicitado na arquitetura |
| Proposta de adicionar terceiro cluster | Retirar do recorte final por decisão da autora | Código e testes de C excluídos desta entrega |
| Interpretação excessiva de PASS | Separar resultado observado e risco residual | Matriz explica leaked-token, rede local, RBAC e auditoria |
| Documento geral misturado ao laboratório | Separar docs/modelo e docs/poc | Teoria reutilizável; arquitetura e resultados específicos |

Fontes das mudanças OpenBao: [release notes 2.7](https://openbao.org/community/release-notes/2-7-0/) e [auditoria declarativa](https://openbao.org/docs/configuration/audit/). A configuração declarativa é carregada em reinicialização ou SIGHUP; no incidente relatado foi usado SIGHUP para preservar o Pod.

A instalação limpa foi executada em 09/10/2026 na máquina da autora, com setup concluído e 16 critérios aprovados, conforme os [prints da rodada](../../evidence/public/2026-10-09-instalacao-limpa/README.md). Não confundir essa evidência real com os testes locais simulados do cliente.
