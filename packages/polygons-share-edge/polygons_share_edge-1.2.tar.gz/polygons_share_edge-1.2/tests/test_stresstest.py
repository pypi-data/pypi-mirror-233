import polygons_share_edge
import numpy as np

N = 10_000
vertex_min, vertex_max = 50, 500

def test_many():
    for _ in range(N):
        # draw number of vertices
        n_vertices_0, n_vertices_1 = np.random.randint(vertex_min, vertex_max, size=2)
        # draw random edges, which do not even form a proper polygon
        p0 = np.random.normal(loc=5., scale=3., size=(n_vertices_0, 2))
        p0x, p0y = p0.T
        p1 = np.random.normal(loc=5., scale=3., size=(n_vertices_1, 2))
        p1x, p1y = p1.T
        # close the generated "polygons"
        p0x = list(p0x[:-1]) + [p0x[0]]
        p0y = list(p0y[:-1]) + [p0y[0]]
        p1x = list(p1x[:-1]) + [p1x[0]]
        p1y = list(p1y[:-1]) + [p1y[0]]
        assert p0x[0] == p0x[-1]
        assert p0y[0] == p0y[-1]
        assert p1x[0] == p1x[-1]
        assert p1y[0] == p1y[-1]
        polygons_share_edge.share_edge(n_vertices_0, n_vertices_1, p0x, p0y, p1x, p1y, int(True))
    return
