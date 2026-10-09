# Fontes e rastreabilidade

As fontes R01–R19 do catálogo original estão listadas abaixo. Elas sustentam mecanismos e contexto; as escolhas concretas e resultados são próprios da POC. Consulta documental consolidada em 09/10/2026. URLs podem mudar; o commit da referência GovHub fixa a inspeção de código.

## R01 — GOVHUB-BR

[Data Application MGI: README e infraestrutura local](https://github.com/GovHub-br/data-application-mgi)

Escopo: Commit 9f9d94761a8867bcdd392a4b10c70b56f2e8c8da; referência observada, não produção validada. Consulta: 2026-10-08.

## R02 — OPENBAO

[Security model](https://openbao.org/docs/internals/security/)

Escopo: Modelo de ameaça e exclusões, incluindo cliente/host comprometidos. Consulta: 2026-10-08.

## R03 — OPENBAO

[Kubernetes auth method](https://openbao.org/docs/auth/kubernetes/)

Escopo: Autenticação e alternativas de JWT/reviewer; consultar seção de tokens curtos. Consulta: 2026-10-08.

## R04 — OPENBAO

[tcp listener](https://openbao.org/docs/configuration/listener/tcp/)

Escopo: Parâmetros de TLS e listener. Consulta: 2026-10-08.

## R05 — KUBERNETES

[Role Based Access Control Good Practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)

Escopo: Privilégio mínimo e caminhos indiretos de elevação. Consulta: 2026-10-08.

## R06 — KUBERNETES

[Good practices for Kubernetes Secrets](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)

Escopo: Acesso e tratamento de Secrets nativos. Consulta: 2026-10-08.

## R07 — KUBERNETES

[Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

Escopo: Semântica e limites de enforcement e tradução de endereços. Consulta: 2026-10-08.

## R08 — TIGERA / CALICO

[Installing on Kind](https://docs.tigera.io/calico/latest/getting-started/kubernetes/kind)

Escopo: CNI para o cenário Kind; a combinação fixada no código precisa de execução. Consulta: 2026-10-08.

## R09 — GITLAB

[GitLab Secrets Manager (OpenBao)](https://docs.gitlab.com/administration/secrets_manager/)

Escopo: Integração documentada, operação e manutenção; não é arquitetura desta POC. Consulta: 2026-10-08.

## R10 — SCHEEL, Alex

[OpenBao @ GitLab - FOSDEM 25, 12 fev. 2025](https://openbao.org/blog/cipherboy-fosdem-25-talk/)

Escopo: Relato técnico por participante do projeto; discussão de custo operacional e benefício. Consulta: 2026-10-08.

## R11 — OPENBAO

[Adopters](https://openbao.org/ecosystem/adopters/)

Escopo: Organizações listadas publicamente; não fornece auditoria de cada implantação. Consulta: 2026-10-08.

## R12 — FERMITOOLS / FERMILAB

[htvault-config: README](https://github.com/fermitools/htvault-config)

Escopo: Configuração pública do OpenBao, clientes, autenticação e renovação. Consulta: 2026-10-08.

## R13 — DYKSTRA, Dave e colaboradores

[Fermilab’s Transition to Token Authentication, 2025](https://arxiv.org/abs/2503.24196)

Escopo: Relato técnico histórico em preprint; usa terminologia Vault, distinguida do README atual. Consulta: 2026-10-08.

## R14 — CNCF

[Spotify: case study, 27 jun. 2019](https://www.cncf.io/case-studies/spotify/)

Escopo: Caso histórico com relatos de profissionais; não evidência atual de segurança ou uso de OpenBao. Consulta: 2026-10-08.

## R15 — GITHUB

[About GitHub Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review)

Escopo: Seção Validating Copilot code reviews: complementar verificação automática com humana. Consulta: 2026-10-08.

## R16 — BRASIL

[Lei 13.709/2018, art. 5º](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

Escopo: Definições legais de dados pessoais e pessoais sensíveis. Consulta: 2026-10-08.

## R17 — ANPD

[Perguntas frequentes](https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes)

Escopo: Categorias e exemplos de dados pessoais. Consulta: 2026-10-08.

## R18 — ANPD

[Glossário ANPD](https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/glossario-anpd)

Escopo: Dados de autenticação em sistemas. Consulta: 2026-10-08.

## R19 — KUBERNETES

[Application Security Checklist](https://kubernetes.io/docs/concepts/security/application-security-checklist/)

Escopo: Checklist original de aplicação: imagens, contexto de segurança e requisitos de execução. Consulta: 2026-10-08.

## Fontes adicionais das revisões

- [Auditoria declarativa OpenBao](https://openbao.org/docs/configuration/audit/): configuração e recarga dos dispositivos.
- [Release notes OpenBao 2.7](https://openbao.org/community/release-notes/2-7-0/): alterações incompatíveis e remoções.
- [GovHub — Quem somos](https://gov-hub.io/govhub/quem-somos/): contexto do projeto; não comprova topologia de produção.
- [Política de version skew Kubernetes](https://kubernetes.io/releases/version-skew-policy/): verificar a compatibilidade de clientes e componentes antes de reproduzir.

## Como citar os resultados

Referenciar a transcrição, a declaração de proveniência e os prints em evidence/public. Informar que os resultados foram enviados pela autora e obtidos após correções manuais. Citar o commit da entrega depois da publicação; não inventar hash antes de existir.
