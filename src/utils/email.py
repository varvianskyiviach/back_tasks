import logging

from config.settings import ROOT_DIR

email_logger = logging.getLogger("email_logger")
email_logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file_path = ROOT_DIR / "email_log.txt"

file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)

email_logger.addHandler(file_handler)


file_handler.flush()


def mock_send_email(email_to: str, subject: str, html_content: str):
    email_logger.info(f"Sending email to: {email_to}")
    email_logger.info(f"Subject: {subject}")
    email_logger.info(f"Content: {html_content}")

    file_handler.flush()
    # console.log
    print(f"Email sent to: {email_to}\n Subject: {subject}\n Content: {html_content}")


def mock_error_hendler_email():
    email_logger.error("Failed to send email: Responsible person was not found!")
