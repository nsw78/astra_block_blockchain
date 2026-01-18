import logging


def configure_logging():
    LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    # reduce verbosity of noisy libs
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.error').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
