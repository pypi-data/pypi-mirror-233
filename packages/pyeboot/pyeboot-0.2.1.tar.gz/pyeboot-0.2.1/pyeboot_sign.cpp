#include "sign_np.h"
int main(int argc, char *argv[]);

#define MALLOC_CHECK(var) if (var == NULL) { PyErr_NoMemory(); return NULL; }

extern "C"
{
    #include <Python.h>

    static PyObject *method_sign(PyObject *self, PyObject *args, PyObject *kwargs)
    {
        char *infile = NULL;
        char *outfile = NULL;
        char *tag = NULL;

        static char *kwlist[] = {"infile", "outfile", "tag",
                                    NULL};

        if(!PyArg_ParseTupleAndKeywords(args, kwargs, "sss", kwlist,
                                        &infile, &outfile, &tag))
            return NULL;

        int argc = 5;
        char** argv = (char**)PyMem_Malloc(sizeof(char*) * (argc + 1));
        MALLOC_CHECK(argv);
        argv[0] = "sign_np";
        argv[1] = "-elf";
        argv[2] = infile;
        argv[3] = outfile;
        argv[4] = tag;
        argv[5] = NULL;
        int result = main(argc, argv);
        PyMem_Free(argv);
        return PyBool_FromLong((long)(result == 0));
    }

    static PyMethodDef SignMethods[] = {
        {"sign", (PyCFunction)method_sign, METH_VARARGS | METH_KEYWORDS, "Python interface for sign_np."},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef signmodule = {
        PyModuleDef_HEAD_INIT,
        "sign",
        "Python interface for sign_np.",
        -1,
        SignMethods
    };

    PyMODINIT_FUNC PyInit_sign(void)
    {
        return PyModule_Create(&signmodule);
    }
}
