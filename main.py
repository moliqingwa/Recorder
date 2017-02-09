#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from recorder.recorder import main

# allow this script to be executed as a child of another script (lsprofcalltree, for example)
sys.path.insert(0, '.')


if __name__ == '__main__':
    main()
