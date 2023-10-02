
## Overview

This is a simple library for utility functions for data processing.
Currently implemented functions are:
- cross-correlation
- transpose-
- window.

## Installation

### Prerequisites

- Python 3.10 or newer.

Just run `pip install turing_transforms2`

## Usage

```python
from turing_transforms2 import window
windows = window(list(range(5)), size=2)
```

### Future improvements

- convolution support for padding and channel dimension.
- transpose support for multiple dimensions.
