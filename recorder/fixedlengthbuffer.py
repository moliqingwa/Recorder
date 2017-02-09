#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017

import numpy as np


class FixedLengthBufferOverflow(Exception):
    def __init__(self, needed_length, current_length):
        self.need_length = needed_length
        self.current_length = current_length


class FixedLengthBuffer: # todo: maybe subclass of np.ndarray much better ???
    def __init__(self, logger, shape=(1, 8192), anotherbuffer=None):
        self.buffer = np.zeros(shape)
        self.buffer_length = shape[1]
        self.logger = logger

        # copy from another buffer
        if anotherbuffer is not None:
            if not isinstance(anotherbuffer, FixedLengthBuffer):
                raise TypeError("anotherbuffer should be an instance of class FixedLengthBuffer")

            buffer = anotherbuffer.read_buffer()
            currentdim, currentlen = shape
            anotherdim, anotherlen = buffer.shape

            if currentdim < anotherdim:
                if currentlen < anotherlen:
                    self.buffer[: currentdim, : currentlen] = buffer[: currentdim, -currentlen:]
                else:
                    self.buffer[: currentdim, : -anotherlen] = buffer[: currentdim, anotherlen:]
            else:  # currentdim >= anotherdim
                if currentlen < anotherlen:
                    self.buffer[: anotherdim, : currentlen] = buffer[: anotherdim, -currentlen:]
                else:
                    self.buffer[: anotherdim, -anotherlen:] = buffer[: anotherdim, : anotherlen]

    def push(self, floatdata):
        dim, length = floatdata.shape

        if length > self.buffer_length:
            print("warning: new data length = {}, which is longer than the bufer length = {}".format(length,
                                                                                                     self.buffer_length))

        # update the buffer
        if dim != self.buffer.shape[0]:
            # switched from single to dual channels or vice versa
            self.buffer = np.zeros((dim, self.buffer_length))

        length = length if length <= self.buffer_length else self.buffer_length
        self.buffer[:, 0: -length] = self.buffer[:, length:]
        self.buffer[:, -length:] = floatdata[:, -length:]

    def read_buffer(self):
        return self.buffer

    def buffer_shape(self):
        return self.buffer.shape

    def buffer_length(self):
        return self.buffer_length
