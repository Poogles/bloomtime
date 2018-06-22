# Bloomtime

A bloom filter where optional TTLs can be set for expiry.


```
>>> bloom = bloomtime.BloomTime(1000, 0.01)
>>> TTL = 400
>>> 
>>> bloom.set('foo', ttl=TTL)
>>> bloom.get('foo')
True
>>> bloom.get('bar')
False
```
