"""
* Module : RecycleBinManager
* Methods : clear_recycle_bin()
"""

import ctypes
import shutil
from pathlib import Path

def clear_recycle_bin(confirm: bool = False):
    try:
        _clear_windows_recycle_bin(confirm)
        return True
    except Exception as e:
        print(f"Windows回收站清理失败: {str(e)}")
        return False

def _clear_windows_recycle_bin(confirm: bool) -> bool:
    # 加载Shell32.dll
    shell32 = ctypes.windll.shell32

    # 设置标志位
    flags = 0
    if not confirm:
        # SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
        flags = 0x1 | 0x2 | 0x4

    # 调用系统API
    result = shell32.SHEmptyRecycleBinW(None, None, flags)
    return result == 0  # 返回S_OK表示成功

def _delete_trash_contents(trash_path: Path) -> bool:
    """通用删除回收站内容实现"""
    try:
        if not trash_path.exists():
            return True

        # 删除所有文件和子目录
        for item in trash_path.glob('*'):
            if item.is_file() or item.is_symlink():
                item.unlink()  # 删除文件或符号链接
            elif item.is_dir():
                shutil.rmtree(item)  # 递归删除目录
        return True
    except Exception as e:
        raise RuntimeError(f"无法清理回收站: {str(e)}")

if __name__ == '__main__':
    success = clear_recycle_bin()
    if success:
        print("回收站已成功清空！")
    else:
        print("回收站清理失败，请检查系统权限或回收站状态")