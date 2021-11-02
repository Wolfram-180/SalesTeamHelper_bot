"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
from aiogram import executor
import aiogram.utils.markdown as md
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from middlewares import AccessMiddleware
import myutils
import datetime
import dbwork
import emailwork

logging.basicConfig(level=logging.INFO)

API_TOKEN = ''  # @imagerfrobot

PROXY_URL = '' # os.getenv("TELEGRAM_PROXY_URL")
PROXY_AUTH = ''
#    = aiohttp.BasicAuth(
#    login=os.getenv("TELEGRAM_PROXY_LOGIN"),
#    password=os.getenv("TELEGRAM_PROXY_PASSWORD")
#)

storage = MemoryStorage()

bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot, storage=storage)

restrict_access = False

if restrict_access:
    ACCESS_ID = '229793913' # os.getenv("TELEGRAM_ACCESS_ID")
    dp.middleware.setup(AccessMiddleware(ACCESS_ID))

cmnd_start = 'start'
cmnd_cancel = 'cancel'
mess_tostart = 'Отправьте /{} для перехода в главное меню'.format(cmnd_start)
mess_exit = 'Отправьте /{} для выхода из процесса ввода'.format(cmnd_cancel)
mess_imwaiting = '\n\n -->> Жду фото подтайки. Отправь фотку!'
mess_start = 'Привет, я бот компании "" для борьбы с подтайкой, проблемами выкладки и т.п. \n\n' \
             'Ваш действия:\n - начать заполнять отчет,\n - выбрать Сеть или Розничную точку,\n - указать адрес точки,\n - сообщить о проблемах,\n - закрыть отчет. \n\n {} \n '.format(mess_tostart)
mess_calltoaction = 'Выберите действие из вариантов ниже. \n'
mess_reportopened = 'Выберите Сеть или Розничную точку \n'
mess_openreport = 'Начать заполнять отчет'
mess_closereport = 'Закрыть отчет'
mess_location = 'Выбрать Сеть или Розничную точку'
mess_havebruk = 'Наличие брака и подтайки в торговой точке'
mess_fckncncr = 'В фирменном холодильнике выложена продукция конкурентов'
mess_emptyholo = 'Пустой фирменный холодильник'
mess_nocennik = 'На мороженом нет ценника'


class Message():
    city   = ''
    street = ''
    bldng  = ''
    subject = ''
    text    = ''
    distrib = ''
    files   = []
    send_to = []

    def __init__(self):
        pass


class LocationProcessStates(StatesGroup):
    start  = State()
    distrib = State()
    city   = State()
    street = State()
    bldng  = State()
    #phone = State()


class BrukProcessStates(StatesGroup):
    photo = State()
    sku  = State()
    skokashtuk = State()
    comment = State()


class CncrProcessStates(StatesGroup):
    photo = State()
    fillperc  = State()


class EmptyholoProcessStates(StatesGroup):
    photo = State()
    skokasetok  = State()
    comment = State()


class CennikiProcessStates(StatesGroup):
    photo = State()
    skuinsell = State()
    skubezcen  = State()
    comment = State()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    logging.info('Отмена состояния %r', current_state)
    #closereport(message)
    if current_state is not None:
        await state.finish()
    await message.reply('Ввод данных сброшен, отчет НЕ ЗАКРЫТ. ' + mess_tostart, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=[cmnd_start])
async def start(message: types.Message):
    id, report_timestamp, phone = dbwork.NumReportInProcess(message.chat.id)
    distributor_id = dbwork.GetDistribByRepId(myutils.safe_cast(id, int, 0))
    # если отчет в процессе и дистриб\локация указаны
    if id != 0 and distributor_id != 0:
        opened_report_info = await openedreportinfo(message.chat.id)
        location_info, distrid, distrname, city, street, bldng = dbwork.format_openedreportlocation(message.chat.id)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row(KeyboardButton(mess_havebruk))
        markup.row(KeyboardButton(mess_fckncncr))
        markup.row(KeyboardButton(mess_emptyholo))
        markup.row(KeyboardButton(mess_nocennik))
        markup.row(KeyboardButton(mess_closereport))
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(mess_start),
                md.text('Ваш Telegram ID: {} \n'.format(message.chat.id)),
                #md.text('Ваш контактный номер: {} '.format(phone)),
                md.text(opened_report_info),
                md.text(location_info),
                md.text(mess_calltoaction),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    # если отчет в процессе и дистриб\локация НЕ указаны
    elif id != 0 and distributor_id == 0:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row(KeyboardButton(mess_location))
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(mess_reportopened),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        # если отчет НЕ в процессе и дистриб\локация НЕ указаны
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row(KeyboardButton(mess_openreport))
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(mess_start),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )


