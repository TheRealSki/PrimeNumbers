# Prime Number Calculator

A comprehensive Python tool for prime number calculations with interrupt capability.

## Features

- **Prime Number Generation**: Generate all primes up to a specified value
- **Prime Checking**: Check if a number is prime
- **Next/Previous Prime**: Find the next or previous prime number
- **Range Counting**: Count primes in a specified range
- **Prime Factorization**: Get prime factors of a number
- **Large Number Support**: Optimized algorithms for numbers > 10,000,000
- **Interrupt Capability**: Press Ctrl+C to interrupt long calculations and get partial results
- **Progress Timer**: Automatic timer display for long-running operations
- **Timing Information**: Detailed timing breakdown with `--timing` flag

## Usage

### Basic Commands

```bash
# Check if a number is prime
python find_primes.py -c 1000000

# Generate all primes up to a value
python find_primes.py -m 1000

# Find next prime after a number
python find_primes.py -n 1000000

# Find previous prime before a number
python find_primes.py -p 1000000

# Count primes in a range
python find_primes.py -r 1000000 1000100

# Get prime factors
python find_primes.py -f 1000000

# Show highest prime in database
python find_primes.py -t

# Use large number optimizations
python find_primes.py -l -c 1000000000

# Show timing information
python find_primes.py --timing -r 1000000 1000100
```

### Interrupt Functionality

The program supports interrupting long calculations:

1. **Automatic Timer**: For operations taking longer than 1 second, a timer automatically appears
2. **Interrupt Instructions**: The timer shows "Press Ctrl+C to interrupt"
3. **Graceful Interruption**: Press Ctrl+C to stop the calculation and get partial results
4. **Partial Results**: The program returns whatever results it has found so far

#### Example Interrupt Usage

```bash
# Start a long calculation
python find_primes.py -r 1000000000 1000010000 --timing

# Wait for timer to appear, then press Ctrl+C
# You'll see output like:
# "Calculation interrupted. Partial result: Found X primes in range..."
```

### Command Line Options

- `-c, --check`: Check if a number is prime
- `-m, --max`: Generate all primes up to a value
- `-n, --next`: Find next prime after a number
- `-p, --prev`: Find previous prime before a number
- `-r, --range`: Count primes in a range (requires start and end values)
- `-f, --factors`: Get prime factorization
- `-t, --top`: Show highest prime in database
- `-l, --large`: Use optimized algorithms for large numbers (>10M)
- `--timing`: Show detailed timing information

## Algorithm Details

### Small Numbers (< 10,000,000)
- Divisibility tests for 2, 3, 5, 7, 11, 13
- Trial division with cached primes

### Large Numbers (> 10,000,000)
- Enhanced divisibility tests
- Miller-Rabin primality test
- Wheel factorization optimization

### Interrupt Handling
- Signal handling for Ctrl+C (SIGINT)
- Check points throughout all calculation loops
- Graceful exception handling with partial results
- Automatic cleanup of threads and timers

## Performance

- **Small numbers**: Very fast with cached results
- **Large numbers**: Optimized with probabilistic tests
- **Memory efficient**: Only stores discovered primes
- **Persistent storage**: Results saved to `primes.txt`

## Examples

### Quick Prime Check
```bash
$ python find_primes.py -c 1000000
Is 1000000 prime? False
```

### Long Calculation with Timer
```bash
$ python find_primes.py -r 1000000000 1000010000 --timing
Processing... Elapsed time: 00:00:15:32 (Press Ctrl+C to interrupt)
Number of primes between 1000000000 and 1000010000: 487
```

### Interrupted Calculation
```bash
$ python find_primes.py -r 1000000000 1000010000 --timing
Processing... Elapsed time: 00:00:08:15 (Press Ctrl+C to interrupt)
^C
Calculation interrupted. Partial result: Found 243 primes in range 1000000000 to 1000010000.
```

## Files

- `find_primes.py`: Main program
- `primes.txt`: Database of discovered primes
- `demo_interrupt.py`: Demonstration of interrupt functionality
- `test_interrupt.py`: Test script for interrupt functionality

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Notes

- The program automatically saves discovered primes to `primes.txt`
- Large number calculations use probabilistic tests (very high accuracy)
- Interrupt functionality works on all calculation types
- Timer appears automatically for operations > 1 second
- All timing information is available with `--timing` flag 