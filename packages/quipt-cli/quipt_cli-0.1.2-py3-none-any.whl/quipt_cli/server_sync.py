from enum import IntEnum
import os
from uuid import UUID
import pyqrcode

from typing import Any, Callable, cast
from rich import print as rprint
from base64 import b64encode
from websockets.sync.client import connect, ClientConnection

from .serialisation import File, ItemType, OverviewTableItem, Quote, Trigger, all_actors

# WS_URI = "wss://quipt.app/ws-connect"
WS_URI = "ws://localhost:5000/ws-connect"
COOKIE_FILE = "quiptcontext.w"

class ErrorReason(IntEnum):
    UserCanceledOperation = 0
    InvalidLogin = 1
    Other = 2

class OperationalError(Exception):
    def __init__(self, reason: ErrorReason):
        super().__init__()
        self.reason = reason

class MessageTypes:
    LoginRequest = b'LR'
    Authentication = b'AT'
    ScriptCreation = b'CS'
    TriggerDeletion = b'DT'
    DivisionDeletion = b'DD'
    TriggerInsertion = b'IT'
    DivisionInsertion = b'ID'
    TriggerChange = b'CT'
    DivisionChange = b'CD'
    AlternateScript = b'AS'
    LeaveAlternate = b'AL'
    
class ScriptContext:
    def __init__(self, websocket: ClientConnection, script_id: UUID):
        self.websocket = websocket
        self.script_id = script_id
    
    def __enter__(self) -> Any:
        buffer = bytearray()
        buffer.extend(MessageTypes.AlternateScript)
        buffer.extend(self.script_id.bytes)
        self.websocket.send(buffer)

        if (response := self.check_error()) is None:
            return None

        assert response == self.script_id.bytes, "Invalid Client Data"

        return self

    def __exit__(self, *_):
        self.websocket.send(MessageTypes.LeaveAlternate)
        self.check_error()

    def delete_trigger(self, trigger_id: UUID):
        self.websocket.send(MessageTypes.TriggerDeletion + trigger_id.bytes)
        self.check_error()

    def delete_division(self, name: str):
        self.websocket.send(MessageTypes.DivisionDeletion + name.encode())
        self.check_error()

    def insert_trigger(self, prev: str, new_trigger: Trigger):
        buffer = bytearray()
        buffer.extend(MessageTypes.TriggerInsertion)  
        encode_previous(buffer, prev) 
        serialize_trigger(buffer, new_trigger)
        self.websocket.send(buffer)
        self.check_error()

    def insert_division(self, prev: str, name: str):
        buffer = bytearray()
        buffer.extend(MessageTypes.DivisionInsertion)
        encode_previous(buffer, prev) 
        buffer.extend(name.encode())
        self.websocket.send(buffer)
        self.check_error()

    def change_trigger(self, new_trigger: Trigger):
        buffer = bytearray()
        buffer.extend(MessageTypes.TriggerChange)
        serialize_trigger(buffer, new_trigger)
        self.websocket.send(buffer)
        self.check_error()

    def change_division(self, old_name: str, new_name: str):
        buffer = bytearray()
        buffer.extend(MessageTypes.DivisionChange)
        buffer.extend(old_name.encode() + b'\x00')
        buffer.extend(new_name.encode())
        self.websocket.send(buffer)
        self.check_error()

    def check_error(self) -> bytes:
        if (result := handle_error(self.websocket)) is not None:
            return result
        raise OperationalError(ErrorReason.Other)

