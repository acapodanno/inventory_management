import logging

def setup_logging(log_file="dummy_data/logs.csv"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(levelname)s,%(name)s,%(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8")],
        datefmt="%Y-%m-%d %H:%M:%S")
