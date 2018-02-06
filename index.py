from flask import Flask, request, abort
from dotenv import load_dotenv, find_dotenv
from wit import Wit
import os
import musixmatchAPI as lirik_api

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
	MessageEvent,
	TextMessage,
	TextSendMessage,
	ButtonsTemplate,
	TemplateSendMessage,
	PostbackTemplateAction,
	MessageTemplateAction,
	URITemplateAction,
	ImageCarouselTemplate,
	ImageCarouselColumn
)

app = Flask(__name__)
load_dotenv(find_dotenv())

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

##WITAI BOT##
client = Wit(os.environ.get('WIT_ACCESS_TOKEN'))

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: {}'.format(body))

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route('/hello', methods=['GET'])
def hello():
	return "Hello World"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	if (event.message.text == '/help'):
		reply_message = TemplateSendMessage(
			alt_text='Message not supported',
			template=ButtonsTemplate(
				title='Helper',
				text='',
				actions=[
				MessageTemplateAction(
					label='Cari lirik lagu',
					text='/help0'
				),
				MessageTemplateAction(
					label='Cari lirik berdasarkan judul',
					text='/help1'
				),
				MessageTemplateAction(
					label='Cari lirik berdasarkan artis',
					text='/help2'
				),
				MessageTemplateAction(
					label='Cari lirik berdasarkan penggalan lirik',
					text='/help3'
				),
				URITemplateAction(
					label='Go to website',
					uri='http://example.com/'
				)
			]
		)
	)
	elif (event.message.text == '/help0'):
		reply_message = TextSendMessage(text='Ketik /lirik (judul lagu atau artis berkaitan)')
	elif (event.message.text == '/help1'):
		reply_message = TextSendMessage(text='Ketik /lirik (judul lagu)')
	elif (event.message.text == '/help2'):
		reply_message = TextSendMessage(text='Ketik /lirik (nama artis)')
	elif (event.message.text == '/help3'):
		reply_message = TextSendMessage(text='Ketik /lirik (penggalan lirik)')


	##### FITUR LIRIK ######

	elif (event.message.text == '/lirik' or event.message.text == '/lyrics'):
		reply_message = TemplateSendMessage(
			alt_text='Pilih kata kategori kata kunci untuk memilih lirik yang kamu ingin cari',
			template=ImageCarouselTemplate(
			columns=[
				ImageCarouselColumn(
					image_url='https://via.placeholder.com/800x800', action=MessageTemplateAction(
						label='Judul-Artist',
						text='/judul+artist',
					)
				),
				ImageCarouselColumn(
				image_url='https://via.placeholder.com/800x800', action=MessageTemplateAction(
					label='Judul Lagu',
					text='/judul',
					)
				),
				ImageCarouselColumn(
				image_url='https://via.placeholder.com/800x800', action=MessageTemplateAction(
					label='Artist',
					text='/artist',
					)
				),
				ImageCarouselColumn(
				image_url='https://via.placeholder.com/800x800', action=MessageTemplateAction(
					label='Sublyrics',
					text='/sublyrics',
					)
				)
			]
		)
	)
	elif (event.message.text == '/judul+artist'):
		reply_message = TextSendMessage(text='Silahkan masukkan judul lagu dan artist yang liriknya ingin kamu cari dengan format: "1-judul-artist"')
	elif (event.message.text[0] == '1'):
		reply_message = TextSendMessage(text=lirik_api.getLyricsWithTrackArtist(event.message.text.split("-")[1], event.message.text.split("-")[2]))
	elif (event.message.text == '/buy product2'):
		reply_message = TextSendMessage(text='Product 2 added')
	else:
		reply_message = TextSendMessage(text='Ketik /help untuk bantuan')

	line_bot_api.reply_message(
	event.reply_token,
	reply_message
)

if __name__ == "__main__":
	app.run()

