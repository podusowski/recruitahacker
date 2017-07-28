import datetime


call_counter = 0
begin = datetime.datetime.now()


def log_nth_call(n):
    def wrapper(f):
        def decorated(*args, **kwargs):
            global call_counter
            global begin

            call_counter += 1

            result = f(*args, **kwargs)

            if call_counter % n == 0:
                now = datetime.datetime.now()
                print(', '.join([
                                 f.__name__,
                                 str(call_counter),
                                 str(now - begin),
                                 *[str(a) for a in args],
                                 str(result)
                                ]), end="\r")

            return result
        return decorated
    return wrapper

