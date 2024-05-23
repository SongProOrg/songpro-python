from invoke import task


@task
def clean(c):
    c.run('rm -rf dist/*')


@task
def test(c):
    c.run('python -m pytest .')


@task
def build(c):
    c.run('python -m build')


@task
def upload_test(c):
    c.run('python -m twine upload --repository testpypi dist/*')


@task(pre=[test, clean, build], default=True)
def default(c):
    pass
