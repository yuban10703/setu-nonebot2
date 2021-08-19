import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="setu-nonebot2",
    version="0.0.2",
    author="yuban10703",
    author_email="yuban10703@foxmail.com",
    python_requires=">=3.8",
    install_requires=["httpx", "httpx-socks[asyncio]", "pydantic", "tinydb"],
    description="QQ机器人 色图姬",
    license='MIT',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuban10703/setu-nonebot2",
    packages=setuptools.find_packages(),
)
