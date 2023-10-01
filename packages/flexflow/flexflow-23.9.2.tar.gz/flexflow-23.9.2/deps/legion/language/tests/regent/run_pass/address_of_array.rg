-- Copyright 2023 Stanford University
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

import "regent"

local arr = regentlib.array(int, 2)

task main()
  var r = region(ispace(ptr, 5), arr)
  var x = dynamic_cast(ptr(arr, r), 0)
  r[0][0] = 123
  r[0][1] = 456
  var y = &r[0]
  regentlib.assert(x == &r[0], "test failed")
  regentlib.assert(x ~= &r[1], "test failed")
  regentlib.assert((@y)[0] == 123, "test failed")
  regentlib.assert((@y)[1] == 456, "test failed")
end
regentlib.start(main)
