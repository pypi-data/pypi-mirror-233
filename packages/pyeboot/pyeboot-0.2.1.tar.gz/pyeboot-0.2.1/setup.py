import platform
import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.name == "nt":
    EXTRA_COMPILE_ARGS = []
    MACROS = [("_WIN", "")]
elif platform.system() == "Darwin":
    EXTRA_COMPILE_ARGS = ["-std=c++11"]
    MACROS = []
else:
    EXTRA_COMPILE_ARGS = []
    MACROS = []

DECRYPT_INCLUDES = ["pspdecrypt", "pspdecrypt/libkirk"]
SIGN_INCLUDES = ["sign_np"]

decrypt_sources = ["pyeboot_decrypt.cpp",
                   "pspdecrypt/PrxDecrypter.cpp",
                   "pspdecrypt/libkirk/AES.c", "pspdecrypt/libkirk/amctrl.c", "pspdecrypt/libkirk/bn.c", "pspdecrypt/libkirk/ec.c", "pspdecrypt/libkirk/kirk_engine.c", "pspdecrypt/libkirk/SHA1.c"]
sign_sources = ["pyeboot_sign.cpp",
                "sign_np/sign_np.c", "sign_np/eboot.c", "sign_np/pgd.c", "sign_np/tlzrc.c", "sign_np/utils.c",
                "sign_np/libkirk/aes.c", "sign_np/libkirk/amctrl.c", "sign_np/libkirk/bn.c", "sign_np/libkirk/ec.c", "sign_np/libkirk/kirk_engine.c", "sign_np/libkirk/sha1.c"]

# Monkey-patch build_ext to remove the "-stc=c++11" flag from c files.
class build_ext_subclass(build_ext):
    def build_extensions(self):
        original__compile = self.compiler._compile
        def new__compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
            if src.endswith(".c"):
                extra_postargs = [s for s in extra_postargs if s != "-std=c++11"]
            return original__compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
        self.compiler._compile = new__compile
        try:
            build_ext.build_extensions(self)
        finally:
            del self.compiler._compile

def main():
    setup(name="pyeboot",
          version="0.2.1",
          author="Illidan",
          description="Python interface for pspdecrypt and sign_np.",
          long_description=long_description,
          long_description_content_type="text/markdown",
          url="https://github.com/Illidanz/pyeboot",
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          ],
          packages=["pyeboot"],
          ext_modules=[
              Extension("pyeboot.decrypt", decrypt_sources, include_dirs=DECRYPT_INCLUDES, define_macros=MACROS, extra_compile_args=EXTRA_COMPILE_ARGS),
              Extension("pyeboot.sign", sign_sources, include_dirs=SIGN_INCLUDES, define_macros=MACROS),
          ],
          cmdclass = {"build_ext": build_ext_subclass},
        )

if __name__ == "__main__":
    main()
