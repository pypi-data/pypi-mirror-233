"""

We don't want any automatic procedures reliant on external apis, as this is a security risk

"""


from ..rag import get_relevant_procedures


def get_relevant_procedures_function(messages):
    return ""


get_relevant_procedures.get_relevant_procedures = get_relevant_procedures_function
