"""
* Module Name : ScanLargeFiles.py
* Methods : scan_large_files()
"""

import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from rich import print

def fast_scan(drive_path, min_size, progress_callback, file_callback):
    large_files = []
    ext_stats = defaultdict(int)
    total_files = 0
    large_files_count = 0

    from os import scandir
    stack = [drive_path]

    while stack:
        current_dir = stack.pop()
        try:
            with scandir(current_dir) as it:
                entries = list(it)
        except (PermissionError, OSError):
            continue

        dirs = []
        files = []

        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                dirs.append(entry)
            else:
                files.append(entry)

        stack.extend([entry.path for entry in reversed(dirs)])

        for entry in files:
            total_files += 1
            try:
                file_callback(entry.path)

                st = entry.stat(follow_symlinks=False)
                if not st.st_size >= min_size:
                    continue

                file_path = entry.path
                large_files.append((file_path, st.st_size))
                ext = os.path.splitext(file_path)[1].lower()
                ext_stats[ext] += st.st_size
                large_files_count += 1

                if large_files_count % 500 == 0:
                    progress_callback(total_files, large_files_count)

            except (PermissionError, OSError):
                continue

    return large_files, ext_stats, total_files, large_files_count


def scan_large_files(drive_path, min_size_mb=100, top_n=50):
    min_size = min_size_mb * 1024 * 1024
    start_time = time.time()

    last_print = time.time()

    def progress(total, large):
        nonlocal last_print
        if time.time() - last_print > 1:
            last_print = time.time()

    last_file_update = 0
    current_file = ""

    def show_current_file(path):
        nonlocal last_file_update, current_file
        current_file = path
        now = time.time()
        if now - last_file_update > 0.1:  # 每秒最多更新10次
            print(f"\r当前: {os.path.basename(path)[:40]:<40}", end="", flush=True)
            last_file_update = now

    print(f"[bold green]扫描 {drive_path} 中大于 {min_size_mb}MB 的文件...[/bold green]")
    print("=" * 60)

    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(fast_scan, drive_path, min_size, progress, show_current_file)
        large_files, ext_stats, total, large_count = future.result()

    print("\r" + " " * 60 + "\r", end="")

    large_files.sort(key=lambda x: x[1], reverse=True)

    print(f"\n[bold green]扫描完成! 耗时 {time.time() - start_time:.2f}秒[/bold green]")
    print(f"总文件: {total:,} | 大文件: {large_count:,}")

    print(f"\n[bold purple]Top {top_n} 大文件:[/bold purple]")
    for i, (path, size) in enumerate(large_files[:top_n], 1):
        print(f"{i:>3}. {size / 1024 / 1024:8.1f}MB | {path}")

    print("\n扩展名统计:")
    for ext, size in sorted(ext_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"{ext or '无扩展名':<10}: {size / 1024 / 1024 / 1024:.2f}GB")


if __name__ == "__main__":
    try:
        scan_large_files("C:/", 500, 2147483647)
    except KeyboardInterrupt:
        print("\n扫描被用户中断")