async def openedreportinfo(chat_id):
    return dbwork.format_openedreportinfo(chat_id)


async def locationinfo(chat_id):
    return dbwork.format_openedreportlocation(chat_id)


@dp.message_handler(text=[mess_openreport])
async def openreport(message: types.Message):
    dbwork.OpenReportInProcess(message.chat.id)
    await message.reply(await openedreportinfo(message.chat.id), reply_markup=types.ReplyKeyboardRemove())
    await start(message)


@dp.message_handler(text=[mess_closereport])
async def closereport(message: types.Message):
    id, report_timestamp, phone = dbwork.NumReportInProcess(message.chat.id)
    if myutils.safe_cast(id, int, 0) > 0:
        dbwork.CloseReportInProcess(id)
        await message.reply('Отчет {} от {} закрыт \n\n'.format(id, report_timestamp), reply_markup=types.ReplyKeyboardRemove())
        await start(message)
    #else:
    #    await message.reply('Нет открытого отчета', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text=[mess_location])
async def set_location(message: types.Message):
    await LocationProcessStates.start.set()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    distrs = dbwork.GetAllDistrs()
    for row in distrs._rows:
        markup.row(KeyboardButton(row['name']))
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Пожалуйста выберите Сеть или "Розничная точка" если это розничный магазин'),
            #md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )
    await LocationProcessStates.next()  #  -> distrib


@dp.message_handler(state=LocationProcessStates.distrib)
async def process_LocationProcessStates_distrib(message: types.Message, state: FSMContext):
    txt = message.text
    distrid = dbwork.getdistridbyname(txt)
    async with state.proxy() as data:
        data['distrib'] = txt
        data['distr_id'] = distrid
    #await message.answer('Пожалуйста введите город \n\n' + mess_exit)
    await message.answer('Пожалуйста введите город \n\n', reply_markup=types.ReplyKeyboardRemove())
    await LocationProcessStates.next()  #  -> city


@dp.message_handler(state=LocationProcessStates.city)
async def process_LocationProcessStates_city(message: types.Message, state: FSMContext):
    txt = message.text
    async with state.proxy() as data:
        data['city'] = txt
    await message.answer('Пожалуйста введите улицу \n\n')
    await LocationProcessStates.next()  #  -> street


@dp.message_handler(state=LocationProcessStates.street)
async def process_LocationProcessStates_street(message: types.Message, state: FSMContext):
    txt = message.text
    async with state.proxy() as data:
        data['street'] = txt
    await message.answer('Пожалуйста введите номер дома \n\n')
    await LocationProcessStates.next()  #  -> bldng


@dp.message_handler(state=LocationProcessStates.bldng)
async def process_LocationProcessStates_bldng(message: types.Message, state: FSMContext):
    txt = message.text
    try:
        async with state.proxy() as data:
            data['bldng'] = txt
            c = dbwork.getconnect()
            id, numrep, phone = dbwork.NumReportInProcess(message.chat.id)
            dbwork.upd(c, 'reports', id, city=data['city'], street=data['street'],  bldng=data['bldng'],
                       distr_name=data['distrib'], distributor_id=data['distr_id'])
        await state.finish()
        await message.answer('Информация сохранена')
        await start(message)
    except Exception as exc:
        print("process_LocationProcessStates_bldng.finish: {} \n {} \n {} \n".format(type(exc), exc.args, exc))


@dp.message_handler(Text(equals=mess_havebruk, ignore_case=True), state='*')
async def BrukProcessStates_start(message: types.Message):
    await BrukProcessStates.photo.set()
    await message.answer('Заполняем часть отчета: {} \n'.format(mess_havebruk))
    await message.answer('Пожалуйста сделайте фото проблемы и отправьте мне \n', reply_markup=types.ReplyKeyboardRemove())  # -> BrukProcessStates.photo


