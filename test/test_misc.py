from __future__ import division, absolute_import, print_function

__copyright__ = "Copyright (C) 2016 Matt Wala"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import six  # noqa
from six.moves import range

import sys

import logging
logger = logging.getLogger(__name__)


def test_compute_sccs():
    from loopy.tools import compute_sccs
    import random

    rng = random.Random(0)

    def generate_random_graph(nnodes):
        graph = dict((i, set()) for i in range(nnodes))
        for i in range(nnodes):
            for j in range(nnodes):
                # Edge probability 2/n: Generates decently interesting inputs.
                if rng.randint(0, nnodes - 1) <= 1:
                    graph[i].add(j)
        return graph

    def verify_sccs(graph, sccs):
        visited = set()

        def visit(node):
            if node in visited:
                return []
            else:
                visited.add(node)
                result = []
                for child in graph[node]:
                    result = result + visit(child)
                return result + [node]

        for scc in sccs:
            result = visit(scc[0])
            assert set(result) == set(scc), (set(result), set(scc))

    for nnodes in range(10, 20):
        for i in range(40):
            graph = generate_random_graph(nnodes)
            verify_sccs(graph, compute_sccs(graph))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from py.test.cmdline import main
        main([__file__])

# vim: foldmethod=marker