# Checklist verificável do modelo de boas práticas

Versão 4.0 | 08/10/2026. São 28 práticas. Cada situação inicial é Pendente. P0 indica pré-condição crítica; P1 indica análise contextual complementar. Fontes sustentam mecanismos, não todas as escolhas. Prioridade não é pontuação de segurança.

## BP01 - Inventariar os fluxos entre clusters (P0)

Risco: Comunicação necessária não identificada ou exposição de interfaces sem finalidade.

Prática recomendada: Registrar origem, destino, porta, protocolo, aplicação, identidade, ativo e justificativa de cada fluxo.

Como verificar: Comparar inventário com manifests, Services, endpoints e tráfego observado no ambiente.

Evidência exigida: Inventário datado, desenho dos fluxos e configuração correspondente, sem credenciais.

Critério de atendimento: Cada fluxo permitido possui finalidade e responsável; fluxos desconhecidos permanecem pendentes até investigação.

Impacto possível: Esforço inicial de levantamento e manutenção quando a arquitetura muda.

Situação na demonstração: Documentado para o laboratório; confirmação por observação de tráfego ainda pendente.

Decisões associadas: D01. Fontes de apoio: [R01].

## BP02 - Delimitar fronteiras e autoridades de identidade (P0)

Risco: Confundir clusters diferentes ou atribuir a mesma autoridade a contas homônimas.

Prática recomendada: Identificar API, CA, namespaces, contas e mount de autenticação por cluster consumidor.

Como verificar: Conferir o endpoint configurado e autenticar uma identidade de cada autoridade efetivamente utilizada.

Evidência exigida: Mapa de confiança e configuração de mounts, endpoints e CAs.

Critério de atendimento: Toda identidade é vinculada à autoridade prevista; novo consumidor não é incluído sem configuração e teste específicos.

Impacto possível: Configuração adicional por cluster e maior responsabilidade sobre rotação de confiança.

Situação na demonstração: Dois clusters criados na instalação limpa de 09/10/2026; A é consumidor com mount próprio. Sem terceiro cluster.

Decisões associadas: D01, D06. Fontes de apoio: [R03].

## BP03 - Verificar TLS em todos os fluxos sensíveis (P0)

Risco: Intercepção de JWT, segredo ou credencial e conexão com servidor indevido.

Prática recomendada: Usar HTTPS com CA confiável e hostname/IP compatível com SAN, sem desabilitar validação; aplicar TLS também ao TokenReview.

Como verificar: Teste positivo com certificado válido e negativo com CA não confiável; revisar destino, SAN e validade.

Evidência exigida: Resultados de handshake e rejeição específica de certificado, sem chave privada.

Critério de atendimento: Fluxo válido funciona e certificado não confiável é rejeitado por causa TLS identificada; conexão em claro não é aceita como alternativa.

Impacto possível: Handshake, gestão de certificados e custo de renovação; medir impacto em vez de presumir.

Situação na demonstração: Comunicação autorizada e rejeição de CA não confiável aprovadas na rodada real de 09/10/2026. Inspeção independente de todos os fluxos TLS permanece pendente.

Decisões associadas: D05. Fontes de apoio: [R04].

## BP04 - Controlar o ciclo de vida de certificados (P0)

Risco: Expiração interrompe o serviço ou confiança antiga permanece ativa.

Prática recomendada: Definir emissor, validade, proprietário, renovação, distribuição de CA e procedimento de substituição.

Como verificar: Simular renovação e verificar acesso após troca; examinar alerta de vencimento.

Evidência exigida: Procedimento e registro de teste de renovação, com datas e responsáveis.

Critério de atendimento: Renovação e recuperação de falha documentadas e verificadas dentro do prazo operacional definido.

Impacto possível: Manutenção recorrente e possível janela de atualização.

Situação na demonstração: Certificados de laboratório de sete dias; renovação automática não implementada.

Decisões associadas: D05, D14. Fontes de apoio: [R04], [R12].

## BP05 - Usar identidade específica por consumidor (P0)

Risco: Credenciais compartilhadas ampliam alcance e dificultam rastreamento.

Prática recomendada: Separar ServiceAccounts por aplicação e autorizar nome e namespace específicos no OpenBao.

