import asyncio


async def main():
    print("Hello_Thailand_1")
    await asyncio.sleep(1)
    print("Hello_Thailand_2")


async def func():
    print("Hello_Thailand_3")

event_loop = asyncio.new_event_loop()
tasks = [event_loop.create_task(main()), event_loop.create_task(func())]
wait_tasks = asyncio.wait(tasks)
event_loop.run_until_complete(wait_tasks)
event_loop.close()
