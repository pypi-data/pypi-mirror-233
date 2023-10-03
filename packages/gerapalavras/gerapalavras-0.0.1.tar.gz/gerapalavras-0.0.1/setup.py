from setuptools import setup

with open("README.md","r") as fh:
    readme = fh.read()

setup(name='gerapalavras',
      version='0.0.1',
      url='',
      license='MIT License',
      author='Leonardo de Medeiros Bernardes',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='leonardo22070053@aluno.cesupa.br',
      keywords='Pacote',
      description='Pacote python para gerar palavras dissilabas aleatorias',
      packages=['base','gerador'],
      install_requires=[''])