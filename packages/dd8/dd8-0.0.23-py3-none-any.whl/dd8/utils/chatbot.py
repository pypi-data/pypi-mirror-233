# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:54:00 2021

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

from typing import Union, IO, Callable, Dict, List
import requests

# from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackContext, 
    CallbackQueryHandler,
    PollAnswerHandler
)

from ..connectivity.base import AsyncConnection

class TelegramRest(AsyncConnection):
    _URL = r'https://api.telegram.org/bot{token}/'
    def __init__(self, token: str='') -> None:
        super().__init__(request_per_second=10)
        self.token = token

    def _token_exists(self) -> bool:
        if not self.token:
            raise ValueError('no telegram token provided')
            return False        
        return True        

    def _send(self, url: str, params: Dict, files: Union[None, Dict]=None) -> None:
        if self._token_exists():
            # requests.get(url, params=params)
            resp = self.gather(self._get, [url], params)
            return resp

    def send_message(self, chat_id: str, message: str) -> None:
        url = ''.join([self._URL, 'sendMessage']).format(token=self.token)
        params = {'chat_id' : chat_id, 'text' : message}
        self._send(url, params)

    def send_document(self, chat_id: str, file_name: str, document: IO) -> bool:
        url = ''.join([self._URL, 'sendDocument']).format(token=self.token)
        params = {'chat_id', chat_id}
        files = {'document' : (file_name, document)}
        self._send(url=url, params=params, files=files)

    def send_poll(self, **kwargs: Dict) -> bool:
        url = ''.join([self._URL, 'sendpoll']).format(token=self.token)
        resp = self._send(url, params=kwargs)
        return resp

class TelegramHandler(object):
    def __init__(self, update: Union[Update, None], context=Union[CallbackContext, None]) -> None:
        self.update = update
        self.context = context

        self.buttons = []
    
    async def reply(self, message: str, chat_id: str = '') -> None:
        # await self.update.message.reply_text(message)
        if not chat_id:
            chat_id = self.update.effective_chat.id
        msg_id = await self.context.bot.send_message(
            chat_id=chat_id,
            text=message
        )
        return msg_id

    async def delete_message(self, chat_id: str = '', message_id: str = '',
                                is_callback: bool = True) -> None:
        if is_callback:
            if not chat_id:
                chat_id = self.update.callback_query.message.chat_id
            if not message_id:
                message_id = self.update.callback_query.message.message_id            
        else:
            if not chat_id:
                chat_id = self.update.effective_chat.id
            if not message_id:
                message_id = self.update.message.message_id
        #msg_id = await self.update.callback_query.message.delete_message(chat_id=chat_id, message_id=message_id)

        msg_id = await self.context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        return msg_id

    def add_inline_keyboard_button(self, **kwargs) -> None:
        self.buttons.append(
            [InlineKeyboardButton(**kwargs)]
        )

    async def send_inline_keyboard(self, chat_id: str = '') -> None:
        if not chat_id:
            chat_id = self.update.effective_chat.id
        msg_id = await self.context.bot.send_message(
                    chat_id=chat_id,
                    reply_markup=InlineKeyboardMarkup(self.buttons),
                    text='What would you like to do?'
                )
        self.buttons = []
        return msg_id
    
    async def remove_inline_keyboard(self, chat_id: str = '', message_id: str = '',
                                        is_callback: bool = True) -> None:
        if is_callback:
            if not chat_id:
                chat_id = self.update.callback_query.message.chat_id
            if not message_id:
                message_id = self.update.callback_query.message.message_id
            msg_id = await self.update.callback_query.edit_message_reply_markup(None)
        else:
            if not chat_id:
                chat_id = self.update.effective_chat.id
            if not message_id:
                message_id = self.update.message.message_id
            msg_id = await self.update.effective_message.edit_reply_markup(None)
        return msg_id
        

class Telegram(object):
    _URL = r'https://api.telegram.org/bot{token}/'
    def __init__(self, token: str='', use_context: bool=True) -> None:
        self.token = token
        self.use_context = use_context
        self.application = Application.builder().token(token).build()
    
    def _token_exists(self) -> bool:
        if not self.token:
            raise ValueError('no telegram token provided')
            return False        
        return True

    def poll(self, timeout: int=100000) -> None:
        self.application.run_polling(timeout=timeout, 
                                     allowed_updates=Update.ALL_TYPES)

    def add_command(self, command_name: str, command_func: Callable) -> bool:
        try:
            handler = CommandHandler(command_name, command_func)
            self.application.add_handler(handler)
            return True
        except:
            return False
    
    def add_callback_query_handler(self, handler: Callable) -> bool:
        try:
            handler = CallbackQueryHandler(handler)
            self.application.add_handler(handler)
            return True
        except:
            return False
    
    def add_poll(self, handler: Callable) -> bool:
        try:
            handler = PollAnswerHandler(handler)
            self.application.add_handler(handler)
            return True
        except:
            return False