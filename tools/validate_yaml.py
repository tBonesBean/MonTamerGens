from __future__ import annotations


def main() -> int:
    try:
        # Your data module already loads + validates at import time.
        import mongens.data  # noqa: F401
    except Exception as e:
        print("YAML validation failed\n")
        print(e)
        return 1

    print("YAML validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