Como verificar: Executar login da conta permitida e da conta outsider.

Evidência exigida: Configuração da role e logs de login permitido/rejeitado.

Critério de atendimento: Conta legítima aceita; conta fora do vínculo rejeitada; exceções têm justificativa e prazo.

Impacto possível: Mais contas e políticas para manter; melhora atribuição de acesso.

Situação na demonstração: wrong-sa aprovado na rodada real de 09/10/2026; a identidade outsider foi recusada conforme o teste.

Decisões associadas: D06, D07. Fontes de apoio: [R03], [R05].

## BP06 - Restringir audience e prazo do JWT (P0)

Risco: Token emitido para outra finalidade é reaproveitado indevidamente.

Prática recomendada: Projetar token com audience específica e expiração; desligar montagem automática onde não necessária.

Como verificar: Tentar login com audience válida e incorreta; revisar volume projetado e validade emitida.

Evidência exigida: Manifest do consumidor e resultados dos testes, sem JWT.

Critério de atendimento: Audience indevida é rejeitada e tokens não são mantidos como Secrets permanentes por conveniência.

Impacto possível: Renovação e compatibilidade das aplicações precisam ser verificadas.

Situação na demonstração: wrong-audience aprovado na rodada real de 09/10/2026; JWT projetado solicita 600 s. Expiração do JWT Kubernetes não foi testada separadamente da expiração do token OpenBao.

Decisões associadas: D06. Fontes de apoio: [R03].

## BP07 - Limitar o reviewer de autenticação (P0)

Risco: Validador ganha poder além do necessário ou sua expiração interrompe autenticação.

Prática recomendada: Conta reviewer dedicada com create em tokenreviews; CA e API corretas; estratégia explícita de renovação.

Como verificar: Verificar can-i para TokenReview e Secrets; testar login após renovação e após falha controlada.

Evidência exigida: Regras RBAC, can-i e procedimento de rotação do reviewer.

Critério de atendimento: Reviewer pode validar tokens e não ler Secrets; ciclo de renovação é conhecido e testado.

Impacto possível: Complexidade operacional e dependência da API remota.

Situação na demonstração: Verificações RBAC do reviewer aprovadas na rodada real de 09/10/2026; renovação feita ao executar test. Automação contínua não implementada.

Decisões associadas: D06. Fontes de apoio: [R03], [R05].

## BP08 - Aplicar autorização mínima por caminho (P0)

Risco: Aplicação lê segredos de outras aplicações ou altera configurações.

Prática recomendada: Política por recurso e ação: permitir apenas caminhos e capacidades necessários.

Como verificar: Ler caminho próprio, ler caminho de outro consumidor e tentar escrita.

Evidência exigida: Policy e logs allowed_read, foreign_path_denied e write_denied.

Critério de atendimento: Acesso necessário funciona; leitura estrangeira e escrita desnecessária são negadas.

Impacto possível: Políticas mais detalhadas e revisão quando a aplicação muda.

Situação na demonstração: authorized, leaked-token e attack-chain aprovados na rodada real de 09/10/2026; leitura do próprio escopo permitida e expansão de permissões recusada nos casos testados.

Decisões associadas: D07. Fontes de apoio: [R02].

## BP09 - Restringir fluxos de entrada e saída (P0)

Risco: Pod comprometido usa caminhos de rede que não são necessários.

Prática recomendada: Aplicar políticas explícitas de origem, destino e porta e comprovar suporte de enforcement da CNI.

Como verificar: Comparar baseline e pós-controle com serviço saudável; tentar acesso de origem não permitida.

Evidência exigida: Políticas aplicadas, sucesso legítimo, bloqueio e, quando disponível, registros do CNI.

Critério de atendimento: Fluxos necessários continuam operacionais e tentativas fora do escopo são bloqueadas com causa identificável.

Impacto possível: Regras podem quebrar dependências legítimas; exige levantamento e diagnóstico.

Situação na demonstração: network-denied aprovado em 08/10 e na instalação limpa de 09/10/2026; bloqueio demonstrado localmente em B, sem comprovação de isolamento de workloads externos.

Decisões associadas: D03. Fontes de apoio: [R07], [R08].

## BP10 - Validar o efeito de NAT e da exposição externa (P0)

