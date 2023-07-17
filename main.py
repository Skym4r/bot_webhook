from datetime import date
import telebot
from telebot import types
from retail import *
import flask
from flask import request
from telebot.types import CallbackQuery,InlineKeyboardButton
bot = telebot.TeleBot('токен_бота')
app = flask.Flask(__name__, static_folder='')
@bot.message_handler(commands=['start'])
def starter(message):   
    bot.send_message(message.chat.id,'Здравствуйте. Ожидайте карточки заказов.')
    print(message.chat.id)
    app.run(host="0.0.0.0", port=7772)
 
@app.route('/hook/', methods=['GET'])
def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''

        else:
            flask.abort(403) 
 
    
@app.route('/push', methods=['GET'])
def push():
    order_id = str(request.form['order_id'])
    status=orderstatus(order_id)
    site=sites(order_id)
    if (status!='order-processing'):
        retail=ordersretail(order_id)
        if site=='117-kafe':
            chat='-946163018'
        if site=='august':
            chat='-919918988'
        markup = telebot.types.InlineKeyboardMarkup()
        button1=InlineKeyboardButton(text='Принят', callback_data="accepted:"+str(order_id))
        button2=InlineKeyboardButton(text='Не принят', callback_data="not_accepted:"+str(order_id))
        markup.add(button1,button2)
        bot.send_message(chat, retail,reply_markup=markup)
    if (status=='order-processing'):
        if site=='117-kafe':
            chat='-942618951'
        if site=='august':
            chat='-908134335'
        number=ordernumb(order_id)
        text='Заказа №'+str(number)+' готов для отправки на доставку? '
        markup = telebot.types.InlineKeyboardMarkup()
        button1=InlineKeyboardButton(text='Готов', callback_data="yes:"+str(order_id))
        button2=InlineKeyboardButton(text='Не готов', callback_data="no:"+str(order_id))
        markup.add(button1,button2)
        bot.send_message(chat, text,reply_markup=markup)
        
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "accepted")
def accepted(call: CallbackQuery):
    order_id=call.data.split(':')[1]
    accepted=orderaccep(order_id)
    if(accepted):
        if accepted=='117-kafe':
            chat='-942618951'
        if accepted=='august':
            chat='-908134335'
        bot.send_message(chat, 'Информация передана в CRM систему')
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "not_accepted")
def accepted(call: CallbackQuery):
    order_id=call.data.split(':')[1]
    not_accepted=notaccepted(order_id) 
    if(not_accepted):
        if not_accepted=='117-kafe':
            chat='-942618951'
        if not_accepted=='august':
            chat='-908134335'
        bot.send_message(chat, 'Информация передана в CRM систему')
     
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "no")
def accepted(call: CallbackQuery):
    order_id=call.data.split(':')[1]
    order=noorder(order_id)
    if(order):
        if order=='117-kafe':
            chat='-942618951'
        if order=='august':
            chat='-908134335'
        bot.send_message(chat, 'Информация передана в CRM систему')

@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "yes")
def accepted(call: CallbackQuery):
    order_id=call.data.split(':')[1]
    order=yesorder(order_id)
    if(order):
        if order=='117-kafe':
            chat='-942618951'
        if order=='august':
            chat='-908134335'
        bot.send_message(chat, 'Информация передана в CRM систему')

 

bot.polling(non_stop=True)  
