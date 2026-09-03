from app.config.settings import settings
from app.core.logger import logger


def main() -> None:
    logger.info("Starting %s", settings.app_name)
    logger.info("Environment: %s", settings.app_env)
    logger.info("Version: %s", settings.app_version)
    logger.info("Trading bot foundation initialized.")


if __name__ == "__main__":
    main()