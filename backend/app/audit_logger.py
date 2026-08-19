import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("audit_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/audit.log")
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def log_audit(user_id, action, status, latency_ms):
    logger.info(
        f"user_id={user_id} | "
        f"action={action} | "
        f"status={status} | "
        f"latency_ms={latency_ms}"
    )   