from aiogram import Router
from aiogram.filters import CommandStart, Text, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from datetime import date
from keyboards.kb_total import kb_role, kb_telega
from keyboards.kb_admin import kb_main_admin
from keyboards.kb_clients import kb_main_client
from lexicon.general_lex import LEX_COMMANDS
from lexicon.lexicon_admin import LEX_ADMIN_MESSAGES
from lexicon.lexicon_clients import LEX_CLIENTS_MESSAGES
from sql_requests.sql_requests import check_user, appoint_user_role, show_user_role

router: Router = Router()


# Срабатывает на команду \start
@router.message(CommandStart())
async def process_start_command(message: Message, command: CommandObject):


    args = command.args  # Получаем аргументы команды /start
    user_role = 'client'  # По умолчанию назначаем роль "client"
    
    # Проверяем, является ли аргумент "admin"
    if args is not None and args == 'admin':
        user_role = 'admin'
    print(user_role)    


    check = await check_user(message.from_user.id) # Проверяем наличие юзера в БД
    if check == 'False': # Если юзера нет в БД, добавляем и назначаем роль
        await appoint_user_role(user_id=message.from_user.id,
                                user_role=user_role,
                                cur_date=str(date.today()))
        
    check_role =await show_user_role(user_id=message.from_user.id)
        
    # Отправляем соответствующее сообщение в зависимости от роли
    if check_role == 'admin':
        await message.answer(text=LEX_ADMIN_MESSAGES['start_message'],
                             reply_markup=kb_main_admin)   

    else:
        await message.answer(text=LEX_CLIENTS_MESSAGES['start_message'],
                             reply_markup=kb_main_client)


# # Выбрана роль АДМИН
# @router.callback_query(Text(text='admin'))
# async def admin_role_chosen(callback: CallbackQuery):
    # await change_user_role(user_id=callback.from_user.id,
#                            user_role='admin')
#     await callback.message.edit_text(text=LEX_ADMIN_MESSAGES['start_message'],
#                                      reply_markup=kb_main_admin)


# # Выбрана роль КЛИЕНТ
# @router.callback_query(Text(text='client'))
# async def client_role_chosen(callback: CallbackQuery):
#     await change_user_role(user_id=callback.from_user.id,
#                            user_role='client')
#     await callback.message.edit_text(text=LEX_CLIENTS_MESSAGES['start_message'],
#                                      reply_markup=kb_main_client)


# Срабатывает на команду \help
@router.message(Command(commands='help'))
async def help_process_command(message: Message):
    await message.answer(text=LEX_COMMANDS['help'])


# Заглушка - когда нажатие на кнопку не должно вызывать реакции
@router.callback_query(Text(text='ignore'))
async def ignore(callback: CallbackQuery):
    await callback.answer()
