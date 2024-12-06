import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform


class NetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Command Tool")
        self.root.geometry("800x600")

        # Создание вкладок
        self.tab_control = ttk.Notebook(root)
        self.ping_tab = ttk.Frame(self.tab_control)
        self.ipconfig_tab = ttk.Frame(self.tab_control)
        self.netstat_tab = ttk.Frame(self.tab_control)
        self.pathping_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.ping_tab, text="Ping")
        self.tab_control.add(self.ipconfig_tab, text="IPConfig")
        self.tab_control.add(self.netstat_tab, text="Netstat")
        self.tab_control.add(self.pathping_tab, text="Pathping")

        self.tab_control.pack(expand=1, fill="both")

        # Вкладки
        self.create_ping_tab()
        self.create_ipconfig_tab()
        self.create_netstat_tab()
        self.create_pathping_tab()

    def create_ping_tab(self):
        ttk.Label(self.ping_tab, text="Введите IP или домен для Ping:").pack(pady=5)
        self.ping_entry = ttk.Entry(self.ping_tab)
        self.ping_entry.pack(pady=5)

        # Параметры Ping
        self.ping_timeout = tk.IntVar(value=4)
        self.ping_packet_size = tk.IntVar(value=32)
        ttk.Label(self.ping_tab, text="Число запросов (-n):").pack()
        ttk.Entry(self.ping_tab, textvariable=self.ping_timeout).pack()
        ttk.Label(self.ping_tab, text="Размер пакета (-l):").pack()
        ttk.Entry(self.ping_tab, textvariable=self.ping_packet_size).pack()

        ttk.Button(self.ping_tab, text="Ping", command=self.run_ping).pack(pady=5)

        # Создание таблицы для вывода результатов
        self.ping_tree = ttk.Treeview(self.ping_tab, columns=("Host", "Time", "TTL"), show="headings")
        self.ping_tree.heading("Host", text="Хост")
        self.ping_tree.heading("Time", text="Время (мс)")
        self.ping_tree.heading("TTL", text="TTL")
        self.ping_tree.pack(pady=5)

    def create_ipconfig_tab(self):
        ttk.Button(self.ipconfig_tab, text="Запустить IPConfig", command=self.run_ipconfig).pack(pady=5)
        self.ipconfig_output = tk.Text(self.ipconfig_tab, wrap="word", height=15)
        self.ipconfig_output.pack(pady=5)

    def create_netstat_tab(self):
        ttk.Label(self.netstat_tab, text="Опции Netstat:").pack()
        self.netstat_a = tk.BooleanVar()
        ttk.Checkbutton(self.netstat_tab, text="-a (Все соединения)", variable=self.netstat_a).pack()
        self.netstat_n = tk.BooleanVar()
        ttk.Checkbutton(self.netstat_tab, text="-n (Адреса и порты)", variable=self.netstat_n).pack()

        ttk.Button(self.netstat_tab, text="Запустить Netstat", command=self.run_netstat).pack(pady=5)
        self.netstat_output = tk.Text(self.netstat_tab, wrap="word", height=15)
        self.netstat_output.pack(pady=5)

    def create_pathping_tab(self):
        ttk.Label(self.pathping_tab, text="Введите IP или домен для Pathping:").pack(pady=5)
        self.pathping_entry = ttk.Entry(self.pathping_tab)
        self.pathping_entry.pack(pady=5)

        # Параметры Pathping
        self.pathping_hops = tk.IntVar(value=30)
        self.pathping_pause = tk.IntVar(value=250)
        ttk.Label(self.pathping_tab, text="Макс. число прыжков (-h):").pack()
        ttk.Entry(self.pathping_tab, textvariable=self.pathping_hops).pack()
        ttk.Label(self.pathping_tab, text="Пауза (-p):").pack()
        ttk.Entry(self.pathping_tab, textvariable=self.pathping_pause).pack()

        ttk.Button(self.pathping_tab, text="Pathping", command=self.run_pathping).pack(pady=5)

        # Создание таблицы для вывода результатов
        self.pathping_tree = ttk.Treeview(self.pathping_tab, columns=(
            "Hop", "Time", "Sent Loss", "Received Loss", "Percent Loss", "Address"), show="headings")
        self.pathping_tree.heading("Hop", text="Прыжок")
        self.pathping_tree.heading("Time", text="Время (мс)")
        self.pathping_tree.heading("Sent Loss", text="Потери исходного узла (%)")
        self.pathping_tree.heading("Received Loss", text="Потери маршрутного узла (%)")
        self.pathping_tree.heading("Percent Loss", text="Общий % потерь")
        self.pathping_tree.heading("Address", text="Адрес")
        self.pathping_tree.pack(pady=5)

    def run_ping(self):
        target = self.ping_entry.get().strip()
        if not target:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите IP или домен.")
            return

        timeout = self.ping_timeout.get()
        packet_size = self.ping_packet_size.get()
        output = self.run_command(f"ping -n {timeout} -l {packet_size} {target}")

        # Очищаем предыдущие данные в таблице
        for row in self.ping_tree.get_children():
            self.ping_tree.delete(row)

        # Обработка вывода команды
        for line in output.splitlines():
            line = line.strip()
            if "Ответ от" in line or "Reply from" in line:  # Для русского и английского языков
                try:
                    parts = line.split()
                    host = parts[2].strip(":")  # IP-адрес или домен
                    time = next((x.split('=')[1] for x in parts if x.startswith("time=")), "N/A")
                    ttl = next((x.split('=')[1] for x in parts if x.startswith("TTL=")), "N/A")
                    self.ping_tree.insert("", "end", values=(host, time, ttl))
                except Exception as e:
                    print(f"Ошибка обработки строки: {line}. Детали: {e}")

    def run_ipconfig(self):
        output = self.run_command("ipconfig")
        self.ipconfig_output.delete(1.0, tk.END)
        self.ipconfig_output.insert(tk.END, output)

    def run_netstat(self):
        options = "-a " if self.netstat_a.get() else ""
        options += "-n " if self.netstat_n.get() else ""
        output = self.run_command(f"netstat {options}")
        self.netstat_output.delete(1.0, tk.END)
        self.netstat_output.insert(tk.END, output)

    def run_pathping(self):
        target = self.pathping_entry.get().strip()
        if not target:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите IP или домен.")
            return

        hops = self.pathping_hops.get()
        pause = self.pathping_pause.get()

        if platform.system() != "Windows":
            messagebox.showerror("Ошибка", "Команда Pathping доступна только на Windows.")
            return

        output = self.run_command(f"pathping -h {hops} -p {pause} {target}")

        # Очищаем предыдущие данные в таблице
        for row in self.pathping_tree.get_children():
            self.pathping_tree.delete(row)

        self.parse_and_display_pathping(output)

    def parse_and_display_pathping(self, output):
        try:
            lines = output.splitlines()
            start_processing = False

            for line in lines:
                line = line.strip()
                # Начинаем обработку после заголовка "Hop"
                if "Hop" in line or "Прыжок" in line:
                    start_processing = True
                    continue

                # Обрабатываем строки, соответствующие прыжкам
                if start_processing and line:
                    parts = line.split()
                    # Проверяем, что строка соответствует формату прыжка
                    if len(parts) >= 6 and parts[0].isdigit():
                        hop = parts[0]
                        time = parts[1] if parts[1] != '-' else 'N/A'
                        sent_loss = parts[2] if len(parts) > 2 else 'N/A'
                        received_loss = parts[3] if len(parts) > 3 else 'N/A'
                        percent_loss = parts[4] if len(parts) > 4 else 'N/A'
                        address = " ".join(parts[5:])
                        self.pathping_tree.insert("", "end", values=(
                            hop, time, sent_loss, received_loss, percent_loss, address))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обработке результатов Pathping: {e}")

    def run_command(self, command):
        try:
            encoding = 'cp866' if platform.system() == "Windows" else 'utf-8'
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True,
                                    encoding=encoding)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Ошибка выполнения команды: {e}"


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()
