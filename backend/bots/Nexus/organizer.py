from .answer import *
from .prompt import *

def nexus_chat(current_question, context):
    question = generate_nexus_prompt(current_question)
    sit = f"{question}\n Context: {context}"
    return answer_query(sit)