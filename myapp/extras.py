from .models import Computers

def getComputerslist():
	retults = Computers.query.order_by(Computers.name)
	returns = [("","")]
	for row in retults:
		returns.append((row.id,row.name))
	return returns
