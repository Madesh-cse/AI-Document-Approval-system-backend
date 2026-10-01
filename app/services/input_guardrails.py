def validate_question(question: str) -> tuple[bool, str | None]:
    if not question or not question.strip():
        return False, "Question cannot be empty."

    question = question.strip()

    if len(question) < 3:
        return False, "Question is too short."

    if len(question) > 500:
        return False, "Question cannot exceed 500 characters."

    return True, None