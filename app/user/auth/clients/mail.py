from worker.celery import send_emal_task


class MailClient:

    @staticmethod
    def send_welcome_email(to: str):
        task_id = send_emal_task.delay(f"Welcome email", f"Welcom to MANICEL", to)
        return task_id