Risco: Regras baseadas em IP passam a representar o nó ou gateway, não a aplicação.

Prática recomendada: Mapear NodePort, LoadBalancer, NAT e firewall; definir onde cada controle enxerga a origem efetiva.

Como verificar: Examinar IP/porta antes e depois da tradução e testar dois consumidores remotos com permissões distintas.

Evidência exigida: Diagrama de encaminhamento, registros de origem e testes entre consumidores.

Critério de atendimento: Não se atribui isolamento por identidade remota a uma regra que apenas permite o IP compartilhado de nó/gateway.

Impacto possível: Pode exigir firewall, gateway ou mudança de topologia; custo depende do ambiente.

Situação na demonstração: Limite documentado; isolamento por identidade remota não demonstrado nesta versão.

Decisões associadas: D01, D03. Fontes de apoio: [R07].

## BP11 - Controlar duração, revogação e renovação do token OpenBao (P0)

Risco: Token continua utilizável além da necessidade ou aplicação perde acesso por renovação mal definida.

Prática recomendada: Definir TTL e máximo, testar expiração e revogação e documentar política de renovação do consumidor.

Como verificar: Ler com token válido, revogar e repetir; emitir token curto, aguardar expiração e repetir.

Evidência exigida: Resultados de revogação e expiração, sem valor de token.

Critério de atendimento: Token inválido é negado; estratégia de continuidade para aplicação real é definida antes da adoção.

Impacto possível: Autenticações adicionais e necessidade de tratar falhas sem laço infinito.

Situação na demonstração: Revogação e expiração do token OpenBao aprovadas na rodada real de 09/10/2026; TTL normal de 300 s e role experimental de 30 s. Renovação contínua não implementada.

Decisões associadas: D07. Fontes de apoio: [R02], [R03].

## BP12 - Manter credenciais administrativas fora dos workloads (P0)

Risco: Root token, unseal key ou chave privada vazam para aplicação, Git ou relatório.

Prática recomendada: Separar bootstrap de operação; aplicar acesso mínimo; não entregar root ao consumidor e não registrar segredos em logs.

Como verificar: Revisar manifests, arquivos e evidências; verificar quem acessa bootstrap e seu descarte.

Evidência exigida: Registro da revisão, permissões e processo de descarte, sem conteúdo sensível.

Critério de atendimento: Aplicação recebe somente sua identidade e token; material administrativo tem proprietário, finalidade e retenção definidos.

Impacto possível: Mais disciplina de operação e controle de acesso.

Situação na demonstração: .state é local, restrito e excluído do pacote; root retido apenas para laboratório, não adequado à operação real.

Decisões associadas: D08, D09. Fontes de apoio: [R02], [R06].

## BP13 - Delimitar a entrega de segredos à aplicação (P1)

Risco: Segredo é persistido, exposto ou copiado sem necessidade após leitura.

Prática recomendada: Escolher mecanismo de entrega compatível com o consumidor e controlar arquivo, memória, permissões e retenção.

Como verificar: Inspecionar consumo, saídas e armazenamento; verificar ausência de valor sensível em logs e artefatos.

Evidência exigida: Descrição do mecanismo e resultado de revisão de saídas.

Critério de atendimento: Mecanismo tem justificativa e destino controlado; valores não aparecem nas evidências publicadas.

Impacto possível: Agent/CSI ou backend específico podem introduzir componentes e manutenção adicionais.

Situação na demonstração: Cliente Python lê dado fictício sem imprimi-lo; Agent/CSI e Airflow não integrados.

Decisões associadas: D10. Fontes de apoio: [R02], [R06].

## BP14 - Registrar e revisar auditoria (P1)

Risco: Acesso indevido não deixa evidência útil ou logs acabam expondo metadados sensíveis.

Prática recomendada: Habilitar auditoria, restringir acesso, definir retenção e correlação de solicitações com teste/identidade.

Como verificar: Gerar leitura permitida e negação; conferir que ambas podem ser correlacionadas nos registros.

Evidência exigida: Registro resumido com resultado da correlação e política de retenção.

Critério de atendimento: Eventos relevantes são rastreáveis sem publicação de tokens ou segredos; contagem sozinha não encerra a análise.

Impacto possível: Armazenamento, processamento, revisão e custo de retenção.

