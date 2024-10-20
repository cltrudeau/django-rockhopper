import nox

#def common(session):
#    session.install("logthing>=1.0.0")
#    session.install("screwdriver>=0.14.0")
#    session.install("waelstow>=0.11.0")
#    session.install("context-temp>=0.11.1")


# 500 is end of life April 2025, Py range is 3.10-3.12
@nox.session(python=["3.10", "3.11", "3.12"])
def test420(session):
#    common(session)
    session.install(f"django>=5.0,<5.1")
    session.run("./load_tests.py", external=True)


# 510 is end of life December 2025, Py range is 3.10-3.12
# (3.13 will be added when 5.1.3 comes out)
@nox.session(python=["3.10", "3.11", "3.12"])
def test420(session):
#    common(session)
    session.install(f"django>=5.1,<5.2")
    session.run("./load_tests.py", external=True)


