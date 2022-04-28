from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from time import perf_counter
import audio_transcribe
from credentials import *
import os

class AudioTranscribe:
	def __init__(self):
		self.updater = None

	def start_command(self, update: Update, context: CallbackContext):
		# update.message.reply_text("Select your audio file or say something on voice message...")
		keyboard = [
			[InlineKeyboardButton("🇮🇩 Indonesia", callback_data='id-ID')],
			[InlineKeyboardButton("🇸🇦 Arabic (SA)", callback_data='ar-SA')],
			[InlineKeyboardButton("🇺🇸 English (US)", callback_data='en-US')],
			[InlineKeyboardButton("🇲🇾 Malaysia", callback_data='ms-MY')],
			[InlineKeyboardButton("🇰🇷 Korean (SK)", callback_data='ko-KR')],
			[InlineKeyboardButton("🇩🇪 Germany", callback_data='de-DE')],
		]

		reply_markup = InlineKeyboardMarkup(keyboard)

		update.message.reply_text("Select the language of your audio file/voice message...", reply_markup=reply_markup)

	def setup_language(self, update: Update, context: CallbackContext):
		self.query = update.callback_query
		self.query.answer()
		languages = {
			'id-ID': 'Indonesia',
			'ar-SA': 'Saudi Arabia',
			'en-US': 'English \(US\)',
			'ms-MY': 'Malaysia',
			'ko-KR': 'South Korea',
			'de-DE': 'Germany'
		}

		self.query.edit_message_text(text=f'''*"{languages.get(self.query.data)}" language has selected\!*
Now, select your audio file or send your wonderful voice message :p''', parse_mode="MarkdownV2")

	def file_temp(self, update: Update, context: CallbackContext):
		file_uploaded = update.message.document
		# print("file_uploaded")

		fname = file_uploaded["file_name"].split('.')[0]
		fformat = file_uploaded["file_name"].split('.')[-1]

		context.bot.get_file(file_uploaded).download(file_uploaded["file_name"])
		start = perf_counter()
		update.message.reply_text('Wait for a sec...')
		text = audio_transcribe.transcribe(file_uploaded["file_name"], self.query.data)
		end = perf_counter()

		update.message.reply_text(text)
		transcribe_length = end - start
		update.message.reply_text(f'lang: {self.query.data}')
		update.message.reply_text(f'time: {transcribe_length}')
		update.message.reply_text(f'Finished! :D')

		os.remove(file_uploaded["file_name"])
		os.remove(file_translated)

	def audio_temp(self, update: Update, context: CallbackContext):
		voice_recorded = update.message.voice
		audio_temp_file_name = f"audio_temp.{voice_recorded['mime_type'].split('/')[-1]}"
		context.bot.get_file(voice_recorded).download(audio_temp_file_name)
		# update.message.reply_text(f'{voice_recorded}')

		start = perf_counter()
		# wait_msg = update.message.reply_text('Wait for a sec...')
		# wait_msg
		update.message.reply_text('Wait for a sec...')
		text = audio_transcribe.transcribe(audio_temp_file_name, self.query.data)
		end = perf_counter()

		# context.bot.delete
		update.message.reply_text(text)
		transcribe_length = end - start
		update.message.reply_text(f'time: {transcribe_length}\nstatus: finished!')

		os.remove(audio_temp_file_name)
		
	def tutorial_command(self, update: Update, context: CallbackContext):
		update.message.reply_text("""\[cmd\] tutorial

1\. Press /start button, then select your audio file or voice message do you want to transcribe
2\. Wait the result
3\. Get your transcribe :D
			""", parse_mode="MarkdownV2")			

	def author_command(self, update: Update, context: CallbackContext):
		update.message.reply_text("""\[cmd\] author

If you facing an error, report and provide the screenshots to:
\- Twitter: [DensenBrad](https://twitter.com/DensenBrad)
\- Telegram: [DensenBrad](https://t.me/DensenBrad)
			""", parse_mode="MarkdownV2")

	def help_command(self, update: Update, context: CallbackContext):
		update.message.reply_text("""[cmd] help
/start transcribe your audio file
/about show the bot information
/author show the author information
			""")

def main():
	audioTranscribe = AudioTranscribe()
	audioTranscribe.updater = Updater(API_KEY_BOT)

	dp = audioTranscribe.updater.dispatcher
	dp.add_handler(CommandHandler('start', audioTranscribe.start_command))
	dp.add_handler(CommandHandler('help', audioTranscribe.help_command))
	dp.add_handler(CommandHandler('tutorial', audioTranscribe.tutorial_command))
	dp.add_handler(CommandHandler('author', audioTranscribe.author_command))

	dp.add_handler(CallbackQueryHandler(audioTranscribe.setup_language))

	dp.add_handler(MessageHandler(Filters.voice, audioTranscribe.audio_temp))
	dp.add_handler(MessageHandler(Filters.document, audioTranscribe.file_temp))
	
	audioTranscribe.updater.start_polling()
	audioTranscribe.updater.idle()

if __name__ == '__main__':
	main()