@dp.message_handler(content_types=['photo'], state=BrukProcessStates.photo)
async def BrukProcessStates_photo(message: types.Message, state: FSMContext):
    await types.ChatActions.upload_photo()
    file = message.photo[-1].file_id
    async with state.proxy() as data:
        data['file'] = file
    await message.answer('Спасибо, фото получено \n\n')
    await message.answer('Пожалуйста введите текстом - по каким наименованиям мороженого  есть проблемы? \n')
    await BrukProcessStates.photo.set()
    await BrukProcessStates.next()  #  -> sku


@dp.message_handler(state=BrukProcessStates.sku)
async def process_BrukProcessStates_sku(message: types.Message, state: FSMContext):
    txt = message.text
    async with state.proxy() as data:
        data['sku'] = txt
    await message.answer('Пожалуйста напишите цифрами или текстом - сколько проблемных наименований мороженого ? \n')
    await BrukProcessStates.next()  #  -> skokashtuk


@dp.message_handler(state=BrukProcessStates.skokashtuk)
async def process_BrukProcessStates_skokashtuk(message: types.Message, state: FSMContext):
    txt = message.text
    async with state.proxy() as data:
        data['skokashtuk'] = txt
    await message.answer('Если еще что-то другое - добавьте дополнительное описание \n')
    await BrukProcessStates.next()  #  -> comment


@dp.message_handler(state=BrukProcessStates.comment)
async def process_BrukProcessStates_comment(message: types.Message, state: FSMContext):
    txt = message.text
    try:
        async with state.proxy() as data:
            data['comment'] = txt
            id, report_timestamp, phone = dbwork.NumReportInProcess(message.chat.id)
            repnum = '№ {} от {}'.format(id, report_timestamp)
            replocation, distrid, distrname, city, street, bldng = dbwork.format_openedreportlocation(message.chat.id)
            subj = 'Часть отчета: {} -> брак/подтайка; {}'.format(repnum, replocation)
            text = '{} \n\n SKU: {} \n\n Сколько штук: {} \n\n Дополнительное описание: {} \n\n {}'.format(subj, data['sku'], data['skokashtuk'], data['comment'], replocation)
            c = dbwork.getconnect()
            dbwork.ins(c, 'reports_parts', False, '', '', id_reports=id, text=text)
            mess = Message()
            mess.send_to = []
            mess.subject = subj
            mess.text = text
            mess.files = []
            mess.files.append(data['file'])
            send_to = dbwork.getmails(distrid, city, street, bldng)
            await types.ChatActions.upload_photo()
            await emailwork.send_mail_from_aiogram(bot, API_TOKEN, send_to, mess.subject, mess.text, mess.files)
            await state.finish()
            await message.answer('Спасибо!')
            await message.answer(subj)
            await message.answer('Со вложенным фото')
            await message.answer('Успешно отправлена на e-mail ответственному \n')
            await start(message)
    except Exception as exc:
        print("BrukProcessStates.finish: {} \n {} \n {} \n".format(type(exc), exc.args, exc))

# BrukProcessStates AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


# CncrProcessStates VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
#photo = State()
#fillperc = State()

@dp.message_handler(Text(equals=mess_fckncncr, ignore_case=True), state='*')
async def CncrProcessStates_start(message: types.Message):
    await CncrProcessStates.photo.set()
    await message.answer('Заполняем часть отчета: {} \n'.format(mess_fckncncr))
    await message.answer('Пожалуйста сделайте фото проблемы и отправьте мне \n', reply_markup=types.ReplyKeyboardRemove())  # -> photo


@dp.message_handler(content_types=['photo'], state=CncrProcessStates.photo)
async def CncrProcessStates_photo(message: types.Message, state: FSMContext):
    await types.ChatActions.upload_photo()
    file = message.photo[-1].file_id
    async with state.proxy() as data:
        data['file'] = file
    await message.answer('Спасибо, фото получено \n\n')
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton('на 100%'))
    markup.row(KeyboardButton('на 75%'))
    markup.row(KeyboardButton('на 50%'))
    markup.row(KeyboardButton('на 25%'))
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Пожалуйста выберите вариант или введите текстом - сколько процентов холодильника  заполнено продукцией конкурентов? \n'),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )
    await CncrProcessStates.photo.set()
    await CncrProcessStates.next()


