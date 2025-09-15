import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def find_and_copy_files(folder_a, folder_b, folder_c, log_widget):
    """
    在文件夹B中查找与文件夹A同名的文件（忽略扩展名），并将匹配的文件复制到文件夹C。
    
    :param folder_a: 查找源文件夹路径
    :param folder_b: 被查找区文件夹路径
    :param folder_c: 存放已找到文件的文件夹路径
    :param log_widget: 日志输出组件
    """
    try:
        # 确保目标文件夹存在
        os.makedirs(folder_c, exist_ok=True)
        
        # 获取文件夹A中的所有文件名（忽略扩展名）
        files_a = set()
        for filename in os.listdir(folder_a):
            name_without_ext = os.path.splitext(filename)[0]
            files_a.add(name_without_ext)
        
        # 在文件夹B中查找同名文件并复制
        for filename in os.listdir(folder_b):
            name_without_ext = os.path.splitext(filename)[0]
            if name_without_ext in files_a:
                src_path = os.path.join(folder_b, filename)
                dst_path = os.path.join(folder_c, filename)
                shutil.copy2(src_path, dst_path)
                log_widget.insert(tk.END, f"已复制文件: {filename}\n")
                log_widget.see(tk.END)
        
        messagebox.showinfo("完成", "操作完成！")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误: {e}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("同名文件查找工具")
        
        # 文件夹路径变量
        self.folder_a = tk.StringVar()
        self.folder_b = tk.StringVar()
        self.folder_c = tk.StringVar()
        
        # 创建界面组件
        self.create_widgets()
    
    def create_widgets(self):
        # 文件夹A选择
        tk.Label(self.root, text="查找源文件夹（A）:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.folder_a, width=50).grid(row=0, column=1)
        tk.Button(self.root, text="选择", command=lambda: self.select_folder(self.folder_a)).grid(row=0, column=2)
        
        # 文件夹B选择
        tk.Label(self.root, text="被查找区文件夹（B）:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.folder_b, width=50).grid(row=1, column=1)
        tk.Button(self.root, text="选择", command=lambda: self.select_folder(self.folder_b)).grid(row=1, column=2)
        
        # 文件夹C选择
        tk.Label(self.root, text="存放已找到文件的文件夹（C）:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.folder_c, width=50).grid(row=2, column=1)
        tk.Button(self.root, text="选择", command=lambda: self.select_folder(self.folder_c)).grid(row=2, column=2)
        
        # 日志输出
        tk.Label(self.root, text="操作日志:").grid(row=3, column=0, sticky="w")
        self.log = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.log.grid(row=4, column=0, columnspan=3)
        
        # 开始按钮
        tk.Button(self.root, text="开始查找", command=self.start_search).grid(row=5, column=1, pady=10)
    
    def select_folder(self, folder_var):
        """选择文件夹"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_var.set(folder_path)
    
    def start_search(self):
        """开始查找"""
        folder_a = self.folder_a.get()
        folder_b = self.folder_b.get()
        folder_c = self.folder_c.get()
        
        if not all([folder_a, folder_b, folder_c]):
            messagebox.showwarning("警告", "请选择所有文件夹！")
            return
        
        self.log.insert(tk.END, "开始查找...\n")
        find_and_copy_files(folder_a, folder_b, folder_c, self.log)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()