# -- coding: utf-8 - -


class ObservableVariable_old:
    """Every instance of this class has the property ``value``. After every change of this property every callback in the property ``callbacks``
    will be called. The callback will receive the value as well as given arguments. If you do not wnat to send the value, set the property ``send_value`` to False.
    To add or remove callbacks use the methods ``bind`` / ``unbind`` / ``unbind_all``.
    """

    def __init__(self, value=None) -> None:
        self._value = value
        self.send_value = True
        self.callbacks = []

    def bind(self, callback, *args):
        """Sending value on change to callback function.

        Args:
            callback (function): your callback
            args (list): arguments to pass to callback
        """
        self.callbacks.append((callback, *args))

    def unbind(self, callback, *args):
        """Remove the (callback, *args) tuple from the callbacks list.

        Args:
            callback (function): your callback
        """
        self.callbacks.remove((callback, *args))

    def unbind_all(self):
        """Remove all hooks"""
        self.callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for c, *args in self.callbacks:
            if self.send_value:
                if len(args) != 0:
                    c(value, *args)
                else:
                    c(value)
            else:
                if len(args) != 0:
                    c(*args)
                else:
                    c()


class ObservableVariable:
    """Every instance of this class has the property ``value``. After every change of this property every callback in the property ``callbacks``
    will be called. The callback will receive the value as well as given arguments. If you do not wnat to send the value, set the property ``send_value`` to False.
    To add or remove callbacks use the methods ``bind`` / ``unbind`` / ``unbind_all``.
    """

    def __init__(self, value=None) -> None:
        self._value = value
        self.callbacks = []

    def bind(self, callback, send_value: bool = True, *args):
        """Sending value on change to callback function.

        Args:
            callback (function): your callback
            args (list): arguments to pass to callback
        """
        self.callbacks.append((callback, send_value, *args))

    def unbind(self, callback, send_value: bool = True, *args):
        """Remove the (callback, *args) tuple from the callbacks list.

        Args:
            callback (function): your callback
        """
        self.callbacks.remove((callback, send_value, *args))

    def unbind_all(self):
        """Remove all hooks"""
        self.callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for c, send_value, *args in self.callbacks:
            if send_value:
                if len(args) != 0:
                    c(value, *args)
                else:
                    c(value)
            else:
                if len(args) != 0:
                    c(*args)
                else:
                    c()


if __name__ == "__main__":

    obs = ObservableVariable()

    def my_callback(value, first_arg, second_arg):
        print("New value:", value)
        print("First argument:", first_arg)
        print("Second argument:", second_arg)

    # binding a callback
    obs.bind(my_callback, "arg 1", "arg 2")
    obs.value = 1
    # >>> New value: 1
    # >>> First argument: arg 1
    # >>> Second argument: arg 2

    # unbinding a specific function-args-combination
    obs.unbind(my_callback, "arg 1", "arg 2")
    obs.value = 2
    # callback not called

    obs.bind(lambda value: print(value))
    # unbind all callbacks
    obs.unbind_all()
    obs.value = 3
    # again callback not called

    # deactivating the sending of the new value as the first argument
    obs.send_value = False
