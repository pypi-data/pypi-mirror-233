import inspect
import json
from types import ModuleType

from functional_cat import data_types, interfaces


def process_module(module: ModuleType, out_path: str):
    tasks = []
    for class_name in module.__all__:
        cls = getattr(module, class_name)
        start_line = inspect.findsource(cls)[1] + 1
        tasks.append(
            {
                "class": f"{module.__name__}.{class_name}",
                "lineOfDef": start_line,
                "description": inspect.cleandoc(cls.__doc__).replace("\n", " ")
                if cls.__doc__ is not None
                else "",
                "filePath": module.__name__.replace(".", "/") + ".py",
            }
        )

    with open(out_path, "w") as f:
        json.dump(tasks, f, indent=2)


if __name__ == "__main__":
    process_module(interfaces, "src/tasks.json")
    process_module(data_types, "src/types.json")
