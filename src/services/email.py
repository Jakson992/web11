from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

def create_fastmail():
    conf = ConnectionConfig(
        MAIL_USERNAME="szcz92@proton.me",
        MAIL_PASSWORD="password",
        MAIL_FROM="szcz92@proton.me",
        MAIL_PORT=465,
        MAIL_SERVER="smtp.meta.ua",
        MAIL_FROM_NAME="Desired Name",
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
    )
    return FastMail(conf)

async def send_email(fm, email: EmailStr, username: str, host: str):
    """
    Функция send_email отправляет email пользователю с ссылкой для подтверждения email-адреса.
    Функция принимает три параметра:
        - email: EmailStr, email-адрес пользователя.
        - username: str, имя пользователя, который регистрируется. Используется в приветственном сообщении в теле email.
        - host: str, место размещения вашего приложения (например, localhost). Используется для создания URL, на который пользователь может перейти в своем браузере.

    :param fm: FastMail, объект FastMail для отправки email.
    :param email: EmailStr: Проверенный email-адрес.
    :param username: str: Имя пользователя для передачи в шаблон email.
    :param host: str: Хост для передачи в шаблон email.
    :return: Объект корутины
    :doc-author: Trelent
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Подтвердите свой email",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)


# from pathlib import Path
#
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
# from fastapi_mail.errors import ConnectionErrors
# from pydantic import EmailStr
#
# from src.services.auth import auth_service
#
# conf = ConnectionConfig(
#     MAIL_USERNAME="szcz92@proton.me",
#     MAIL_PASSWORD="password",
#     MAIL_FROM="szcz92@proton.me",
#     MAIL_PORT=465,
#     MAIL_SERVER="smtp.meta.ua",
#     MAIL_FROM_NAME="Desired Name",
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,
#     TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
# )
#
#
# async def send_email(email: EmailStr, username: str, host: str):
#     """
# The send_email function sends an email to the user with a link to confirm their email address.
#     The function takes in three parameters:
#         -email: EmailStr, the user's email address.
#         -username: str, the username of the user who is registering for an account.  This will be used in a greeting message within the body of the email sent to them.
#         -host: str, this is where we are hosting our application (i.e., localhost).  This will be used as part of a URL that they can click on within their browser.
#
# :param email: EmailStr: Validate the email address
# :param username: str: Pass the username to the email template
# :param host: str: Pass the hostname to the email template
# :return: A coroutine object
# :doc-author: Trelent
# """
#
#     try:
#         token_verification = auth_service.create_email_token({"sub": email})
#         message = MessageSchema(
#             subject="Confirm your email ",
#             recipients=[email],
#             template_body={"host": host, "username": username, "token": token_verification},
#             subtype=MessageType.html
#         )
#
#         fm = FastMail(conf)
#         await fm.send_message(message, template_name="email_template.html")
#     except ConnectionErrors as err:
#         print(err)
