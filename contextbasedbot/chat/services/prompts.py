def build_rephrase_prompt(current_question, previous_question=None):
    return f"""You are a helpful assistant. 
    -Your job is to rewrite unclear or follow-up questions into complete, standalone questions.
    -If the current question refers to something previously mentioned (like "what about that?"), use the previous question to infer the missing context.

    Previous Question: {previous_question or 'None'}

    Current Question: {current_question}

    Rephrased Standalone Question:"""


def build_prompt(current_question, context):
    return f"""You are a helpful assistant. Use the provided context to answer the user's question as best as possible. If the answer is not explicitly stated but can be reasonably inferred, do so and clearly indicate it's an assumption.

Keep your answer concise (5-6 lines).

- If the context clearly lacks the information, respond with: "The document doesn't provide this information."
- If the question asks what the document is about, provide a short summary using only the context.
- Avoid markdown and line breaks like '\\n'.

Context: {context}

Current User Question: {current_question}

Answer: """

