from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='Promptuner',
    version='0.0.1',
    description='Turning small task descriptions into mega prompts automatically.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/unclecode/promptuner',
    author='Your Name',
    author_email='unclecode@kidocode.com',
    license='Apache License 2.0',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'promptuner': ['metaprompts/*.md'],
    },
    install_requires=required,
    entry_points={
        "console_scripts": [
            "promptuner=promptuner.__main__:main",
        ]
    },
    python_requires='>=3.6',
)
