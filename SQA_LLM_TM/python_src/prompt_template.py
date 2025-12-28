from langchain_core.prompts import PromptTemplate
def prompt_temp():
   return  PromptTemplate.from_template(
            """You are an expert educator creating exam questions.

    Context:
    {context}

    Task: Generate exactly {num_questions} two-mark questions with answers from the context above.

    Requirements:
    - Each answer must be EXACTLY {words_per_answer} words
    - Format each Q&A as:
    Q1. [Question]
    Answer: [Exactly {words_per_answer} words answer]
    
    Q2. [Question]
    Answer: [Exactly {words_per_answer} words answer]

    Generate the questions and answers now:"""
        )