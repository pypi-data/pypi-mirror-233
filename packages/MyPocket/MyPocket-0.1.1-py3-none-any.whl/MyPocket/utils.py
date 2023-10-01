
def generate_custom_message(message):
    '''for any input of message, center it into a 80 long box surrounded by #'''
    
    border = "=" * 80

    # Calculate the number of spaces needed on each side to center the message
    total_spaces = 78 - len(message)  # 78 spaces account for the '#' characters and spaces on both sides
    left_spaces = total_spaces // 2
    right_spaces = total_spaces - left_spaces

    formatted_message = f"{border}\n#{' ' * left_spaces}{message}{' ' * right_spaces}#\n{border}\n"
    print(formatted_message)


def verboseprint(msg, verbose):
    '''
    for any message, add a verbose parameter to control if it need to be printed 
    '''
    if verbose:
        print(msg)


class Spinner:
    '''
    An spinning anime, with program running, show a spinning wheel.
    Usage:
        With Spinner:
            your_function_to_be_runed
    '''
    busy = False
    delay = 0.1

    def __init__(self, delay=None):
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            for char in "|/-\\":
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(self.delay)
                sys.stdout.write('\b')
                sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False


