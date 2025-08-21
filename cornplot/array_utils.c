#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <math.h>


double real_to_window_x(double x, int min_x, int width, double real_width, double x_start)
{
    return (min_x + width / real_width * (x - x_start));
}

double real_to_window_y(double y, int min_y, int height, double real_height, double y_stop)
{
    return (min_y + height / real_height * (y_stop - y));
}

double window_to_real_x(double x, int width, double real_width, double x_start)
{
    return real_width * x / (double)width + x_start;
}

double window_to_real_y(double y, int height, double real_height, double y_stop, int offset_y)
{
    y -= offset_y;
    return y_stop - real_height * y / (double)height;
}


double real_to_window_x_log(double x, int min_x, int width, double x_start, double x_stop)
{
    if (x <= 0) return min_x;
    return min_x + width / log10(x_stop / x_start) * log10(x / x_start);
}

double real_to_window_y_log(double y, int min_y, int max_y, int height, double y_start, double y_stop)
{
    if (y <= 0) return max_y;
    return min_y + height / log10(y_stop / y_start) * log10(y_stop / y);
}

double window_to_real_x_log(double x, int width, double x_start, double x_stop)
{
    return pow(10, log10(x_stop / x_start) * x / (double)width + log10(x_start));
}

double window_to_real_y_log(double y, int height, double y_start, double y_stop, int offset_y)
{
    y -= offset_y;
    return pow(10, log10(y_stop) - log10(y_stop / y_start) * y / (double)height);
}


PyObject* c_real_to_window_x(PyObject* self, PyObject* args)
{
    double x, x_start, real_width;
    int min_x, width;
    PyArg_ParseTuple(args, "diidd", &x, &min_x, &width, &real_width, &x_start);
    double ret = real_to_window_x(x, min_x, width, real_width, x_start);
    return PyFloat_FromDouble(ret);
}


PyObject* c_real_to_window_y(PyObject* self, PyObject* args)
{
    double y, y_stop, real_height;
    int min_y, height;
    PyArg_ParseTuple(args, "diidd", &y, &min_y, &height, &real_height, &y_stop);
    double ret = real_to_window_y(y, min_y, height, real_height, y_stop);
    return PyFloat_FromDouble(ret);
}


PyObject* c_window_to_real_x(PyObject* self, PyObject* args)
{
    double x_start, real_width, x;
    int width;
    PyArg_ParseTuple(args, "didd", &x, &width, &real_width, &x_start);
    return PyFloat_FromDouble(window_to_real_x(x, width, real_width, x_start));
}


PyObject* c_window_to_real_y(PyObject* self, PyObject* args)
{
    double y_stop, real_height, y;
    int height, offset_y;
    PyArg_ParseTuple(args, "diddi", &y, &height, &real_height, &y_stop, &offset_y);
    return PyFloat_FromDouble(window_to_real_y(y, height, real_height, y_stop, offset_y));
}


PyObject* c_real_to_window_x_log(PyObject* self, PyObject* args)
{
    double x, x_start, x_stop;
    int min_x, width;
    PyArg_ParseTuple(args, "diidd", &x, &min_x, &width, &x_start, &x_stop);
    double ret = real_to_window_x_log(x, min_x, width, x_start, x_stop);
    return PyFloat_FromDouble(ret);
}


PyObject* c_real_to_window_y_log(PyObject* self, PyObject* args)
{
    double y, y_stop, y_start;
    int min_y, max_y, height;
    PyArg_ParseTuple(args, "diiidd", &y, &min_y, &max_y, &height, &y_start, &y_stop);
    double ret = real_to_window_y_log(y, min_y, max_y, height, y_start, y_stop);
    return PyFloat_FromDouble(ret);
}


PyObject* c_window_to_real_x_log(PyObject* self, PyObject* args)
{
    double x_start, x_stop, x;
    int width;
    PyArg_ParseTuple(args, "didd", &x, &width, &x_start, &x_stop);
    return PyFloat_FromDouble(window_to_real_x_log(x, width, x_start, x_stop));
}


PyObject* c_window_to_real_y_log(PyObject* self, PyObject* args)
{
    double y_stop, y_start, y;
    int height, offset_y;
    PyArg_ParseTuple(args, "diddi", &y, &height, &y_start, &y_stop, &offset_y);
    return PyFloat_FromDouble(window_to_real_y(y, height, y_start, y_stop, offset_y));
}


