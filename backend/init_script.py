import asyncio
from app.database import init_db, async_session_factory
from app.services.auth_service import seed_admin

async def main():
    await init_db()
    async with async_session_factory() as s:
        await seed_admin(s)
        await s.commit()
    print("DB initialized and admin seeded.")

if __name__ == "__main__":
    asyncio.run(main())