@dp.message_handler(state=CncrProcessStates.fillperc)
async def CncrProcessStates_fillperc(message: types.Message, state: FSMContext):
    txt = message.text
    try:
        async with state.proxy() as data:
            data['perc'] = txt
            id, report_timestamp, phone = dbwork.NumReportInProcess(message.chat.id)
            repnum = '№ {} от {}'.format(id, report_timestamp)
            replocation, distrid, distrname, city, street, bldng = dbwork.format_openedreportlocation(message.chat.id)
            subj = 'Часть отчета: {} -> продукт конкурентов в холодильнике ; {}'.format(repnum, replocation)
            text = '{} \n\n Заполнение: {} \n\n {}'.format(subj, data['perc'], replocation)
            c = dbwork.getconnect()
            dbwork.ins(c, 'reports_parts', False, '', '', id_reports=id, text=text)
            mess = Message()
            mess.send_to = []
            mess.subject = subj
            mess.text = text
            mess.files = []
            mess.files.append(data['file'])
            send_to = dbwork.getmails(distrid, city, street, bldng)
            await types.ChatActions.upload_photo()
            await emailwork.send_mail_from_aiogram(bot, API_TOKEN, send_to, mess.subject, mess.text, mess.files)
            await state.finish()
            await message.answer('Спасибо!')
            await message.answer(subj)
            await message.answer('Со вложенным фото')
            await message.answer('Успешно отправлена на e-mail ответственному \n')
            await start(message)
    except Exception as exc:
        print("CncrProcessStates_fillperc.finish: {} \n {} \n {} \n".format(type(exc), exc.args, exc))

# CncrProcessStates AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


# EmptyholoProcessStates VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
#photo = State()
#skokasetok = State()
#comment = State()

@dp.message_handler(Text(equals=mess_emptyholo, ignore_case=True), state='*')
async def EmptyholoProcessStates_start(message: types.Message):
    await EmptyholoProcessStates.photo.set()
    await message.answer('Заполняем часть отчета: {} \n'.format(mess_emptyholo))
    await message.answer('Пожалуйста сделайте фото проблемы и отправьте мне \n', reply_markup=types.ReplyKeyboardRemove())  # -> photo


@dp.message_handler(content_types=['photo'], state=EmptyholoProcessStates.photo)
async def EmptyholoProcessStates_photo(message: types.Message, state: FSMContext):
    await types.ChatActions.upload_photo()
    file = message.photo[-1].file_id
    async with state.proxy() as data:
        data['file'] = file
    await message.answer('Спасибо, фото получено \n\n')
    await message.answer('Пожалуйста введите текстом или цифрами - сколько сеток у холодильника? \n')
    await EmptyholoProcessStates.photo.set()
    await EmptyholoProcessStates.next()


@dp.message_handler(state=EmptyholoProcessStates.skokasetok)
async def EmptyholoProcessStates_skokasetok(message: types.Message, state: FSMContext):
    txt = message.text
    async with state.proxy() as data:
        data['skokasetok'] = txt
    await message.answer('Если еще что-то другое - добавьте дополнительное описание \n')
    await EmptyholoProcessStates.next()  #  -> comment


@dp.message_handler(state=EmptyholoProcessStates.comment)
async def EmptyholoProcessStates_comment(message: types.Message, state: FSMContext):
    txt = message.text
    try:
        async with state.proxy() as data:
            data['comment'] = txt
            id, report_timestamp, phone = dbwork.NumReportInProcess(message.chat.id)
            repnum = '№ {} от {}'.format(id, report_timestamp)
            replocation, distrid, distrname, city, street, bldng = dbwork.format_openedreportlocation(message.chat.id)
            subj = 'Часть отчета: {} -> пустой фирменный холодильник ; {}'.format(repnum, replocation)
            text = '{} \n\n Сеток в холодильнике: {} \n\n Дополнительное описание: {} \n\n {}'.format(subj, data['skokasetok'], data['comment'], replocation)
            c = dbwork.getconnect()
            dbwork.ins(c, 'reports_parts', False, '', '', id_reports=id, text=text)
            mess = Message()
            mess.send_to = []
            mess.subject = subj
            mess.text = text
            mess.files = []
            mess.files.append(data['file'])
            send_to = dbwork.getmails(distrid, city, street, bldng)
            await types.ChatActions.upload_photo()
            await emailwork.send_mail_from_aiogram(bot, API_TOKEN, send_to, mess.subject, mess.text, mess.files)
            await state.finish()
            await message.answer('Спасибо!')
            await message.answer(subj)
            await message.answer('Со вложенным фото')
            await message.answer('Успешно отправлена на e-mail ответственному \n')
            await start(message)
    except Exception as exc:
        print("EmptyholoProcessStates.finish: {} \n {} \n {} \n".format(type(exc), exc.args, exc))

