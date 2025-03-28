import asyncpg
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                min_size=1,
                max_size=10
            )
            logger.info("Successfully connected to database")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    async def create_tables(self):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        tg_id BIGINT NOT NULL UNIQUE,
                        username VARCHAR(32),
                        first_name VARCHAR(64),
                        last_name VARCHAR(64),
                        created_at TIMESTAMP DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS donations(
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT REFERENCES users(tg_id),
                        amount INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                ''')
                logger.info("Tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise

    async def add_user(self, user_id: int, username: str, first_name: str, last_name: str):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO users(tg_id, username, first_name, last_name)
                    VALUES($1, $2, $3, $4)
                    ON CONFLICT (tg_id) DO NOTHING
                ''', user_id, username, first_name, last_name)
        except Exception as e:
            logger.error(f"Error adding user: {e}")

    async def add_donation(self, user_id: int, amount: int):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO donations(user_id, amount)
                    VALUES($1, $2)
                ''', user_id, amount)
        except Exception as e:
            logger.error(f"Error adding donation: {e}")


db = Database()