Situação na demonstração: Auditoria declarativa: 91 linhas na rodada de 08/10 e 85 na instalação limpa de 09/10, conforme evidências da autora; correlação manual, completude e retenção pendentes.

Decisões associadas: D11, D12. Fontes de apoio: [R02].

## BP15 - Reduzir privilégios dos containers (P1)

Risco: Comprometimento da aplicação permite escalada ou alterações desnecessárias.

Prática recomendada: Executar sem root, sem escalada, com capacidades removidas, seccomp e escrita restrita ao necessário.

Como verificar: Revisar securityContext e admissão; verificar comportamento do workload com restrições.

Evidência exigida: Manifest e registro de execução sob perfil restrito.

Critério de atendimento: Aplicação opera com privilégios justificados; exceções são registradas com risco e revisão.

Impacto possível: Algumas imagens precisam de adaptação de permissões e caminhos de escrita.

Situação na demonstração: Restrições e Pod Security restricted configurados; workloads executaram na rodada real de 09/10/2026. Não houve teste de escape ou avaliação completa de endurecimento.

Decisões associadas: D08. Fontes de apoio: [R19].

## BP16 - Verificar imagens e dependências (P1)

Risco: Versão vulnerável ou imagem alterada compromete o controle aplicado.

Prática recomendada: Inventariar versões, fixar referência reproduzível e revisar vulnerabilidades conforme contexto.

Como verificar: Registrar digest e executar varredura; avaliar achados e correções com responsável.

Evidência exigida: Inventário, relatório de varredura e tratamento de achados.

Critério de atendimento: Dependências conhecidas e achados relevantes tratados ou explicitamente aceitos com justificativa e prazo.

Impacto possível: Atualização e correção recorrentes; possível incompatibilidade ao atualizar.

Situação na demonstração: Digest OpenBao observado no diagnóstico anterior e registrado na arquitetura; tags ainda usadas no script. Não houve verificação independente da cadeia de fornecimento nem varredura de vulnerabilidades.

Decisões associadas: D14. Fontes de apoio: [R19].

## BP17 - Proteger disponibilidade e recuperação (P1)

Risco: Reinício, perda de armazenamento ou falha de dependência interrompe acesso.

Prática recomendada: Definir persistência, recuperação, backup, unseal e disponibilidade de acordo com a criticidade.

Como verificar: Simular reinício e restauração em laboratório apropriado; medir recuperação.

Evidência exigida: Plano e resultado de teste de recuperação, sem chaves.

Critério de atendimento: Perda ou recuperação atende requisito definido; limitações são conhecidas antes da adoção.

Impacto possível: Redundância e backup consomem recursos e trabalho operacional.

Situação na demonstração: emptyDir é descartável; HA, backup e recuperação persistente fora do laboratório atual.

Decisões associadas: D09. Fontes de apoio: [R02], [R09].

## BP18 - Controlar recursos e abuso de solicitações (P1)

Risco: Carga ou falha de consumidor esgota recursos e degrada comunicação.

Prática recomendada: Definir limites, observabilidade e estratégia de tentativas; avaliar rate limiting no ponto adequado.

Como verificar: Observar consumo e executar carga controlada com autorização e limites conhecidos.

Evidência exigida: Registro de recursos, erros e resultado do ensaio controlado.

Critério de atendimento: Saturação é detectável e o comportamento em falha é conhecido; não inferir proteção DoS apenas de limits.

Impacto possível: Limites podem reduzir throughput; precisam de ajuste por demanda.

Situação na demonstração: Requests/limits definidos; carga e DoS não testados.

Decisões associadas: D04. Fontes de apoio: [R09].

## BP19 - Medir impacto sobre desempenho e operação (P1)

Risco: Decisões de segurança são julgadas só por percepção ou comparação desigual.

Prática recomendada: Comparar cenários equivalentes e separar latência, erros, consumo e esforço operacional.

Como verificar: Repetir mesma carga, versões e período; registrar p50/p95, erros, CPU/memória e ações de manutenção.

Evidência exigida: Tabela antes/depois com método, amostras e condições; não incluir resultados inventados.

Critério de atendimento: O impacto é descrito com dados e limites acordados; ganhos ou perdas não são presumidos.

