# Registro de decisões e efeitos

Versão 4.0. Justificativas explícitas da POC; efeitos positivos são esperados, não ganhos já medidos.

## D01 - Dois clusters independentes

Por que foi escolhida: Tornar explícita a fronteira entre consumidor e autoridade de segredos e manter o recorte entre clusters.

Efeito positivo esperado: Permite examinar endpoints e identidades de autoridades distintas.

Efeito negativo ou risco residual: Mais consumo e complexidade de rota; não produz conectividade geral entre Pods.

Alternativa considerada: Um cluster com namespaces seria mais simples, mas não representaria a fronteira pretendida.

Como verificar: Conferir APIs distintas e os fluxos F01/F02.

Condição de revisão: Reavaliar topologia se o ambiente real tiver outra separação de autoridades.

Fontes de apoio: [R01], [R03]. A seleção concreta é uma decisão desta POC.

## D02 - Kind para reprodução local

Por que foi escolhida: Facilitar um laboratório descartável que a autora possa testar em Linux.

Efeito positivo esperado: Criação e limpeza delimitadas; não exige contratar infraestrutura.

Efeito negativo ou risco residual: Rede Docker e kubeconfig local diferem da operação institucional.

Alternativa considerada: Clusters gerenciados ou VMs seriam mais representativos, com mais requisitos de acesso e recursos.

Como verificar: Criar os clusters, confirmar versões e contextos; rejeitar nomes preexistentes.

Condição de revisão: Se o objetivo passar a disponibilidade ou desempenho institucional, substituir o cenário local.

Fontes de apoio: [R08]. A seleção concreta é uma decisão desta POC.

## D03 - Calico como CNI do ensaio

Por que foi escolhida: A política de rede precisa de um mecanismo que a aplique, não apenas de YAML aceito pela API.

Efeito positivo esperado: Oferece um caminho de enforcement para os testes propostos.

Efeito negativo ou risco residual: Adiciona componentes, permissões e manutenção; NAT pode afetar a interpretação.

Alternativa considerada: Usar a CNI já aprovada no ambiente real pode evitar um componente novo; comprovar seu suporte.

Como verificar: Testar acesso permitido/bloqueado e investigar origem efetiva.

Condição de revisão: Não instalar Calico sobre CNI institucional somente por ser a escolha do laboratório.

Fontes de apoio: [R07], [R08]. A seleção concreta é uma decisão desta POC.

## D04 - OpenBao para o fluxo de segredos

Por que foi escolhida: Demonstrar autenticação e autorização de consumidor que acessa configuração mantida em outro cluster.

Efeito positivo esperado: Centraliza o ponto de política e permite testar validade e revogação.

Efeito negativo ou risco residual: Torna-se dependência operacional; falha do servidor ou cliente autorizado comprometido ainda importa.

Alternativa considerada: Secrets nativos ou gerenciador já adotado podem bastar em outros contextos; comparar requisitos antes de acrescentar serviço.

Como verificar: Login, leitura restrita, negação administrativa e resposta à revogação.

Condição de revisão: Remover ou substituir se não houver requisito que justifique operação e manutenção adicionais.

Fontes de apoio: [R02], [R06], [R10]. A seleção concreta é uma decisão desta POC.

## D05 - TLS de servidor e identidade por token

Por que foi escolhida: Proteger o transporte e verificar o destino, mantendo separado o teste da identidade da aplicação.

Efeito positivo esperado: Cliente rejeita CA não confiável e usa identidade específica.

Efeito negativo ou risco residual: Certificados expiram; mTLS de cliente não está demonstrado nesta versão.

Alternativa considerada: mTLS pode ser necessário em outro modelo de confiança, com mais gestão de certificados.

Como verificar: CA inválida rejeitada; SAN e destino compatíveis; login correto.

Condição de revisão: Reavaliar se o serviço exigir certificado cliente ou política de confiança diferente.

Fontes de apoio: [R04]. A seleção concreta é uma decisão desta POC.

## D06 - Kubernetes Auth e reviewer dedicado

Por que foi escolhida: Avaliar o vínculo entre identidade do cluster A e autorização no OpenBao B.

Efeito positivo esperado: Validação usa a API da autoridade prevista com permissões delimitadas.

Efeito negativo ou risco residual: Disponibilidade e renovação do reviewer influenciam o login.

Alternativa considerada: JWT/OIDC é alternativa documentada, cuja validade e revogação precisam de análise própria.

Como verificar: ServiceAccount/audience errados negados; reviewer cria somente TokenReview.

Condição de revisão: Reconsiderar se o endpoint da API não puder ser alcançado com segurança.

Fontes de apoio: [R03], [R05]. A seleção concreta é uma decisão desta POC.

## D07 - TTL de laboratório e política de leitura estreita

Por que foi escolhida: Limitar alcance e tornar revogação/expiração observáveis em um ensaio curto.

Efeito positivo esperado: A credencial não autoriza outros caminhos nem escrita.

Efeito negativo ou risco residual: Token válido copiado ainda permite seu próprio acesso; renovação frequente tem custo.

Alternativa considerada: Prazo maior reduz autenticações, mas aumenta janela de uso; definir conforme risco e operação reais.

Como verificar: TTL 300 s no ensaio normal e 30 s na role de expiração; testar ambas.

Condição de revisão: Esses valores são parâmetros da POC, não recomendação universal das fontes.

Fontes de apoio: [R02], [R03]. A seleção concreta é uma decisão desta POC.

## D08 - Um titular humano de administração geral

Por que foi escolhida: Atender à regra de governança proposta pela autora e reduzir dispersão do poder global.

