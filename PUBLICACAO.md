# Preparação para GitHub

Este diretório é a raiz do repositório a publicar. Repositório de destino confirmado: `yaraxavier/boas-praticas-comunicacao-clusters`. A ativação do GitHub Pages deve ser conferida separadamente. O responsável deve escolher o repositório, a visibilidade, a autoria e a licença adequada antes da publicação. Não adicionar licença de terceiros por inferência.

1. Ler README, resultados e limitações; conferir os prints antes de torná-los públicos.
2. Executar os testes locais e revisar `git status` e `git diff --cached`.
3. Adicionar somente documentação, código, testes e evidências públicas revisadas. Nunca adicionar `.state` ou usar `git add -f` para contornar exclusões de credenciais.
4. Registrar commit e versões na próxima execução real. Não alterar retrospectivamente a proveniência do resultado de 08/10/2026.
5. Publicar no remoto escolhido após revisão do responsável. Se houver requisito de repositório institucional, confirmar suas regras de autoria/licenciamento.

Exemplo de preparação local, somente se ainda não houver um repositório Git nesse diretório:

```bash
git init
git add README.md AGENTS.md PUBLICACAO.md .gitignore docs scripts tests evidence/public
git diff --cached --stat
git diff --cached
```

O conteúdo pronto inclui documentação geral, arquitetura A/B, decisões, checklist, scripts, testes locais e evidências informadas. Não inclui terceiro cluster, credenciais reais, estado do laboratório ou afirmação de homologação institucional.


## Configuração do Git

O pacote não contém `.git`, um remoto presumido ou identidade de commit. A configuração local deve ser feita na pasta extraída. Se o projeto já tiver um repositório, preservar seu histórico e revisar as diferenças antes de copiar arquivos. Não executar `git init` em outra pasta nem usar push forçado.

Antes do commit:

```bash
python3 scripts/build_docs.py
python3 -m unittest discover -s tests -v
git status --short
git diff --cached
```

Após revisão, criar o commit, escolher o remoto real e enviar a branch. O endereço do repositório é necessário para fornecer os comandos finais sem adivinhar conta ou projeto. Não publicar credenciais, backups ou logs brutos.

## Publicar a documentação no GitHub Pages

A página foi preparada sem dependências externas de CSS, JavaScript ou bibliotecas de frontend. O gerador usa apenas a biblioteca padrão Python e produz o HTML completo. O arquivo `docs/.nojekyll` acompanha a página.

No repositório escolhido, depois de enviar os arquivos:

1. Abrir **Settings → Pages**.
2. Em **Build and deployment**, selecionar **Deploy from a branch**.
3. Escolher a branch usada (por exemplo `main`) e a pasta **/docs**.
4. Salvar e aguardar o endereço informado pelo GitHub.
5. Abrir a página publicada e conferir navegação, tabela de testes, figuras e links para os originais.

A disponibilidade depende do plano e das regras da organização. Em publicação comum, o site pode ser público mesmo que o repositório seja privado; revisar os arquivos da pasta docs antes de ativar.

Fonte: [GitHub — configuração da origem de publicação](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), consultada em 09/10/2026.
