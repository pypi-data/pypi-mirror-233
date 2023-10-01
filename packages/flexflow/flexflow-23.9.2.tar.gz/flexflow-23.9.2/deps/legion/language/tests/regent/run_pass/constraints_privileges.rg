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

task bar(r : region(ispace(int2d), float))
where reads writes(r) do
  for idx in r do
    r[idx] += 1
  end
end

task foo(r : region(ispace(int2d), float),
         p1_c1 : region(ispace(int2d), float))
where reads writes(r), p1_c1 <= r do
  bar(p1_c1)
end

task main()
  var r = region(ispace(int2d,{6,6}), float)
  var cs1 = ispace(int2d,{2,1})
  var p1 = partition(equal, r, cs1)
  for c1 in cs1 do
    foo(r, p1[c1])
  end
end
regentlib.start(main)

