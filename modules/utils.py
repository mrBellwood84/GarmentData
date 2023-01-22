def normalize(input: str, corrections: list[list[str]]) -> str:

    for corr in corrections:
        input = input.replace(corr[0], corr[1])

    return input.upper()

