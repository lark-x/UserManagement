import pkg_resources
dependencies = [pkg.key for pkg in pkg_resources.working_set]
d = str(dependencies)
print(d)
