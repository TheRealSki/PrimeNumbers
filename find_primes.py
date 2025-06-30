import argparse, math
from atexit import register
from os.path import isfile
import random
import time
import sys
import threading
import signal

class PrimeListInitializationError(Exception):
	pass

class InterruptException(Exception):
	"""Exception raised when user interrupts the calculation"""
	pass

# Global interrupt flag
_interrupt_requested = False

def signal_handler(signum, frame):
	"""Handle Ctrl+C signal to request interruption"""
	global _interrupt_requested
	_interrupt_requested = True

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

class PrimeList():
	_list = []
	_listIter = 0
	
	def __init__(self):
		try:
			if isfile("primes.txt"):
				with open("primes.txt", 'r') as f:
					result = f.read()
				# Split by lines, ignore empty lines
				self._list = [int(x) for x in result.splitlines() if x.strip()]
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
		# Write one prime per line, ending with a newline
		return "\n".join([str(x) for x in self._list]) + "\n"
	
	def ConvertIntToDigitList(self, num: int):
		return [int(x) for x in str(num)]
	
	def ConvertListToInt(self, numList: list):
		return int("".join([str(x) for x in numList]))
	
	def SumIntDigits(self, num: int):
		return sum(int(i) for i in str(num))
	
	def GetMax(self):
		if not self._list:
			return 0
		return self._list[-1]
	
	def AppendValue(self, val: int):
		if not self.IsInPrimeList(val):
			self._list.append(val)
			# Keep the list sorted for efficient operations
			self._list.sort()
	
	def IsInPrimeList(self, val: int):
		return val in self._list
	
	def UpdatePrimesToValue(self, maxVal: int, timer_callback=None):
		global _interrupt_requested
		currentMax = self.GetMax()
		if maxVal > currentMax:
			# Start from 2 if list is empty, otherwise start from currentMax + 1
			start = 2 if currentMax == 0 else currentMax + 1
			for x in range(start, maxVal + 1):
				# Check for interrupt request
				if _interrupt_requested:
					raise InterruptException("Calculation interrupted by user")
				
				if self.IsPrime(x):
					self.AppendValue(x)
				# Call timer callback every 1000 iterations to check if timer should start
				if timer_callback and x % 1000 == 0:
					timer_callback()
	
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
		global _interrupt_requested
		topRange = math.isqrt(val)
		for x in self._list:
			# Check for interrupt request
			if _interrupt_requested:
				raise InterruptException("Calculation interrupted by user")
			
			if x > topRange:
				break
			if x > 13 and x < val:
				if val % x == 0:
					return False
		return True
	
	def IsPrime(self, val: int):
		if self.PossiblyPrime(val):
			if val <= 17:
				return True
			if self.DefinitelyPrime(val):
				return True
		return False
	
	# New functions for large prime numbers (>10,000,000)
	
	def IsDivisibleBy17(self, num: int):
		if num < 1000:
			return num % 17 == 0
		
		numList = self.ConvertIntToDigitList(num)
		topNum = self.ConvertListToInt(numList[:-1])
		botNum = numList[-1:][0] * 5
		
		return self.IsDivisibleBy17(topNum - botNum)
	
	def IsDivisibleBy19(self, num: int):
		if num < 1000:
			return num % 19 == 0
		
		numList = self.ConvertIntToDigitList(num)
		topNum = self.ConvertListToInt(numList[:-1])
		botNum = numList[-1:][0] * 2
		
		return self.IsDivisibleBy19(topNum + botNum)
	
	def PossiblyPrimeLarge(self, val: int):
		"""Enhanced divisibility tests for large numbers"""
		if val % 2 == 0:
			return False
		
		# Quick divisibility tests for small primes
		for prime in [3, 5, 7, 11, 13, 17, 19]:
			if val % prime == 0:
				return False
		
		return True
	
	def MillerRabinTest(self, n: int, k: int = 5):
		"""Miller-Rabin primality test for large numbers"""
		global _interrupt_requested
		if n <= 3:
			return n > 1
		if n % 2 == 0:
			return False
		
		# Write n as 2^r * d + 1
		r, d = 0, n - 1
		while d % 2 == 0:
			r += 1
			d //= 2
		
		# Witness loop
		for _ in range(k):
			# Check for interrupt request
			if _interrupt_requested:
				raise InterruptException("Calculation interrupted by user")
			
			a = random.randint(2, n - 2)
			x = pow(a, d, n)
			if x == 1 or x == n - 1:
				continue
			for _ in range(r - 1):
				x = (x * x) % n
				if x == n - 1:
					break
			else:
				return False
		return True
	
	def IsPrimeLarge(self, val: int):
		"""Optimized prime check for large numbers (>10,000,000)"""
		if val < 10000000:
			return self.IsPrime(val)
		
		# Quick divisibility tests
		if not self.PossiblyPrimeLarge(val):
			return False
		
		# For very large numbers, use Miller-Rabin with more iterations
		if val > 1000000000:
			return self.MillerRabinTest(val, 10)
		else:
			return self.MillerRabinTest(val, 5)
	
	def WheelFactorization(self, val: int):
		"""Wheel factorization for efficient large number testing"""
		global _interrupt_requested
		if val < 2:
			return False
		if val < 4:
			return True
		if val % 2 == 0:
			return False
		
		# Wheel of 30: only test numbers ≡ 1, 7, 11, 13, 17, 19, 23, 29 (mod 30)
		wheel = [1, 7, 11, 13, 17, 19, 23, 29]
		limit = math.isqrt(val)
		
		# Test small primes first
		for prime in [3, 5, 7, 11, 13, 17, 19, 23, 29]:
			if val % prime == 0:
				return val == prime
		
		# Wheel factorization
		for i in range(31, limit + 1, 30):
			# Check for interrupt request
			if _interrupt_requested:
				raise InterruptException("Calculation interrupted by user")
			
			for j in wheel:
				if i + j > limit:
					break
				if val % (i + j) == 0:
					return False
		return True
	
	def FindNextPrime(self, start: int, timer_callback=None):
		"""Find the next prime number after start"""
		global _interrupt_requested
		if start < 2:
			return 2
		
		# Start checking from the next number after start
		start += 1
		
		# Ensure we start with an odd number
		if start % 2 == 0:
			start += 1
		
		iterations = 0
		while True:
			# Check for interrupt request
			if _interrupt_requested:
				raise InterruptException("Calculation interrupted by user")
			
			if self.IsPrimeLarge(start):
				# Add the newly discovered prime to our list
				self.AppendValue(start)
				return start
			start += 2
			iterations += 1
			# Call timer callback every 100 iterations to check if timer should start
			if timer_callback and iterations % 100 == 0:
				timer_callback()
	
	def FindPreviousPrime(self, start: int, timer_callback=None):
		"""Find the previous prime number before start"""
		global _interrupt_requested
		if start <= 2:
			return None
		
		# Ensure we start with an odd number
		if start % 2 == 0:
			start -= 1
		
		iterations = 0
		while start > 2:
			# Check for interrupt request
			if _interrupt_requested:
				raise InterruptException("Calculation interrupted by user")
			
			if self.IsPrimeLarge(start):
				# Add the newly discovered prime to our list
				self.AppendValue(start)
				return start
			start -= 2
			iterations += 1
			# Call timer callback every 100 iterations to check if timer should start
			if timer_callback and iterations % 100 == 0:
				timer_callback()
		
		return 2 if start >= 2 else None
	
	def CountPrimesInRange(self, start: int, end: int, timer_callback=None):
		"""Count prime numbers in a range (inclusive)"""
		global _interrupt_requested
		count = 0
		if start <= 2 and end >= 2:
			count += 1
		
		# Ensure we start with an odd number
		if start % 2 == 0:
			start += 1
		
		iterations = 0
		for num in range(start, end + 1, 2):
			# Check for interrupt request
			if _interrupt_requested:
				raise InterruptException("Calculation interrupted by user")
			
			if self.IsPrimeLarge(num):
				# Add the newly discovered prime to our list
				self.AppendValue(num)
				count += 1
			iterations += 1
			# Call timer callback every 1000 iterations to check if timer should start
			if timer_callback and iterations % 1000 == 0:
				timer_callback()
		
		return count
	
	def GetPrimeFactors(self, num: int):
		"""Get prime factorization of a number"""
		global _interrupt_requested
		if num < 2:
			return []
		
		factors = []
		# Handle 2 separately
		while num % 2 == 0:
			factors.append(2)
			num //= 2
		
		# Check odd numbers up to sqrt(num)
		for i in range(3, math.isqrt(num) + 1, 2):
			# Check for interrupt request
			if _interrupt_requested:
				raise InterruptException("Calculation interrupted by user")
			
			while num % i == 0:
				factors.append(i)
				num //= i
		
		if num > 2:
			factors.append(num)
		
		return factors

