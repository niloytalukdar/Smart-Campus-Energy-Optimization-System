import pytest
from unittest.mock import patch, MagicMock
from app.services.llm_interpreter import interpret_notes, LLMParseError

@patch('app.services.llm_interpreter.openai.OpenAI')
def test_interpret_notes_valid(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_message = MagicMock(content='[{"directive_type": "no_charge_window", "hours": [14, 15], "factor": null}]')
    mock_response.choices = [MagicMock(message=mock_message)]
    mock_client.chat.completions.create.return_value = mock_response

    result = interpret_notes(["Do not charge between 2 PM and 4 PM"])
    assert len(result) == 1
    assert result[0]["directive_type"] == "no_charge_window"
    assert result[0]["hours"] == [14, 15]
    assert result[0].get("factor") is None

@patch('app.services.llm_interpreter.openai.OpenAI')
def test_interpret_notes_malformed(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_message = MagicMock(content='Not a JSON')
    mock_response.choices = [MagicMock(message=mock_message)]
    mock_client.chat.completions.create.return_value = mock_response

    with pytest.raises(LLMParseError):
        interpret_notes(["Some note"])

def test_interpret_notes_empty():
    # Should not call API
    result = interpret_notes([])
    assert result == []
