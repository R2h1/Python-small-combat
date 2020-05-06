from datetime import datetime

output = '''<html>
	<body>
	<p>Generated {}</p>
	</body>
	</html>
'''
print(output.format(datetime.now()))