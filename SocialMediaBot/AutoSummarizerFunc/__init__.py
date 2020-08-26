import logging
import urllib
import azure.functions as func

from bs4 import BeautifulSoup
from transformers import pipeline

# set up nlp pipeline
nlp_summarizer = pipeline('summarization')

# function entry point
def main(req: func.HttpRequest) -> func.HttpResponse:

    # get the url
    url = req.params.get('url')
    if not url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            url = req_body.get('url')

    # log function start
    logging.info(f'Start AutoSummarizeFunc with url: {url}')
    summary = ''
    if url:

        # grab the web page
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, features='lxml')

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # get remaining text
        text = soup.get_text()

        # summarize text
        summary = nlp_summarizer(text, min_length=100, max_length=500)[0]['summary_text']

    # log function start
    logging.info(f'End AutoSummarizeFunc with summary: {summary}')

    # return result
    return func.HttpResponse(summary)
