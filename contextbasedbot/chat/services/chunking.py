def read_and_chunk_text(text, chunk_size=300, overlap=50):
    text = text.replace("\n", " ")
    sentences = text.split(". ")
    chunks = []
    chunk = []
    length = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence.endswith("."):
            sentence += "."
        if length + len(sentence) > chunk_size and chunk:
            chunks.append(" ".join(chunk))
            overlap_words = overlap // max(1, len(sentence.split()))
            chunk = chunk[-overlap_words:] + [sentence]
            length = sum(len(s) for s in chunk)
        else:
            chunk.append(sentence)
            length += len(sentence)

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks
