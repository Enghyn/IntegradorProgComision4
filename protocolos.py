from typing import Protocol


class Exportable(Protocol):
    def exportar(self) -> str: ...


def exportar_todo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]