# EmptyholoProcessStates AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


# CennikiProcessStates VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
# photo = State()
# skuinsell = State()
# skubezcen  = State()
# comment = State()

@dp.message_handler(Text(equals=mess_nocennik, ignore_case=True), state='*')
async def CennikiProcessStates_start(message: types.Message):
    await CennikiProcessStates.photo.set()
    await message.answer('Заполняем часть отчета: {} \n'.format(mess_nocennik))
    await message.answer('Пожалуйста сделайте фото проблемы и отправьте мне \n', reply_markup=types.ReplyKeyboardRemove())  # -> photo


@dp.message_handler(content_types=['photo'], state=CennikiProcessStates.photo)
async def CennikiProcessStates_photo(message: types.Message, state: FSMContext):
    await types.ChatActions.upload_photo()
    file = message.photo[-1].file_id
    async with state.proxy() as data:
        data['file'] = file
    await message.answer('Спасибо, фото получено \n\n')
    await message.answer('Пожалуйста введите текстом или цифрами - сколько наименований мороженого  в продаже? \n')
    await CennikiProcessStates.photo.set()
    await CennikiProcessStates.next()


@dp.message_handler(state=CennikiProcessStates.skuinsell)
async def CennikiProcessStates_skuinsell(message: types.Message, state: FSMContext):
    txt = message.text
    async with state.proxy() as data:
        data['skuinsell'] = txt
    await message.answer('На какие наименования мороженого  нет ценников? \n')
    await CennikiProcessStates.next()  #  -> skubezcen


@dp.message_handler(state=CennikiProcessStates.skubezcen)
async def CennikiProcessStates_skubezcen(message: types.Message, state: FSMContext):
    txt = message.text
    async with state.proxy() as data:
        data['skubezcen'] = txt
    await message.answer('Если еще что-то другое - добавьте дополнительное описание \n')
    await CennikiProcessStates.next()  #  -> comment


@dp.message_handler(state=CennikiProcessStates.comment)
async def CennikiProcessStates_comment(message: types.Message, state: FSMContext):
    txt = message.text
    try:
        async with state.proxy() as data:
            data['comment'] = txt
            id, report_timestamp, phone = dbwork.NumReportInProcess(message.chat.id)
            repnum = '№ {} от {}'.format(id, report_timestamp)
            replocation, distrid, distrname, city, street, bldng = dbwork.format_openedreportlocation(message.chat.id)
            subj = 'Часть отчета: {} -> наличие ценников на каждое наименование мороженого ; {}'.format(repnum, replocation)
            text = '{} \n\n Наименование мороженого  в продаже: {} \n\n Нет ценников: {} \n\n Дополнительное описание: {} \n\n {}'.format(subj, data['skuinsell'], data['skubezcen'], data['comment'], replocation)
            c = dbwork.getconnect()
            dbwork.ins(c, 'reports_parts', False, '', '', id_reports=id, text=text)
            mess = Message()
            mess.send_to = []
            mess.subject = subj
            mess.text = text
            mess.files = []
            mess.files.append(data['file'])
            send_to = dbwork.getmails(distrid, city, street, bldng)
            await types.ChatActions.upload_photo()
            await emailwork.send_mail_from_aiogram(bot, API_TOKEN, send_to, mess.subject, mess.text, mess.files)
            await state.finish()
            await message.answer('Спасибо!')
            await message.answer(subj)
            await message.answer('Со вложенным фото')
            await message.answer('Успешно отправлена на e-mail ответственному \n')
            await start(message)
    except Exception as exc:
        print("CennikiProcessStates_comment.finish: {} \n {} \n {} \n".format(type(exc), exc.args, exc))

# EmptyholoProcessStates AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
