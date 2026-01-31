"""Aplica meta_info.sensitivity e meta_info.complexity a um JSON do dataset."""
import json
import sys
from pathlib import Path

from classify_meta import add_meta_labels_to_list

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset"


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python add_meta_to_file.py <arquivo.json>")
        print("Ex.: python add_meta_to_file.py produtos_cancelar_50.json")
        sys.exit(1)
    name = sys.argv[1]
    path = DATASET_DIR / name if not Path(name).is_absolute() else Path(name)
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print("Arquivo não é uma lista de itens.")
        sys.exit(1)
    add_meta_labels_to_list(data)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Atualizado: {path} ({len(data)} itens)")


if __name__ == "__main__":
    main()
