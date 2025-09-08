from __future__ import annotations
from typing import Any



from typing import Any

from langchain_core.prompts.string import (
    DEFAULT_FORMATTER_MAPPING,

)
from langchain_core.runnables.config import RunnableConfig
from langchain_core.prompts import PromptTemplate


class ExtendedPromptTemplate(PromptTemplate):
    """PromptTemplate с дополнительной обработкой плейсхолдеров во вложенных partial_variables. Короче сначала рендерим partial_variables, input_variables, чтобы 
    можно было использовать input_variables в partial_variables."""

    def format(self, **kwargs: Any) -> str:
        """
        Расширенный метод:
        1) Сливает partial_variables и пользовательские переменные.
        2) Заново рендерит строки, находящиеся в partial_variables, если в них остались плейсхолдеры.
        3) Формирует итоговую строку из основного self.template.
        """

        # Шаг 1. Собираем все переменные (partial + пользовательские).
        merged_kwargs = self._merge_partial_and_user_variables(**kwargs)

        # Шаг 2. Проходимся по результату и рендерим все строки, 
        #        в которых ещё могут быть плейсхолдеры (например, {Lexical}).
        #        Особенно это актуально для тех, что пришли из partial_variables.
        rendered_kwargs = {}
        for key, value in merged_kwargs.items():

            if str(key).startswith("format"):
                rendered_kwargs[key] = value
            
            elif isinstance(value, str):
                    # Вызовем тот же форматтер, что и для основного template
                    # чтобы подставить значения из merged_kwargs.
                    rendered_value = DEFAULT_FORMATTER_MAPPING[self.template_format](
                        value, **merged_kwargs
                    )
                    rendered_kwargs[key] = rendered_value
            else:
                rendered_kwargs[key] = value

        # Шаг 3. Теперь рендерим финальный шаблон self.template,
        #        где уже "подрендеренные" partial переменные.
        return DEFAULT_FORMATTER_MAPPING[self.template_format](
            self.template, **rendered_kwargs
        )

    def format_noargs(self) -> str:
        """
        Форматирует шаблон, используя только доступные переменные из partial_variables.
        Если для какого-либо плейсхолдера нет значения, он остается в строке без изменений.
        """
        # Используем только partial_variables
        merged_kwargs = self._merge_partial_and_user_variables()
        
        # SafeDict возвращает placeholder в виде {ключ}, если ключ отсутствует.
        class SafeDict(dict):
            def __missing__(self, key):
                return "{" + key + "}"

        # Рендерим переменные из partial_variables с безопасным форматированием.
        rendered_kwargs = {}
        for key, value in merged_kwargs.items():
            if str(key).startswith("format"):
                rendered_kwargs[key] = value
            elif isinstance(value, str):
                # Используем метод format_map с SafeDict, чтобы избежать KeyError.
                rendered_kwargs[key] = value.format_map(SafeDict(merged_kwargs))
            else:
                rendered_kwargs[key] = value

        # Форматируем основной шаблон с безопасным форматированием.
        return self.template.format_map(SafeDict(rendered_kwargs))