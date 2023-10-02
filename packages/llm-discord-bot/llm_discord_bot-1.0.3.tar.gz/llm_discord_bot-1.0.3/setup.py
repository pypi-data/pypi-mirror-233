from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='llm_discord_bot',
    version='1.0.3',
    description='LLM Discord Bot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='Jimming Cheng',
    author_email='jimming@gmail.com',
    packages=['llm_discord_bot'],
    install_requires=[
        'arrow',
        'discord',
        'langchain',
        'llm_task_handler',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
