"""
* PixelCleaner v1.0.0
* Created by 写代码的bow@bilibili.com
* Published GitHub
"""

import os
import ctypes
import psutil
import winsound
from rich import print
from rich.console import Console
from CTempFile import clear_temp_files
from CRecycleBin import clear_recycle_bin
from ScanLargeFiles import scan_large_files
from CWinUpdate import clear_update_cache

console = Console(force_terminal=True, color_system="truecolor")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def calc_disk_space():
    disk_usage = psutil.disk_usage(f'{os.getcwd().split(":")[0]}:\\')
    used_space_gb = disk_usage.used / (1024 ** 3)

    return f"{used_space_gb:.4f} GiB"

def calc_disk_free():
    disk_usage = psutil.disk_usage(f'{os.getcwd().split(":")[0]}:\\')
    free_space_gb = disk_usage.free / (1024 ** 3)

    return f"{free_space_gb:.4f} GiB"

def mainloop():
    console.print("[bold green]Welcome to PixelCleaner[/bold green]")
    console.print("[bold blue]Version 1.0.0[/bold blue]")
    console.print("[bold yellow]Created by 写代码的bow@bilibili.com[/bold yellow]")
    console.print(f"[bold magenta]你好，{os.getlogin()}，欢迎使用 PixelCleaner，开始你的清理之旅吧！[/bold magenta]")
    console.print("[bold purple]请确认是否以管理员身份运行程序[/bold purple]")
    print()

    while 1:
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
        console.print(f"[yellow]当前主分区({os.getcwd().split(':')[0]}:)已用空间：{calc_disk_space()}"
              f"\n剩余空间：{calc_disk_free()}[/yellow]")
        print()
        console.print("[bold cyan]请选择清理方式：[/bold cyan]")
        console.print("[bold green]1.[/bold green][bold blue]清理缓存文件[/bold blue]")
        console.print("[bold green]2.[/bold green][bold blue]彻底删除回收站内容[/bold blue]")
        console.print("[bold green]3.[/bold green][bold blue]大文件扫描[/bold blue]")
        console.print("[bold green]4.[/bold green][bold blue]清理Windows更新[/bold blue]")
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
        else:
            console.print("[bold red]输入错误，请重新输入[/bold red]")
            print()

if __name__ == '__main__':
    try:
        mainloop()
    except KeyboardInterrupt:
        console.print("\n[bold red]程序已终止[/bold red]")
