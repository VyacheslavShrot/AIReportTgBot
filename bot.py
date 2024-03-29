import tempfile

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, FSInputFile

from utils import dp, bot, expected_locations, get_points_option, handle_points, handle_points_with_comment, Form, handle_check_photo, \
    handle_photo, get_format_data, client

_locations = []
for location in expected_locations:
    keyboard_buttons = KeyboardButton(text=f"{location}")
    _locations.append(keyboard_buttons)


@dp.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):
    await message.answer("Hello! Let's get started")
    await message.answer(
        "Now you can choose one of 5 locations to create report by using OpenAI",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[_locations],
            resize_keyboard=True
        )
    )

    await state.set_state(Form.location)


@dp.message(Form.location)
async def handle_location_choice(message: Message, state: FSMContext):
    if message.text not in expected_locations:
        await message.answer("Please choose an answer from the given options")
        return

    await state.update_data(location=message.text)

    await message.answer(f"Okay, you've chosen {message.text} location")

    await message.answer(
        f"Now let's fill out the checklist, shall we?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Sure, let's do it"),
                    KeyboardButton(text="I don't want to do that anymore :(")
                ]
            ],
            resize_keyboard=True
        )
    )

    await state.set_state(Form.checklist)


@dp.message(Form.checklist)
async def handle_checklist(message: Message, state: FSMContext):
    if message.text not in ["Sure, let's do it", "I don't want to do that anymore :("]:
        await message.answer("Please choose an answer from the given options")
        return

    if message.text == "I don't want to do that anymore :(":
        await message.answer(
            text="It's sad :( But i'd love to see you again in the future",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/start")
                    ]
                ],
                resize_keyboard=True
            )
        )
        return

    await message.answer(
        f"Moving on to the point 1:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[await get_points_option()],
            resize_keyboard=True
        )
    )

    await state.set_state(Form.first_point)


"""
                                    STRUCTURE OF POINTS
                        HANDLER for selecting the user for certain points
                        HANDLER if the user wants to enter a comment
                        HANDLER for giving the user the choice to attach a photo
                        HANDLER for attaching a photo from the user
"""
"""
                                    FOR FIRST POINT 
"""


@dp.message(Form.first_point)
async def handle_first_point(message: Message, state: FSMContext):
    current_state_name = "first_point"
    next_point = Form.second_point
    point_with_comment = Form.first_point_with_comment
    next_point_num = 2

    await handle_points(message, state, next_point, point_with_comment, next_point_num, current_state_name)


@dp.message(Form.first_point_with_comment)
async def handle_first_point_with_comment(message: Message, state: FSMContext):
    current_state_name = "first_point_with_comment"
    next_point = Form.check_first_photo

    await handle_points_with_comment(message, state, next_point, current_state_name)


@dp.message(Form.check_first_photo)
async def handle_check_first_photo_after_comment(message: Message, state: FSMContext):
    next_point = Form.second_point
    next_point_num = 2
    state_handle_photo = Form.first_photo

    await handle_check_photo(message, state, next_point, next_point_num, state_handle_photo)


@dp.message(Form.first_photo)
async def handle_first_photo(message: Message, state: FSMContext):
    next_point_num = 2
    next_point = Form.second_point
    current_state_name = "first_photo"

    await handle_photo(message, state, next_point_num, next_point, current_state_name)


"""
                                FOR SECOND POINT
"""


@dp.message(Form.second_point)
async def handle_second_point(message: Message, state: FSMContext):
    current_state_name = "second_point"
    next_point = Form.third_point
    point_with_comment = Form.second_point_with_comment
    next_point_num = 3

    await handle_points(message, state, next_point, point_with_comment, next_point_num, current_state_name)


@dp.message(Form.second_point_with_comment)
async def handle_second_point_with_comment(message: Message, state: FSMContext):
    current_state_name = "second_point_with_comment"
    next_point = Form.check_second_photo

    await handle_points_with_comment(message, state, next_point, current_state_name)


