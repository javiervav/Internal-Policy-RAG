import pytest

from app.infrastructure.manual_text_chunker import ManualTextChunker


@pytest.fixture
def chunker():
    return ManualTextChunker()


def test_chunk_text_should_return_correct_chunks(chunker):
    text = """
        Title
        
        1. First section
        Content A
        
        2. Second section
        
        Content B
    """

    result = chunker.chunk(text)

    assert result == [
        "Title",
        "1. First section\nContent A",
        "2. Second section\nContent B",
    ]
