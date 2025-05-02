"""
* Module Name: CTempFile
* Methods : clear_temp_files() delete_files_in_directory()
"""

from pathlib import Path
import os
import shutil

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn

def delete_files_in_directory(directory):
    """删除指定目录中的所有文件和子目录，并显示进度"""
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
                progress.update(task, advance=1, description=f"[bold red]清理单个文件时出现错误: [red]{path.name}: {str(e)}")

def clear_temp_files():
    """清理系统临时目录"""
    temp_dir1 = Path(os.environ["TEMP"])  # 正确获取环境变量
    temp_dir2 = Path("C:/Windows/Temp")

    delete_files_in_directory(temp_dir1)
    delete_files_in_directory(temp_dir2)

if __name__ == '__main__':
    clear_temp_files()