Efeito positivo esperado: Facilita inventário de concessões e responsabilização.

Efeito negativo ou risco residual: Cria concentração de poder e risco de indisponibilidade; compromisso dessa identidade tem grande impacto.

Alternativa considerada: Outra organização pode precisar de modelo de concessão temporária e custódia diferente; não transplantar a regra sem revisão.

Como verificar: Inventariar concessões equivalentes, substituição e uso cotidiano de contas limitadas.

Condição de revisão: A documentação Kubernetes sustenta privilégio mínimo, não exige exatamente um administrador. Unseal/custódia de chaves é decisão distinta.

Fontes de apoio: [R05], [R02]. A seleção concreta é uma decisão desta POC.

## D09 - Armazenamento temporário e bootstrap simplificado

Por que foi escolhida: Reduzir montagem do laboratório para observar o fluxo sem construir uma plataforma de produção.

Efeito positivo esperado: Instalação pequena, baixo esforço inicial e descarte fácil.

Efeito negativo ou risco residual: Recriar o Pod perde armazenamento; chave única de unseal e root retido são simplificações com risco.

Alternativa considerada: Persistência, backup e custódia de chaves são necessários quando a criticidade exigir.

Como verificar: Registrar limites e não declarar BP17 atendido por essa escolha.

Condição de revisão: Nunca usar essa decisão como desenho de produção ou prova de recuperação.

Fontes de apoio: [R02], [R09]. A seleção concreta é uma decisão desta POC.

## D10 - Probes diretos, sem Agent/CSI nesta versão

Por que foi escolhida: Manter transparente o ensaio de API, token e autorização antes de adicionar mecanismo de entrega.

Efeito positivo esperado: Menos componentes para diagnosticar o comportamento básico.

Efeito negativo ou risco residual: Não cobre renovação automática, lifecycle nem integração real do pipeline.

Alternativa considerada: Agent/CSI ou backend de secrets do consumidor podem resolver requisitos reais, após justificar privilégios e dependências.

Como verificar: Testar o cliente e revisar ausência de valores privados nos logs.

Condição de revisão: Reavaliar quando a aplicação tiver requisito de entrega/renovação contínua.

Fontes de apoio: [R03], [R02]. A seleção concreta é uma decisão desta POC.

## D11 - Log por campos operacionais controlados

Por que foi escolhida: Demonstrar uma exposição simples por excesso de conteúdo e uma saída reduzida.

Efeito positivo esperado: Evita os marcadores restritos no caso testado.

Efeito negativo ou risco residual: Pode retirar informação útil e não detecta todos os vazamentos ou campos novos.

Alternativa considerada: Redação automática pode complementar, mas exige tratamento de falhas e teste de conteúdo.

Como verificar: Executar leak_demo e revisar o que se perde ou permanece no log.

Condição de revisão: Testar novos eventos antes de liberar campos; não confundir o exemplo com scanner universal.

Fontes de apoio: [R06]. A seleção concreta é uma decisão desta POC.

## D12 - Suíte automatizada com revisão humana

Por que foi escolhida: Repetir verificações observáveis sem terceirizar a conclusão de segurança.

Efeito positivo esperado: Consistência e rastreabilidade do procedimento.

Efeito negativo ou risco residual: PASS pode refletir um teste errado ou causa equivocada; simulação não valida cluster real.

Alternativa considerada: Revisão manual sem automação reduz infraestrutura de teste, mas dificulta repetição; combinar conforme escopo.

Como verificar: Revisar premissa, negativo, resultado e causa antes de marcar Conforme.

Condição de revisão: Mudar a suíte quando o risco mudar; não aprovar somente porque ferramenta ou IA afirmou.

Fontes de apoio: [R15], [R07]. A seleção concreta é uma decisão desta POC.

## D13 - Não adicionar scanners, service mesh e plataformas sem requisito

Por que foi escolhida: Evitar aumentar a superfície e o custo sem identificar qual lacuna o componente trata.

Efeito positivo esperado: Menos interfaces, integrações, permissões e dependências para manter.

Efeito negativo ou risco residual: Adiar uma ferramenta necessária também mantém gaps; simplificar não é omitir controle obrigatório.

Alternativa considerada: Adicionar componente somente com risco, responsável, teste e comparação com capacidade existente.

Como verificar: Revisar BP26 e decisão da inclusão/adiamento com evidência.

Condição de revisão: Se surgir gap demonstrado, reconsiderar; menos componentes não significa menos proteção necessária.

Fontes de apoio: [R10]. A seleção concreta é uma decisão desta POC.

## D14 - Atualização controlada, sem troca cega de versões

Por que foi escolhida: Conservar compatibilidade e proteção durante a evolução do modelo.

Efeito positivo esperado: Mudança fica associada a motivo, testes e retorno.

Efeito negativo ou risco residual: Exige tempo e pode manter risco enquanto correção não é aplicada.

Alternativa considerada: Atualização automática exige pipeline capaz de detectar regressões e recuperar falhas.

Como verificar: Aplicar BP25 e repetir verificações afetadas.

Condição de revisão: Priorização conforme exposição; os números fixados no script precisam de revisão.

Fontes de apoio: [R09], [R12]. A seleção concreta é uma decisão desta POC.


## Nota da entrega A–B de 09/10/2026

Este catálogo registra critérios e decisões do modelo. Situações iniciais não são uma avaliação atual preenchida. Os resultados efetivamente informados estão em [Testes e resultados](poc/TESTES_E_RESULTADOS.md). Aprovação da suíte não torna automaticamente conformes as 28 práticas.
