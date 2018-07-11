"""Time windowed bloom filter.

"""
import array
import logging
import math
import time


log = logging.getLogger('bloomtime')

# This is mostly lifted from this lovely guide and the calculator here...
# https://bugra.github.io/work/notes/2016-06-05/a-gentle-introduction-to-bloom-filter/
# https://hur.st/bloomfilter/?n=20000000&p=1.0E-5&m=&k=


class BloomTime:

    def __init__(self, capacity: int, error_rate: float) -> None:
        """Initialise a TTL based bloom filter.

        Args:
            capacity: Total expected capacity of the bloom filter.
            error_rate: Target error rate of the bloom filter.

        This will take some time to initialise for large capacities due to
        provisioning a fixed size array.
        """
        if error_rate > 0.01:
            raise ValueError('Error rate must be less than 0.01.')
        if capacity < 1:
            raise ValueError('Capacity must be greater than one.')
        self._capacity = capacity
        self.error_rate = error_rate
        # TODO: Calculate hashes and array dynamically based upon a best guess.
        # This hashes number always need to be an odd number due to the way
        # we summarise the TTLs by chosing to glob together on the modal TTL.
        self.hashes = 9
        self.array_size = (
            math.ceil((self._capacity * math.log(self.error_rate)) / math.log(
                1 / pow(2, math.log(2)))))

        log.debug('Initialising an array of %s size.', self.array_size)
        # Initialise an empty Array of unssigned ints.
        # They're intialised empty with 0s as the initial char.
        self._container = array.array('I', [0 for x in range(self.array_size)])

    def __contains__(self, key: str) -> bool:
        return self.get(key)

    def set(self, key: str, ttl: int = 0) -> None:
        """Set a key in the bloom filter.

        Args:
            path: string path to set.
        Kwargs:
            ttl: TTL expiry time to set keys for.


        """
        if ttl:
            expire_time = int(time.time() + ttl)
        # Else set this value to the largest thing we can.
        else:
            expire_time = 2147483647

        # Insert the key based upon the total number of hashes.
        for i in range(self.hashes):
            bucket = hash(str(key) + str(i)) % self.array_size
            log.debug('Setting bucket %s with %s.', bucket, ttl)
            self._container[bucket] = expire_time

        log.debug('All hashes set.')

    def get(self, key: str) -> bool:
        """Check if a key is present in the bloom filter.

        Args:
            key: string path to check.

        Returns:
            bool: True if key is present in bloom filter and has not
                expired.  False if the key is not present or the TTL has
                expired.
        """
        results = []

        # Fetch all hashes for the given key.
        for i in range(self.hashes):
            bucket = hash(str(key) + str(i)) % self.array_size
            result = self._container[bucket]
            log.debug('Reading bucket %s as %s.', bucket, result)
            results.append(result)

        # Due to us abusing how bloom filters work, we need to find the
        # most common result.
        most_common_result = max(set(results), key=results.count)
        now = time.time()

        # If the most common result is 0, nothing has been set here.
        if most_common_result == 0:
            return False
        # Check to see if the Key has expired out.
        elif now > most_common_result:
            return False
        # Else the result must be True.
        else:
            return True