@dp.message(Form.check_second_photo)
async def handle_check_second_photo_after_comment(message: Message, state: FSMContext):
    next_point = Form.third_point
    next_point_num = 3
    state_handle_photo = Form.second_photo

    await handle_check_photo(message, state, next_point, next_point_num, state_handle_photo)


@dp.message(Form.second_photo)
async def handle_second_photo(message: Message, state: FSMContext):
    next_point_num = 3
    next_point = Form.third_point
    current_state_name = "second_photo"

    await handle_photo(message, state, next_point_num, next_point, current_state_name)


"""
                                FOR THIRD POINT
"""


@dp.message(Form.third_point)
async def handle_third_point(message: Message, state: FSMContext):
    current_state_name = "third_point"
    next_point = Form.fourth_point
    point_with_comment = Form.third_point_with_comment
    next_point_num = 4

    await handle_points(message, state, next_point, point_with_comment, next_point_num, current_state_name)


@dp.message(Form.third_point_with_comment)
async def handle_third_point_with_comment(message: Message, state: FSMContext):
    current_state_name = "third_point_with_comment"
    next_point = Form.check_third_photo

    await handle_points_with_comment(message, state, next_point, current_state_name)


@dp.message(Form.check_third_photo)
async def handle_check_third_photo_after_comment(message: Message, state: FSMContext):
    next_point = Form.fourth_point
    next_point_num = 4
    state_handle_photo = Form.third_photo

    await handle_check_photo(message, state, next_point, next_point_num, state_handle_photo)


@dp.message(Form.third_photo)
async def handle_third_photo(message: Message, state: FSMContext):
    next_point_num = 4
    next_point = Form.fourth_point
    current_state_name = "third_photo"

    await handle_photo(message, state, next_point_num, next_point, current_state_name)


"""
                                FOR FOURTH POINT
"""


@dp.message(Form.fourth_point)
async def handle_fourth_point(message: Message, state: FSMContext):
    current_state_name = "fourth_point"
    next_point = Form.fifth_point
    point_with_comment = Form.fourth_point_with_comment
    next_point_num = 5

    await handle_points(message, state, next_point, point_with_comment, next_point_num, current_state_name)


@dp.message(Form.fourth_point_with_comment)
async def handle_fourth_point_with_comment(message: Message, state: FSMContext):
    current_state_name = "fourth_point_with_comment"
    next_point = Form.check_fourth_photo

    await handle_points_with_comment(message, state, next_point, current_state_name)


@dp.message(Form.check_fourth_photo)
async def handle_check_fourth_photo_after_comment(message: Message, state: FSMContext):
    next_point = Form.fifth_point
    next_point_num = 5
    state_handle_photo = Form.fourth_photo

    await handle_check_photo(message, state, next_point, next_point_num, state_handle_photo)


@dp.message(Form.fourth_photo)
async def handle_fourth_photo(message: Message, state: FSMContext):
    next_point_num = 5
    next_point = Form.fifth_point
    current_state_name = "fourth_photo"

    await handle_photo(message, state, next_point_num, next_point, current_state_name)


"""
                                FOR FIFTH POINT
"""


@dp.message(Form.fifth_point)
async def handle_fifth_point(message: Message, state: FSMContext):
    current_state_name = "fifth_point"
    next_point = Form.report
    point_with_comment = Form.fifth_point_with_comment
    next_point_num = None

    await handle_points(message, state, next_point, point_with_comment, next_point_num, current_state_name)


@dp.message(Form.fifth_point_with_comment)
async def handle_fifth_point_with_comment(message: Message, state: FSMContext):
    current_state_name = "fifth_point_with_comment"
    next_point = Form.check_fifth_photo

    await handle_points_with_comment(message, state, next_point, current_state_name)


@dp.message(Form.check_fifth_photo)
async def handle_check_fifth_photo_after_comment(message: Message, state: FSMContext):
    next_point = Form.report
    next_point_num = None
    state_handle_photo = Form.fifth_photo

    await handle_check_photo(message, state, next_point, next_point_num, state_handle_photo)


