import telegram.constants
from telegram.ext import (ContextTypes)
from telegram import Update
import openai


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if len(prompt) == 0:
        await update.message.reply_text(f'No argument found!\n\n'
                                        f'Usage : \n\n'
                                        f'/image <prompt>\n\n'
                                        f'for example : /image A dog overlooking a lake')
        return
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.constants.ChatAction.TYPING)
    message = await update.effective_chat.send_message(text='Please wait, image is being generated...')
    try:
        response = openai.Image.create(
            prompt=update.message.text,
            n=1,
            size="1024x1024"
        )
    except openai.error.InvalidRequestError:
        await message.delete()
        await update.effective_chat.send_message(text='Oops! could not make this request due '
                                                      'to restricted words in the prompt! Enter a new prompt or /cancel')
        return

    image_url = response['data'][0]['url']
    await message.delete()
    await update.message.reply_photo(photo=image_url)
    return


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if len(prompt) == 0:
        await update.message.reply_text(f'No argument found!\n\n'
                                        f'Usage : \n\n'
                                        f'/text <prompt>\n\n'
                                        f'for example : /text What is a decorator in Python?')
        return
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.constants.ChatAction.TYPING)
    message = await update.effective_message.reply_text(text='Please wait while I respond..')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": ""},
            {"role": "assistant",
             "content": ""},
            {"role": "user", "content": update.effective_message.text}
        ]
    )
    response_text = response['choices'][0]['message']['content']
    await message.delete()
    await update.message.reply_text(response_text)


async def instructions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(text=f'Hello! my name is {context.bot.name}! '
                                                   f'I was created for a Python workshop by MCC!\n'
                                                   f'My commands :\n\n'
                                                   f'/image <prompt>\n'
                                                   f'/text <promp>')