class QuiptApp:
    def __init__(
            self, 
            cookie: bytes,
            connection_tpl: tuple[ClientConnection, UUID] | None, 
            data_path: str
        ):
        self.cookie = cookie
        self.data_path = data_path

        if connection_tpl is None:
            websocket = connect(WS_URI)
            websocket.send(MessageTypes.Authentication + self.cookie)
            if (res := serialize_login_cookie(websocket, self.data_path)) is None:
                websocket.close()
                raise OperationalError(ErrorReason.InvalidLogin)
            uuid, cookie = res
        else:
            websocket, uuid = connection_tpl
        self.websocket = websocket
        self.user_uuid = uuid

    @classmethod
    def login(cls, data_path: str) -> Any:
        cookie_path = os.path.join(data_path, COOKIE_FILE)
        if os.path.isfile(cookie_path):
            with open(cookie_path, 'rb') as cookie_file:
                cookie = cookie_file.read()
            return cls(cookie, None, data_path)
        connection = connect(WS_URI)

        connection.send(MessageTypes.LoginRequest)
        connection_token = connection.recv()
        assert type(connection_token) == bytes, "Invalid Server Response"
        assert len(connection_token) == 6, "Invalid Server Response"
        connection_token = b64encode(connection_token).decode()

        print_qr_for_token(connection_token)
        rprint("Scan with your Smartphone or press ^C to cancel")

        try:
            if (res := serialize_login_cookie(connection, data_path)) is None:
                raise OperationalError(ErrorReason.InvalidLogin)
            uuid, cookie = res
        except KeyboardInterrupt:
            connection.send(b'\x00')
            connection.close()
            raise OperationalError(ErrorReason.UserCanceledOperation)

        return cls(cookie, (connection, uuid), data_path)

    def create_script(self, script_file: File, script_id: UUID, script_name: str):
        buffer = bytearray(MessageTypes.ScriptCreation)
        buffer.extend(script_id.bytes)
        buffer.extend(script_name.encode())
        buffer.extend(b'\x00')

        buffer.extend(
            b'\f'.join(actor.encode() for actor in script_file.actors)
        )
        buffer.extend(b'\v')

        for item in script_file.overview_talbe:
            serialize_item(buffer, item)
        self.websocket.send(buffer)
        if handle_error(self.websocket) is None:
            raise OperationalError(ErrorReason.Other)

    def alternate_script(self, script_id: UUID) -> ScriptContext:
        return ScriptContext(self.websocket, script_id)

    def close(self):
        self.websocket.close()

def encode_previous(buffer: bytearray, prev: str): 
    if prev == 'Top':
        buffer.extend(b'T')
    elif (uuid := str_to_uuid(prev)) is not None:
        buffer.extend(b'U' + uuid.bytes)
    else:
        buffer.extend(b'D' + prev.replace('\x1b', ' ').encode() + b'\x00')

def str_to_uuid(test: str) -> UUID | None:
    try:
        return UUID(test)
    except ValueError:
        return

def serialize_item(buffer: bytearray, item: OverviewTableItem):
    if item.item_type == ItemType.DIVISION:
        buffer.append(0x05)
        buffer.extend(item.item.encode())
        buffer.append(0x00)
    elif item.item_type == ItemType.TRIGGER:
        buffer.append(0x04)
        serialize_trigger(buffer, item.item)

def serialize_trigger(buffer: bytearray, trigger: Trigger):
    buffer.extend(trigger.uuid)
    if trigger.request_type == ItemType.DIVISION:
        buffer.append(0x1A)
    else:
        if trigger.request.actor_id is all_actors:
            buffer.append(0x19)
        else:
            actor_string = bytes(id - 1 for id in trigger.request.actor_id)
            buffer.extend(actor_string)
    buffer.extend(b'\t')
    if trigger.response.actor_id is all_actors:
        buffer.append(0x19)
    else:
        actor_string = bytes(id - 1 for id in trigger.response.actor_id)
        buffer.extend(actor_string)
    buffer.extend(b'\v')
    serialize_text(buffer, trigger.request_type, trigger.request, trigger.response)

def serialize_text(buffer: bytearray, request_type: ItemType, request: int | Quote, response: Quote):
    if request_type == ItemType.DIVISION:
        buffer.append(request)
    else:
        request = cast(Quote, request)
        if request.content.divisions[0][0]:
            buffer.extend(b'\x10')
        request_content_str = b'\x10'.join(div[1].encode() for div in request.content.divisions)
        buffer.extend(request_content_str)
    buffer.extend(b'\t')
    if response.content.divisions[0][0]:
        buffer.extend(b'\x10') # )
    response_content_str = b'\x10'.join(div[1].encode() for div in response.content.divisions)
    buffer.extend(response_content_str)

def serialize_login_cookie(websocket: ClientConnection, data_path: str) -> tuple[UUID, bytes] | None:
    if (response := handle_error(websocket)) is None:
        return

    assert type(response) == bytes, "Invalid Server Response"
    uuid, cookie = response[:16], response[16:]
    assert type(uuid) == bytes, "Invalid Server Response"
    assert len(uuid) == 16, "Invalid Server Response"

    uuid = UUID(bytes=uuid)
    rprint(f"Connected with user [italic green]{uuid}[/]")

    cookie_path = os.path.join(data_path, COOKIE_FILE)
    with open(cookie_path, 'wb') as cookie_file:
        cookie_file.write(cookie)

    return uuid, cookie

def handle_error(websocket: ClientConnection, *, expected:bool = False) -> bytes | None:
    response = websocket.recv()
    if response[0] == 0x00:  # success
        return response[1:]

    errorno = response[0]
    message = response[1:].decode()
    rprint(f"Request failed with {errorno}: [italic red]{message}[/]")

    return None

def print_qr_for_token(token: str):
    code = pyqrcode.create(token)
    print(code.terminal(quiet_zone=0, background='default', module_color='white'))
