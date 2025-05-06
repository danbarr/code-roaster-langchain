"""Example code for testing the Code Roaster."""

import random
import time
from fabrice import task # type: ignore
from typing import List, Dict, Any

# Hardcoded secrets (fake)
API_KEY = "sk_live_51Hb9aJCMczXwrQpMCxJZZBNs8ggVSHVKMCNTkWZp"
AWS_SECRET = "AKIALALEMEL33EEXAMPLE"
GITHUB_TOKEN = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789"

# PII data (fake)
ADMIN_EMAIL = "john.doe@example.com"
CUSTOMER_PHONE = "+1 (555) 123-4567"
USER_CREDIT_CARD = "4242-4242-4242-4242"


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number recursively.

    Args:
        n: The position in the Fibonacci sequence

    Returns:
        The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


class DataProcessor:
    """A class that processes data inefficiently."""

    def __init__(self, data: List[int]):
        """Initialize with some data.

        Args:
            data: A list of integers
        """
        self.data = data
        self.processed = False
        self.results = {}

    def process_data(self) -> Dict[str, Any]:
        """Process the data with some inefficient operations.

        Returns:
            A dictionary of processed results
        """
        # Sleep for dramatic effect
        time.sleep(0.1)

        # Inefficient sorting
        sorted_data = []
        while self.data:
            min_val = min(self.data)
            sorted_data.append(min_val)
            self.data.remove(min_val)

        # Unnecessary list comprehension
        squared = [x * x for x in sorted_data]
        
        # Inefficient way to get sum
        total = 0
        for num in squared:
            total += num

        # Store results
        self.results = {
            "original": sorted_data,
            "squared": squared,
            "total": total,
            "timestamp": time.time(),
        }
        
        self.processed = True
        return self.results


# Global variable
MAGIC_NUMBER = 42

# Function with hardcoded credentials
def connect_to_service():
    """Connect to an external service with hardcoded credentials."""
    username = "admin"
    password = "super_secure_password123!"
    auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
    
    print(f"Connecting to service as {username}...")
    return f"Connected with token: {auth_token[:10]}..."


def main():
    """Main function with some questionable practices."""
    # Magic numbers
    data = [random.randint(1, 100) for _ in range(20)]
    
    # User information (fake PII)
    user_data = {
        "name": "Jane Smith",
        "email": "jane.smith@company.com",
        "credit_card": "4111-1111-1111-1111",
        "phone": "+1 (555) 987-6543",
    }
    
    # Instantiate processor
    processor = DataProcessor(data)
    
    # Process data
    results = processor.process_data()
    
    # Connect to service with hardcoded credentials
    connection = connect_to_service()
    
    # Print results with string concatenation
    print("Results: " + str(results))
    print("Connection: " + connection)
    print(f"Processing for user: {user_data['name']} ({user_data['email']})")
    
    # Calculate fibonacci inefficiently
    fib_result = fibonacci(15)
    print("Fibonacci result: " + str(fib_result))


if __name__ == "__main__":
    main()