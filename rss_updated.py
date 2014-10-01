import urllib.request

from flask import Flask, request
import lxml.etree


app = Flask(__name__)


@app.route('/<path:path>')
def atom(path):
    url = request.full_path[1:]
    response = urllib.request.urlopen(url)
    if response.headers.get_content_type() == 'application/atom+xml':
        feed = lxml.etree.parse(response)
        for entity in feed.xpath("//*[local-name()='entry']"):
            entity_id = entity.xpath("./*[local-name()='id']")[0]
            entity_updated = entity.xpath("./*[local-name()='updated']")[0]
            entity_id.text = entity_id.text + '#' + entity_updated.text
        body = lxml.etree.tostring(feed)
    else:
        body = response.read()
    return body, 200, response.headers.items()


if __name__ == '__main__':
    app.run()
