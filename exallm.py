from exa_py import Exa
from dotenv import load_dotenv
import os

load_dotenv()

EXA_API_TOKEN = os.getenv("EXA_API_TOKEN")

exa = Exa(api_key = EXA_API_TOKEN)

def web_search(text="https://www.amazon.com/b?node=17938598011"):
    """
    Uses Exa to search the web for information on a given topic.

    Args:
        None
    """

    result = exa.search_and_contents(
    f"Search the web to determine if the following information is true:\n\n {text}\n\n. KEEP OUTPUT WITHIN 4096 CHARACTERS.",
    summary=True,
    num_results=3
    )
    summaries = [res.summary for res in result.results]
    return summaries

# thing = web_search()
# print(thing, type(thing), type(thing[0]))
