import asyncio
import sys


if __name__ == "__main__":
    from config import start_bot

    asyncio.run(start_bot(sys.argv))