def ParseArgs():
	parser = argparse.ArgumentParser(description='Generate a list of prime numbers.')
	
	# Optional Arguments
	parser.add_argument('-m', '--max', dest='isMax', action='store_true', help='Use <value> to find all primes from 1 to <value>.')
	parser.add_argument('-c', '--check', dest='isCheck', action='store_true', help='Determine if <value> is a prime number.')
	parser.add_argument('-t', '--top', dest='isHighest', action='store_true', help='Display the highest prime number saved in primes.txt.')
	parser.add_argument('-l', '--large', dest='isLarge', action='store_true', help='Use optimized algorithms for large numbers (>10M).')
	parser.add_argument('-n', '--next', dest='isNext', action='store_true', help='Find the next prime number after <value>.')
	parser.add_argument('-p', '--prev', dest='isPrev', action='store_true', help='Find the previous prime number before <value>.')
	parser.add_argument('-r', '--range', dest='isRange', action='store_true', help='Count primes in range from <value> to <end_value>.')
	parser.add_argument('-f', '--factors', dest='isFactors', action='store_true', help='Get prime factorization of <value>.')
	parser.add_argument('--timing', dest='showTiming', action='store_true', help='Display timing information for calculations and display.')
	
	# Required (positional) Arguments - only needed for -m and -c options
	parser.add_argument('value', type=int, nargs='?', help='Integer value to use for prime number operations (required for -m, -c, -n, -p, -f options).')
	parser.add_argument('end_value', type=int, nargs='?', help='End value for range operations (required for -r option).')
	
	return parser.parse_args()

