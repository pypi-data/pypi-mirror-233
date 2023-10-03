# observable_variable
[GitHub](https://github.com/ICreedenI/observable_variable) | [PyPI](https://pypi.org/project/observable-variable/)  


Do you want to call a function every time a variable gets a new value?
This package allows you to create an observable. This instance of the `ObservableVariable` class has an attribute `value`. If you set a new value to this attribute, every callback will be called. You can add callbacks by calling the method `bind` with the function and arguments to be passed to the callback. Removing is as easy as to call `unbind` with the same callback and arguments or by calling `unbind_all` to remove all bound callbacks for this observable. By default the new value will be the first argument to be passed to the callback. To disable this set the attribute `send_value` to False.

```python
obs = ObservableVariable()

def my_callback(value, first_arg, second_arg):
    print("New value:", value)
    print("First argument:", first_arg)
    print("Second argument:", second_arg)

# binding a callback
obs.bind(my_callback, "arg 1", "arg 2")
obs.value = 1
>>> New value: 1
>>> First argument: arg 1
>>> Second argument: arg 2

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
```