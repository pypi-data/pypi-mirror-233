from setuptools import setup, find_packages

with open ("README.md", "r") as f:
    long_description = f.read()

setup(name='pyleetcode-cli',
      version='0.2.0',
      description='A CLI tool to access LeetCode',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Jakub Kubiak',
      author_email='jakubkubiak234@gmail.com',
      packages=find_packages(),
      entry_points={'console_scripts': ['leet = leetcode.main:main'],},
      package_data={'': ['*.yaml', '*.graphql']},
      url='https://github.com/Coderbeep/LeetCode-CLI',
      license='MIT',
      )