from pathlib import Path

from src.sources.generator_source import GeneratorTaskSource
from src.sources.file_source import JSONTaskSource
from src.sources.API_stub_source import APIStubTasksSource
from src.processing_simulation import process_tasks


JSON_FILE_PATH = Path(__file__).parent.parent / "examples" / "tasks.json"


def main() -> None:
    """
    Main entry point for the application.
    :return:   None
    """
    sources = [
        GeneratorTaskSource(count=5),
        JSONTaskSource(JSON_FILE_PATH),
        APIStubTasksSource("https://url/tasks"),
    ]
    for source in sources:
        process_tasks(source)


if "__main__" == __name__:
    main()
