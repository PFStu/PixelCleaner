"""
* Module Name: CLogFile.py
* Methods : clear_log_files()
"""

import os
import glob
from pathlib import Path
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TaskProgressColumn

def clear_log_files():
    user_profile = Path(os.environ['USERPROFILE'])
    log_files = [
        Path("C:\\Windows\\WindowsUpdate.log"),
        *[Path(p) for p in glob.glob(str(user_profile / "**" / "*.log"), recursive=True)]
    ]

    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        transient=True
    ) as progress:
        for log_path in log_files:
            current_file = progress.add_task(f"清理日志文件: {log_path.name}", total=100)

            try:
                if not log_path.exists():
                    progress.console.print(f"[yellow]文件不存在: {log_path.name}[/]")
                    progress.remove_task(current_file)
                    continue

                file_size = log_path.stat().st_size
                progress.update(current_file, total=file_size, description=f"清理日志文件: {log_path.name}")

                with log_path.open('w') as f:
                    f.truncate()

                progress.update(current_file, advance=file_size)
                progress.console.print(f"[green]已清理: {log_path.name}[/]")

            except PermissionError:
                progress.console.print(f"[red]权限不足: {log_path.name}[/]")
            except Exception as e:
                progress.console.print(f"[red]错误: ({type(e).__name__}): {log_path.name}[/]")
            finally:
                progress.remove_task(current_file)

if __name__ == "__main__":
    clear_log_file()
