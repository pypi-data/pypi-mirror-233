from setuptools import setup, find_packages

# Read the contents of your README.md file
with open("readme.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name='qs-files',
    version='1.0.4',
    description='Python library for managing .qs files and configurations.',
    author='Quadrat.Ik',
    author_email='quadrat.ik@yandex.com',
    url='https://github.com/QuadratNew/qs-files',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)