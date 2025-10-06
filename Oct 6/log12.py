import logging

class InvalidMarksError(Exception):
    pass

def check_marks(marks):
    if marks < 0 and marks > 100:
        raise InvalidMarksError("Marks should be between 0 and 100")

    try:
        check_marks(120)

    except InvalidMarksError as e:
        logging.error(e)
