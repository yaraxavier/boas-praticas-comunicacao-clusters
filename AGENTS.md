# Regras para trabalhar nesta POC

Este arquivo é uma proposta própria; não é o AGENTS.md do GovHub.

1. Preserve o foco: modelo documentado de boas práticas para comunicação entre clusters; OpenBao apoia a demonstração.
2. Use apenas laboratório descartável e dados fictícios.
3. Documente risco, prática, controle existente, gap, implementação, teste e evidência.
4. Não trate um manifesto aplicado como evidência de bloqueio efetivo.
5. Nunca registre JWT, root token, chave privada, unseal key ou valor de segredo nos logs.
6. Valide CA e hostname; não use `curl -k`, TLS desabilitado ou modo dev.
7. Diferencie controle demonstrado, resultado esperado e pendência.
8. Não altere produção nem copie configurações do laboratório para produção sem revisão.
9. Antes de modificar scripts, rode os testes do cliente e a compilação Python.
10. Após mudança de rede ou identidade, repita a matriz de testes no laboratório.
11. Mantenha commit e caminhos das referências verificáveis; não invente estado de produção.
12. Mantenha os 28 itens do checklist, seus critérios, impactos e situações consistentes entre Markdown e JSON.
13. Não use conclusão de segurança garantida nem presuma que segurança é sempre oposta à eficiência.
14. Diferencie dados pessoais, pessoais sensíveis, credenciais e informação técnica; não classifique automaticamente CPF ou senha como pessoal sensível.
15. Preserve um único titular humano geral, contas individuais e privilégios mínimos; documente risco de indisponibilidade e substituição controlada.
16. Todo ataque/vazamento é simulado com dados fictícios em laboratório; registre alcance residual de um token válido comprometido.
17. Exigir risco tratado e alternativa antes de adicionar ferramenta; menos componentes não autoriza omitir proteção necessária.
18. IA, scanner e PASS não substituem revisão humana das premissas e evidências.
19. Registrar efeitos positivos, negativos, alternativas e condição de revisão de cada decisão, com documentação original.
20. Não converter relato público de uso em prova de segurança nem presumir que uma fonte exige escolhas próprias da POC.


## Escopo e organização desta entrega

- Trabalhar somente com A (`sbd-app`) e B (`sbd-bao`). Não criar terceiro cluster sem nova solicitação.
- Manter teoria em `docs/modelo/` e implementação/resultados em `docs/poc/`.
- Não tratar o `AGENTS.md` como mecanismo de segurança: é instrução de trabalho, sujeita à revisão humana.
- Este arquivo é próprio da POC; não foi copiado de um AGENTS.md do GovHub.
- Preservar a distinção entre execução informada pela autora, testes locais simulados e teste ainda pendente.
- Não substituir o resultado histórico por uma nova execução: guardar data, versão e proveniência.
- Nunca executar `cleanup` antes de preservar evidências; não modificar clusters alheios.
- Não publicar `.state`, kubeconfig, chaves, bootstrap, tokens, logs brutos nem backups do código.
- Revisar o diff e o conteúdo de cada arquivo público; `.gitignore` não substitui revisão.
- Após editar código, executar `python3 -m unittest discover -s tests -v` e `python3 -m compileall -q scripts tests`.
- Testes locais não substituem `python3 scripts/lab.py test` no laboratório real.
- Fontes e datas devem ser verificáveis. Não inventar versões compatíveis, ganhos de desempenho ou adoção institucional.
- Não publicar no GitHub, escolher licença ou atribuir autoria institucional sem decisão do responsável.
