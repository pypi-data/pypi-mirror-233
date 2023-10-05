import polygons_share_edge


def test_shared_edges_0():
    # checks reverse chirality
    square_0 = [(0., 0.), (1., 0.), (1., 1.), (0., 1.), (0., 0.)]
    square_1 = [(1., 0.), (2., 0.), (2., 1.), (1., 1.), (1., 0.)]
    sq_0_x, sq_0_y = zip(*square_0)
    sq_1_x, sq_1_y = zip(*square_1)
    assert polygons_share_edge.share_edge(5, 5, sq_0_x, sq_0_y, sq_1_x,
                                          sq_1_y, True)
    return

def test_shared_edges_1():
    # does not check with inverse chirality
    square_0 = [(0., 0.), (1., 0.), (1., 1.), (0., 1.), (0., 0.)]
    square_1 = [(1., 0.), (2., 0.), (2., 1.), (1., 1.), (1., 0.)]
    sq_0_x, sq_0_y = zip(*square_0)
    sq_1_x, sq_1_y = zip(*square_1)
    assert not polygons_share_edge.share_edge(5, 5, sq_0_x, sq_0_y, sq_1_x,
                                              sq_1_y, False)
    return

def test_shared_edges_2():
    square_0 = [(0., 0.), (1., 0.), (1.1, 1.), (0., 1.), (0., 0.)]
    square_1 = [(1., 0.), (2., 0.), (2., 1.), (1., 1.), (1., 0.)]
    sq_0_x, sq_0_y = zip(*square_0)
    sq_1_x, sq_1_y = zip(*square_1)
    assert not polygons_share_edge.share_edge(5, 5, sq_0_x, sq_0_y, sq_1_x,
                                              sq_1_y, True)
    return

def test_shared_edges_3():
    # with keyword arguments
    square_0 = [(0., 0.), (1., 0.), (1.1, 1.), (0., 1.), (0., 0.)]
    square_1 = [(1., 0.), (2., 0.), (2., 1.), (1., 1.), (1., 0.)]
    sq_0_x, sq_0_y = zip(*square_0)
    sq_1_x, sq_1_y = zip(*square_1)
    assert not polygons_share_edge.share_edge(n_vertices_0=5, n_vertices_1=5,
                                              polygon_0_x=sq_0_x, polygon_0_y=sq_0_y,
                                              polygon_1_x=sq_1_x, polygon_1_y=sq_1_y,
                                              check_reverse=True)
    assert not polygons_share_edge.share_edge(n_vertices_0=5, 
                                              polygon_0_x=sq_0_x, polygon_0_y=sq_0_y,
                                              polygon_1_x=sq_1_x, n_vertices_1=5, polygon_1_y=sq_1_y,
                                              check_reverse=True)
    assert not polygons_share_edge.share_edge(n_vertices_0=5, n_vertices_1=5,
                                              polygon_0_x=sq_0_x, polygon_0_y=sq_0_y,
                                              polygon_1_x=sq_1_x, polygon_1_y=sq_1_y,
                                              check_reverse=True)
    return
