from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='body-oc',
	version='1.0.2',
	description='Body contains shared concepts among all body parts',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/body/',
	project_urls={
		'Documentation': 'https://ouroboroscoding.com/body/',
		'Source': 'https://github.com/ouroboroscoding/body',
		'Tracker': 'https://github.com/ouroboroscoding/body/issues'
	},
	keywords=['rest','microservices'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='Custom',
	packages=['body'],
	python_requires='>=3.10',
	install_requires=[
		'Rest-OC>=1.2.4'
	],
	zip_safe=True
)