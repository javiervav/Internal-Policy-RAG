import asyncio
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from app.di.container import Container

load_dotenv()

JUDGE_MODEL = "gpt-4o-mini"


async def main():
    with open("eval/test_cases.json") as f:
        test_cases = json.load(f)

    container = Container()
    await container.load_initial_data_use_case.execute()

    client = AsyncOpenAI()
    results = []

    for case in test_cases:
        question = case["question"]
        expected = case["expected"]
        actual = await container.ask_question_use_case.execute(question)
        if not actual:
            score = 1
            reason = "No answer returned."
        else:
            score, reason = await _judge_answer(client, question, expected, actual)
        results.append({
            "question": question,
            "expected": expected,
            "actual": actual,
            "score": score,
            "reason": reason,
        })

    print("\n=== RAG Evaluation Results ===\n")
    for r in results:
        label = {1: "FAIL", 2: "PARTIAL", 3: "PASS"}[r["score"]]
        print(f"[{label}] {r['question']}")
        print(f"  Expected : {r['expected']}")
        print(f"  Actual   : {r['actual']}")
        print(f"  Reason   : {r['reason']}")
        print()

    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"Average score: {avg_score:.1f}/3.0 ({len(results)} questions)")


async def _judge_answer(client: AsyncOpenAI, question: str, expected: str, actual: str) -> tuple[int, str]:
    prompt = f"""You are evaluating the output of a RAG system.

        Question: {question}
        Expected answer: {expected}
        Actual answer: {actual}

        Score the actual answer against the expected answer:
        1 - Incorrect or missing key information
        2 - Partially correct
        3 - Correct and complete

        Respond only with JSON: {{"score": <1|2|3>, "reason": "<brief reason>"}}
"""

    response = await client.responses.create(
        model=JUDGE_MODEL,
        input=prompt,
        max_output_tokens=100,
    )
    text = response.output_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    result = json.loads(text)
    return result["score"], result["reason"]


if __name__ == "__main__":
    asyncio.run(main())
