from event_manager import *

def read_text(text):
    evManager.fire(IEvents.TEXT_READ_EVENT, text)

def split_into_words(text):
    words = text.split()
    return [(text, word) for word in words]

def create_context(text_with_word):
    text, keyword = text_with_word
    words = text.split()
    context_index = words.index(keyword)
    left = " ".join(words[:context_index])
    right = " ".join(words[context_index + 1:])
    context = f"{left:<20} |{keyword}| {right:<20}"
    evManager.fire(IEvents.CONTEXT_READY_EVENT, [left, keyword, right])

def collect_and_sort(context):
    contexts.append(context)
    # Wait all parts to be created
    if len(contexts) == context_size:
        contexts.sort(key=lambda x: x[1].strip().split()[0])
        evManager.fire(IEvents.DISPLAY_CONTEXT_EVENT, contexts)

def display_sorted_contexts(contexts):
    print("\nResult:")
    for context in contexts:
        print(f"{context[0]:<20} | {context[1]:<10} | {context[2]:<20}")

evManager = EventManager()

evManager.subscribe(IEvents.TEXT_READ_EVENT, lambda text: [create_context(pair) for pair in split_into_words(text)])
evManager.subscribe(IEvents.CONTEXT_READY_EVENT, collect_and_sort)
evManager.subscribe(IEvents.DISPLAY_CONTEXT_EVENT, display_sorted_contexts)

contexts = []
text_input = input("Input: ")
context_size = len(text_input.split())
evManager.fire(IEvents.TEXT_READ_EVENT, text_input)
