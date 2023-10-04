from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('GausBinom_probability_Dist/README.md', 'rst')
except(IOError, ImportError):
    long_description = open('GausBinom_probability_Dist/README.md').read()

setup(name='GausBinom_probability_Dist',
      version='0.3',
      description='Gaussian and Bionomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['GausBinom_probability_Dist'],
      author = "Rojan Saghian",
      zip_safe=False)
