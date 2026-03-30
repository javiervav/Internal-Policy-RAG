import pytest
from app.domain.services.text_chunker import TextChunker

@pytest.fixture
def chunker():
    return TextChunker()

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
