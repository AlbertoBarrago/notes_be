"""
 Email Service
"""
from typing import List

from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr, BaseModel

from app.core.settings import settings


class EmailSchema(BaseModel):
    """
    Email Schema
    """
    username: str
    email: List[EmailStr]


class EmailService:
    """
       Initialize FastMail
       :return: None
    """

    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=587,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=False
        )
        self.fastmail = FastMail(self.conf)

    async def welcome_email(self, schema: EmailSchema):
        """Send welcome email"""
        body = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Welcome to Notes App! 🎉</h2>

                    <p style="color: #555; font-size: 16px; line-height: 1.5;">
                        Hi {schema.username},
                    </p>

                    <p style="color: #555; font-size: 16px; line-height: 1.5;">
                        We're thrilled to have you on board! With Notes App, you can:
                        <ul style="color: #555;">
                            <li>Create and organize your notes</li>
                            <li>Access your content from anywhere</li>
                            <li>Share and collaborate seamlessly</li>
                        </ul>
                    </p>

                    <p style="color: #555; font-size: 16px; line-height: 1.5;">
                        Ready to get started? Click the button below to begin your journey:
                    </p>

                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{settings.FRONTEND_URL}/notes"
                        style="background-color: #007bff;
                        color: white;
                        padding: 12px 25px;
                        text-decoration: none; 
                        border-radius: 5px; font-weight: bold;">
                            Start Using Notes App
                        </a>
                    </div>

                    <p style="color: #555; font-size: 16px; line-height: 1.5;">
                        Best regards,<br>
                        Notes App Team
                    </p>
                </div>

                <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
                    © 2024 Notes App. All rights reserved.
                </div>
            </div>
            """
        try:
            message = MessageSchema(
                subject="Welcome to Notes App",
                recipients=schema.email,
                body=body,
                subtype=MessageType.html
            )
            await self.fastmail.send_message(message)
        except ConnectionErrors as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send welcome email: {str(e)}"
            ) from e

    async def send_password_setup_email(self, schema: EmailSchema, token: str):
        """Send password setup email for OAuth users"""
        body = f"""
           <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
               <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                   <h2 style="color: #333; margin-bottom: 20px;">Complete Your Notes App Setup 🔐</h2>

                   <p style="color: #555; font-size: 16px; line-height: 1.5;">
                       Hi {schema.username},
                   </p>

                   <p style="color: #555; font-size: 16px; line-height: 1.5;">
                       Thanks for registering with Google OAuth! To ensure full access to all Notes App features, 
                       please set up your password by clicking the button below:
                   </p>

                   <div style="text-align: center; margin: 30px 0;">
                       <a href="{settings.FRONTEND_URL}/reset/password?token={token}"
                          style="background-color: #28a745;
                          color: white; padding: 12px 25px;
                          text-decoration: none;
                          border-radius: 5px;
                          font-weight: bold;">
                           Set Your Password
                       </a>
                   </div>

                   <p style="color: #ff6b6b; font-size: 14px; text-align: center;">
                       ⚠️ This link will expire in 15 minutes.
                   </p>

                   <p style="color: #555; font-size: 16px; line-height: 1.5;">
                       For your security, please:
                       <ul style="color: #555;">
                           <li>Use a strong, unique password</li>
                           <li>Never share your password with others</li>
                           <li>Complete this setup as soon as possible</li>
                       </ul>
                   </p>

                   <p style="color: #555; font-size: 16px; line-height: 1.5;">
                       Best regards,<br>
                       Notes App Team
                   </p>
               </div>

               <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
                   © 2024 Notes App. All rights reserved.<br>
                   If you didn't request this email, please ignore it.
               </div>
           </div>
           """
        try:
            message = MessageSchema(
                subject="Reset Your Password",
                recipients=schema.email,
                body=body,
                subtype=MessageType.html
            )
            await self.fastmail.send_message(message)
        except ConnectionErrors as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send password setup email: {str(e)}"
            ) from e
