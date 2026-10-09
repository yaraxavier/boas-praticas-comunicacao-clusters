# Verificação local desta entrega

Data: 09/10/2026. Ambiente do assistente, sem execução de clusters Kubernetes.

- `python3 -m unittest discover -s tests -v`: 13 testes aprovados.
- `python3 -m compileall -q scripts tests`: concluído sem erro.
- Links relativos dos documentos conferidos: nenhum destino ausente.
- Arquivos JSON lidos com parser; sem erros.
- Pacote sem extensão de terceiro cluster, estado privado, caches ou chaves.

Os testes verificam cliente HTTPS simulado, formulário de checklist e demonstração de sanitização de logs. Não substituem os resultados de Kubernetes informados pela autora. Atualização: instalação limpa executada pela autora em 09/10/2026 e documentada em [evidências da nova rodada](2026-10-09-instalacao-limpa/README.md). Código inalterado nesta atualização documental.

## Organização da documentação

Página estática gerada a partir dos Markdown, com links e âncoras conferidos e quatro enquadramentos de evidências. Cópias de imagens comparadas byte a byte com os originais. 13 testes locais novamente aprovados; código do laboratório não alterado. A revisão visual em navegador automatizado não foi concluída porque o executável Chromium não está instalado no ambiente de geração; conferir a apresentação ao abrir docs/index.html antes de publicar.
