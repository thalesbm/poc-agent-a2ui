import json
from pathlib import Path
from typing import Any

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset"

def load_all_datasets(
    directory: str | Path | None = None,
    pattern: str = "*.json",
) -> dict[str, Any]:
    """Carrega todos os arquivos da pasta dataset. Retorna um dict nome_arquivo -> conteúdo."""
    dir_path = Path(directory) if directory else DATASET_DIR
    if not dir_path.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {dir_path}")
    result: dict[str, Any] = {}
    for file_path in sorted(dir_path.glob(pattern)):
        with open(file_path, encoding="utf-8") as f:
            result[file_path.name] = json.load(f)
    return result


def main() -> None:
    datasets = load_all_datasets()
    print(f"Arquivos carregados: {len(datasets)}")
    for name, data in datasets.items():
        n = len(data) if isinstance(data, list) else "(objeto)"
        print(f"  - {name}: {n} registros")
        if isinstance(data, list) and data:
            item = data[0]
            meta = item.get("meta_info", {})
            print(f"    exemplo: category={meta.get('category')}, agent_id={meta.get('agent_id')}")


if __name__ == "__main__":
    main()
