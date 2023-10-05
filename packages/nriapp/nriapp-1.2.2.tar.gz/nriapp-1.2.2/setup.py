
from setuptools import setup, find_packages
from glob import glob

#with open('requirements.txt') as f:
#    requirements = f.read().splitlines()


setup(
   name='nriapp',
   version='1.2.02',
   description='This is an internal tool for querying MS 365 Defender using MSGraph and MS Sentinels API with NRI\n'
               'Added capability for MDR portal',
    license='MIT',
   author='Llallum Victoria',
   author_email='llallumvictoria@gmail.com',
#   packages=find_packages('src'),
   package_dir = {'':'src/nriapp'},
    
   packages=['.','config', 'core', 'helper'],  #same as name
#   packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
   data_files=[('.', ['src/nriapp/changelog.txt']),
               ('./session', glob('./src/session/*.*')),
               ('./logs', glob('./src/logs/*.*')),
               ('./output', glob('./src/output/*.*'))
              ],
   #setup_requires=['session', 'logs', 'output'],
   include_package_data=True,
   install_requires=[],
#   install_requires=requirements, #external packages as dependencies,
   entry_points = '''
        [console_scripts]
        nriapp=nriapp:main
    '''

)
