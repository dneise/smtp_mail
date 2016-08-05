from setuptools import setup

setup(
    name='smtp_mail',
    version='0.0.1',
    description='a simple smtp mailer with CLI',
    url='https://github.com/dneise/smtp_mail',
    author='Dominik Neise',
    author_email='neised@phys.ethz.ch',
    license='MIT',
    install_requires=[
        'docopt',
    ],
    package_data={'smtp_mail': ['config.json_template']},
    include_package_data=True,
    packages=['smtp_mail'],
    entry_points={
        'console_scripts': [
            'mail = smtp_mail.__main__:main',
        ]
    }
)