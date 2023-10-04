




from flask import Flask

from QR.GENERATE import GENERATE_QR

def START ():
	app = Flask (__name__)

	@app.route ("/")
	def hello_world ():
		return "<p>Hello, World!</p>"
		
	@app.route ("/QR")
	def QR ():
		QR_CODE = GENERATE_QR (
			STRING = 'THIS IS A QR CODE MESSAGE!'
		)
	
		return f"""
<body style="background: #222">
	<img src='{ QR_CODE }' />
</body>
		"""
		
	app.run ()