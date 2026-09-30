"""Entry #1 — programmatic OpenXE (skeleton; extract needs Runner LM wiring)."""

from openxe import BiMetadata, OpenXE

# Example metadata (power / BI demo)
METADATA = BiMetadata(
    metrics=["售电量"],
    dimensions=[],
    filters={
        "地市": ["南京", "苏州"],
        "年份": ["2025", "2026"],
        "分类": ["乡村居民", "城镇居民"],
    },
    aliases={"居民": ["乡村居民", "城镇居民"]},
)


def main() -> None:
    xe = OpenXE(metadata=METADATA)
    print("OpenXE ready:", xe.metadata.summary_text())
    # Full extract raises NotImplementedError until pipeline.runner is wired:
    # print(xe.extract_dict("南京市2026年居民售电量"))


if __name__ == "__main__":
    main()
