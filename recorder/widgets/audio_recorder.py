#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017

import numpy as np
import queue
import threading
import time
import wave

from recorder.utilities.audioFeatureExtraction import stZCR, stEnergy, stEnergyEntropy


class AudioRecorder():
    def __init__(self):
        self.writers = []

    def start(self, fname, channels, rate, sampwidth, ratio):
        self.stop()
        writer = Writer(fname, channels, rate, sampwidth, ratio)
        writer.start()
        self.writers.append(writer)
        return writer

    def stop(self):
        for w in self.writers:
            w.stop()
        self.writers.clear()


class Writer(threading.Thread):
    def __init__(self, fname, channels, rate, sampwidth, ratio = 1.0):
        super(Writer, self).__init__()
        self._stopped = False
        self._queue = queue.Queue()

        self.fname = fname
        self.channels = channels
        self.samplerate = rate
        self.sampwidth = sampwidth
        self.ratio = ratio

        self._filter = None

    def set_filter(self, **kwargs):#zcr=None, energy=None, entropy=None
        self._filter = Filter()
        self._filter.set_filter(**kwargs)

    def disable_filter(self):
        self._filter = None

    def run(self):
        with self._prepare_file(self.fname, self.channels, self.samplerate, self.sampwidth) as wavefile:
            while not self._stopped:
                while not self._queue.empty():
                    try:
                        floatdata = self._queue.get(block=False)

                        # filter
                        if self._filter and not self._filter.test(floatdata[0, :]):
                            continue

                        intdata = floatdata * self.ratio
                        intdata = intdata.astype(np.uint16, copy=False)
                        if floatdata is not None:
                            wavefile.writeframes(self._array2wav(intdata, self.sampwidth))
                        else:
                            pass  # wait
                    except queue.Empty:
                        pass
                time.sleep(1) # 1 seconds

    def stop(self):
        self._stopped = True

    def write(self, floatdata):
        self._queue.put(floatdata)

    def _prepare_file(self, fname, channels, rate, sampwidth=2, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(channels)
        wavefile.setsampwidth(sampwidth)  # 2 bytes, e.g. uint 16
        wavefile.setframerate(rate)
        return wavefile

    def _array2wav(self, a, sampwidth):
        """
        Convert the input array `a` to a string of WAV data.

        a.dtype must be one of uint8, int16 or int32.  Allowed sampwidth
        values are:
            dtype    sampwidth
            uint8        1
            int16        2
            int32      3 or 4
        When sampwidth is 3, the *low* bytes of `a` are assumed to contain
        the values to include in the string.
        """
        if sampwidth == 3:
            # `a` must have dtype int32
            if a.ndim == 1:
                # Convert to a 2D array with a single column.
                a = a.reshape(-1, 1)
            # By shifting first 0 bits, then 8, then 16, the resulting output
            # is 24 bit little-endian.
            a8 = (a.reshape(a.shape + (1,)) >> np.array([0, 8, 16])) & 255
            wavdata = a8.astype(np.uint8).tostring()
        else:
            # Make sure the array is little-endian, and then convert using
            # tostring()
            a = a.astype('<' + a.dtype.str[1:], copy=False)
            wavdata = a.tostring()
        return wavdata


class Filter():
    def __init__(self):
        self.stZCR = None
        self.stEnergy = None
        self.stEnergyEntropy = None

    def set_filter(self, zcr=None, energy=None, entropy=None): # zcr=None, energy=None, entropy=None
        self.stZCR = zcr
        self.stEnergy = energy
        self.stEnergyEntropy = entropy
        # self.stZCR = kwargs.get("zcr", None)
        # self.stEnergy = kwargs.get("energy", None)
        # self.stEnergyEntropy = kwargs.get("entropy", None)

    def test(self, floatdata):
        if self.stZCR is not None and self.stZCR > stZCR(floatdata):
            return False

        if self.stEnergy is not None and self.stEnergy > stEnergy(floatdata):
            return False

        if self.stEnergyEntropy is not None and self.stEnergyEntropy > stEnergyEntropy(floatdata):
            return False
        return True