from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'pollboy',
    version = '0.4.0',
    author = 'Blake Bengtson',
    author_email = 'blake@bengtson.us',
    license = 'MIT',
    description = 'Check RSS feed for new posts and send notifications',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/bbeng89/pollboy',
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.8',
    classifiers=[
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities"
    ],
    entry_points = {
        'console_scripts': [
            'pollboy=pollboy.pollboy:run'
        ]
    }
)
