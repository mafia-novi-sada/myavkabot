from .config import Config
from .utils import MyavkaBot, di_container


def main() -> None:
    config: Config = di_container.get(Config)
    MyavkaBot.setup(
        owner_id=config.BOT_OWNER_ID,
        description=config.BOT_DESCRIPTION,
    )
    MyavkaBot.run(token=config.BOT_TOKEN)


if __name__ == "__main__":
    main()
