# Operação, coleta e encerramento

## Preparação

Use apenas máquina/laboratório autorizado com dados fictícios. São necessários Docker Engine funcional, kind, kubectl, OpenSSL, Python 3.10+ e acesso aos registries/manifests. `preflight` verifica ferramentas e Docker; não certifica recursos disponíveis ou compatibilidade. Consulte as versões em [Arquitetura](ARQUITETURA.md). Não há dimensionamento mínimo medido.

Na raiz do pacote, antes de alterar clusters:

```bash
python3 scripts/lab.py preflight
kind get clusters
kubectl config get-contexts
```

Para ambiente novo, execute `python3 scripts/lab.py setup` e depois `python3 scripts/lab.py test`. Para A/B já configurados, execute somente `test`. O setup recusa nomes existentes. A suíte retira temporariamente as políticas próprias para produzir baseline; nunca executar em produção.

O teste renova o token reviewer, gera Jobs e grava `evidence/results.json`. Aguarde conclusão; expiração e recusas de rede podem demorar. Não confundir Pod de Job Completed com serviço indisponível. OpenBao deve permanecer em execução.

## Diagnóstico sem revelar credenciais

```bash
kubectl --context kind-sbd-bao -n poc get pods
kubectl --context kind-sbd-bao -n poc logs deployment/openbao --tail=80
kubectl --context kind-sbd-app -n poc get jobs
kubectl --context kind-sbd-bao -n poc get networkpolicy
```

Revise logs antes de compartilhar. Se ocorrer HTTP 400, registre mensagem sanitizada e etapa; não refaça init em servidor já inicializado. Se o Pod de OpenBao foi substituído, o volume efêmero pode ter sido perdido: bootstrap antigo deixa de representar o servidor novo. Não tentar resolver com desativação de TLS ou permissões globais.

## Evidências antes de apagar

1. Preserve `evidence/results.json` original, horário e versão do código em armazenamento controlado.
2. Guarde logs dos Jobs selecionados localmente após revisar segredos e dados pessoais. Registre nomes concretos a partir de `get jobs`.
3. Capture contexto/nome dos clusters, OpenBao em execução, resultados dos Jobs e JSON final.
4. Para publicação, recorte a região pertinente e mantenha comando, contexto e resultado legíveis. Remova credenciais antes de capturar; não alterar PASS/FAIL.
5. Identifique as figuras e explique o que cada uma comprova. O anexo fornecido contém três recortes dos prints da autora.

Não publicar `.state/bootstrap.json`, chaves, kubeconfig, JWTs ou valores de segredo. Auditoria bruta pode expor metadados mesmo com HMAC de campos.

## Encerramento — somente depois de preservar evidências

```bash
python3 scripts/lab.py cleanup
kind get clusters
```

O cleanup remove A/B apenas quando encontra marcadores locais de propriedade. Não remove clusters de outros nomes e não apaga automaticamente `.state`. Se faltar marcador, investigar a propriedade antes de qualquer exclusão manual. Após confirmar o encerramento e não precisar recuperar o laboratório, excluir o estado sensível local de forma controlada; nunca incluí-lo no Git. A exclusão dos clusters é destrutiva para os volumes efêmeros.

## Reteste após mudança

Mudanças de imagem, CNI, TLS, identidade, ACL ou política de rede exigem repetir a suíte real. Salve resultados por execução em vez de substituir a evidência histórica publicada. O teste deve falhar quando a operação autorizada é negada ou uma operação proibida é aceita.