Impacto possível: Coleta adicional e desenho de experimento; segurança pode custar recursos ou evitar retrabalho.

Situação na demonstração: Protocolo documentado; medições ainda não realizadas.

Decisões associadas: D12. Fontes de apoio: [R14].

## BP20 - Executar testes positivos e negativos (P0)

Risco: Controle parece correto no arquivo mas falha em operação ou bloqueia o acesso legítimo.

Prática recomendada: Associar cada item do checklist a teste e critério; confirmar serviço saudável antes de interpretar bloqueio.

Como verificar: Executar matriz e investigar falhas sem remover controles apenas para obter PASS.

Evidência exigida: Comando, data, ambiente, resultado e evidência revisada.

Critério de atendimento: Conclusão distingue configuração escrita, teste executado e resultado comprovado.

Impacto possível: Esforço de teste e manutenção da matriz após mudanças.

Situação na demonstração: 13 testes locais aprovados e 16 critérios da suíte Kubernetes aprovados na instalação limpa de 09/10/2026, conforme prints recebidos e conferidos.

Decisões associadas: D12. Fontes de apoio: [R07], [R15].

## BP21 - Tratar gaps, exceções e responsabilidades (P0)

Risco: Não conformidade é esquecida ou não aplicável é usado para esconder falha.

Prática recomendada: Atribuir responsável, ação, prazo, justificativa e revisão a cada pendência e exceção.

Como verificar: Revisar formulário de avaliação e verificar evidência/justificativa dos estados.

Evidência exigida: Formulário versionado e plano de ações.

Critério de atendimento: P0 sem evidência permanece pendente; exceção não equivale a teste aprovado nem elimina risco.

Impacto possível: Coordenação e acompanhamento; documentação passa a fazer parte da operação.

Situação na demonstração: Formulário e verificador documental incluídos; preenchimento é responsabilidade da revisão.

Decisões associadas: D08, D12. Fontes de apoio: [R05].

## BP22 - Reavaliar após mudanças e incidentes (P1)

Risco: Checklist fica desatualizado diante de novos endpoints, versões ou consumidores.

Prática recomendada: Definir gatilhos de revisão: mudança de CNI, identidade, CA, política, componente, exposição ou incidente.

Como verificar: Identificar mudança e repetir itens/testes afetados; revisar periodicidade conforme criticidade.

Evidência exigida: Histórico de revisão com alteração, testes repetidos e conclusões.

Critério de atendimento: Estado de conformidade tem data e contexto; mudança relevante invalida evidências afetadas até nova verificação.

Impacto possível: Manutenção contínua, proporcional ao risco.

Situação na demonstração: Gatilhos documentados; integração a CI/CD e acompanhamento contínuo não implementados.

Decisões associadas: D14. Fontes de apoio: [R05], [R12].

## BP23 - Distinguir dados e credenciais (P0)

Risco: Proteger categorias inadequadamente ou ignorar o poder de acesso de uma credencial.

Prática recomendada: Classificar dado pessoal, pessoal sensível, credencial e informação técnica; definir tratamento por risco e finalidade.

Como verificar: Revisar inventário de campos e executar simulação de exposição por log com marcadores fictícios.

Evidência exigida: Inventário classificado e resultado leak_demo, sem valores privados.

Critério de atendimento: Categorias e sobreposições são explícitas; credenciais e dados restritos não aparecem na saída operacional.

Impacto possível: Revisão de campos e manutenção da classificação.

Situação na demonstração: Demonstração local de log incluída; classificação do ambiente real pendente.

Decisões associadas: D11. Fontes de apoio: [R16], [R17], [R18].

## BP24 - Manter um titular geral e limitar administração (P0)

Risco: Dispersão de privilégios, conta compartilhada e acesso excessivo a dados e infraestrutura.

Prática recomendada: Um titular humano ativo de administração geral; identidades individuais e permissões por tarefa; revisar caminhos equivalentes de elevação.

Como verificar: Inventariar titulares e permissões globais, políticas wildcard, bind/escalate/impersonate, criação de workloads e acesso ao host; testar contas limitadas.

Evidência exigida: Inventário de concessões, responsável global, processo de substituição e testes de negação.

