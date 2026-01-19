from langchain_core.prompts import PromptTemplate

def prompt_temp():
    return PromptTemplate(
        input_variables=[
            "context",
            "num_questions",
            "words_per_answer",
            "user_context"
        ],
        template="""
You are an expert academic question–answer generator.

PRIMARY GOAL:
Generate high-quality, DISTINCT academic questions and answers STRICTLY from the provided document context.

MANDATORY PLANNING STEP (DO NOT SKIP):
1. First, analyze the document context.
2. Identify ALL distinct concepts, sections, or ideas present.
3. Internally create a list of UNIQUE topics.
4. Generate ONE question per topic.
5. If topics are fewer than required questions, subdivide topics logically WITHOUT repetition.

INTENT UNDERSTANDING:
- Infer the user's intention from USER PREFERENCE.
- Adapt language, depth, tone, and format accordingly.
- If unclear, use neutral academic style.

ANTI-REPETITION RULES (VERY STRICT):
- EACH question MUST be semantically different.
- NO two questions may test the same concept.
- NO paraphrased or reworded duplicates.
- If a generated question is similar to a previous one, DISCARD it and generate a new one.

ANSWER RULES:
- Each answer MUST contain EXACTLY {words_per_answer} words.
- Answers must be grounded ONLY in the document context.
- Do NOT reuse sentence structures across answers.

DOCUMENT CONTEXT:
{context}

USER PREFERENCE:
{user_context}

FINAL OUTPUT RULES:
- Generate EXACTLY {num_questions} questions.
- Ensure ALL questions are unique in topic and intent.
- Output ONLY the final questions and answers.
- DO NOT explain your reasoning.

OUTPUT FORMAT (STRICT):

Q1. <Unique Question>
Answer: <Answer>

Q2. <Unique Question>
Answer: <Answer>

...
"""
    )
