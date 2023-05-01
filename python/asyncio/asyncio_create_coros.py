"""
4 ways to run coros

1. using `asyncio.run()`
2. using `await`
3. using `asyncio.create_task`
4. using `asyncio.TaskGroup`

"""
import asyncio


async def main1():
    await asyncio.sleep(1)
    print("hello foo")


async def main2():
    await asyncio.sleep(1)
    print("hello bar")

    
async def main3():
   await asyncio.sleep(1) 
   print("Hello foobar")
   await main1()
   await main2()

   
async def non_blocking_func(wait): 
    await asyncio.sleep(wait)
    print(f"i m not blocking | {wait}")
  
   
async def main4():
    # here only after `non_blocking_func(3)`` finished, `non_block_func(1)`` will start
    await non_blocking_func(3)
    await non_blocking_func(1)

    # With `create_task` both will run concurrently. create_task is kinda like defer, doesn't wait till func get executed. 
    task1 = asyncio.create_task(non_blocking_func(3))
    task2 = asyncio.create_task(non_blocking_func(1))
    await task1
    await task2

  
async def main5(): 
    # with TaskGroup no need of `await`. `await` will be called automatically on exiting context-manager. Added in python3.11
    async with asyncio.TaskGroup() as tg:
        tg.create_task(non_blocking_func(3))
        tg.create_task(non_blocking_func(1))
   
    
asyncio.run(main1())
asyncio.run(main1())
asyncio.run(main2())
asyncio.run(main3())
asyncio.run(main4())
asyncio.run(main5())
