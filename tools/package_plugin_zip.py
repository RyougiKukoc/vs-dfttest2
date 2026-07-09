from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "dfttest2"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Create a DFTTest2 plugin package zip.")
    parser.add_argument("--input-dir", default=str(ROOT / "dist" / "windows"))
    parser.add_argument("--output", default=str(ROOT / "dist" / "dfttest2-cu121-win64.zip"))
    args = parser.parse_args(argv)

    input_dir = Path(args.input_dir).resolve()
    output = Path(args.output).resolve()
    package_dir = input_dir / PLUGIN_NAME
    required = [
        package_dir / "dfttest2_cpu.dll",
        package_dir / "dfttest2_nvrtc.dll",
        package_dir / "manifest.vs",
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(path)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(input_dir))

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

