import re


class TextChunker:

    @staticmethod
    # Divide text into chunks based on section headers (e.g., "1. ", "2. ", etc.)
    def chunk(text: str) -> list[str]:
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        chunks = []

        if lines:
            chunks.append(lines[0])
            lines = lines[1:]

        section_pattern = re.compile(r"^\d+\.\s")
        current_chunk = ""

        for line in lines:
            if section_pattern.match(line):
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line
            else:
                current_chunk += "\n" + line

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
