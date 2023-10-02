
import os
import re
from abc import ABC

from pydantic import BaseModel, root_validator


def _get_env_name_by_field_name(class_name: str, field_name: str) -> str:
    """
    Generate the environment variable name based on the class name and field name.

    This function is used when defining a custom configuration class that extends BaseConfig
    or any other BaseConfig extended class, in order to use different names for environment
    variables for them.

    :param class_name: The name of the class.
    :type class_name: str
    :param field_name: The name of the field.
    :type field_name: str
    :return: The environment variable name generated based on the class name and field name.
    :rtype: str
    """
    return "_".join(
        [
            i.replace("_", "").upper()
            for i in re.findall(
                r"[A-ZА-Я_][a-zа-я\d]*",
                f'{class_name.replace("Config", "")}_{field_name}'
            )
         ],
    )


def _get_field_form_env(
    *,
    class_name: str | None = None,
    field_name: str | None = None,
    env_name: str | None = None
) -> any:  # type: ignore[valid-type]
    """
    Get the value of a field from the environment variables.

    If the `env_name` parameter is provided, it returns the value of the corresponding
    environment variable.
    If the `class_name` and `field_name` parameters are provided, it generates the
    environment variable name using
    `_get_env_name_by_field_name` function and returns the value of the corresponding
    environment variable.

    :param class_name: The name of the class.
    :type class_name: str, optional
    :param field_name: The name of the field.
    :type field_name: str, optional
    :param env_name: The name of the environment variable.
    :type env_name: str, optional
    :return: The value of the field from the environment variables.
    :rtype: any
    :raises TypeError: If the key type for the variable is invalid.
    """
    if isinstance(env_name, str):
        return os.getenv(env_name)
    elif isinstance(class_name, str) and isinstance(field_name, str):
        return os.getenv(_get_env_name_by_field_name(class_name, field_name))
    else:
        raise TypeError("Invalid key type for variable")


class BaseConfig(BaseModel, ABC):
    """
    Provides to receive values from the environment variables on the validation step of
    pydantic model.
    """

    @root_validator(pre=True)
    def _change_form_env_if_none(cls, values: dict) -> dict:
        """
        This function checks if any value in the 'values' dictionary is None.
        If a value is None, it retrieves the value from the environment variables
        based on the class name and field name.

        :param cls: The class that the function is called on.
        :type cls: type
        :param values: The dictionary of values to check and update.
        :type values: dict
        :return: The updated dictionary of values that will be stored in config instance.
        :rtype: dict
        """
        for k, field in cls.model_fields.items():
            if values.get(k) is None:
                value = _get_field_form_env(
                    class_name=cls.__name__,
                    field_name=k,
                    env_name=(field.json_schema_extra
                              or {}).get("env_name")  # type: ignore[union-attr]
                )
                if value is not None:
                    values[k] = value

        return values
