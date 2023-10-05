/* CPython extension for checking if two polygons share an edge */

// will be replaced be "DOCKER_BUILD" for the wheel building inside docker
#define DOCKER_BUILD

#ifdef DOCKER_BUILD
  // docker build for wheel
  #include <Python.h>
#else
  // local builds
  #include <python3.10/Python.h>
#endif

#include <vector>
#include <string>


class PolyEdge
{
    public:
        double x0, y0, x1, y1;
        bool reversible;

        PolyEdge(double x0, double y0, double x1, double y1,
                 bool check_reverse)
        {
            this->x0 = x0;
            this->y0 = y0;
            this->x1 = x1;
            this->y1 = y1;
            this->reversible = check_reverse;
        }
        bool operator==(const PolyEdge &other);
        std::string print();
};
bool PolyEdge::operator==(const PolyEdge &other)
{
    if ((this->x0 == other.x0) &&
        (this->y0 == other.y0) &&
        (this->x1 == other.x1) &&
        (this->y1 == other.y1))
        return true;
    if (this->reversible &&
        (this->x1 == other.x0) &&
        (this->y1 == other.y0) &&
        (this->x0 == other.x1) &&
        (this->y0 == other.y1))
        return true;
    return false;
}
std::string PolyEdge::print()
{
    std::string representation = "Edge: (";
    representation += std::to_string(this->x0) + ",";
    representation += std::to_string(this->y0) + "),(";
    representation += std::to_string(this->x1) + ",";
    representation += std::to_string(this->y1) + ")";
    return representation;
}


bool share_edge_cpp(std::vector<double> polygon_0_x,
                    std::vector<double> polygon_0_y,
                    std::vector<double> polygon_1_x,
                    std::vector<double> polygon_1_y,
                    const bool check_reverse)
{
    std::vector<PolyEdge> edges_0, edges_1;
    // upper limit requires closed polygon
    for (size_t idx = 0; idx < polygon_0_x.size()-1; ++idx) {
        edges_0.push_back(PolyEdge(polygon_0_x.at(idx), polygon_0_y.at(idx),
                                   polygon_0_x.at(idx+1), polygon_0_y.at(idx+1),
                                   check_reverse));
    }
    for (size_t idx = 0; idx < polygon_1_x.size()-1; ++idx) {
        edges_1.push_back(PolyEdge(polygon_1_x.at(idx), polygon_1_y.at(idx),
                                   polygon_1_x.at(idx+1), polygon_1_y.at(idx+1),
                                   check_reverse));
    }

    // check every edge pair twice, optimise if necessary
    for (size_t idx_0 = 0; idx_0 < edges_0.size(); ++idx_0) {
        for (size_t idx_1 = 0; idx_1 < edges_1.size(); ++idx_1) {
            const bool match = (edges_0.at(idx_0) == edges_1.at(idx_1));
            if (match)
                return true;
        }
    }

    return false;
}


