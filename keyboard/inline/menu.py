from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard.inline.cb_data import week_day, action_data, add_group_id_data


menu_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Ежедневное",
            callback_data=week_day.new(
                week_day="everyday",
            )
        )
    ],

    [
        InlineKeyboardButton(
            text="Понедельник",
            callback_data=week_day.new(
                week_day="monday",
            )
        ),
        InlineKeyboardButton(
            text="Вторник",
            callback_data=week_day.new(
                week_day="tuesday",
            )
        ),
    ],

    [
        InlineKeyboardButton(
            text="Среда",
            callback_data=week_day.new(
                week_day="wednesday",
            )
        ),
        InlineKeyboardButton(
            text="Четверг",
            callback_data=week_day.new(
                week_day="thursday",
            )
        ),
    ],

    [
        InlineKeyboardButton(
            text="Пятница",
            callback_data=week_day.new(
                week_day="friday",
            )
        ),
        InlineKeyboardButton(
            text="Суббота",
            callback_data=week_day.new(
                week_day="saturday",
            )
        ),
    ],

    [
        InlineKeyboardButton(
            text="Воскресенье",
            callback_data=week_day.new(
                week_day="sunday",
            )
        ),
    ]
], resize_keyboard=True)

status_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✏️ Изменить значение",
                callback_data=action_data.new(
                    action_choice="change",
                )
            ),

            InlineKeyboardButton(
                text="🌄 Прикрепить фото",
                callback_data=action_data.new(
                    action_choice="attach_photo",
                )
            )
        ],

        [
            InlineKeyboardButton(
                text="🪧 Статус",
                callback_data=action_data.new(
                    action_choice="status_day"
                )
            )
        ],

        [
            InlineKeyboardButton(
                text="🏮 Назад",
                callback_data=action_data.new(
                    action_choice="go_back"
                ),
            )
        ]
    ]
)

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏮 Назад",
                callback_data=action_data.new(
                    action_choice="cancel"
                )
            )
        ]
    ]
)

add_group_id = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✍️ Добавить",
                callback_data=add_group_id_data.new(
                    group_id="add_group_id"
                )
            ),
        ]
    ]
)

