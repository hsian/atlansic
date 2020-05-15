import os
import sys
import click

from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate, upgrade

# COV = None
# if os.environ.get('FLASK_COVERAGE'):
# 	import coverage
# 	COV = coverage.coverage(branch=True, include='app/*')
# 	COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Role=Role)

# example flask test user
@app.cli.command()
@click.argument('module')	
@click.option('--coverage/--no-coverage', default=False,
			help='Run tests under code coverage.')
def test(coverage, module):
	COV = None
	
	"""Run the unit tests."""
	if coverage:
		os.environ['FLASK_COVERAGE'] = '1'
		# 设定完环境变量 FLASK_COVERAGE 后，脚本会重启自身,貌似不支持windows
		# os.execvp(sys.executable, [sys.executable] + sys.argv)
		import coverage
		COV = coverage.coverage(branch=True, include='app/*')
		COV.start()	

	import unittest
	# if module == 'all':
	# 	tests =  unittest.TestLoader().discover('app', pattern='*/test_*.py')
	# else:
	tests =  unittest.TestLoader().discover('app/tests/', pattern='test_%s.py' % module)
	unittest.TextTestRunner(verbosity=2).run(tests)
	
	if COV:
		COV.stop()
		COV.save()
		print('Coverage Summary:')
		COV.report()
		basedir = os.path.abspath(os.path.dirname(__file__))
		covdir = os.path.join(basedir, 'tmp/coverage')
		COV.html_report(directory=covdir)
		print('HTML version: file://%s/index.html' % covdir)
		COV.erase()

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

    User.insert_admin()
