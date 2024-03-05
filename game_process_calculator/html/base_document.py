from phtml import *

def start_base_document():
    base_document = Document()
    base_document.add_body_element(
        Header(1, "Game Process Calculator"),
    )
    return base_document
