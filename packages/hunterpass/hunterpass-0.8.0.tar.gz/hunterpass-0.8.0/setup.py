from setuptools import setup, find_packages

VERSION = '0.8.0'
DESCRIPTION = 'Generate dictionary with AI'
LONG_DESCRIPTION = 'A python tool that generates a dictionary for break password. This passwords will be generated' \
                   'by a LLM (AI) and this tool will have an integration with John, The Ripper'

# Setting up
setup(
    name="hunterpass",
    version=VERSION,
    author="rafa_dev (Rafael Macedo)",
    author_email="<rafaelrodriguesmacedo2004@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['os.path', 'argparse'],  # packages that requires to project work correctly
    keywords=['python', 'dictionary', 'generate', 'llm', 'security', 'hashes', 'hash', 'cybersecurity', 'cyber',
              'hacking', ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