@dp.message(Form.fifth_photo)
async def handle_fifth_photo(message: Message, state: FSMContext):
    next_point_num = None
    next_point = Form.report
    current_state_name = "fifth_photo"

    await handle_photo(message, state, next_point_num, next_point, current_state_name)


"""
                                WORKING WITH USER DATA
"""


@dp.message(Form.report)
async def handle_report(message: Message, state: FSMContext):
    if message.text != "View your information":
        await message.answer(
            "Here's your information:",
            reply_markup=ReplyKeyboardRemove()
        )
    await get_format_data(message, state)

    await message.answer(
        f"Now we can generate a response from OpenAI, shall we begin?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Generate"),
                    KeyboardButton(text="I want to re-fill")
                ]
            ],
            resize_keyboard=True
        )
    )

    await state.set_state(Form.OpenAI)


@dp.message(Form.OpenAI)
async def handle_report_from_openai(message: Message, state: FSMContext):
    if message.text not in ["Generate", "I want to re-fill"]:
        await message.answer(f"Please choose an answer from the given options")
        return

    if message.text == "Generate":
        text_to_send, photos = await get_format_data(message, state)

        await message.answer(f"Generate an OpenAI response\nWait...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": 'You have a good understanding of countries and their stories, so you can help others by answering their '
                               'questions.'
                               ' Observe the following :'
                               '1. Even if the punts go out of order, still answer in order and dont skip anything.'
                               '2. Always give a full answer.'
                               '3. If you dont have the answer to that point, write "I dont know the answer on this '
                               'point" and go to the next point.'
                               '4. Take information only from verified sources such as WIKI and others.'
                               '5. At the end of your reply, add a sentence from yourself in which you simply thank the user for using '
                               'your services to answer their questions.'
                },
                {"role": "user",
                 "content":
                     "Location: USA "
                     "First_point_with_comment: Who is the first president of my country? "
                     "Second point: njkasnvsvja131 "
                     "Fourth point: All clear "
                     "Fifth point: When my country became independent? "
                     "Third point: All clear "
                 },
                {
                    "role": "assistant", "content": "1. The first president of Israel was Chaim Weizmann."
                                                    "2. I dont know the answer on this point"
                                                    "3. Clear"
                                                    "4. Clear"
                                                    "5. Israel became independent in May 14, 1948"
                },
                {"role": "user", "content": text_to_send}
            ],
            temperature=0.85
        )

        generated_text = response.choices[0].message.content
        await message.answer(f"OpenAI Response:\n{generated_text}", reply_markup=ReplyKeyboardRemove())

        await message.answer(f"Generate an audio response\nWait...")
        audio = client.audio.speech.create(
            model='tts-1',
            voice='nova',
            input=generated_text
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
            temp_audio_file.write(audio.content)
            temp_audio_file_name = temp_audio_file.name

        generated_audio = FSInputFile(temp_audio_file_name)
        await bot.send_audio(chat_id=message.chat.id, audio=generated_audio)

        if photos:
            for photo in photos:
                if photo:
                    await message.answer(f"Generate an image variation\nWait...")

                    photo_response = client.images.create_variation(
                        model='dall-e-2',
                        image=photo,
                        n=1,
                        size='1024x1024'
                    )
                    await bot.send_photo(chat_id=message.chat.id, photo=f"{photo_response.data[0].url}")

        await message.answer(
            "Now you can choose again one of 5 locations to create another report by using OpenAI",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[_locations],
                resize_keyboard=True
            )
        )

        await state.clear()
        await state.set_state(Form.location)
    elif message.text == "I want to re-fill":
        await state.clear()

        await message.answer(
            f"Moving on to the point 1:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[await get_points_option()],
                resize_keyboard=True
            )
        )

        await state.set_state(Form.first_point)


if __name__ == '__main__':
    dp.run_polling(bot, skip_updates=True)
