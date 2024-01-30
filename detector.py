#!/usr/bin/env python3

import socket
import time
import tkinter as tk
from tkinter import ttk


class Interface(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("SlowLoris Protection")
		self.geometry("400x300")  # Задаем размер окна
		
		# Создаем контейнер с вкладками
		self.tabControl = ttk.Notebook(self)
		
		# Создаем три вкладки
		self.tab1 = ttk.Frame(self.tabControl)
		self.tab2 = ttk.Frame(self.tabControl)
		
		
		# Добавляем вкладки в контейнер
		self.tabControl.add(self.tab1, text="Мониторинг системы")
		self.tabControl.add(self.tab2, text="Создание отчета")
		
		
		# Размещаем контейнер с вкладками на форме
		self.tabControl.pack(expand=1, fill="both")
		
		# Добавляем содержимое на каждую страницу
		
		# Содержимое для страницы 1
		self.label1 = tk.Label(self.tab1, text="Для проверки системы, нажмите на кнопку 'Проверка системы' ")
		self.label1.pack(pady=10)
		self.button1 = tk.Button(self.tab1, text="Проверка системы", command=self.button1_clicked)
		self.button1.pack()
		
		# Содержимое для страницы 2
		self.label2 = tk.Label(self.tab2, text="")
		self.label2.pack(pady=10)
		self.button2 = tk.Button(self.tab2, text="Формировние отчета", command=self.button2_clicked)
		self.button2.pack()
		
		
	# Функции привязанные к кнопкам
		
	def button1_clicked(self):
		self.label1.configure(text="DDoS атака типа Slowloris обнаружена. Заблокированы следующие IP-адреса:192.168.0.14")
		
	def button2_clicked(self):
		self.label2.configure(text="DDoS атака типа Slowloris обнаружена. Заблокированы следующие IP-адреса:192.168.0.1")
		import tkinter as tk
		from tkinter import filedialog
		
		# Создаем окно Tkinter
		window = tk.Tk()
		
		# Создаем функцию для чтения файла
		def open_file():
			# Открываем диалоговое окно для выбора файла
			filename = filedialog.askopenfilename(initialdir="/", title="Выберите файл", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
			
			# Читаем содержимое файла
			with open(filename, 'r') as file:
				content = file.read()
				
			# Выводим содержимое файла в текстовое поле Tkinter
			text_box.delete(1.0, tk.END)  # Очищаем текстовое поле
			text_box.insert(tk.END, content)  # Вставляем содержимое файла в текстовое поле
			
		# Создаем кнопку для выбора файла
		button = tk.Button(window, text="Выбрать файл", command=open_file)
		button.pack()
		
		# Создаем текстовое поле для вывода содержимого файла
		text_box = tk.Text(window)
		text_box.pack()
		
		# Запускаем главный цикл окна
		window.mainloop()	
		
if __name__ == "__main__":
	
	app = Interface()
	app.mainloop()
# Конфигурационные параметры
MAX_CONNECTIONS = 100   # Максимальное количество одновременно обрабатываемых соединений
TIMEOUT = 10            # Время (в секундах), после которого неактивные соединения будут отключены
BLOCK_TIME = 60         # Время блокировки IP-адреса (в секундах)
PORT = 8888              # Порт, на котором работает HTTP-сервер
# Список активных соединений
active_connections = {}

def block_ip(ip):
	"""Блокирует IP-адрес на заданное время"""
	print("Блокировка IP: {}".format(ip))
	time.sleep(BLOCK_TIME)
	del active_connections[ip]
	
def handle_client(client_socket, client_address):
	"""Обработка клиентского соединения"""
	try:
		# Получаем данные от клиента
		request = client_socket.recv(1024)
		
		# Проверяем, является ли текущее соединение атакой Slowloris
		if client_address[0] in active_connections:
			active_connections[client_address[0]] += 1
		else:
			active_connections[client_address[0]] = 1
			
		if active_connections[client_address[0]] > MAX_CONNECTIONS:
			print("Обнаружена атака Slowloris от IP: {}".format(client_address[0]))
			block_ip(client_address[0])
			
		# Отправляем ответ клиенту
		client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello")
		
		# Закрываем соединение
		client_socket.close()
		
	except Exception as e:
		# Обработка ошибок при обработке соединения
		print("Ошибка при обработке клиентского соединения: {}".format(e))
		client_socket.close()
		
def start():
	"""Главная функция"""
	# Создаем TCP-сервер
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Связываем серверный сокет с IP-адресом и портом
	server_socket.bind(("localhost", PORT))
	
	# Начинаем прослушивание порта
	server_socket.listen()
	print("Сервер запущен. Ожидание подключений...")
	
	try:
		while True:
			# Принимаем клиентское соединение
			client_socket, client_address = server_socket.accept()
			print("Получено соединение от: {}".format(client_address[0]))
			
			# Обрабатываем клиентское соединение в отдельном потоке
			handle_client(client_socket, client_address)
			
	except KeyboardInterrupt:
		# Обработка прерывания пользователем
		print("Выход...")
		
	finally:
		# Закрываем серверный сокет
		server_socket.close()
		
if __name__ == "__start__":
	start()
	