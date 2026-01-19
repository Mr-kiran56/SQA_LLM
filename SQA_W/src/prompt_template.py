
from langchain_core.prompts import PromptTemplate

def prompt_temp():
    return PromptTemplate(
        input_variables=["context", "num_questions", "words_per_answer","user_context"],
        template="""
You are an academic question paper generator.

RULES (VERY IMPORTANT):
- Use ONLY the information from the context
- Take USER PREFERENCE context based on that genarate means how they want to generate answers
- DO NOT use outside knowledge
- DO NOT repeat topics
- Answers must be EXACTLY {words_per_answer} words
- Generate EXACTLY {num_questions} questions

CONTEXT:
{context}

USER PREFERENCE:
{user_context}


FORMAT:
Q1. Question text
Answer: Answer text

Q2. Question text
Answer: Answer text
"""
    )
