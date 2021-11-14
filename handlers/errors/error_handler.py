from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted, BadRequest, NetworkError, ChatNotFound, MigrateToChat)

    if isinstance(exception, MigrateToChat):
        print("Chat was migrated! New id is : %s" % exception.migrate_to_chat_id)
        return True

    if isinstance(exception, ChatNotFound):
        print("Chat is not found! Check GROUPS!")
        return True

    if isinstance(exception, NetworkError):
        print("Connection was interrupted!")
        return True

    if isinstance(exception, CantDemoteChatCreator):
        print("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        print('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        print('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        print('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        print('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        print(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        print(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        print(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, RetryAfter):
        print(f'RetryAfter: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        print(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, BadRequest):
        print(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True