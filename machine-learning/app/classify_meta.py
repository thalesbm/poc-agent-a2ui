"""
Classifica cada item do dataset em:
- sensitivity: neutro | sensível | crítico
- complexity: baixo | médio | alto
"""
from __future__ import annotations

import re
from typing import Any


# --- Sensitivity: crítico (check first) ---
SENSITIVITY_CRITICO_PATTERNS = [
    r"encerrar\s+conta",
    r"reset\s+(de\s+)?senha",
    r"troca\s+de\s+dispositivo\s+confi[aá]vel",
    r"desbloqueio",
    r"recupera[cç][aã]o\s+de\s+conta",
    r"open\s+finance",
    r"revogar\s+consentimento",
    r"conceder\s+consentimento",
    r"autoriza[cç][oõ]es",
    r"procura[cç][oõ]es",
    r"revogar\s+chaves?\s+pix",
    r"remessa\s+internacional",
    r"c[aâ]mbio",
    r"chargeback",
    r"contesta[cç][aã]o",
    r"fraude",
    r"suspeita\s+de\s+fraude",
    r"token\s+.*\s+seguran[cç]a",
    r"bloqueio\s+de\s+seguran[cç]a",
]

# --- Sensitivity: sensível (movimentação, cancelamento, auth) ---
SENSITIVITY_SENSIVEL_PATTERNS = [
    r"cancelar",
    r"cancelamento",
    r"pagar",
    r"transferir",
    r"investir",
    r"resgatar",
    r"cadastrar\s+favorecido",
    r"alterar\s+limite",
    r"alterar\s+cadastr",
    r"autentica[cç][aã]o\s+forte",
    r"biometria",
    r"token\s*[\/\(]",
    r"cpf",
    r"ag[eê]ncia\s*\/\s*conta",
    r"dados\s+pessoais",
]

# Category -> default sensitivity when no critical/sensitive text override
CATEGORY_NEUTRO = {"consultar", "visualizar", "informar"}
CATEGORY_SENSIVEL = {"cancelar", "pagar", "transferir", "investir", "resgatar", "comprar"}


# --- Complexity: rule classes (count distinct types) ---
COMPLEXITY_RULE_PATTERNS = [
    (r"autentica[cç][aã]o|biometria|token", "auth"),
    (r"confirma[cç][aã]o|confirme|revisar", "confirmacao"),
    (r"impacto|tarifa|cobran[cç]a", "impacto"),
    (r"prazo|vencimento|d\+n|d\+\d", "prazo"),
    (r"limite|pix\s+noturno|diurno", "limite"),
    (r"car[eê]ncia", "carencia"),
    (r"imposto|ir\s+sobre|iof|tributa[cç][aã]o", "imposto"),
    (r"hor[aá]rio\s+de\s+corte|liquida[cç][aã]o|cotiza[cç][aã]o", "mercado"),
    (r"suitability|elegibilidade|an[aá]lise\s+de\s+perfil", "elegibilidade"),
    (r"ordem\s+limitada|stop|oco|mercado", "tipos_ordem"),
    (r"pr[oó]-rata|marca[cç][aã]o\s+a\s+mercado", "regras_invest"),
]


def _extract_text_from_item(item: dict[str, Any]) -> str:
    """Concatena título, subtítulo, texto e keys/values de listas em uma string."""
    parts: list[str] = []
    meta = item.get("meta_info") or {}
    category = (meta.get("category") or "").strip().lower()
    parts.append(category)

    su = item.get("surface_update") or {}
    components = su.get("components") or []
    for comp in components:
        c = comp.get("component") or {}
        ctype = (c.get("type") or "").strip().lower()
        data = c.get("data") or {}
        if ctype == "header":
            parts.append((data.get("title") or "").strip())
            parts.append((data.get("subtitle") or "").strip())
        elif ctype == "text":
            parts.append((data.get("text") or "").strip())
        elif ctype == "informative":
            parts.append((data.get("title") or "").strip())
            parts.append((data.get("subtitle") or "").strip())
            parts.append(str(data.get("value", "")))
        elif ctype == "list":
            for list_item in data.get("items") or []:
                parts.append(str(list_item.get("key", "")))
                parts.append(str(list_item.get("value", "")))
    return " ".join(parts).lower()


def _count_components_and_lists(item: dict[str, Any]) -> tuple[int, int]:
    """Retorna (número de componentes de conteúdo, maior tamanho de lista)."""
    su = item.get("surface_update") or {}
    components = su.get("components") or []
    content_types = {"header", "text", "list", "informative"}
    content_count = 0
    max_list_items = 0
    for comp in components:
        c = comp.get("component") or {}
        ctype = (c.get("type") or "").strip().lower()
        if ctype in content_types:
            content_count += 1
        if ctype == "list":
            data = c.get("data") or {}
            items = data.get("items") or []
            max_list_items = max(max_list_items, len(items))
    return content_count, max_list_items


def _count_rule_classes(text: str) -> int:
    """Conta quantas classes de regras aparecem no texto."""
    found: set[str] = set()
    for pattern, tag in COMPLEXITY_RULE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            found.add(tag)
    return len(found)


def classify_sensitivity(item: dict[str, Any]) -> str:
    """Retorna 'neutro' | 'sensível' | 'crítico'."""
    text = _extract_text_from_item(item)
    meta = item.get("meta_info") or {}
    category = (meta.get("category") or "").strip().lower()

    for pat in SENSITIVITY_CRITICO_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return "crítico"

    if category in CATEGORY_SENSIVEL:
        return "sensível"

    for pat in SENSITIVITY_SENSIVEL_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return "sensível"

    if category in CATEGORY_NEUTRO:
        return "neutro"

    return "sensível"


def classify_complexity(item: dict[str, Any]) -> str:
    """Retorna 'baixo' | 'médio' | 'alto'."""
    text = _extract_text_from_item(item)
    content_count, max_list_items = _count_components_and_lists(item)
    rule_classes = _count_rule_classes(text)

    if content_count >= 7 or max_list_items >= 9 or rule_classes >= 3:
        return "alto"
    if content_count >= 4 or max_list_items >= 4 or rule_classes >= 1:
        return "médio"
    return "baixo"


def add_meta_labels_to_item(item: dict[str, Any]) -> None:
    """Adiciona meta_info.complexity e meta_info.sensitivity ao item (in-place)."""
    if "meta_info" not in item:
        item["meta_info"] = {}
    item["meta_info"]["sensitivity"] = classify_sensitivity(item)
    item["meta_info"]["complexity"] = classify_complexity(item)


def add_meta_labels_to_list(items: list[dict[str, Any]]) -> None:
    """Adiciona labels a cada item da lista (in-place)."""
    for it in items:
        add_meta_labels_to_item(it)
