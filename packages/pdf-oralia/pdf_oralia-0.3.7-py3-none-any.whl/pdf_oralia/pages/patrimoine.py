def is_it(page_text):
    if "VOTRE PATRIMOINE" in page_text:
        return True
    return False
