def build_rephrase_prompt(current_question, previous_question=None):
    return f"""You are a helpful assistant. 
    -Your job is to rewrite unclear or follow-up questions into complete, standalone questions.
    -If the current question refers to something previously mentioned (like "what about that?"), use the previous question to infer the missing context.

    Previous Question: {previous_question or 'None'}

    Current Question: {current_question}

    Rephrased Standalone Question:"""


def build_prompt(current_question, context):
    return f"""You are a helpful assistant. Use only the provided context to answer the user's question.
               Keep your answer concise (5-6 lines).

        - If the context does not include enough information to answer, respond with: 
            "I can't answer this according to the provided document."
        - If the question asks for a summary or uses words like "about", summarize using only the context.

        Do not use markdown or line breaks like '\\n' or '\\n\\n.

        Context: {context}

        Current User Question: {current_question}

        Answer: """
