# Copyright 2014-2015 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xml.sax.saxutils import escape
from xml.sax.saxutils import quoteattr


def get_xunit_content(report, testname, elapsed):
    test_count = len(report)
    error_count = sum([1 if r[1] else 0 for r in report])
    data = {
        'testname': testname,
        'test_count': test_count,
        'error_count': error_count,
        'time': '%.3f' % round(elapsed, 3),
    }
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<testsuite
  name="%(testname)s"
  tests="%(test_count)d"
  failures="%(error_count)d"
  time="%(time)s"
>
''' % data

    for (filename, diff_lines) in report:

        if diff_lines:
            # report any diff as a failing testcase
            data = {
                'quoted_location': quoteattr(filename),
                'testname': testname,
                'quoted_diff': escape(''.join(diff_lines)),
            }
            xml += '''  <testcase
    name=%(quoted_location)s
    classname="%(testname)s"
  >
      <system-err>%(quoted_diff)s</system-err>
  </testcase>
''' % data

        else:
            # if there is no diff report a single successful test
            data = {
                'quoted_location': quoteattr(filename),
                'testname': testname,
            }
            xml += '''  <testcase
    name=%(quoted_location)s
    classname="%(testname)s"
    status="No errors"/>
''' % data

    # output list of checked files
    data = {
        'escaped_files': escape(''.join(['\n* %s' % r[0] for r in report])),
    }
    xml += '''  <system-out>Checked files:%(escaped_files)s</system-out>
''' % data

    xml += '</testsuite>\n'
    return xml
