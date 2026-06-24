import asyncio, sys


async def check_package(package_name):
    process = await asyncio.create_subprocess_exec(

        sys.executable, "-m", "pip", "show", package_name,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await process.wait()
    return package_name, process.returncode == 0


async def main():
    package_check = sys.argv[1] if len(sys.argv) > 1 else 'pandas numpy'
    tasks = [asyncio.create_task(check_package(package)) for package in package_check.split()]
    for task in tasks:
        result = await task
        print(result)


if __name__ == '__main__':
    asyncio.run(main()) 
