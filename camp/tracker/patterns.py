"""
Copyright 2016, Michael DeHaan <michael.dehaan@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from camp.band.selectors.endlessly import Endlessly
from camp.band.selectors.repeatedly import Repeatedly
from camp.band.selectors.randomly import Randomly

class Patterns(object):

    def __init__(self):
        self._patterns = dict()

    def _produce(self):
        raise Exception("Patterns is not a thing, did you mean BasicPatterns, EndlessPatterns, RandomPatterns, or RepeatedPatterns?")

    def set(self, **kwargs):
        def callback(song):
            for (name, pattern) in kwargs.items():
                if isinstance(pattern, str):
                    pattern = pattern.replace("|","").split()
                self._patterns[name] = self._produce(pattern)
            return self
        return callback

    def as_dict(self):
        return self._patterns

class RandomPatterns(Patterns):

    def __init__(self, mode):
        self.mode = mode
        super().__init__()

    def _produce(self, pattern):
        return Randomly(pattern, mode=self.mode)

class EndlessPatterns(Patterns):

    def _produce(self, pattern):
        return Endlessly(pattern)

class BasicPatterns(Patterns):

    def _produce(self, pattern):
        return pattern

class RepeatedPatterns(Patterns):

    def __init__(self, hold=None):
        self.hold = hold
        super().__init__()


    def _produce(self, pattern):
        return Repeatedly(pattern, hold=self.hold)