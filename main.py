import pytracer
import sys
def main(arg1):
    tracer = pytracer.Py_Trace()
    tracer.trace_route(arg1)
if __name__ == "__main__":
    main(sys.argv[1])