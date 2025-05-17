from redis import Redis

from core import config


r = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main():
    print(r.ping())
    r.set("first_name", "Vadim")
    r.set("last_name", "Konovalov")
    r.set("age", "43")
    print("first_name:", r.get("first_name"))
    print("age:", r.getdel("age"))
    print("age:", r.get("age"))


if __name__ == "__main__":
    main()
