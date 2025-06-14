from transformers import pipeline


summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_text(text: str) -> str:
    summary = summarizer_pipeline(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]["summary_text"]  # type: ignore