#ifdef __cplusplus
extern "C" {
#endif

static PyObject* share_edge(PyObject* self, PyObject* args, PyObject* kwargs)
{
    static char* keywords[] = {"n_vertices_0", "n_vertices_1", "polygon_0_x",
                               "polygon_0_y", "polygon_1_x", "polygon_1_y",
                               "check_reverse", NULL};
    int py_n_vert_0, py_n_vert_1, py_check_reverse = 1;
    PyObject *py_polygon_0_x;
    PyObject *py_polygon_0_y;
    PyObject *py_polygon_1_x;
    PyObject *py_polygon_1_y;
   /* Parse the input tuple */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiOOOO|i:share_edge",
                                     keywords, &py_n_vert_0, &py_n_vert_1,
                                     &py_polygon_0_x, &py_polygon_0_y,
                                     &py_polygon_1_x, &py_polygon_1_y,
                                     &py_check_reverse))
        return NULL;
    const bool check_reverse = (bool)py_check_reverse;

    const size_t n_vert_0 = (size_t)py_n_vert_0;
    const size_t n_vert_1 = (size_t)py_n_vert_1;
    std::vector<double> polygon_0_x, polygon_0_y, polygon_1_x, polygon_1_y;

    // parse polygon 0 into vectors
    PyObject *iterator_polygon_x = PyObject_GetIter(py_polygon_0_x);
    if (!iterator_polygon_x)
        return NULL;
    PyObject *iterator_polygon_y = PyObject_GetIter(py_polygon_0_y);
    if (!iterator_polygon_y)
        return NULL;
    for (size_t idx = 0; idx < n_vert_0; ++idx) {
        polygon_0_x.push_back(PyFloat_AsDouble(PyIter_Next(iterator_polygon_x)));
        polygon_0_y.push_back(PyFloat_AsDouble(PyIter_Next(iterator_polygon_y)));
    }
    if (polygon_0_x.at(0) != polygon_0_x.at(n_vert_0-1)) {
        PyErr_SetString(PyExc_ValueError, "Polygon 0 is not closed.");
        return NULL;
    }
    if (polygon_0_y.at(0) != polygon_0_y.at(n_vert_0-1)) {
        PyErr_SetString(PyExc_ValueError, "Polygon 0 is not closed.");
        return NULL;
    }

    // parse polygon 1 into vectors
    iterator_polygon_x = PyObject_GetIter(py_polygon_1_x);  // reuse var names
    if (!iterator_polygon_x)
        return NULL;
    iterator_polygon_y = PyObject_GetIter(py_polygon_1_y);
    if (!iterator_polygon_y)
        return NULL;
    for (size_t idx = 0; idx < n_vert_1; ++idx) {
        polygon_1_x.push_back(PyFloat_AsDouble(PyIter_Next(iterator_polygon_x)));
        polygon_1_y.push_back(PyFloat_AsDouble(PyIter_Next(iterator_polygon_y)));
    }
    if (polygon_1_x.at(0) != polygon_1_x.at(n_vert_1-1)) {
        PyErr_SetString(PyExc_ValueError, "Polygon 1 is not closed.");
        return NULL;
    }
    if (polygon_1_y.at(0) != polygon_1_y.at(n_vert_1-1)) {
        PyErr_SetString(PyExc_ValueError, "Polygon 1 is not closed.");
        return NULL;
    }

    const int c = share_edge_cpp(polygon_0_x, polygon_0_y, polygon_1_x,
                                  polygon_1_y, check_reverse);

    return Py_BuildValue("i", c);
}


static PyMethodDef pse_methods[] = {
    { "share_edge", (PyCFunction) share_edge, METH_VARARGS | METH_KEYWORDS,
    "Checks if two polygon share an edge. Polygons \n"
    "need to be closed, i.e. polygon_0[0] == polygon_0[-1] \n"
    "and polygon_1[0] == polygon_1[-1].\n"
    "\n"
    "Parameters\n"
    "----------\n"
    "n_vertices_0: int\n"
    "    Number of vertices of the first polygon.\n"
    "n_vertices_1: int\n"
    "    Number of vertices of the second polygon.\n"
    "polygon_0_x: list\n"
    "    X coordinates of the first polygon.\n"
    "polygon_0_y: list\n"
    "    Y coordinates of the first polygon.\n"
    "polygon_1_x: list\n"
    "    X coordinates of the second polygon.\n"
    "polygon_1_y: list\n"
    "    Y coordinates of the second polygon.\n"
    "check_reverse: bool | int\n"
    "    Also check the reversed edges, i.e. polygon_0[i]->polygon_0[i+1]\n"
    "    and polygon_0[i+1]->polygon_0[i] against polygon_1[j]->polygon_1[j+1]\n"
    "\n"
    "Returns\n"
    "-------\n"
    "share_edge: int\n"
    "    Nonzero iff the polygons share an edge.\n"
    "\n"
    "Raises\n"
    "------\n"
    "ValueError\n"
    "    If one of the polygons is not closed.\n"
    "\n" },
    { NULL, NULL, 0, NULL }
};


static struct PyModuleDef pse_module = {
    PyModuleDef_HEAD_INIT,
    "polygons_share_edge",
    NULL,
    -1,
    pse_methods
};


PyMODINIT_FUNC PyInit_polygons_share_edge(void)
{
    return PyModule_Create(&pse_module);
}

#ifdef __cplusplus
}  // closes extern "C"
#endif
