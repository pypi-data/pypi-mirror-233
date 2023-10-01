import inspect

from .TypeValidatorError import TypeValidatorError

import logging

logger = logging.getLogger(__name__)


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