def format_time(seconds):
	"""Format time in hours:minutes:seconds:hundredths format"""
	# Round up to nearest 1/100th of a second
	seconds = math.ceil(seconds * 100) / 100
	
	hours = int(seconds // 3600)
	minutes = int((seconds % 3600) // 60)
	secs = int(seconds % 60)
	hundredths = int((seconds * 100) % 100)
	
	return f"{hours:02d}:{minutes:02d}:{secs:02d}:{hundredths:02d}"

def show_processing_animation():
	"""Display animated processing message that updates every 10ms"""
	animation_states = ["Processing", "Processing.", "Processing..", "Processing..."]
	state_index = 0
	stop_animation = False
	
	def update_animation():
		nonlocal state_index
		# Clear the line and move cursor back
		sys.stdout.write('\r' + ' ' * 50 + '\r')
		# Write the current animation state
		sys.stdout.write(animation_states[state_index])
		sys.stdout.flush()
		state_index = (state_index + 1) % len(animation_states)
	
	def animation_loop():
		while not stop_animation:
			update_animation()
			time.sleep(0.01)  # 10 milliseconds
	
	def stop():
		nonlocal stop_animation
		stop_animation = True
	
	return update_animation, animation_loop, stop

def show_processing_timer():
	"""Display a timer that shows elapsed time when processing takes longer than 1 second, fixed in position."""
	start_time = time.time()
	stop_timer = False
	first_print = True

	def update_timer():
		nonlocal first_print
		elapsed = time.time() - start_time
		timer_str = f"Processing... Elapsed time: {format_time(elapsed)} (Press Ctrl+C to interrupt)"
		if first_print:
			# Print the timer line once
			print("\n" + timer_str)
			first_print = False
		else:
			# Move cursor up, overwrite timer, move cursor back down
			sys.stdout.write("\033[F")  # Move cursor up one line
			sys.stdout.write("\r" + timer_str + "\n")
			sys.stdout.flush()

	def timer_loop():
		while not stop_timer:
			update_timer()
			time.sleep(0.1)  # Update every 100ms

	def stop():
		nonlocal stop_timer
		stop_timer = True
		# Clear the timer line
		sys.stdout.write("\033[F\r" + ' ' * 80 + "\n")
		sys.stdout.flush()

	return update_timer, timer_loop, stop

def check_and_start_timer(calc_start_time, timer_started, timer_thread):
	"""Check if processing has been running for more than 1 second and start timer if needed"""
	if not timer_started and time.time() - calc_start_time > 1.0:
		update_timer, timer_loop, stop_timer = show_processing_timer()
		timer_thread = threading.Thread(target=timer_loop, daemon=True)
		timer_thread.start()
		timer_started = True
		return update_timer, timer_loop, stop_timer, timer_thread, timer_started
	return None, None, None, timer_thread, timer_started

def main():
	global _interrupt_requested
	start_time = time.time()
	args = ParseArgs()
	if not args.isMax and not args.isCheck and not args.isHighest and not args.isNext and not args.isPrev and not args.isRange and not args.isFactors:
		print("Please provide an optional argument (-m, -c, -t, -l, -n, -p, -r, or -f) for use with <value>.")
		return -1
	
	pl = PrimeList()
	
	# Reset interrupt flag at start
	_interrupt_requested = False
	
	# Track calculation start time
	calc_start_time = time.time()
	
	# Setup processing animation if timing is enabled
	animation_thread = None
	if args.showTiming:
		update_animation, animation_loop, stop_animation = show_processing_animation()
		update_animation()  # Show initial state
		animation_thread = threading.Thread(target=animation_loop, daemon=True)
		animation_thread.start()
	
	# Setup automatic timer for long-running operations
	timer_thread = None
	timer_started = False
	stop_timer = None
	update_timer = None
	timer_loop = None
	
	# Timer callback function to check if timer should start
	def timer_callback():
		nonlocal timer_started, timer_thread, stop_timer, update_timer, timer_loop
		if not timer_started and time.time() - calc_start_time > 1.0:
			update_timer, timer_loop, stop_timer = show_processing_timer()
			timer_thread = threading.Thread(target=timer_loop, daemon=True)
			timer_thread.start()
			timer_started = True
	
	# Initial timer check - if we've already been running for more than 1 second
	if time.time() - calc_start_time > 1.0:
		timer_callback()
	
	if args.isHighest:
		if not pl._list:
			result = "No prime numbers found in primes.txt."
		else:
			highest_prime = pl.GetMax()
			result = "Highest prime number: {}".format(highest_prime)
	
	if args.isCheck:
		if args.value is None:
			print("Error: <value> is required for the -c/--check option.")
			return -1
		
		# Check if we need to start the timer (after 1 second)
		if not timer_started and time.time() - calc_start_time > 1.0:
			update_timer, timer_loop, stop_timer = show_processing_timer()
			timer_thread = threading.Thread(target=timer_loop, daemon=True)
			timer_thread.start()
			timer_started = True
		
		try:
			if args.isLarge or args.value > 10000000:
				is_prime = pl.IsPrimeLarge(args.value)
				# If the number is prime and not already in our list, add it
				if is_prime and not pl.IsInPrimeList(args.value):
					pl.AppendValue(args.value)
				result = "Is {} prime? {}".format(args.value, is_prime)
			else:
				sqrVal = math.isqrt(args.value)
				pl.UpdatePrimesToValue(sqrVal, timer_callback)
				is_prime = pl.IsPrime(args.value)
				result = "Is {} prime? {}".format(args.value, is_prime)
		except InterruptException:
			result = "Calculation interrupted. Partial result: Unable to determine if {} is prime.".format(args.value)
	
	if args.isMax:
		if args.value is None:
			print("Error: <value> is required for the -m/--max option.")
			return -1
		
		# Check if we need to start the timer (after 1 second)
		if not timer_started and time.time() - calc_start_time > 1.0:
			update_timer, timer_loop, stop_timer = show_processing_timer()
			timer_thread = threading.Thread(target=timer_loop, daemon=True)
			timer_thread.start()
			timer_started = True
		
		try:
			pl.UpdatePrimesToValue(args.value, timer_callback)
			result = "List of prime numbers:\n{}".format(pl)
		except InterruptException:
			result = "Calculation interrupted. Partial result - primes found up to {}:\n{}".format(pl.GetMax(), pl)
	
	if args.isNext:
		if args.value is None:
			print("Error: <value> is required for the -n/--next option.")
			return -1
		
		# Check if we need to start the timer (after 1 second)
		if not timer_started and time.time() - calc_start_time > 1.0:
			update_timer, timer_loop, stop_timer = show_processing_timer()
			timer_thread = threading.Thread(target=timer_loop, daemon=True)
			timer_thread.start()
			timer_started = True
		
		try:
			next_prime = pl.FindNextPrime(args.value, timer_callback)
			result = "Next prime after {}: {}".format(args.value, next_prime)
		except InterruptException:
			result = "Calculation interrupted. Unable to find next prime after {}.".format(args.value)
	
	if args.isPrev:
		if args.value is None:
			print("Error: <value> is required for the -p/--prev option.")
			return -1
		
		# Check if we need to start the timer (after 1 second)
		if not timer_started and time.time() - calc_start_time > 1.0:
			update_timer, timer_loop, stop_timer = show_processing_timer()
			timer_thread = threading.Thread(target=timer_loop, daemon=True)
			timer_thread.start()
			timer_started = True
		
		try:
			prev_prime = pl.FindPreviousPrime(args.value, timer_callback)
			if prev_prime is None:
				result = "No prime number exists before {}.".format(args.value)
			else:
				result = "Previous prime before {}: {}".format(args.value, prev_prime)
		except InterruptException:
			result = "Calculation interrupted. Unable to find previous prime before {}.".format(args.value)
	
	if args.isRange:
		if args.value is None or args.end_value is None:
			print("Error: Both <value> and <end_value> are required for the -r/--range option.")
			return -1
		if args.value > args.end_value:
			args.value, args.end_value = args.end_value, args.value
		
		# Check if we need to start the timer (after 1 second)
		if not timer_started and time.time() - calc_start_time > 1.0:
			update_timer, timer_loop, stop_timer = show_processing_timer()
			timer_thread = threading.Thread(target=timer_loop, daemon=True)
			timer_thread.start()
			timer_started = True
		
		try:
			count = pl.CountPrimesInRange(args.value, args.end_value, timer_callback)
			result = "Number of primes between {} and {}: {}".format(args.value, args.end_value, count)
		except InterruptException:
			result = "Calculation interrupted. Partial result: Found {} primes in range {} to {}.".format(len([p for p in pl._list if args.value <= p <= args.end_value]), args.value, args.end_value)
	
	if args.isFactors:
		if args.value is None:
			print("Error: <value> is required for the -f/--factors option.")
			return -1
		
		# Check if we need to start the timer (after 1 second)
		if not timer_started and time.time() - calc_start_time > 1.0:
			update_timer, timer_loop, stop_timer = show_processing_timer()
			timer_thread = threading.Thread(target=timer_loop, daemon=True)
			timer_thread.start()
			timer_started = True
		
		try:
			factors = pl.GetPrimeFactors(args.value)
			if factors:
				result = "Prime factors of {}: {}".format(args.value, factors)
			else:
				result = "{} has no prime factors.".format(args.value)
		except InterruptException:
			result = "Calculation interrupted. Unable to determine prime factors of {}.".format(args.value)
	
	# Track calculation end time
	calc_end_time = time.time()
	calc_time = calc_end_time - calc_start_time
	
	# Stop processing animation if it was running
	if args.showTiming and animation_thread:
		stop_animation()
		animation_thread.join(timeout=0.1)  # Wait up to 100ms for thread to stop
		sys.stdout.write('\r' + ' ' * 50 + '\r')
		sys.stdout.flush()
	
	# Stop timer if it was running
	if timer_started and timer_thread and stop_timer:
		stop_timer()
		timer_thread.join(timeout=0.1)  # Wait up to 100ms for thread to stop
		sys.stdout.write('\r' + ' ' * 60 + '\r')
		sys.stdout.flush()
	
	# Display result
	display_start_time = time.time()
	print(result)
	display_end_time = time.time()
	display_time = display_end_time - display_start_time
	
	# Display timing information if requested
	if args.showTiming:
		total_time = time.time() - start_time
		print("\n--- Timing Information ---")
		print("Calculation time: {}".format(format_time(calc_time)))
		print("Display time: {}".format(format_time(display_time)))
		print("Total runtime: {}".format(format_time(total_time)))
	
	# Reset interrupt flag for next run
	_interrupt_requested = False

main()