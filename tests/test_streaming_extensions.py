"""Tests for non-streaming response extensions."""

from claude_code_api.utils.streaming import create_non_streaming_response


def _create_response(messages):
    return create_non_streaming_response(
        messages=messages,
        session_id="session-test",
        model="claude-3-5-haiku-20241022",
        usage_summary={"total_tokens": 10, "total_cost": 0.001},
    )


def test_additive_tool_calls_are_preserved_with_assistant_text():
    response = _create_response(
        [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "Let me ask a quick question."},
                        {
                            "type": "tool_use",
                            "id": "toolu_ask_1",
                            "name": "AskUserQuestion",
                            "input": {"question": "What environment should I use?"},
                        },
                    ]
                },
            },
            {"type": "result"},
        ]
    )

    assert response["choices"][0]["message"]["content"] == "Let me ask a quick question."
    assert response["choices"][0]["finish_reason"] == "tool_calls"
    assert response["tool_calls"] == [
        {
            "id": "toolu_ask_1",
            "name": "AskUserQuestion",
            "input": {"question": "What environment should I use?"},
        }
    ]


def test_tool_only_output_does_not_inject_fake_greeting():
    response = _create_response(
        [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "toolu_ask_2",
                            "name": "AskUserQuestion",
                            "input": {"question": "Do you want me to continue?"},
                        }
                    ]
                },
            },
            {"type": "result"},
        ]
    )

    assert response["choices"][0]["message"]["content"] == ""
    assert response["choices"][0]["finish_reason"] == "tool_calls"
    assert response["tool_calls"] == [
        {
            "id": "toolu_ask_2",
            "name": "AskUserQuestion",
            "input": {"question": "Do you want me to continue?"},
        }
    ]


def test_text_only_output_has_empty_tool_calls():
    response = _create_response(
        [
            {
                "type": "assistant",
                "message": {
                    "content": [{"type": "text", "text": "Done. Here's the answer."}]
                },
            },
            {"type": "result"},
        ]
    )

    assert response["choices"][0]["message"]["content"] == "Done. Here's the answer."
    assert response["choices"][0]["finish_reason"] == "stop"
    assert response["tool_calls"] == []


def test_plain_string_assistant_content_has_empty_tool_calls():
    response = _create_response(
        [
            {
                "type": "assistant",
                "message": {"content": "A plain string response from assistant."},
            },
            {"type": "result"},
        ]
    )

    assert response["choices"][0]["message"]["content"] == "A plain string response from assistant."
    assert response["choices"][0]["finish_reason"] == "stop"
    assert response["tool_calls"] == []
