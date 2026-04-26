import asyncio

from src.common.logging_config import setup_logging
from src.sources.generator_source import GeneratorTaskSource
from src.demo_execution import demo_execution


async def main() -> None:
    """
    Main entry point for the application.
    :return:   None
    """
    source = GeneratorTaskSource(count=15)

    await demo_execution(source)


if "__main__" == __name__:
    setup_logging(level="INFO")
    asyncio.run(main())
