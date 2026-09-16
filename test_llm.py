from generation.llm import generate_answer

answer = generate_answer(
    "What is cybersecurity? Explain in one simple sentence."
)

print("\nLLM Response:")
print(answer)