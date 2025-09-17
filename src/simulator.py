import secrets
import hashlib

class AviatorSimulator:
    def __init__(self, seed=None):
        """
        Initialize the simulator with an optional seed.
        If no seed is provided, generate a random one.
        """
        if seed is None:
            self.seed = secrets.token_hex(16)
        else:
            self.seed = seed
        self.hash = self._hash_seed(self.seed)

    def _hash_seed(self, seed):
        """
        Compute SHA-256 hash of the seed for provably fair mechanism.
        """
        return hashlib.sha256(seed.encode()).hexdigest()

    def generate_crash_multiplier(self):
        """
        Generate a crash multiplier using a cryptographically secure RNG.
        The multiplier is >= 1.0 and can be arbitrarily large.
        This example uses a simple formula for demonstration.
        """
        # Use the seed hash as entropy source
        entropy = int(self.hash, 16)
        # Generate a random float between 0 and 1 using entropy
        random_float = (entropy % 1000000) / 1000000.0
        # Calculate multiplier: minimum 1.0, max 100.0 for example
        multiplier = 1.0 + random_float * 99.0
        return round(multiplier, 2)

    def get_provably_fair_hash(self):
        """
        Return the hash used for provably fair verification.
        """
        return self.hash

if __name__ == "__main__":
    sim = AviatorSimulator()
    print("Seed:", sim.seed)
    print("Hash:", sim.get_provably_fair_hash())
    print("Crash Multiplier:", sim.generate_crash_multiplier())
