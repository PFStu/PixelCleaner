"""
* PixelCleaner v1.0.0
* Created by 写代码的bow@bilibili.com
* Published GitHub
"""

import os
import ctypes
from rich import print
from CTempFile import clear_temp_files
from CRecycleBin import clear_recycle_bin

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def mainloop():
    print("[bold green]Welcome to PixelCleaner[/bold green]")
    print("[bold blue]Version 1.0.0[/bold blue]")
    print("[bold yellow]Created by 写代码的bow@bilibili.com[/bold yellow]")
    print(f"[bold magenta]你好，{os.getlogin()}，欢迎使用 PixelCleaner，开始你的清理之旅吧！[/bold magenta]")
    print("[bold purple]请确认是否以管理员身份运行程序[/bold purple]")

    while 1:
        print("[bold cyan]请选择清理方式：[/bold cyan]")
        print("[bold green]1.[/bold green][bold blue]清理缓存文件[/bold blue]")
        print("[bold green]2.[/bold green][bold blue]彻底删除回收站内容[/bold blue]")
        print()
        choice = input("请输入数字：")
        if choice == "1":
            try:
                clear_temp_files()
                print()
            except Exception as e:
                print(f"Error clearing temp files: {e}")
                print()
        elif choice == "2":
            try:
                clear_recycle_bin()
                print("[bold green]回收站清理完成！[/bold green]")
            except Exception as e:
                print(f"Error clearing recycle bin: {e}")
                print()
        else:
            print("[bold red]输入错误，请重新输入[/bold red]")

if __name__ == '__main__':
    mainloop()
