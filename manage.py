from pathlib import Path

from config import start_bot


def start():
    start_bot()


def startapp(app_name: str):
    apps_path = Path("apps")
    path = apps_path / Path(app_name)
    path.mkdir()

    init_path = (path / "__init__.py")
    init_path.touch()
    with open(init_path, "w") as f:
        f.write('from .handlers import router as router\n')

    handlers_path = (path / "handlers.py")
    handlers_path.touch()
    with open(handlers_path, "w") as f:
        f.write('from aiogram import Router\n\nrouter = Router()\n')

    with open(apps_path / "__init__.py", "a") as f:
        f.write(f"from .{app_name} import router as {app_name}_router\nmain_router.include_router({app_name}_router)\n")

    print(f"App {app_name} created")


def main(args: list[str]):
    commands = {
        "start": start,
        "startapp": startapp
    }
    try:
        commands[args[0]](*args[1:])
    except KeyError:
        print("Unknown command")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
