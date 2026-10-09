# Modelo geral de boas práticas

**Período de desenvolvimento: setembro a outubro de 2026.** O trabalho compreende pesquisa, definição do recorte, decisões de arquitetura, implementação e revisão. As datas específicas de execução são registradas nas evidências.

## 1. Problema e pergunta

Uma aplicação pode alcançar um serviço em outro cluster e ainda assim usar identidade errada, permissões excessivas ou credenciais duradouras. A pergunta desta proposta é: como permitir a comunicação necessária, restringir o alcance de um comprometimento e produzir evidências de que os controles funcionam?

O objeto é a comunicação entre clusters Kubernetes. A POC escolhe um fluxo concreto: uma aplicação em A busca um segredo fictício no OpenBao em B. Não cobre todos os serviços ou protocolos de uma organização.

## 2. Origem do modelo

Este é um modelo próprio de avaliação, fundamentado na documentação de Kubernetes e OpenBao e contextualizado pelo projeto público GovHub. Não é uma norma oficial, um framework publicado por MGI/Ipea ou cópia do modelo de segurança do OpenBao. A referência GovHub oferece um caso de pipelines e integrações; a distribuição em A/B é uma proposta experimental deste trabalho. As fontes estão em [FONTES](../FONTES.md).

O uso de assistência de IA na elaboração não transfere responsabilidade: a autora e os revisores devem conferir código, fontes, resultados e adequação ao ambiente. O modelo exato de IA não é registrado como evidência técnica do laboratório; não há base para atribuir a ele validação independente.

## 3. Fundamentos

**Confidencialidade:** limitar quem lê dados. **Integridade:** restringir alterações e autenticar endpoints. **Disponibilidade:** manter o serviço utilizável e prever falhas. TLS protege o transporte, mas um cliente autenticado pode receber um segredo e vazá-lo depois.

Autenticação responde quem apresenta uma identidade. Autorização decide quais ações essa identidade pode realizar. A identidade da ServiceAccount de A é avaliada pela autoridade Kubernetes de A; o token emitido pelo OpenBao recebe uma política de acesso. RBAC Kubernetes e ACL OpenBao são controles diferentes.

Segmentação limita caminhos de rede; não identifica sozinha o usuário da aplicação. A política de rede depende do CNI e do caminho efetivo do pacote. NAT pode mudar o endereço observado. Por isso, aplicar YAML não comprova isolamento.

Privilégio mínimo reduz operações e dados acessíveis. Credenciais temporárias limitam a janela de abuso, mas um token válido roubado continua utilizável até expirar ou ser revogado. Defesa em profundidade combina controles para riscos distintos; quantidade de ferramentas não é medida de segurança.

Segurança não é necessariamente o oposto de eficiência. Alguns controles adicionam latência e esforço operacional; padronização e automação podem reduzir erros e retrabalho. Esta POC não mediu desempenho nem demonstra ganho ou perda quantitativa.

## 4. Classificação dos ativos

| Classe | Exemplo | Tratamento proposto |
|---|---|---|
| Dado pessoal | Nome, CPF ou identificador associado a pessoa natural | Finalidade, acesso necessário e retenção definida |
| Dado pessoal sensível | Saúde, biometria vinculada à pessoa, opinião política | Controles proporcionais e enquadramento conforme art. 5º, II, da LGPD |
| Credencial | Senha, JWT, token OpenBao, chave privada, kubeconfig com material de autenticação | Acesso mínimo, expiração ou rotação, revogação e exclusão de repositórios/logs |
| Informação técnica confidencial | Endereços internos, configurações e metadados de auditoria | Publicação revisada e acesso conforme necessidade |
| Dado sintético | Mensagens fictícias da POC | Uso exclusivo nos testes e identificação explícita |

Uma senha não é automaticamente dado pessoal sensível na classificação legal. Pode ser informação de segurança crítica e também estar associada a uma pessoa. Um CPF é dado pessoal, mas não integra automaticamente a categoria legal de dados sensíveis. As categorias técnicas e legais não são equivalentes [R16].

