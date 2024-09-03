import pytracer

print(dir(pytracer))
tracer = pytracer.Py_Trace()
tracer.trace_route("google.com")
