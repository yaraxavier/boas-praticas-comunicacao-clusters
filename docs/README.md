# Documentação completa — roteiro de leitura

A documentação pode ser lida neste repositório ou na página estática `docs/index.html`, preparada para GitHub Pages. A página é gerada a partir dos mesmos arquivos Markdown para evitar versões editoriais divergentes.

| Ordem | Documento | Pergunta respondida |
|---|---|---|
| 1 | [Modelo geral](modelo/MODELO_GERAL.md) | Qual o problema, a teoria e o método? |
| 2 | [Referência GovHub/MGI/Ipea](modelo/REFERENCIA_GOVHUB.md) | De onde veio o contexto e o que é proposta própria? |
| 3 | [Arquitetura](poc/ARQUITETURA.md) | Quais componentes e fluxos foram implementados? |
| 4 | [Decisões](02-registro-decisoes.md) | Por que cada escolha e quais seus custos? |
| 5 | [Checklist](01-checklist-modelo.md) | Como avaliar as 28 práticas? |
| 6 | [Operação](poc/OPERACAO.md) | Como preparar, executar, coletar e encerrar? |
| 7 | [Testes e resultados](poc/TESTES_E_RESULTADOS.md) | O que foi testado, aprovado e o que falta? |
| 8 | [Revisões](poc/REVISOES.md) | O que deu erro e como foi corrigido? |
| 9 | [Evidências da instalação limpa](../evidence/public/2026-10-09-instalacao-limpa/README.md) | Quais registros sustentam a conclusão? |
| 10 | [Fontes](FONTES.md) | Quais documentos originais foram consultados? |

## Organização dos testes

- `tests/test_probe.py`: 7 testes locais do cliente HTTPS com servidor simulado.
- `tests/test_checklist.py`: 4 testes do registro documental e requisitos de evidência.
- `tests/test_leak_demo.py`: 2 testes da demonstração de sanitização de logs.
- `scripts/lab.py test`: execução real no laboratório, com dez Jobs e seis verificações adicionais, totalizando 16 critérios.
- `evidence/public/2026-10-09-instalacao-limpa/`: rodada atual, prints, transcrição identificada e manifesto de integridade.
- `evidence/public/VALIDACAO_AUTORA.md`: registro histórico da rodada anterior; não representa o estado atual da instalação limpa.

Os testes locais verificam o cliente e utilitários. Os testes reais verificam os cenários Kubernetes descritos na matriz. Não somar 13 e 16 como se fossem controles equivalentes.

## Fotos e rastreabilidade

Os PNGs originais ficam junto da rodada em `evidence/public/`. A página de leitura enquadra apenas a área relevante de cada figura, com legenda e link para o original integral. O enquadramento é feito na apresentação, sem reconstruir texto ou modificar pixels. As cópias em `docs/assets/` tornam o site independente de arquivos fora da pasta publicada.

Para atualizar: editar os Markdown, executar `python3 scripts/build_docs.py` e revisar a página. Não editar o HTML gerado manualmente.
