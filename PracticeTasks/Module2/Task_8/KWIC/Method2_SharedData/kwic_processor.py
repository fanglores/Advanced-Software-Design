def find_keyword_context(text, keyword):
    # Finds and saves the context of a keyword
    lines = text.split('. ')
    context = []
    for line in lines:
        if keyword in line:
            position = line.find(keyword)
            context.append((line, position))
    return context