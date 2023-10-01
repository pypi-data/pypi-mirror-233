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

-- fails-with:
-- vectorize_loops11.rg:27: vectorization failed: loop body has an expression as a statement
--     regentlib.c.printf("test\n")
--              ^

import "regent"

task f(r : region(int))
where reads writes(r)
do
  __demand(__vectorize)
  for e in r do
    regentlib.c.printf("test\n")
  end
end
