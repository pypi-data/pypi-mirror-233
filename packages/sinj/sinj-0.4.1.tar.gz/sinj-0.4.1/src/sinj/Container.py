import inspect

from .DependencyNotFoundError import DependencyNotFoundError
from .CircularDependencyError import CircularDependencyError
from .DependencyConflictError import DependencyConflictError
from .DependencyNotMappedError import DependencyNotMappedError


def _class_name(cls):
    if hasattr(cls, "__name__"):
        return cls.__name__

    if hasattr(cls, "__class__"):
        if hasattr(cls.__class__, "__name__"):
            return cls.__class__.__name__

    return "-non-class-"


class Container:
    def __init__(self, validator=None):
        self._label_index = dict()  # label -> class
        self._dict_label_index = dict()  # dict_label -> set<label>
        self._resolved = dict()  # (label | dict_label) -> instance
        self._validator = validator

    def register(self, cls, label=None, dict_label=None):
        if label is None:
            if hasattr(cls, "inject"):
                label = cls.inject

        if label is None:
            raise DependencyNotMappedError(f"label not assigned for {_class_name(cls)}")

        if dict_label is None:
            if hasattr(cls, "inject_dict"):
                dict_label = cls.inject_dict

        if isinstance(dict_label, str):
            dict_label = [dict_label]

        if dict_label is None:
            dict_label = []

        if label in self._label_index:
            raise DependencyConflictError(f"label_index conflict for {label}")

        if label in self._dict_label_index:
            raise DependencyConflictError(f"dict_label_index conflict for {label}")

        if label in self._resolved:
            raise DependencyConflictError(f"resolved conflict for {label}")

        for i in dict_label:
            if i in self._label_index:
                raise DependencyConflictError(f"dict_label conflict for {i}")

        for i in dict_label:
            if i not in self._dict_label_index:
                self._dict_label_index[i] = set()

            self._dict_label_index[i].add(label)

        self._label_index[label] = cls

    def resolve(self, label, throw_if_missing=True):
        unresolved = set()
        return self._resolve_recursive(label, throw_if_missing, unresolved)

    def resolve_all(self):
        for label in self._label_index:
            self.resolve(label)
        return self._resolved

    def inject(self, instance, label=None, dict_label=None):
        if label is None:
            if hasattr(instance, "inject"):
                label = instance.inject
        if label is None:
            raise DependencyNotMappedError(
                f"label not assigned for {_class_name(instance)}"
            )

        if dict_label is None:
            if hasattr(instance, "inject_dict"):
                dict_label = instance.inject_dict

        if isinstance(dict_label, str):
            dict_label = [dict_label]

        if dict_label is None:
            dict_label = []

        if label in self._label_index:
            raise DependencyConflictError(f"label_index conflict for {label}")

        if label in self._dict_label_index:
            raise DependencyConflictError(f"dict_label_index conflict for {label}")

        if label in self._resolved:
            raise DependencyConflictError(f"resolved conflict for {label}")

        for i in dict_label:
            if i in self._label_index:
                raise DependencyConflictError(f"dict_label conflict for {i}")

        if label in self._resolved:
            raise DependencyConflictError(f"resolved index conflict for {label}")

        for i in dict_label:
            if i not in self._dict_label_index:
                self._dict_label_index[i] = set()

            self._dict_label_index[i].add(label)

        self._resolved[label] = instance

    def _resolve_recursive(self, label, throw_if_missing, unresolved):
        if label in self._resolved:
            return self._resolved[label]

        if label in unresolved:
            raise CircularDependencyError(f"circular dependency detected for {label}")

        unresolved.add(label)

        if label in self._label_index:
            instance = self._resolve_instance(label, unresolved)
            self._resolved[label] = instance
            unresolved.remove(label)
            return instance

        if label in self._dict_label_index:
            instance = self._resolve_dict(label, unresolved)
            self._resolved[label] = instance
            unresolved.remove(label)
            return instance

        if throw_if_missing:
            raise DependencyNotFoundError(f"could not resolve dependency for {label}")

        return None

    def _resolve_instance(self, label, unresolved):
        cls = self._label_index[label]
        instance = self._instanciate(cls, unresolved)
        return instance

    def _resolve_dict(self, dict_label, unresolved):
        result = dict()
        for i in self._dict_label_index[dict_label]:
            instance = self._resolve_recursive(i, True, unresolved)
            result[i] = instance
        return result

    def _instanciate(self, cls, unresolved):
        sig = inspect.signature(cls)
        args = []
        kwargs = dict()
        for param in sig.parameters.values():
            if param.kind == param.VAR_POSITIONAL:
                continue
            if param.kind == param.VAR_KEYWORD:
                continue

            arg = self._resolve_recursive(param.name, False, unresolved)
            if param.kind == param.POSITIONAL_ONLY:
                if arg is None:
                    raise DependencyNotFoundError(
                        f"could not resolve POSITIONAL_ONLY dependency for {_class_name(cls)} {param.name}"
                    )
                self._validate_arg(arg, param)
                args.append(arg)
                continue

            if (
                param.kind == param.KEYWORD_ONLY
                and param.default is param.empty
                and arg is None
            ):
                raise DependencyNotFoundError(
                    f"could not resolve non default KEYWORD_ONLY dependency for {_class_name(cls)} {param.name}"
                )

            if (
                param.kind == param.POSITIONAL_OR_KEYWORD
                and param.default is param.empty
                and arg is None
            ):
                raise DependencyNotFoundError(
                    f"could not resolve non default POSITIONAL_OR_KEYWORD dependency for {_class_name(cls)} {param.name}"
                )

            if arg is not None:
                self._validate_arg(arg, param)
                kwargs[param.name] = arg
                continue

        instance = cls(*args, **kwargs)
        return instance

    def _validate_arg(self, arg, param):
        if self._validator is None:
            return

        self._validator.validate(arg, param)
