"""Measure the RAM of the local embedding container while it embeds a batch of questions.

Usage: python -m eval.embedding_memory
"""

import csv
import subprocess
import threading
import time
from datetime import date
from pathlib import Path

from assistant.settings import load_settings
from eval.run import load_questions

OUTPUT = Path(__file__).resolve().parents[1] / "results" / "embedding_memory.csv"
CONTAINER = "mdcc-norms-assistant-ollama-1"


def memory_mib(container: str = CONTAINER) -> float:
    usage = subprocess.run(
        ["docker", "stats", "--no-stream", "--format", "{{.MemUsage}}", container],
        check=True, capture_output=True, text=True,
    ).stdout.split("/")[0].strip()
    number, unit = float(usage[:-3]), usage[-3:]
    return number * {"KiB": 1 / 1024, "MiB": 1, "GiB": 1024}[unit]


def main() -> None:
    from langchain_ollama import OllamaEmbeddings

    settings = load_settings()
    embeddings = OllamaEmbeddings(model=settings.embed_model, base_url=settings.embed_url)
    questions = [q["question"] for q in load_questions()] * 5
    idle = memory_mib()
    samples: list[float] = []
    done = threading.Event()

    def sample() -> None:
        while not done.is_set():
            samples.append(memory_mib())

    sampler = threading.Thread(target=sample)
    sampler.start()
    started = time.perf_counter()
    embeddings.embed_documents(questions)
    elapsed_ms = (time.perf_counter() - started) * 1000 / len(questions)
    done.set()
    sampler.join()
    with OUTPUT.open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["model", "idle_mib", "peak_mib", "ms_per_question", "measured_on"])
        writer.writerow([settings.embed_model, round(idle), round(max(samples + [idle])), round(elapsed_ms, 1), date.today()])
    print(OUTPUT.read_text())


if __name__ == "__main__":
    main()