Critério de atendimento: Um único titular geral ativo; demais identidades sem privilégio global ou equivalente injustificado; revisão de substituição e recuperação documentada.

Impacto possível: Coordenação de concessões e risco de indisponibilidade do titular; acesso de recuperação precisa de controle.

Situação na demonstração: Regra documental proposta; verificações RBAC de reader/reviewer aprovadas em 09/10/2026. Unicidade de administrador e governança institucional não verificadas.

Decisões associadas: D08. Fontes de apoio: [R05], [R02].

## BP25 - Atualizar com teste, rastreabilidade e retorno (P1)

Risco: Correções ausentes ou atualização introduz regressão e permissões excessivas.

Prática recomendada: Inventário de versões, revisão de correções, ensaio controlado, plano de retorno e repetição de testes afetados.

Como verificar: Registrar mudança e repetir TLS, login, autorização, rede e tokens; conferir revisão de achados de vulnerabilidade.

Evidência exigida: Versões anterior/posterior, motivo, testes, decisão e pendências.

Critério de atendimento: Mudança tem responsável e evidências; falha não é contornada removendo proteção de modo permanente.

Impacto possível: Janela de manutenção e trabalho de compatibilidade/retorno.

Situação na demonstração: Configurações de armazenamento e auditoria corrigidas para OpenBao 2.7.1, com instalação limpa e suíte aprovadas. Migração entre versões, rollback e varredura de vulnerabilidades não ensaiados.

Decisões associadas: D14. Fontes de apoio: [R09], [R12].

## BP26 - Justificar o conjunto mínimo de ferramentas (P0)

Risco: Complexidade e privilégios adicionados sem benefício demonstrável.

Prática recomendada: Antes de adicionar ou manter um componente, registrar gap, alternativas, custo, responsável e condição de remoção.

Como verificar: Revisar D01-D14 e inventário de componentes; justificar também o que não foi incluído.

Evidência exigida: Registro de decisão e teste que responde ao risco.

Critério de atendimento: Cada componente tem necessidade explícita; simplificação não deixa requisito obrigatório sem tratamento.

Impacto possível: Pode adiar adoção e exige comparação de opções.

Situação na demonstração: Regra documental entregue; revisão humana do contexto permanece necessária.

Decisões associadas: D04, D10, D13. Fontes de apoio: [R10].

## BP27 - Manter responsabilidade humana pela verificação (P0)

Risco: IA ou ferramenta fornece conclusão incorreta e ela é aceita sem examinar o fluxo.

Prática recomendada: Revisar sugestões, fonte original, premissas, positivos/negativos e causa do resultado.

Como verificar: Examinar evidência bruta e distinguir teste local simulado de cluster real.

Evidência exigida: Registro de revisão humana, decisão e limitação.

Critério de atendimento: Conformidade não depende apenas de opinião da IA, PASS ou ausência de alerta.

Impacto possível: Tempo de revisão e necessidade de compreensão técnica.

Situação na demonstração: Regra documental entregue; revisão humana do contexto permanece necessária.

Decisões associadas: D12. Fontes de apoio: [R15].

## BP28 - Explicitar alternativas e efeitos de cada decisão (P0)

Risco: Escolha parece obrigatória e seus custos ou riscos ficam ocultos.

Prática recomendada: Registrar motivo, benefício esperado, efeito negativo, alternativa, fonte e condição de revisão.

Como verificar: Relacionar cada prática ao registro Dxx e conferir o limite da fonte usada.

Evidência exigida: Decisão rastreável, documentação original e evidência contextual.

Critério de atendimento: Fonte sustenta a afirmação feita; escolhas próprias são identificadas e podem ser reavaliadas.

Impacto possível: Mais documentação, reduzindo decisões difíceis de revisar.

Situação na demonstração: Regra documental entregue; revisão humana do contexto permanece necessária.

Decisões associadas: D01, D13, D14. Fontes de apoio: [R02], [R05].


## Nota da entrega A–B de 09/10/2026

Este catálogo registra critérios e decisões do modelo. Situações iniciais não são uma avaliação atual preenchida. Os resultados efetivamente informados estão em [Testes e resultados](poc/TESTES_E_RESULTADOS.md). Aprovação da suíte não torna automaticamente conformes as 28 práticas.
