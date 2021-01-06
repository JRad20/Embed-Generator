from flask import Flask, render_template, request, json
from dhooks import Webhook, Embed
import webview
import _thread
from ast import literal_eval


def send_hook(webhook,title,description,color,author):

    if len(color) == 0 and len(title) == 0 and len(author) == 0:
        hook = Webhook(webhook)
        hook.send(description)

    else:
        if len(title) == 0:
            title = None
        if len(description) == 0:
            description = None
        if len(color) == 0:
            color = 0x0d0d0d
        if len(author) == 0:
            author = None

        hook = Webhook(webhook)
        embed = Embed(title=title, description=description, color=literal_eval(color))
        embed.set_author(name=author)

        hook.send(embed=embed)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/post",methods=['POST'])
def post():
    data = request.json
    if len(data['webhook']) > 0:
        send_hook(data['webhook'],data['title'],data['desc'],data['color'],data['author'])

    return '200'


if __name__ == '__main__':
    _thread.start_new_thread(app.run, ())
    webview.create_window('Webhook Sender', 'http://127.0.0.1:5000/')
    webview.start()
