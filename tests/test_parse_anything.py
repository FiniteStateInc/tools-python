# Copyright (c) 2021 spdx tool contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest
from spdx.parsers import parse_anything


dirname = os.path.join(os.path.dirname(__file__), "data", "formats")
test_files = [os.path.join(dirname, fn) for fn in os.listdir(dirname)]


@pytest.mark.parametrize("test_file", test_files)
def test_parse_anything(test_file):
    doc, error = parse_anything.parse_file(test_file)

    in_basename = os.path.basename(test_file)
    if in_basename == "SPDXJSONExample-v2.2.spdx.json":
        # conversion of spdx2.2 is not yet done
        chksum_error_suffix = 'File checksum must be instance of spdx.checksum.Algorithm'
        expected_errors = set([chksum_error_suffix])  # spdx/tools-python/pull/197 should fix
        validation_errors = set(msg.rsplit(':').pop().strip() for msg in doc.validate())
        assert not validation_errors.difference(expected_errors)
    else:
        assert not error

    # test a few fields, the core of the tests are per parser
    assert doc.name in ('Sample_Document-V2.1', 'xyz-0.1.0', 'SPDX-Tools-v2.0')
    assert doc.comment in (
        None,
        'This is a sample spreadsheet',
        'Sample Comment',
        'This document was created using SPDX 2.0 using licenses from the web site.',
    )
