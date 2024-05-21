from invoke import task


@task
def test(c):
    c.run('python -m pytest .')


@task
def build(c):
    c.run('python -m build .')


@task(pre=[test, build], default=True)
def default(c):
    pass
