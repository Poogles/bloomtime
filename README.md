# Bloomtime

A bloom filter where optional TTLs can be set for expiry.

TTLs are handled very very very naively, this is not an optimal implementation
at all.  This should not be used in production unless you really know what
you are doing.  If you did know what you were doing you'd likely use one of the
other working bloom filters out there!

If you do however want to use it, the API is as follows. 

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
