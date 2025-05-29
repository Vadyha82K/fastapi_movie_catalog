from typing import reveal_type

from redis import Redis

from core import config


r = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def add(a: int, b: int) -> int:
    return a + b


def main() -> None:
    a = 1
    b = 2
    c = add(a, b)
    print(c)
    print("type c:", type(c))
    reveal_type(c)
    print(r.ping())
    r.set("first_name", "Vadim")
    r.set("last_name", "Konovalov")
    r.set("age", "43")
    print("first_name:", r.get("first_name"))
    print("age:", r.getdel("age"))
    print("age:", r.get("age"))


if __name__ == "__main__":
    main()
