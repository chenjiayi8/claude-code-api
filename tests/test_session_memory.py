#!/usr/bin/env python3
"""Test script to verify session ID and memory persistence fixes."""

import requests


def test_session_id_and_memory():
    """Test that session_id is returned and memory is persisted."""
    base_url = "http://localhost:8000"

    try:
        print("=" * 60)
        print("Test 1: Session ID with Standard Claude Model")
        print("=" * 60)

        # Test 1: Standard Claude model with session continuity
        print("\n1. First request - introducing name...")
        response1 = requests.post(
            f"{base_url}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "claude-3-5-haiku-20241022",
                "messages": [{"role": "user", "content": "My name is Alice"}],
            },
            timeout=30,
        )
    except requests.exceptions.ConnectionError:
        print(f"\n✗ FAIL: Could not connect to server at {base_url}")
        print("Please ensure the server is running and try again.")
        return
    except requests.exceptions.Timeout:
        print("\n✗ FAIL: Request timed out")
        print("The server is taking too long to respond.")
        return
    except Exception as e:
        print(f"\n✗ FAIL: Unexpected error: {str(e)}")
        return

    print(f"Status Code: {response1.status_code}")
    if response1.status_code == 200:
        data1 = response1.json()
        session_id = data1.get("session_id")
        print(f"✓ Session ID: {session_id}")
        print(f"Response: {data1['choices'][0]['message']['content'][:100]}...")

        if session_id:
            print("\n2. Second request - testing memory...")
            response2 = requests.post(
                f"{base_url}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "claude-3-5-haiku-20241022",
                    "messages": [{"role": "user", "content": "What is my name?"}],
                    "session_id": session_id,
                },
            )

            print(f"Status Code: {response2.status_code}")
            if response2.status_code == 200:
                data2 = response2.json()
                response_content = data2["choices"][0]["message"]["content"]
                print(f"Response: {response_content}")

                if "alice" in response_content.lower():
                    print("✓ PASS: Memory persisted - Claude remembered the name!")
                else:
                    print(
                        "✗ FAIL: Memory not persisted - Claude didn't remember the name"
                    )
            else:
                print(f"✗ FAIL: Second request failed: {response2.text}")
        else:
            print("✗ FAIL: Session ID not found in response")
    else:
        print(f"✗ FAIL: First request failed: {response1.text}")

    print("\n" + "=" * 60)
    print("Test 2: Session ID with Custom Model (glm-4.7)")
    print("=" * 60)

    # Test 2: Custom model with manual conversation history
    print("\n1. First request - setting favorite color...")
    response3 = requests.post(
        f"{base_url}/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "glm-4.7",
            "messages": [{"role": "user", "content": "My favorite color is blue"}],
        },
    )

    print(f"Status Code: {response3.status_code}")
    if response3.status_code == 200:
        data3 = response3.json()
        custom_session_id = data3.get("session_id")
        print(f"✓ Session ID: {custom_session_id}")
        print(f"Response: {data3['choices'][0]['message']['content'][:100]}...")

        if custom_session_id:
            print("\n2. Second request - testing memory with custom model...")
            response4 = requests.post(
                f"{base_url}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "glm-4.7",
                    "messages": [
                        {"role": "user", "content": "What is my favorite color?"}
                    ],
                    "session_id": custom_session_id,
                },
            )

            print(f"Status Code: {response4.status_code}")
            if response4.status_code == 200:
                data4 = response4.json()
                response_content = data4["choices"][0]["message"]["content"]
                print(f"Response: {response_content}")

                if "blue" in response_content.lower():
                    print(
                        "✓ PASS: Memory persisted for custom model - mentioned favorite color!"
                    )
                else:
                    print(
                        "✗ FAIL: Memory not persisted for custom model - didn't mention color"
                    )
            else:
                print(f"✗ FAIL: Second request failed: {response4.text}")
        else:
            print("✗ FAIL: Session ID not found in response")
    else:
        print(f"✗ FAIL: First request failed: {response3.text}")

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    test_session_id_and_memory()
