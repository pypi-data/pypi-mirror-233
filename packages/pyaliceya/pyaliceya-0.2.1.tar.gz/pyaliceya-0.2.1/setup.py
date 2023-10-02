import setuptools
with open(r'/Users/admin/Desktop/python/pyAlice/README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='pyaliceya',
	version='0.2.1',
	author='oboroksergey',
	author_email='oborok05@bk.ru',
	description='lib for yandex alice demo',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/sergey200519/pyAlice',
	packages=['pyAlice', 'pyAlice/errors', 'pyAlice/messages'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)