from setuptools import setup, find_packages

setup(
    name="mcc_workshop",
    version="0.0.5",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot==20.5",
        "python-dotenv==1.0.0",
        "openai==0.27.6"
    ]
)
