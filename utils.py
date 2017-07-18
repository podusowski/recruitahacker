import datetime


call_counter = 0
last_call = datetime.datetime.now()


def log_nth_call(n, time=False):
    def wrapper(f):
        def decorated(*args, **kwargs):
            global call_counter
            global last_call

            call_counter += 1

            if call_counter % n == 0:
                if time:
                    now = datetime.datetime.now()
                    print(', '.join([str(now - last_call), *args]), end="\r")
                    last_call = now
                else:
                    print(', '.join(args), end="\r")

            f(*args, **kwargs)
        return decorated
    return wrapper
