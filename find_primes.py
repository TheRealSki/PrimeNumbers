import argparse, math
from atexit import register
from os.path import isfile

class PrimeListInitializationError(Exception):
	pass

class PrimeList():
	_list = []
	_listIter = 0
	
	def __init__(self):
		try:
			if isfile("primes.txt"):
				with open("primes.txt", 'r') as f:
					result = f.read()
				self._list = [int(x) for x in result.split(',')]
		except Exception as err:
			raise PrimeListInitializationError(err)
		register(self._exit)
	
	def _exit(self):
		with open("primes.txt", 'w') as f:
			f.write(self.__str__())
	
	def __iter__(self):
		self._listIter = 0
		return self
	
	def __next__(self):
		if self._listIter > len(self._list):
			raise StopIteration
		return self._list[self._listIter]
	
	def __repr__(self):
		return "PrimeList()"
	
	def __str__(self):
		return ",".join([str(x) for x in self._list])
	
	def ConvertIntToDigitList(self, num: int):
		return [int(x) for x in str(num)]
	
	def ConvertListToInt(self, numList: list):
		return int("".join([str(x) for x in numList]))
	
	def SumIntDigits(self, num: int):
		return sum(int(i) for i in str(num))
	
	def GetMax(self):
		return self._list[-1:][0]
	
	def AppendValue(self, val: int):
		if not self.IsInPrimeList(val):
			self._list.append(val)
	
	def IsInPrimeList(self, val: int):
		return val in self._list
	
	def UpdatePrimesToValue(self, maxVal: int):
		currentMax = self.GetMax()
		if maxVal > currentMax:
			for x in range(currentMax, maxVal + 1):
				if self.IsPrime(x):
					self.AppendValue(x)
	
	def IsDivisibleBy3(self, num: int):
		if num < 1000:
			return num % 3 == 0
		
		return self.IsDivisibleBy3(sum(self.ConvertIntToDigitList(num)))
	
	def IsDivisibleBy5(self, num: int):
		return ((self.ConvertIntToDigitList(num)[-1:][0]) % 5 == 0)
	
	# Modified from https://www.geeksforgeeks.org/divisibility-by-7/
	# Function to check whether a number is divisible by 7
	def IsDivisibleBy7(self, num: int): 
		if num < 1000 : 
			return num % 7 == 0
		
		numList = self.ConvertIntToDigitList(num)
		topNum = self.ConvertListToInt(numList[:-1])
		botNum = numList[-1:][0] * 2
		return self.IsDivisibleBy7(topNum - botNum)

	# Modified from https://www.geeksforgeeks.org/check-large-number-divisible-11-not/
	# Function to find that number divisible by 11 or not
	def IsDivisibleBy11(self, num: int):
		numList = self.ConvertIntToDigitList(num)
		
		# Compute sum of even and odd digit
		# sums
		oddDigSum = sum(numList[0::2])
		evenDigSum = sum(numList[1::2])
		
		# Check its difference is divisible by 11 or not
		return ((oddDigSum - evenDigSum) % 11 == 0)
	
	def IsDivisibleBy13(self, num: int):
		if num < 1000:
			return num % 13 == 0
		
		numList = self.ConvertIntToDigitList(num)
		topNum = self.ConvertListToInt(numList[:-1])
		botNum = numList[-1:][0] * 4
		
		return self.IsDivisibleBy13(topNum + botNum)
	
	def PossiblyPrime(self, val: int):
		# Checks if a number is prime based on the basic values (1, 2, 3, 5, 7, 11, and 13)
		if val % 2 == 0:
			return False
		
		if self.IsDivisibleBy3(val):
			return False
		
		if self.IsDivisibleBy5(val):
			return False
		
		if self.IsDivisibleBy7(val):
			return False
		
		if self.IsDivisibleBy11(val):
			return False
		
		if self.IsDivisibleBy13(val):
			return False
		
		return True
	
	def DefinitelyPrime(self, val: int):
		topRange = math.isqrt(val)
		for x in self._list:
			if x > topRange:
				break
			if x > 13 and x < val:
				if val % x == 0:
					return False
		return True
	
	def IsPrime(self, val: int):
		if self.PossiblyPrime(val):
			if val < 17:
				return True
			if self.DefinitelyPrime(val):
				return True
		return False
	
def ParseArgs():
	parser = argparse.ArgumentParser(description='Generate a list of prime numbers.')
	
	# Required (positional) Arguments
	parser.add_argument(dest='value', type=int, help='Integer value to use for prime number operations.')
	
	# Optional Arguments
	parser.add_argument('-m', '--max', dest='isMax', action='store_true', help='Use <value> to find all primes from 1 to <value>.')
	parser.add_argument('-c', '--check', dest='isCheck', action='store_true', help='Determine if <value> is a prime number.')
	
	return parser.parse_args()

def main():
	args = ParseArgs()
	if not args.isMax and not args.isCheck:
		print("Please provide an optional argument (-m or -c) for use with <value>.")
		return -1
	
	pl = PrimeList()
	if args.isCheck:
		sqrVal = math.isqrt(args.value)
		pl.UpdatePrimesToValue(sqrVal)
		print("Is {} prime? {}".format(args.value, pl.IsPrime(args.value)))
	if args.isMax:
		pl.UpdatePrimesToValue(args.value)
		print("List of prime numbers:\n{}".format(pl))
	
main()