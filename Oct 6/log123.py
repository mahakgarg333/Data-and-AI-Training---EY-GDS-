import logging

logging.basicConfig(
    filename = 'app.log',
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')

try:
    value = int(input("Enter a number: "))
    print(10/value)
except ValueError:
    print("You did not enter a number")
except ZeroDivisionError:
    print("You did not enter a number")
finally:
    print("Execution completed")
