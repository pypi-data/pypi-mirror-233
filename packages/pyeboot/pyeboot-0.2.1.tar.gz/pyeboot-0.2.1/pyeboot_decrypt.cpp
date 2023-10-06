#include "PrxDecrypter.h"
#include <fstream>

int WriteFile(const char *file, void *buf, int size)
{
    std::fstream myfile;
    myfile = std::fstream(file, std::ios::out | std::ios::binary);
    myfile.write((char*)buf, size);
    myfile.close();
    return size;
}

#define MALLOC_CHECK(var, additional) if (var == NULL) { PyErr_NoMemory(); additional; return NULL; }

extern "C"
{
    #include <Python.h>
    #include <stdio.h>

    static PyObject *method_decrypt(PyObject *self, PyObject *args, PyObject *kwargs)
    {
        char *infile = NULL;
        char *outfile = NULL;

        static char *kwlist[] = {"infile", "outfile",
                                    NULL};

        if(!PyArg_ParseTupleAndKeywords(args, kwargs, "ss", kwlist,
                                        &infile, &outfile))
            return NULL;

        // Open file
        FILE* f = fopen(infile, "rb");
        if (f == NULL)
            return NULL;
        fseek(f, 0, SEEK_END);
        long size = ftell(f);
        fseek(f, 0, SEEK_SET);
        // Allocate memory
        char* indata = (char*)PyMem_Malloc(sizeof(char) * size);
        MALLOC_CHECK(indata, fclose(f));
        char* outdata = (char*)PyMem_Malloc(sizeof(char) * size);
        MALLOC_CHECK(outdata, fclose(f));
        // Read and close file
        fread(indata, 1, size, f);
        fclose(f);
        // Decrypt and write it to file
        int outsize = pspDecryptPRX((const u8*)indata, (u8 *)outdata, size, NULL, true);
        if (outsize > 0)
            WriteFile(outfile, outdata, outsize);
        // Free memory and return
        PyMem_Free(indata);
        PyMem_Free(outdata);
        return PyBool_FromLong(outsize > 0 ? 1 : 0);
    }

    static PyMethodDef DecryptMethods[] = {
        {"decrypt", (PyCFunction)method_decrypt, METH_VARARGS | METH_KEYWORDS, "Python interface for pspdecrypt."},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef decryptmodule = {
        PyModuleDef_HEAD_INIT,
        "decrypt",
        "Python interface for pspdecrypt.",
        -1,
        DecryptMethods
    };

    PyMODINIT_FUNC PyInit_decrypt(void)
    {
        return PyModule_Create(&decryptmodule);
    }
}