PyObject* c_recalculate_window_x(PyObject* self, PyObject* args)
{
    PyListObject *X_real;
    double x_start, real_width;
    int min_x, width, i0, ik, step;

    PyArg_ParseTuple(args, "O!iiddiii", &PyList_Type, &X_real, &min_x, &width, &real_width, &x_start, &i0, &ik, &step);
    int len = (int)round((float)(ik - i0) / (float)step);
    PyListObject *ret = PyList_New(len);
    int j = 0;
    for(int i = i0; i < ik; i += step)
    {
        double x = PyFloat_AsDouble(PyList_GetItem(X_real, i));
        double x_win = real_to_window_x(x, min_x, width, real_width, x_start);
        if(j < len)
            PyList_SetItem(ret, j++, PyFloat_FromDouble(x_win));
    }

    return (PyObject*)ret;
}


PyObject* c_recalculate_window_y(PyObject* self, PyObject* args)
{
    PyListObject *Y_real;
    double y_stop, real_height;
    int min_y, height, i0, ik, step;

    PyArg_ParseTuple(args, "O!iiddiii", &PyList_Type, &Y_real, &min_y, &height, &real_height, &y_stop, &i0, &ik, &step);
    int len = (int)round((float)(ik - i0) / (float)step);
    PyListObject *ret = PyList_New(len);
    int j = 0;
    for(int i = i0; i < ik; i += step)
    {
        double y = PyFloat_AsDouble(PyList_GetItem(Y_real, i));
        double y_win = real_to_window_y(y, min_y, height, real_height, y_stop);
        if(j < len)
            PyList_SetItem(ret, j++, PyFloat_FromDouble(y_win));
    }

    return (PyObject*)ret;
}


PyObject* c_get_nearest_value(PyObject* self, PyObject* args)
{
    PyListObject *X;
    double x_real;

    PyArg_ParseTuple(args, "O!d", &PyList_Type, &X, &x_real);

    double x_nearest;
    int i_nearest = 0;

    for(int i = 0; i < PyList_Size(X); ++i)
    {
        if(i == 0)
        {
            x_nearest = PyFloat_AsDouble(PyList_GetItem(X, i));
            continue;
        }
        double val_cur = PyFloat_AsDouble(PyList_GetItem(X, i));
        if(fabs(val_cur - x_real) < fabs(x_nearest - x_real))
        {
            x_nearest = val_cur;
            i_nearest = i;
        }
    }

    PyObject *ret = PyList_New(2);
    PyList_SetItem(ret, 0, PyFloat_FromDouble(x_nearest));
    PyList_SetItem(ret, 1, PyLong_FromLong(i_nearest));
    return ret;
}


// array containing the module's methods' definitions
// put here the methods to export
// the array must end with a {NULL} struct
PyMethodDef module_methods[] =
{
    {"c_real_to_window_x", c_real_to_window_x, METH_VARARGS, "Перевод реальных координат в оконные"},
    {"c_real_to_window_y", c_real_to_window_y, METH_VARARGS, "Перевод реальных координат в оконные"},
    {"c_window_to_real_x", c_window_to_real_x, METH_VARARGS, "Перевод оконных координат в реальные"},
    {"c_window_to_real_y", c_window_to_real_y, METH_VARARGS, "Перевод оконных координат в реальные"},
    {"c_real_to_window_x_log", c_real_to_window_x_log, METH_VARARGS, "Перевод реальных координат в оконные при логарифмическом масштабе"},
    {"c_real_to_window_y_log", c_real_to_window_y_log, METH_VARARGS, "Перевод реальных координат в оконные при логарифмическом масштабе"},
    {"c_window_to_real_x_log", c_window_to_real_x_log, METH_VARARGS, "Перевод оконных координат в реальные при логарифмическом масштабе"},
    {"c_window_to_real_y_log", c_window_to_real_y_log, METH_VARARGS, "Перевод оконных координат в реальные при логарифмическом масштабе"},
    {"c_recalculate_window_x", c_recalculate_window_x, METH_VARARGS, "Пересчёт оконных координат по Х"},
    {"c_recalculate_window_y", c_recalculate_window_y, METH_VARARGS, "Пересчёт оконных координат по У"},
    {"c_get_nearest_value", c_get_nearest_value, METH_VARARGS, "Нахождение ближайшего значения в массиве"},
    {NULL} // this struct signals the end of the array
};

// struct representing the module
struct PyModuleDef array_utils =
{
    PyModuleDef_HEAD_INIT, // Always initialize this member to PyModuleDef_HEAD_INIT
    "array_utils", // module name
    "Модуль содержит функции, наиболее критичные по времени, реализованные на С", // module description
    -1, // module size (more on this later)
    module_methods // methods associated with the module
};

// function that initializes the module
PyMODINIT_FUNC PyInit_array_utils()
{
    return PyModule_Create(&array_utils);
}