## 5. Método de aplicação

1. Inventariar origem, destino, porta, protocolo, finalidade, identidade, ativo e responsável.
2. Identificar ameaças e impacto: interceptação, identidade indevida, permissões excessivas, token vazado e interrupção.
3. Escolher controles proporcionais, registrando alternativa, benefício, custo e risco residual.
4. Implementar em laboratório isolado com dados fictícios.
5. Executar teste positivo e negativo, preservar evidências e avaliar falsos positivos.
6. Revisar resultados com pessoa responsável, registrar pendências e repetir após mudanças.

A unidade de avaliação é a prática com evidência, não a ferramenta instalada. Usar o [checklist de 28 práticas](../01-checklist-modelo.md) e o [registro de decisões](../02-registro-decisoes.md). Cada item exige responsável, data, evidência e justificativa. O formulário pode ser criado por `python3 scripts/checklist.py init` e analisado por `python3 scripts/checklist.py report`. Ele verifica preenchimento, não descobre controles nem certifica segurança.

## 6. Governança e administração

A proposta da autora é um único titular humano de administração geral ativa, com conta individual, evitando contas compartilhadas e distribuição rotineira de privilégios globais. Demais pessoas e workloads recebem apenas o necessário. Essa é uma decisão de governança deste trabalho, não exigência das fontes.

A concentração reduz a quantidade de acessos globais, mas cria dependência e risco de indisponibilidade. A adoção deve prever substituição formal, acesso emergencial rastreável e revisão independente; não depender de senha compartilhada. MFA, revisão periódica de acessos e processo de desligamento são requisitos a avaliar no ambiente real. Nenhum deles foi comprovado pela suíte desta POC.

O root token mantido no estado local é uma simplificação do bootstrap e dos testes. Não é identidade de aplicação nem demonstra gestão de administradores em produção. Não publicá-lo. Separar responsabilidades de operação, aprovação e revisão das evidências.

## 7. Atualizações e ciclo de vida

Antes de atualizar: inventariar versões e imagens, ler release notes, verificar compatibilidade entre cliente/API/CNI, avaliar mudanças de configuração e preparar recuperação. Aplicar em ambiente de teste, repetir testes positivos e negativos e comparar resultados. Registrar versão anterior, nova versão, motivo, responsável e evidência. Tags facilitam o laboratório, mas digests e integridade dos manifests devem ser controlados em uma adoção real.

A remoção do backend `file` e a mudança para auditoria declarativa no OpenBao 2.7 ilustram por que copiar configuração antiga é insuficiente. Atualização de software não equivale a atualização validada do sistema. Certificados, JWTs e tokens também expiram; sua renovação é parte da operação.

## 8. Resposta a vazamento

Conter o acesso afetado, revogar a credencial comprometida, identificar escopo e período, analisar registros preservados, corrigir a origem e emitir nova credencial quando necessário. Rotacionar também o segredo de destino se seu valor foi exposto: revogar o token do OpenBao não apaga um segredo já lido nem invalida automaticamente a senha de outro sistema.

Repetir os testes após a correção e documentar o risco residual. Não publicar material comprometido como evidência. Na POC todos os valores são fictícios e o cenário de vazamento é controlado.

## 9. Critério de aceite e limites

A demonstração técnica exige comunicação autorizada funcionando, recusas esperadas, evidências datadas e interpretação correta. O modelo completo exige avaliação das 28 práticas, pendências e responsáveis. Uma adoção produtiva demanda ainda persistência, recuperação, disponibilidade, operação de certificados, resposta a incidentes e testes no caminho real da rede.

O aceite documental não transforma resultados limitados em garantia geral. Serviço indisponível também pode causar timeout: combinar teste autorizado funcional, baseline e teste negativo reduz essa ambiguidade, mas ainda é necessário verificar onde o bloqueio ocorreu.
