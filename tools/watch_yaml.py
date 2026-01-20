from __future__ import annotations

import time
import threading
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = Path("src/mongens/data")
VALIDATE_CMD = [".venv/Scripts/python.exe", "tools/validate_yaml.py"]

OUT_DIR = Path("output")
OUT_FILE = OUT_DIR / "last_validation.txt"

DEBOUNCE_SECONDS = 0.75


class DebouncedRunner:
    def __init__(self, debounce_seconds: float):
        self.debounce_seconds = debounce_seconds
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None
        self._last_path: str | None = None

    def trigger(self, changed_path: str) -> None:
        with self._lock:
            self._last_path = changed_path
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce_seconds, self._run)
            self._timer.daemon = True
            self._timer.start()

    def _run(self) -> None:
        with self._lock:
            changed = self._last_path
            self._last_path = None
            self._timer = None

        OUT_DIR.mkdir(exist_ok=True)
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            proc = subprocess.run(
                VALIDATE_CMD,
                cwd=Path("."),
                capture_output=True,
                text=True,
            )
            stdout = (proc.stdout or "").strip()
            stderr = (proc.stderr or "").strip()
            ok = proc.returncode == 0
        except Exception as e:
            ok = False
            stdout = ""
            stderr = f"Watcher failed to run validator: {e}"
            proc = None

        status = "PASS" if ok else "FAIL"
        lines = [
            f"[{stamp}] {status}",
            f"Changed: {changed}",
            "",
        ]
        if stdout:
            lines += ["--- stdout ---", stdout, ""]
        if stderr:
            lines += ["--- stderr ---", stderr, ""]
        lines += [f"ExitCode: {0 if ok else (proc.returncode if proc else 999)}", ""]

        OUT_FILE.write_text("\n".join(lines), encoding="utf-8")

        # Keep terminal output minimal
        print(f"[watch_yaml] {status} -> {OUT_FILE}")


runner = DebouncedRunner(DEBOUNCE_SECONDS)


class Handler(FileSystemEventHandler):
    def _maybe(self, path: str) -> None:
        p = path.lower()
        if p.endswith((".yaml", ".yml")):
            runner.trigger(path)

    def on_modified(self, event):
        if not event.is_directory:
            self._maybe(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._maybe(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._maybe(getattr(event, "dest_path", event.src_path))


def main() -> int:
    if not WATCH_DIR.exists():
        print(f"[watch_yaml] WATCH_DIR not found: {WATCH_DIR.resolve()}")
        return 2

    observer = Observer()
    observer.schedule(Handler(), str(WATCH_DIR), recursive=True)
    observer.start()
    print(f"[watch_yaml] Watching: {WATCH_DIR.resolve()} (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[watch_yaml] Stopping...")
        observer.stop()
    observer.join()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
