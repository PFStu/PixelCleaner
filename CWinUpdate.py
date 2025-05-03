"""
* Module Name : CWinUpdate.py
* Methods : clear_update_cache()
"""

import os
import shutil
from pathlib import Path
import psutil

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn
from rich.console import Console

def delete_files_in_directory(directory):
    console = Console()
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
    ) as progress:
        # 获取所有文件和目录（包括子目录）
        file_list = list(directory.glob("**/*"))
        task = progress.add_task("[bold red]删除文件...", total=len(file_list))

        for path in file_list:
            try:
                if path.is_file():
                    os.remove(path)
                elif path.is_dir():
                    shutil.rmtree(path)
                progress.update(task, advance=1, description=f"[bold red]清理中... [bold green]{path.name}")
            except Exception as e:
                progress.update(task, advance=1, description=f"[bold red]清理失败 [red]{path.name}: {str(e)}")

def clear_update_cache():
    console = Console()

    update_cache_dir = (Path(os.getenv("SystemDrive") + "\\$Windows.~WS"), Path(os.getenv("SystemDrive") + "\\$Windows.~LS"))

    for path in update_cache_dir:
        if path.exists() and path.is_dir():
            console.print(f"[bold yellow]正在清理更新缓存目录: {update_cache_dir}[/bold yellow]")
            delete_files_in_directory(path)
        else:
            console.print(f"[bold green]更新缓存目录不存在或不是目录: {path}[/bold green]")

if __name__ == '__main__':
    clear_update_cache()
