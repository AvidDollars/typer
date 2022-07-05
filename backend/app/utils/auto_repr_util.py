__all__ = ("auto_repr", )


def auto_repr(cls=None, **kwargs):
    """
    class decorator factory to be used as automatic custom "__repr__" method provider
        - provides string representation of an instance based on its items in self.__dict__
        - does not work for instances with __slots__ (__dict__ attribute is missing)

    basic usage -> no fields are hidden or excluded:

        @auto_repr
        class Test:
            ...

    second usage -> hides or excludes values

        @auto_repr(hide="password", exclude="not_important")
        class Test:
            ...

    third usage -> arguments can be also specified in sequence types (e.g. tuple or list)

        @auto_repr(hide=("password", "api_key"), exclude=("not_important", "lol"))
        class Test:
            ...
    """

    def inner(cls):
        cls.__repr__ = add_repr
        return cls

    def add_repr(self) -> str:
        class_name = type(self).__name__

        stats = ", ".join(
            f"{key}={value if key not in kwargs['hide'] else '<hidden>'}"
            for key, value
            in vars(self).items()
            if key not in kwargs["exclude"]
        )
        return f"{class_name}({stats})"

    kwargs = normalize_kwargs(**kwargs)

    # if called as @auto_repr
    if cls is not None and callable(cls):
        cls.__repr__ = add_repr
        return cls

    # if called as @auto_repr(<optional_content>)
    else:
        return inner


def normalize_kwargs(**kwargs):
    exclude_content = kwargs.get("exclude", ())
    hide_content = kwargs.get("hide", ())

    if exclude_content and isinstance(exclude_content, str):
        exclude_content = (exclude_content, )  # making one item tuple

    if hide_content and isinstance(hide_content, str):
        hide_content = (hide_content, )

    return {"exclude": exclude_content, "hide": hide_content}
