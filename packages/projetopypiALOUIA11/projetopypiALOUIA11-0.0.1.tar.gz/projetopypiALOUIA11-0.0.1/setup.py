from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='projetopypiALOUIA11',
    version='0.0.1',
    license='MIT License',
    author='Rafael Juliano',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='rafael22070063@aluno.cesupa.br',
    keywords='Pacote',
    description='Pacote python para gerar palavras dissílabas',
    install_requires=['random'],
    packages=['base', 'gerador'],)