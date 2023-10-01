
# 💉 sinj

`sinj` (**S**imple **Inj**ect) is yet another IoC framework for python. If you try to avoid global variables and singletons you might end up with a complex graph of dependencies in your application. With `sinj` everything is just flat. If you are coming from Java or C# you might be more familiar with IoC frameworks where dependencies are resolved by interface. In python we do not have interfaces and strict types so here we resolve dependencies by constructor argument names or "inject labels".

# Basic usage and examples

```python
import sinj
c = sinj.Container() # create dependencies container
c.register(SomeClass, "some_class") # add labeled class into container
c.resolve("some_class") # resolve instance by given label
c.inject(some_instance, "some_instance") # add resolved instance to an index
```


The simplest example:

```python
import sinj

class A:
    def a(self):
        return "a"

class B:
    def __init__(self, a):
        self._a = a
    
    def b(self):
        return self._a() + " b"

ioc_container = sinj.Container()
ioc_container.register(A, "a")
ioc_container.register(B, "b")

b = ioc_container.resolve("b")
print(b.b()) # -> "a b"
```

The same example with annotated classes:

```python
import sinj

class A:
    inject = "a" # this label will be used to resolve instance of A
    def a(self):
        return "a"

class B:
    inject = "b" # this label will be used to resolve instance of B
    def __init__(self, a): # instance of A is injected here
        self._a = a
    
    def b(self):
        return self._a() + " b"

ioc_container = sinj.Container()
ioc_container.register(A) # no need to specify label here
ioc_container.register(B) # but you can overwrite it if you want

b = ioc_container.resolve("b")
print(b.b()) # -> "a b"
```

More examples will be available in `./examples`


# Errors


- `sinj.DependencyNotFoundError` - thrown on `resolve` when dependency is not found for a given label (and it is not optional).
- `sinj.CircularDependencyError` - thrown on `resolve` when circular dependency is detected.
- `sinj.DependencyConflictError` - thrown on `register` or `inject` when the container already has something by the label.
- `sinj.DependencyNotMappedError` - thrown on `register` or `inject` when the class is not annotated and the label is not provided in register method.


# Validating types

You have an option to pass a validator into `sinj.Container` to check injected types. `sinj` has a simple built in validator which is able to log warnings or raise errors. You can create more complicated validators if you want, it is just a class with `validate(self, instance, param: inspect.Parameter):` method:

```python

class TypeValidator:
    def __init__(self, log_warning=True, raise_error=False):
        self._log_warning = log_warning
        self._raise_error = raise_error

    def validate(self, instance, param: inspect.Parameter):
        err_msg = self._get_err_msg(instance, param)
        if err_msg is None:
            return

        if self._log_warning:
            logger.warning(err_msg)

        if self._raise_error:
            raise TypeValidatorError(err_msg)

    def _get_err_msg(self, instance, param: inspect.Parameter):
        if not hasattr(instance, "__class__"):
            return f"could not determine class of instance for {param.name}"

        if param.annotation == param.empty:
            return None

        if not inspect.isclass(param.annotation):
            return f"param annotated with a non-class for {param.name}"

        if not issubclass(instance.__class__, param.annotation):
            return f"instance is not derived from annotated type for {param.name}"

        return None

ioc_container = sinj.Container(validator=TypeValidator(True, True))
```


# Install


### From [pypi.org](https://pypi.org/project/sinj/)

```bash
pip install sinj
```

### From [repository](https://gitlab.com/mrsk/sinj)

```bash
pip install git+https://gitlab.com/mrsk/sinj
```

