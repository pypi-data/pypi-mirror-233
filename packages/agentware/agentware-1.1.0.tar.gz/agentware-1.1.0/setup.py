from setuptools import setup, find_packages

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='agentware',
    version='1.1.0',
    description='A framework that makes it easy to generate controlled LLM output in json format',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='darthjaja',
    author_email='darthjaja6@gmail.com',
    packages=find_packages(),
    package_data={
        'agentware': ['base_agent_configs/*.json']
    },
    install_requires=[
        "openai<=0.27.2",
        "python-dotenv<=1.0.0",
        "pystache<=0.6.0",
        'jsonschema<=4.19.1',
    ],
)
