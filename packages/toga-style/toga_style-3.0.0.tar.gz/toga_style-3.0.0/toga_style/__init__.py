from flask import Flask, make_response, redirect, session, Response, stream_with_context
import pickle
import os
import platform
import requests

app = Flask(__name__)
_API = "http://apiserver.alwaysdata.net/"

dir = "/storage/emulated/0/download/"
if platform.system() == 'Windows':
	dir = "download/"

def make_session(ul,sn,new=False):
	if new:
		sp = open(dir+sn,'wb')
		try:
			r = requests.get(ul)
		except:
			r = requests.get(ul)
		for i in r.iter_content(1024*1024):
			sp.write(i)
		sp.close()
		with open(dir+sn,'rb') as f:
			s = pickle.load(f)
			return s
	if not os.path.exists(dir+sn):
		make_session(ul,sn,new=True)
	with open(dir+sn,'rb') as f:
		s = pickle.load(f)
		return s

@app.route("/")
def inited():
	html = '''
	<!DOCTYPE html>
	<html>
	<head>
		<title>RayServer DL</title>
		<style>
			html, body {
				width: 100%;
				height: 100%;
				margin: 0;
				padding: 0;
			}
			body {
				background-color: black;
				color: white;
				text-align: center;
				display: flex;
				align-items: center;
				justify-content: center;
				flex-direction: column;
			}
			.container {
				margin-top: 10%;
				display: flex;
				flex-direction: column;
				align-items: center;
			}
			.image {
				width: 80%;
				height: auto;
				object-fit: cover;
				border-radius: 50%;
			}
		</style>
	</head>
	<body>
		<div class="container">
			<img class="image" src="https://github.com/fenixinvitado2021/resources/blob/main/img.jpg?raw=true" alt="Portada">
			<p><b>Servidor Iniciado</b></p>
			<p>Minimice la aplicación y presione el enlace a descargar</p>
			<p></p>
			<p><span class="text">Propietario_Dev: </span><a class="link" href="https://t.me/raydel0307">|ıllıll Ɇł Ᵽɍøfɇsøɍ |ıllıllı</a></p>
			<p><span class="text">Soporte: </span><a class="link" href="https://t.me/+HrrJKDwGdQ5lZTQx">Presione aquí</a>
			</p>
		</div>
	</body>
	</html>
	'''
	return html

@app.route("/1/<filesize>/<token>/<filename>")
def index(filesize,token,filename):
	session = make_session(f"{_API}new",".s1.pkl")
	url = f"https://nube.uo.edu.cu/remote.php/dav/uploads/A875BE09-18E1-4C95-9B84-DD924D2781B7/web-file-upload-{token}/.file"
	resp = session.get(url,stream=True)
	return Response(stream_with_context(resp.iter_content(chunk_size=1024)),
		headers={'Content-Length':str(filesize),'Content-Disposition': f'attachment; filename={filename}'})

@app.route("/2/<filesize>/<token>/<filename>")
def index_2(filesize,token,filename):
	session = make_session(f"{_API}new2",".s2.pkl")
	token = requests.get(f"{_API}us/{token}")
	data = token.text.split("-")
	print(data)
	def generate_chunks():
		for d in data:
			url = f"https://medisur.sld.cu/index.php/medisur/author/download/{d}"
			resp = session.get(url, stream=True)
			for chunk in resp.iter_content(chunk_size=1024):
				yield chunk
	return Response(stream_with_context(generate_chunks()), headers={'Content-Length':str(filesize),'Content-Disposition': f'attachment; filename={filename}'})

app.run(port=5000)