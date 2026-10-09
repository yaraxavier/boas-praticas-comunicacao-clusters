# BOAS PRÁTICAS DE SEGURANÇA NA COMUNICAÇÃO ENTRE CLUSTERS

DESENVOLVIMENTO: SETEMBRO A OUTUBRO DE 2026• LABORATÓRIO DESCARTÁVEL COM DADOS FICTÍCIOS.

A comunicação entre clusters exige atenção às permissões, às credenciais e aos caminhos de acesso. Pequenas decisões de configuração podem permitir acessos indevidos ou expor informações, mesmo quando existem ferramentas de segurança.

A proposta é transformar boas práticas em decisões justificadas e verificáveis: identificar fluxos e riscos, escolher controles necessários, testar acessos e recusas, registrar evidências e revisar limitações. O OpenBao apoia a gestão de segredos nessa comunicação. Documentações públicas de alguns órgãos foram utilizadas como referências para o estudo.

## Trajetória do trabalho

A pesquisa reuniu definição do problema, estudo das boas práticas, decisões de arquitetura, implementação e revisão da POC. Cada escolha foi analisada considerando o risco tratado, os benefícios, as limitações e as alternativas disponíveis. Os testes permitem confrontar o modelo proposto com o comportamento observado no laboratório.

## Estado da entrega

A instalação limpa foi concluída e a suíte apresentou 16 critérios atendidos e dez Jobs com resultado PASS. Foram registradas 85 linhas de auditoria.

Os [quatro prints e a transcrição dos resultados](evidence/public/2026-10-09-instalacao-limpa/README.md) documentam essa execução. A documentação apresenta os cenários avaliados, as respostas obtidas e as limitações observadas. As revisões anteriores permanecem registradas para acompanhar a evolução da POC.

## Acesso à documentação

Repositório: https://github.com/yaraxavier/boas-praticas-comunicacao-clusters

Comece pelo [índice completo](docs/README.md). A [versão HTML](docs/index.html) reúne a documentação em uma página de leitura. Para consultá-la localmente, abra o arquivo `docs/index.html` no navegador após baixar e extrair o repositório.

## Onde está cada coisa

| Pasta ou arquivo | Conteúdo |
|---|---|
| `README.md` | Entrada do repositório e estado atual |
| `docs/modelo/` | Teoria e referências utilizadas |
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
2. [Referências públicas utilizadas no estudo](docs/modelo/REFERENCIA_GOVHUB.md).
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
