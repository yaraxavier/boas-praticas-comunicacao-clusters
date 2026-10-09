# Boas práticas de segurança na comunicação entre clusters Kubernetes

Desenvolvimento: setembro a outubro de 2026 • POC A–B • laboratório descartável com dados fictícios.

A proposta é um modelo verificável: identificar fluxos e riscos, escolher controles mínimos, testar permissões e recusas, registrar evidências e revisar limitações. OpenBao demonstra gestão de segredos nessa comunicação. A arquitetura não pretende reproduzir a infraestrutura de produção do GovHub, MGI ou Ipea.

## Trajetória do trabalho

A pesquisa foi desenvolvida entre setembro e outubro de 2026, incluindo definição do problema, estudo das boas práticas, decisões de arquitetura, implementação e revisão da POC. A validação final é uma etapa desse percurso, não a data de início do trabalho.

## Estado da entrega

Instalação limpa executada pela autora em 09/10/2026, com setup concluído e suíte aprovada: 16 critérios true, dez Jobs PASS e 85 linhas de auditoria, às 11:08:55 UTC (08:08:55 Brasília). Os [quatro prints e a transcrição](evidence/public/2026-10-09-instalacao-limpa/README.md) foram conferidos. Essa rodada encerra a pendência de instalação limpa no ambiente testado. A execução anterior após correções manuais permanece registrada separadamente. O terceiro cluster está fora do escopo; não há certificação de produção ou do modelo completo.

## Acesso à documentação

Repositório: https://github.com/yaraxavier/boas-praticas-comunicacao-clusters

Comece pelo [índice completo](docs/README.md). A versão de leitura está em `docs/index.html`, pronta para GitHub Pages. Abra esse arquivo no navegador após extrair o pacote. O endereço público será informado pelo GitHub depois da ativação; ainda não há site publicado.

## Onde está cada coisa

| Pasta ou arquivo | Conteúdo |
|---|---|
| `README.md` | Entrada do repositório e estado atual |
| `docs/modelo/` | Teoria e referência institucional |
| `docs/poc/` | Arquitetura, operação, testes e correções |
| `docs/index.html` | Página completa de leitura e figuras enquadradas |
| `scripts/` | Automação da POC, checklist e geração da página |
| `tests/` | Testes locais do código |
| `evidence/public/` | Evidências revisadas e separadas por rodada |
| `AGENTS.md` | Regras para pessoas e assistentes contribuírem |
| `PUBLICACAO.md` | Preparação Git e publicação no GitHub Pages |
| `.state/` | Estado privado gerado localmente; nunca publicar |

## Ordem de leitura

1. [Modelo geral e teoria](docs/modelo/MODELO_GERAL.md).
2. [Referência GovHub, MGI e Ipea](docs/modelo/REFERENCIA_GOVHUB.md).
3. [Arquitetura implementada](docs/poc/ARQUITETURA.md).
4. [Testes, respostas e limitações](docs/poc/TESTES_E_RESULTADOS.md).
5. [Revisões e correções](docs/poc/REVISOES.md).
6. [Operação, evidências e encerramento](docs/poc/OPERACAO.md).
7. [28 práticas do checklist](docs/01-checklist-modelo.md), [14 decisões](docs/02-registro-decisoes.md) e [fontes](docs/FONTES.md).
8. [Regras de contribuição](AGENTS.md) e [publicação no GitHub](PUBLICACAO.md).

## Executar

Em Linux com Python 3.10+, OpenSSL, Docker Engine, kind e kubectl, leia primeiro as restrições de versão e operação. Em ambiente novo:

```bash
python3 scripts/lab.py preflight
python3 scripts/lab.py setup
python3 scripts/lab.py test
```

Se os clusters A/B já existem e estão configurados, execute somente `test`. Não rode `setup` por cima e não apague o laboratório antes de guardar as evidências.

Testes locais do código, sem Kubernetes:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
```

As evidências publicáveis estão em [evidence/public](evidence/public). Credenciais ficam em `.state/` e são excluídas do Git. O baseline da suíte remove temporariamente apenas as NetworkPolicies criadas por esta POC; execute apenas no laboratório.
