import re

def clean_text(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def split_sentences(text):
    text = text.replace("\n", " ")

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def split_long_sentence(sentence, max_words):
    words = sentence.split()

    return [" ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)]

def get_overlap(sentences, overlap_words):
    overlap = []
    word_count = 0

    for sentence in reversed(sentences):
        sentence_words = len(sentence.split())

        if word_count + sentence_words > overlap_words:
            break

        overlap.insert(0, sentence)
        word_count += sentence_words

    return overlap


def create_chunks(pages,file_name,max_words=300,overlap_words=50):
    chunks = []

    for page in pages:
        page_number = page["page_number"]

        text = clean_text(
            page["text"]
        )

        if not text:
            continue

        sentences = split_sentences(text)

        units = []

        for sentence in sentences:
            word_count = len(
                sentence.split()
            )

            if word_count <= max_words:
                units.append(sentence)
            else:
                units.extend(
                    split_long_sentence(
                        sentence,
                        max_words
                    )
                )

        current_chunk = []
        current_words = 0

        for sentence in units:
            sentence_words = len(
                sentence.split()
            )

            if (current_chunk and current_words + sentence_words > max_words):
                chunk_text = " ".join(
                    current_chunk
                )

                chunks.append({
                    "text": chunk_text,
                    "file_name": file_name,
                    "page_number": page_number
                })

                current_chunk = get_overlap(
                    current_chunk,
                    overlap_words
                )

                current_words = sum(
                    len(item.split())
                    for item in current_chunk
                )

                while (
                    current_chunk
                    and current_words + sentence_words > max_words
                ):
                    removed = current_chunk.pop(0)

                    current_words -= len(
                        removed.split()
                    )

            current_chunk.append(
                sentence
            )

            current_words += sentence_words

        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "file_name": file_name,
                "page_number": page_number
            })

    return chunks