"""Entry #1 — programmatic OpenXE (skeleton; extract needs Runner LM wiring)."""

from pathlib import Path

from openxe import BiMetadata, OpenXE

# Full warehouse / product catalog
METADATA = BiMetadata(
    metrics=["售电量", "电费", "负荷"],
    dimensions=["地市", "行业"],
    filters={
        "地市": ["南京", "苏州"],
        "年份": ["2024", "2025", "2026"],
        "分类": ["乡村居民", "城镇居民"],
        "行业": ["工业", "商业"],
    },
    aliases={"居民": ["乡村居民", "城镇居民"]},
)

# Optional business-rule graph: scopes which catalog names the model may see
KG_PATH = Path(__file__).resolve().parent / "testdata" / "knowledge_graph.xlsx"


def main() -> None:
    xe = OpenXE(metadata=METADATA, knowledge_graph=KG_PATH)
    print("OpenXE ready")
    print("  effective metadata:", xe.metadata.summary_text())
    print("  knowledge_graph:", xe.knowledge_graph is not None)


if __name__ == "__main__":
    main()
