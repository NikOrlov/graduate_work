import asyncio
import logging

import typer
from fastapi import HTTPException
from pydantic.error_wrappers import ValidationError
from redis.client import Redis
from db.postgres import DbService, async_session
from schemas.base import SignUpUser
from services.auth import AuthService
from services.roles import RolesService
from core.logger import LoggerSetup

logging_setup = LoggerSetup()
logger = logging.getLogger("auth_api_cli")


async def main():
    while True:
        try:
            admin = SignUpUser(
                login=typer.prompt("Login", default="admin"),
                email=typer.prompt("Email address", default="admin@example.com"),
                password=typer.prompt(
                    "Password", hide_input=True, confirmation_prompt=True
                ),
            )

            async with async_session() as session:
                ds = DbService(db=session)
                auth_serv = AuthService(ds, Redis())
                role_serv = RolesService(ds)
                await role_serv.create_role("admin", "admin role")
                await auth_serv.create_user(admin)
                await role_serv.set_role_to_user(admin.email, "admin")
                logger.info("Created admin user with email %s", admin.email)
                break

        except ValidationError:
            logging.info("Invalid credentials for admin user")
        except HTTPException as err:
            logging.info(err)


if __name__ == "__main__":
    asyncio.run(main())
