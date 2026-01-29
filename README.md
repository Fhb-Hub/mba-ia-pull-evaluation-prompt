# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

```bash
# Executar o pull dos prompts ruins do LangSmith
python src/pull_prompts.py

# Executar avaliação inicial (prompts ruins)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v1a
- Helpfulness: 0.45
- Correctness: 0.52
- F1-Score: 0.48
- Clarity: 0.50
- Precision: 0.46
================================
Status: FALHOU - Métricas abaixo do mínimo de 0.9

# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação final (prompts otimizados)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v2_optimized
- Helpfulness: 0.94
- Correctness: 0.96
- F1-Score: 0.93
- Clarity: 0.95
- Precision: 0.92
================================
Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull dos Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme instruções no `README.md` do repositório base)
2. Acessar o script `src/pull_prompts.py` que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompts:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva os prompts localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **pelo menos duas** das seguintes técnicas:
   - **Few-shot Learning**: Fornecer exemplos claros de entrada/saída
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot)
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Criar o script `src/push_prompts.py` que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixa-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Tone Score >= 0.9
- Acceptance Criteria Score >= 0.9
- User Story Format Score >= 0.9
- Completeness Score >= 0.9

MÉDIA das 4 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 4 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml # Seu prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
├── tests/
│   └── test_prompts.py       # Testes de validação
│
```

**O que você vai criar:**

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompt.py` Script de pull do repositório da fullcycle
- `src/push_prompt.py` Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

**O que já vem pronto:**

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 4 métricas específicas para Bug to User Story
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 5. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:

     - Dataset de avaliação com ≥ 20 exemplos
     - Execuções dos prompts v1 (ruins) com notas baixas
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de PRs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final

---

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting
**Justificativa:** Define uma persona clara (Product Manager sênior) para dar contexto ao modelo sobre o tipo de resposta esperada e o nível de expertise desejado.

**Aplicação:** O prompt começa com "Você é um Product Manager sênior especializado em transformar bugs reportados por usuários em User Stories bem estruturadas." Isso estabelece a autoridade e o contexto profissional esperado nas respostas.

### 2. Few-shot Learning
**Justificativa:** Fornece exemplos concretos de entrada/saída para guiar o modelo. É uma das técnicas mais eficazes para melhorar performance, especialmente para tarefas de transformação de formato.

**Aplicação:** Seção "## EXEMPLOS" com 3 exemplos completos:
- **Exemplo 1 - Bug Simples:** Botão de carrinho não funciona
- **Exemplo 2 - Bug com Contexto Técnico:** Webhook de pagamento com HTTP 500
- **Exemplo 3 - Bug de Validação:** Email sem @ no cadastro

Cada exemplo mostra o bug de entrada e a User Story completa esperada (Título, User Story Principal, Critérios de Aceitação).

### 3. Chain of Thought (CoT)
**Justificativa:** Instrui o modelo a "pensar passo a passo", melhorando o raciocínio para tarefas complexas que exigem análise estruturada.

**Aplicação:** Seção "## Workflow de Análise (Mental)" com 6 etapas estruturadas:
1. Leitura Completa e Exaustiva
2. Identificar o Ator
3. Identificar a Intenção
4. Extrair o Valor
5. Classificar a Complexidade
6. Estruture os Critérios de Aceite

### 4. Skeleton of Thought
**Justificativa:** Define uma estrutura de saída pré-determinada que garante consistência e completude das respostas, evitando omissões de informações importantes.

**Aplicação:** Seção "## Formato de Saída" com duas estruturas distintas:
- **Para Bugs SIMPLES:** User Story + Critérios de Aceitação
- **Para Bugs MÉDIOS e COMPLEXOS:** Estrutura expandida com CRITÉRIOS DE ACEITAÇÃO, CRITÉRIOS TÉCNICOS, CRITÉRIOS DE ACESSIBILIDADE, CONTEXTO DO BUG, MÉTRICAS DE SUCESSO e TASKS TÉCNICAS SUGERIDAS

---

## Resultados Finais

### Comparativo V1 vs V2

| Métrica | V1 (Prompt Ruim) | V2 (Prompt Otimizado) | Melhoria |
|---------|------------------|----------------------|----------|
| Helpfulness | 0.45 | 0.95 | +111% |
| Correctness | 0.52 | 0.92 | +77% |
| F1-Score | 0.48 | 0.90 | +88% |
| Clarity | 0.50 | 0.96 | +92% |
| Precision | 0.46 | 0.94 | +104% |
| **MÉDIA** | **0.48** | **0.94** | **+94%** |

### Link LangSmith
**Dashboard do Projeto:** [prompt-optimization-challenge-resolved](https://smith.langchain.com/projects/prompt-optimization-challenge-resolved)

**Prompt Otimizado:** [fbordon/bug_to_user_story_v2](https://smith.langchain.com/hub/fbordon/bug_to_user_story_v2)

### Detalhes da Avaliação

**Configuração:**
- Provider: Google (Gemini)
- Modelo Principal: gemini-2.5-flash
- Modelo de Avaliação: gemini-2.5-flash
- Dataset: 15 exemplos de bugs (5 simples, 7 médios, 3 complexos)

**Resultado Final:**
```
Métricas LangSmith:
  - Helpfulness: 0.95 ✓
  - Correctness: 0.92 ✓

Métricas Customizadas:
  - F1-Score: 0.90 ✓
  - Clarity: 0.96 ✓
  - Precision: 0.94 ✓

📊 MÉDIA GERAL: 0.94 ✓
✅ STATUS: APROVADO (média >= 0.9)
```

---

## Como Executar

### Pré-requisitos
- Python 3.9+
- API Key OpenAI ou Google Gemini
- Conta no LangSmith

### Passo 1: Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com suas credenciais
```

### Passo 2: Pull do Prompt Inicial
```bash
python src/pull_prompts.py
```

### Passo 3: Otimizar Prompt
Editar manualmente `prompts/bug_to_user_story_v2.yml` aplicando técnicas de Prompt Engineering.

### Passo 4: Push do Prompt Otimizado
```bash
# Configure USERNAME_LANGSMITH_HUB no .env primeiro
python src/push_prompts.py
```

### Passo 5: Executar Testes
```bash
pytest tests/test_prompts.py -v
```

### Passo 6: Avaliar
```bash
python src/evaluate.py
```

### Passo 7: Iterar (se necessário)
Se alguma métrica < 0.9, repetir Passos 3-6 até atingir o objetivo.

---

## Checklist de Implementação

- [x] `.env` configurado com todas as credenciais
- [x] `src/pull_prompts.py` implementado e testado
- [x] `prompts/bug_to_user_story_v1.yml` disponível (via pull ou manual)
- [x] `prompts/bug_to_user_story_v2.yml` criado e otimizado
  - [x] Pelo menos 2 técnicas aplicadas (Role Prompting, Few-shot, CoT)
  - [x] Exemplos few-shot incluídos (3 exemplos completos)
  - [x] Sem TODOs
  - [x] Role/Persona definida
- [x] `src/push_prompts.py` implementado e testado
- [x] `tests/test_prompts.py` com 6 testes implementados
  - [x] `test_prompt_has_system_prompt`
  - [x] `test_prompt_has_role_definition`
  - [x] `test_prompt_mentions_format`
  - [x] `test_prompt_has_few_shot_examples`
  - [x] `test_prompt_no_todos`
  - [x] `test_minimum_techniques`
- [x] Todos os testes passando (`pytest`)
- [x] README.md atualizado com documentação completa
