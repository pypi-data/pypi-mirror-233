from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='logmag',
      version='1.1',
      description='Logging',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['logmag'],
      author_email='zhassulanissayev@gmail.com',
      zip_safe=False)
