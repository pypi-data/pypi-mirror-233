# Copyright 2022 The FeatHub Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from concurrent.futures import Future

from feathub.processors.processor_job import ProcessorJob


class LocalJob(ProcessorJob):
    """
    A job instantiated by a LocalProcessor.
    """

    def __init__(self) -> None:
        super().__init__()

    def cancel(self) -> Future:
        f: Future[None] = Future()
        f.set_result(None)
        return f

    def wait(self, timeout_ms: int = None) -> None:
        pass
