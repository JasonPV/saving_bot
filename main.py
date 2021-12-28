from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from cnf import token
import methods
import pickle
import cv2
import pydub


TOKEN = token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
try:
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
except:
    data = {'id_i': 0, 'id_a': 0}


methods.create_db()
path_audios = 'audios/audio_message_'
path_images = 'images/image_message_'


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Здравствуйте, отправляйте свои медиафайлы. Буду сохранять только те картинки, на которых есть лица.\nА аудиосообщения буду сохранять в формате wav с частатой 16kHz')


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    type = 'photo'
    path = path_images + str(data['id_i']) + '.jpeg'

    file_info = await bot.get_file(msg.photo[-1].file_id)
    photo = (await bot.download_file(file_info.file_path)).read()
    faces, img = methods.find_faces(photo)
    if faces > 0:
        data['id_i'] += 1
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)
        cv2.imwrite(path, img)
        methods.add_in_db(user_id, chat_id, type, path)
        await bot.send_message(msg.chat.id, f"На данной картинке есть лица: {faces}\nПоэтому это изображение сохранено")
    else:
        await bot.send_message(msg.chat.id, "На данной картинке нет лиц, поэтому она не сохранена")


@dp.message_handler(content_types=['audio'])
async def get_text_messages(msg: types.Message):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    type = 'audio'
    path = path_audios + str(data['id_a']) + '.wav'
    data['id_a'] += 1
    # print(msg.as_json())
    file_info = await bot.get_file(msg.audio.file_id)
    audio = await bot.download_file(file_info.file_path)
    audio = pydub.AudioSegment.from_file(audio)
    audio = audio.set_frame_rate(16000)
    audio.export(path, format='wav')
    methods.add_in_db(user_id, chat_id, type, path)
    await bot.send_message(msg.chat.id, "Данное аудиосообщение сохранено в формате wav и частотой дискретизации 16kHz")
    

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    await msg.answer('Отправьте аудиофайл. Я его конвертирую в wav 16kHz\nИли отправьте изображение с лицом человека, оно будет сохранено')


if __name__ == '__main__':
   executor.start_polling(dp)
