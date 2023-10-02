# limited 🚀

**limited** is your go-to Python rate limiting package, designed for advanced and efficient performance. It seamlessly supports both synchronous programs, using threads through `SyncLimiter`, and asynchronous programs, utilizing asyncio through `AsyncLimiter`.

## Examples 📝

Getting started with **limited** is effortless! For regular, synchronous functions declared with `def`, use `SyncLimiter`:

```python
from limited import SyncLimiter

@SyncLimiter(limit=3, every=5)
def job():
    pass
```

For asynchronous functions declared with `async def`, opt for `AsyncLimiter`:

```python
from limited import AsyncLimiter

@AsyncLimiter(limit=3, every=5)
async def async_job():
    pass
```

### Share Limits 👨‍👦‍👦

Take it up a notch by creating a limiter instance and share it across multiple functions. This allows you to enforce the same constraints on **multiple** functions simultaneously. In the example below, both first_job and second_job are limited to 3 calls every 5 seconds, **collectively**.

```python
from limited import SyncLimiter

my_limiter = SyncLimiter(limit=3, every=5)

@my_sync_limiter
def first_job():
    pass

@my_sync_limiter
def second_job():
    pass
```

For asynchronous functions, employ `AsyncLimiter` in a similar fashion.

### Stack Limits 📚

Stack limits on a single function to satisfy multiple constraints simultaneously. In the following example, both limiting constrained are enforces separately.

```python
from limited import SyncLimiter

my_first_limiter = SyncLimiter(limit=3, every=5)
my_second_limiter = SyncLimiter(limit=1, every=1)

@my_first_limiter
@my_second_limiter
def my_job():
    pass

```

Combining sharing limits with multiple functions, and stacking multiple limits to the same functions, allows for complex limiting logic.

**limited** offers the flexibility you need to create complex rate limiting logic effortlessly. Fine-tune your applications, experiment, and let your projects soar to new heights! 🚀✨
