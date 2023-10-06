# pyeboot
Python interface for pspdecrypt and sign_np.

## Installation
`pip install pyeboot`

## Usage
```
import pyeboot
pyeboot.decrypt("EBOOT.BIN", "BOOT.BIN")
pyeboot.sign("BOOT.BIN", "EBOOT.BIN", "1")
```
