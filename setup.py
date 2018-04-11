from distutils.core import setup

setup(
    name='zhb_auto_interface',
    version='python27',
    packages=['spongebob', 'test_suites', 'test_suites.test_article', 'test_suites.test_red_packet',
              'test_suites.test_app', 'test_suites.test_order_manage'],
    url='',
    license='',
    author='jishanshan',
    author_email='jishanshan@zuihuibao.com',
    description='',
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
