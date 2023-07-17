import retailcrm 
import telebot
import requests

client = retailcrm.v5('https://cronmarket.retailcrm.ru','I2RpVdfUksGws7tEVwNLUZun6QZoYBkC')

def ordernumb(id):
    order = client.order(id, uid_type='id')
    order = order.get_response()['order']
    return order['number']

def sites(id):
    order = client.order(id, uid_type='id')
    order = order.get_response()['order']
    return order['site']

def notaccepted(id):
    order = client.order(id, uid_type='id')
    order = order.get_response()['order']
    site=order['site']
    orderedit={
        'statusComment':'Не принят',
        'customFields':{'priniat_ne_priniat_zakaz':'Не принят'},
        'id':id
            }
    result = client.order_edit(orderedit,'id',site).get_response()
    return order['site']
    
def orderstatus(id):
    order = client.order(id, uid_type='id')
    order = order.get_response()['order']
    return order['status']

def orderaccep(id):
    order = client.order(uid=id, uid_type='id').get_response()['order']
    site=order['site']
    orderedit={
        'status':'order-processing',
        'customFields':{'priniat_ne_priniat_zakaz':'Принят'},
        'id':id
            }
    result = client.order_edit(orderedit,'id',site).get_response()
    return order['site']


def yesorder(id):
    order = client.order(uid=id, uid_type='id').get_response()['order']
    site=order['site']
    orderedit={
        'status':'partially-completed',
        'id':id
            }
    result = client.order_edit(orderedit,'id',site).get_response()
    return order['site']

def noorder(id):
    order = client.order(uid=id, uid_type='id').get_response()['order']
    site=order['site']
    orderedit={
        'customFields':{'zakaz_ne_gotov':False},
        'id':id
            }
    result = client.order_edit(orderedit,'id',site).get_response()
    return order['site']

def ordersretail(id):
    order = client.order(id, uid_type='id')   
    order = order.get_response()['order']
    items = assign_order(id)
    name=""
    summ = order['totalSumm']
    if 'site' in order.keys():
        site = order['site'] 
    if 'lastName' in order.keys():
        name += order['lastName'] + " "
    if 'firstName' in order.keys():
        name += " " + order['firstName'] + " "
    if 'patronymic' in order.keys():
        name += " " + order['patronymic'] + " "
    if 'date' in order['delivery'].keys(): 
        adress = "Дата доставки: " + str(order['delivery']['date'])
    else: 
        adress = "Дата доставки не указана"
    if 'time' in order['delivery'].keys():
        vremia = " от %s до %s" % (order['delivery']['time']['from'], order['delivery']['time']['to'])
    else: 
        vremia = " Время доставки не указано"  
    if 'text' in order['delivery']['address'].keys():                   
        dom = order['delivery']['address']['text'] 
    else: 
        dom = " Адрес не указан"
    if 'phone' in order.keys():
        phone = order['phone']
    else:
        phone =" отсутствует"         
    if 'managerComment' in order.keys():
        managerComment = order['managerComment'] 
    else:
        managerComment = "отсутствует" 
    text="Информация о заказе" +"\nНомер заказа: " + str(order['number']) + "\nПартнер: " + str(site)+ "\nФИО: " + str(name)+ "\nАдрес: " +  str(dom) + "\nВремя доставки:"+ str(vremia)  +  "\nДата доставки:" + str(adress) +  "\nТелефон клиента: " + str(phone)+"\nСостав заказа: " + str(items) + "\nCумма за заказ: "+ str(summ)+"р." + "\nКомментарий к доставке: " + str(managerComment)
    return text 



def assign_order(order_id):
    answer = client.order(uid=order_id, uid_type='id')
    order = answer.get_response()['order']
    string = ""
    for it in order['items']:
        string += "%s : %s\n" % (it['offer']['displayName'], it['quantity'])
    return string