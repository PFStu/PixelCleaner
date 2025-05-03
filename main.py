"""
* PixelCleaner v1.0.0
* Created by 写代码的bow@bilibili.com
"""

import os
import ctypes
import time

import psutil
import winsound

from rich.table import Table
from rich.progress_bar import ProgressBar
from rich.style import Style

from rich import print
from rich.console import Console
from CTempFile import clear_temp_files
from CRecycleBin import clear_recycle_bin
from ScanLargeFiles import scan_large_files
from CWinUpdate import clear_update_cache
from CLogFile import clear_log_files

console = Console(force_terminal=True, color_system="truecolor")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

# def calc_disk_space():
#     disk_usage = psutil.disk_usage(f'{os.getcwd().split(":")[0]}:\\')
#     used_space_gb = disk_usage.used / (1024 ** 3)
#
#     return f"{used_space_gb:.4f} GiB"
#
# def calc_disk_free():
#     disk_usage = psutil.disk_usage(f'{os.getcwd().split(":")[0]}:\\')
#     free_space_gb = disk_usage.free / (1024 ** 3)
#
#     return f"{free_space_gb:.4f} GiB"


def format_size(bytes):
    """将字节转换为易读的单位（如 GB/TB）"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} PB"

def get_disk_usage():
    """获取所有磁盘分区的使用情况"""
    partitions = psutil.disk_partitions(all=False)
    usage_list = []
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            usage_list.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except PermissionError:
            continue  # 跳过无权限访问的分区
    return usage_list

def display_disk_table():
    disks = get_disk_usage()

    # 创建带样式的表格
    table = Table(title="[bold cyan]磁盘占用情况[/]", show_header=True, header_style="bold magenta")
    table.add_column("分区", style="cyan", no_wrap=True)
    table.add_column("挂载点", style="blue")
    table.add_column("总空间", justify="right")
    table.add_column("已用空间", justify="right")
    table.add_column("剩余空间", justify="right")
    table.add_column("占用率", justify="center")
    table.add_column("进度", justify="full")

    for disk in disks:
        # 动态颜色逻辑
        if disk["percent"] >= 80:
            style = Style(color="red", bold=True)
        elif disk["percent"] >= 50:
            style = Style(color="yellow", bold=True)
        else:
            style = Style(color="green", bold=True)

        # 添加进度条
        progress = ProgressBar(
            total=100,
            completed=disk["percent"],
            width=20,
            style="bar.back",
            complete_style=style,
            pulse_style=style
        )

        # 填充表格行
        table.add_row(
            disk["device"],
            disk["mountpoint"],
            format_size(disk["total"]),
            f"[red]{format_size(disk['used'])}[/]",
            f"[green]{format_size(disk['free'])}[/]",
            f"{disk['percent']}%",
            progress
        )

    console.print(table)

def mainloop():
    console.print("[bold green]Welcome to PixelCleaner[/bold green]")
    console.print("[bold blue]Version 1.0.0[/bold blue]")
    console.print("[bold yellow]Created by 写代码的bow@bilibili.com[/bold yellow]")
    console.print(f"[bold magenta]({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})你好，{os.getlogin()}，欢迎使用 PixelCleaner，开始你的清理之旅吧！[/bold magenta]")
    console.print("[bold purple]请确认是否以管理员身份运行程序[/bold purple]")
    print()

    while 1:
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
        display_disk_table()
        print()
        console.print("[bold cyan]请选择清理方式：[/bold cyan]")
        console.print("[bold green]1.[/bold green][bold blue]清理缓存文件[/bold blue]")
        console.print("[bold green]2.[/bold green][bold blue]彻底删除回收站内容[/bold blue]")
        console.print("[bold green]3.[/bold green][bold blue]大文件扫描[/bold blue]")
        console.print("[bold green]4.[/bold green][bold blue]清理Windows更新[/bold blue]")
        console.print("[bold green]5.[/bold green][bold blue]清理日志文件[/bold blue]")
        print()
        choice = input("请输入数字：")
        if choice == "1":
            try:
                clear_temp_files()
                print()
            except Exception as e:
                console.print(f"Error clearing temp files: {e}")
                print()
        elif choice == "2":
            try:
                clear_recycle_bin()
                console.print("[bold green]回收站清理完成！[/bold green]")
            except Exception as e:
                console.print(f"Error clearing recycle bin: {e}")
                print()
        elif choice == "3":
            try:
                console.print("[bold green]注意：扫描大文件可能需要较长时间，可另外开一个Shell进行扫描[/bold green]")

                drive_path = input("请输入要扫描的路径（例如：D:\\，C:\\Users）")
                if not os.path.exists(drive_path):
                    print("[bold red]输入路径不存在，请重新输入[/bold red]")
                    print()
                    continue

                file_size = input("[bold yellow]请输入要扫描的文件大小（单位：MB）[/bold yellow]")
                if not file_size.isdigit():
                    print("[bold red]输入文件大小格式错误，请重新输入[/bold red]")
                    print()
                    continue

                scan_large_files(drive_path, int(file_size), 2147483647)
                print()
            except Exception as e:
                print(f"Error scanning large files: {e}")
                print()
        elif choice == "4":
            try:
                clear_update_cache()
                console.print("[bold green]Windows更新缓存清理完成！[/bold green]")
            except Exception as e:
                console.print(f"Error clearing Windows update cache: {e}")
                print()
        elif choice == "5":
            try:
                clear_log_files()
                console.print("[bold green]日志文件清理完成！[/bold green]")
            except Exception as e:
                console.print(f"Error clearing log files: {e}")
                print()
        else:
            console.print("[bold red]输入错误，请重新输入[/bold red]")
            print()

if __name__ == '__main__':
    try:
        mainloop()
    except KeyboardInterrupt:
        console.print("\n[bold red]程序已终止[/bold red]")
    except Exception as e:
        console.print(f"[bold red]:( 发生了一些错误：{e}[/bold red]")