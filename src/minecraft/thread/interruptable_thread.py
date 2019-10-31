import ctypes
import threading


class InterruptException(BaseException):
    pass


class InterruptableThread(threading.Thread):
    """
    A thread class that supports raising exception in the thread from
    another thread.
    """
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

    def interrupt(self):
        """
        Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an exception in the context of the
        thread represented by this instance.
        """
        thread_id = self._get_my_tid()
        if not thread_id:
            return True
        result = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id),
                                                            ctypes.py_object(InterruptException))
        if result == 0:
            return False
        elif result != 1:
            # "if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), None)
            return False
        return True

    def _get_my_tid(self):
        """
        Determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.is_alive():
            return None

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("Could not find thread id!")
