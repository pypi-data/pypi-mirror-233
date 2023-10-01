/*
    src/nb_func.cpp: nanobind function type

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

#include "nb_internals.h"
#include "buffer.h"

/// Maximum number of arguments supported by 'nb_vectorcall_simple'
#define NB_MAXARGS_SIMPLE 8

#if defined(__GNUG__)
#  include <cxxabi.h>
#endif

#if defined(_MSC_VER)
#  pragma warning(disable: 4706) // assignment within conditional expression
#  pragma warning(disable: 6255) // _alloca indicates failure by raising a stack overflow exception
#endif

NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

// Forward/external declarations
extern Buffer buf;

static PyObject *nb_func_vectorcall_simple(PyObject *, PyObject *const *,
                                           size_t, PyObject *) noexcept;
static PyObject *nb_func_vectorcall_complex(PyObject *, PyObject *const *,
                                            size_t, PyObject *) noexcept;
static void nb_func_render_signature(const func_data *f) noexcept;

int nb_func_traverse(PyObject *self, visitproc visit, void *arg) {
    size_t size = (size_t) Py_SIZE(self);

    if (size) {
        func_data *f = nb_func_data(self);

        for (size_t i = 0; i < size; ++i) {
            if (f->flags & (uint32_t) func_flags::has_args) {
                for (size_t j = 0; j < f->nargs; ++j) {
                    Py_VISIT(f->args[j].value);
                }
            }
            ++f;
        }
    }

    return 0;
}

int nb_func_clear(PyObject *self) {
    size_t size = (size_t) Py_SIZE(self);

    if (size) {
        func_data *f = nb_func_data(self);

        for (size_t i = 0; i < size; ++i) {
            if (f->flags & (uint32_t) func_flags::has_args) {
                for (size_t j = 0; j < f->nargs; ++j) {
                    Py_CLEAR(f->args[j].value);
                }
            }
            ++f;
        }
    }

    return 0;
}

/// Free a function overload chain
void nb_func_dealloc(PyObject *self) {
    PyObject_GC_UnTrack(self);

    size_t size = (size_t) Py_SIZE(self);
    if (size) {
        func_data *f = nb_func_data(self);

        // Delete from registered function list
        auto &funcs = internals->funcs;
        auto it = funcs.find(self);
        check(it != funcs.end(),
              "nanobind::detail::nb_func_dealloc(\"%s\"): function not found!",
              ((f->flags & (uint32_t) func_flags::has_name) ? f->name
                                                            : "<anonymous>"));
        funcs.erase(it);

        for (size_t i = 0; i < size; ++i) {
            if (f->flags & (uint32_t) func_flags::has_free)
                f->free_capture(f->capture);

            if (f->flags & (uint32_t) func_flags::has_args) {
                for (size_t j = 0; j < f->nargs; ++j) {
                    Py_XDECREF(f->args[j].value);
                    Py_XDECREF(f->args[j].name_py);
                }
            }

            free(f->args);
            free((char *) f->descr);
            free(f->descr_types);
            ++f;
        }
    }

    PyObject_GC_Del(self);
}

int nb_bound_method_traverse(PyObject *self, visitproc visit, void *arg) {
    nb_bound_method *mb = (nb_bound_method *) self;
    Py_VISIT((PyObject *) mb->func);
    Py_VISIT(mb->self);
    return 0;
}

int nb_bound_method_clear(PyObject *self) {
    nb_bound_method *mb = (nb_bound_method *) self;
    Py_CLEAR(mb->func);
    Py_CLEAR(mb->self);
    return 0;
}

void nb_bound_method_dealloc(PyObject *self) {
    nb_bound_method *mb = (nb_bound_method *) self;
    PyObject_GC_UnTrack(self);
    Py_DECREF((PyObject *) mb->func);
    Py_DECREF(mb->self);
    PyObject_GC_Del(self);
}

static arg_data method_args[2] = {
    { "self", nullptr, nullptr, false, false },
    { nullptr, nullptr, nullptr, false, false }
};

static bool set_builtin_exception_status(builtin_exception &e) {
    PyObject *o;

    switch (e.type()) {
        case exception_type::runtime_error: o = PyExc_RuntimeError; break;
        case exception_type::stop_iteration: o = PyExc_StopIteration; break;
        case exception_type::index_error: o = PyExc_IndexError; break;
        case exception_type::key_error: o = PyExc_KeyError; break;
        case exception_type::value_error: o = PyExc_ValueError; break;
        case exception_type::type_error: o = PyExc_TypeError; break;
        case exception_type::buffer_error: o = PyExc_BufferError; break;
        case exception_type::import_error: o = PyExc_ImportError; break;
        case exception_type::attribute_error: o = PyExc_AttributeError; break;
        case exception_type::next_overload: return false;
        default:
            check(false, "nanobind::detail::set_builtin_exception_status(): "
                         "invalid exception type!");
    }

    PyErr_SetString(o, e.what());
    return true;
}

void *malloc_check(size_t size) {
    void *ptr = malloc(size);
    if (!ptr)
        fail("nanobind: malloc() failed!");
    return ptr;
}

/**
 * \brief Wrap a C++ function into a Python function object
 *
 * This is an implementation detail of nanobind::cpp_function.
 */
PyObject *nb_func_new(const void *in_) noexcept {
    func_data_prelim<0> *f = (func_data_prelim<0> *) in_;
    arg_data *args_in = std::launder((arg_data *) f->args);

    bool has_scope      = f->flags & (uint32_t) func_flags::has_scope,
         has_name       = f->flags & (uint32_t) func_flags::has_name,
         has_args       = f->flags & (uint32_t) func_flags::has_args,
         has_var_args   = f->flags & (uint32_t) func_flags::has_var_args,
         has_var_kwargs = f->flags & (uint32_t) func_flags::has_var_kwargs,
         has_doc        = f->flags & (uint32_t) func_flags::has_doc,
         is_implicit    = f->flags & (uint32_t) func_flags::is_implicit,
         is_method      = f->flags & (uint32_t) func_flags::is_method,
         return_ref     = f->flags & (uint32_t) func_flags::return_ref,
         is_constructor = false;

    PyObject *name = nullptr;
    PyObject *func_prev = nullptr;

    // Check for previous overloads
    if (has_scope && has_name) {
        name = PyUnicode_FromString(f->name);
        check(name, "nb::detail::nb_func_new(\"%s\"): invalid name.", f->name);

        func_prev = PyObject_GetAttr(f->scope, name);
        if (func_prev) {
            if (Py_TYPE(func_prev) == internals->nb_func ||
                Py_TYPE(func_prev) == internals->nb_method) {
                func_data *fp = nb_func_data(func_prev);

                check((fp->flags & (uint32_t) func_flags::is_method) ==
                          (f->flags & (uint32_t) func_flags::is_method),
                      "nb::detail::nb_func_new(\"%s\"): mismatched static/"
                      "instance method flags in function overloads!",
                      f->name);

                /* Never append a method to an overload chain of a parent class;
                   instead, hide the parent's overloads in this case */
                if (fp->scope != f->scope)
                    Py_CLEAR(func_prev);
            } else if (f->name[0] == '_') {
                Py_CLEAR(func_prev);
            } else {
                check(false,
                      "nb::detail::nb_func_new(\"%s\"): cannot overload "
                      "existing non-function object of the same name!", f->name);
            }
        } else {
            PyErr_Clear();
        }

        // Is this method a constructor that takes a class binding as first parameter?
        is_constructor = is_method &&
                         (strcmp(f->name, "__init__") == 0 ||
                          strcmp(f->name, "__setstate__") == 0) &&
                         strncmp(f->descr, "({%}", 4) == 0;

        // Don't use implicit conversions in copy constructors (causes infinite recursion)
        if (is_constructor && f->nargs == 2 && f->descr_types[0] &&
            f->descr_types[0] == f->descr_types[1]) {
            if (has_args) {
                f->args[1].convert = false;
            } else {
                args_in = method_args + 1;
                has_args = true;
            }
        }
    }

    // Create a new function and destroy the old one
    Py_ssize_t to_copy = func_prev ? Py_SIZE(func_prev) : 0;
    nb_func *func = (nb_func *) PyType_GenericAlloc(
        is_method ? internals->nb_method : internals->nb_func, to_copy + 1);
    check(func, "nb::detail::nb_func_new(\"%s\"): alloc. failed (1).",
          has_name ? f->name : "<anonymous>");

    func->max_nargs_pos = f->nargs;
    func->complex_call = has_args || has_var_args || has_var_kwargs;

    if (func_prev) {
        func->complex_call |= ((nb_func *) func_prev)->complex_call;
        func->max_nargs_pos = std::max(func->max_nargs_pos,
                                       ((nb_func *) func_prev)->max_nargs_pos);

        func_data *cur  = nb_func_data(func),
                  *prev = nb_func_data(func_prev);

        memcpy(cur, prev, sizeof(func_data) * to_copy);
        memset(prev, 0, sizeof(func_data) * to_copy);

        ((PyVarObject *) func_prev)->ob_size = 0;

        auto it = internals->funcs.find(func_prev);
        check(it != internals->funcs.end(),
              "nanobind::detail::nb_func_new(): internal update failed (1)!");
        internals->funcs.erase(it);
    }

    func->complex_call |= func->max_nargs_pos >= NB_MAXARGS_SIMPLE;

    func->vectorcall = func->complex_call ? nb_func_vectorcall_complex
                                          : nb_func_vectorcall_simple;

    // Register the function
    auto [it, success] = internals->funcs.try_emplace(func, nullptr);
    check(success,
          "nanobind::detail::nb_func_new(): internal update failed (2)!");

    func_data *fc = nb_func_data(func) + to_copy;
    memcpy(fc, f, sizeof(func_data_prelim<0>));
    if (has_doc && fc->doc[0] == '\n')
        fc->doc++;

    if (is_constructor)
        fc->flags |= (uint32_t) func_flags::is_constructor;
    if (has_args)
        fc->flags |= (uint32_t) func_flags::has_args;

    if (!has_name)
        fc->name = "";

    if (is_implicit) {
        check(fc->flags & (uint32_t) func_flags::is_constructor,
              "nb::detail::nb_func_new(\"%s\"): nanobind::is_implicit() "
              "should only be specified for constructors.",
              f->name);
        check(f->nargs == 2,
              "nb::detail::nb_func_new(\"%s\"): implicit constructors "
              "should only have one argument.",
              f->name);

        if (f->descr_types[1])
            implicitly_convertible(f->descr_types[1], f->descr_types[0]);
    }

    for (size_t i = 0;; ++i) {
        if (!f->descr[i]) {
            fc->descr = (char *) malloc_check(sizeof(char) * (i + 1));
            memcpy((char *) fc->descr, f->descr, (i + 1) * sizeof(char));
            break;
        }
    }

    for (size_t i = 0;; ++i) {
        if (!f->descr_types[i]) {
            fc->descr_types = (const std::type_info **)
                malloc_check(sizeof(const std::type_info *) * (i + 1));
            memcpy(fc->descr_types, f->descr_types,
                        (i + 1) * sizeof(const std::type_info *));
            break;
        }
    }

    if (has_args) {
        fc->args = (arg_data *) malloc_check(sizeof(arg_data) * f->nargs);

        if (is_method) // add implicit 'self' argument annotation
            fc->args[0] = method_args[0];
        for (size_t i = is_method; i < fc->nargs; ++i)
            fc->args[i] = args_in[i - is_method];

        for (size_t i = 0; i < fc->nargs; ++i) {
            arg_data &a = fc->args[i];
            if (a.name)
                a.name_py = PyUnicode_InternFromString(a.name);
            else
                a.name_py = nullptr;
            a.none |= a.value == Py_None;
            Py_XINCREF(a.value);
        }
    }

    if (has_scope && name) {
        int rv = PyObject_SetAttr(f->scope, name, (PyObject *) func);
        check(rv == 0, "nb::detail::nb_func_new(\"%s\"): setattr. failed.",
              f->name);
    }

    Py_XDECREF(name);

    if (return_ref) {
        return (PyObject *) func;
    } else {
        Py_DECREF(func);
        return nullptr;
    }
}

/// Used by nb_func_vectorcall: generate an error when overload resolution fails
static NB_NOINLINE PyObject *
nb_func_error_overload(PyObject *self, PyObject *const *args_in,
                       size_t nargs_in, PyObject *kwargs_in) noexcept {
    const uint32_t count = (uint32_t) Py_SIZE(self);
    func_data *f = nb_func_data(self);

    if (f->flags & (uint32_t) func_flags::is_operator)
        return not_implemented().release().ptr();

    buf.clear();
    buf.put_dstr(f->name);
    buf.put("(): incompatible function arguments. The following argument types "
            "are supported:\n");

    for (uint32_t i = 0; i < count; ++i) {
        buf.put("    ");
        buf.put_uint32(i + 1);
        buf.put(". ");
        nb_func_render_signature(f + i);
        buf.put('\n');
    }

    buf.put("\nInvoked with types: ");
    for (size_t i = 0; i < nargs_in; ++i) {
        str name = steal<str>(nb_inst_name(args_in[i]));
        buf.put_dstr(name.c_str());
        if (i + 1 < nargs_in)
            buf.put(", ");
    }

    if (kwargs_in) {
        if (nargs_in)
            buf.put(", ");
        buf.put("kwargs = { ");

        size_t nkwargs_in = (size_t) NB_TUPLE_GET_SIZE(kwargs_in);
        for (size_t j = 0; j < nkwargs_in; ++j) {
            PyObject *key   = NB_TUPLE_GET_ITEM(kwargs_in, j),
                     *value = args_in[nargs_in + j];

            const char *key_cstr = PyUnicode_AsUTF8AndSize(key, nullptr);
            buf.put_dstr(key_cstr);
            buf.put(": ");
            str name = steal<str>(nb_inst_name(value));
            buf.put_dstr(name.c_str());
            buf.put(", ");
        }
        buf.rewind(2);
        buf.put(" }");
    }

    PyErr_SetString(PyExc_TypeError, buf.get());
    return nullptr;
}

/// Used by nb_func_vectorcall: generate an error when result conversion fails
static NB_NOINLINE PyObject *nb_func_error_noconvert(PyObject *self,
                                                     PyObject *const *, size_t,
                                                     PyObject *) noexcept {
    if (PyErr_Occurred())
        return nullptr;
    func_data *f = nb_func_data(self);
    buf.clear();
    buf.put("Unable to convert function return value to a Python "
            "type! The signature was\n    ");
    nb_func_render_signature(f);
    PyErr_SetString(PyExc_TypeError, buf.get());
    return nullptr;
}

/// Used by nb_func_vectorcall: convert a C++ exception into a Python error
static NB_NOINLINE void nb_func_convert_cpp_exception() noexcept {
    std::exception_ptr e = std::current_exception();

    for (nb_translator_seq *cur = &internals->translators; cur;
         cur = cur->next) {
        try {
            // Try exception translator & forward payload
            cur->translator(e, cur->payload);
            return;
        } catch (...) {
            e = std::current_exception();
        }
    }

    PyErr_SetString(PyExc_SystemError,
                    "nanobind::detail::nb_func_error_except(): exception "
                    "could not be translated!");
}

/// Dispatch loop that is used to invoke functions created by nb_func_new
static PyObject *nb_func_vectorcall_complex(PyObject *self,
                                            PyObject *const *args_in,
                                            size_t nargsf,
                                            PyObject *kwargs_in) noexcept {
    const size_t count      = (size_t) Py_SIZE(self),
                 nargs_in   = (size_t) NB_VECTORCALL_NARGS(nargsf),
                 nkwargs_in = kwargs_in ? (size_t) NB_TUPLE_GET_SIZE(kwargs_in) : 0;

    func_data *fr = nb_func_data(self);

    const bool is_method      = fr->flags & (uint32_t) func_flags::is_method,
               is_constructor = fr->flags & (uint32_t) func_flags::is_constructor;

    PyObject *result = nullptr,
             *self_arg = (is_method && nargs_in > 0) ? args_in[0] : nullptr;

    /* The following lines allocate memory on the stack, which is very efficient
       but also potentially dangerous since it can be used to generate stack
       overflows. We refuse unrealistically large number of 'kwargs' (the
       'max_nargs_pos' value is fine since it is specified by the bindings) */
    if (nkwargs_in > 1024) {
        PyErr_SetString(PyExc_TypeError,
                        "nanobind::detail::nb_func_vectorcall(): too many (> "
                        "1024) keyword arguments.");
        return nullptr;
    }

    // Handler routine that will be invoked in case of an error condition
    PyObject *(*error_handler)(PyObject *, PyObject *const *, size_t,
                               PyObject *) noexcept = nullptr;

    // Small array holding temporaries (implicit conversion/*args/**kwargs)
    cleanup_list cleanup(self_arg);

    // Preallocate stack memory for function dispatch
    size_t max_nargs_pos = ((nb_func *) self)->max_nargs_pos;
    PyObject **args = (PyObject **) alloca(max_nargs_pos * sizeof(PyObject *));
    uint8_t *args_flags = (uint8_t *) alloca(max_nargs_pos * sizeof(uint8_t));
    bool *kwarg_used = (bool *) alloca(nkwargs_in * sizeof(bool));

    /*  The logic below tries to find a suitable overload using two passes
        of the overload chain (or 1, if there are no overloads). The first pass
        is strict and permits no implicit conversions, while the second pass
        allows them.

        The following is done per overload during a pass

        1. Copy positional arguments while checking that named positional
           arguments weren't *also* specified as kwarg. Substitute missing
           entries using keyword arguments or default argument values provided
           in the bindings, if available.

        3. Ensure that either all keyword arguments were "consumed", or that
           the function takes a kwargs argument to accept unconsumed kwargs.

        4. Any positional arguments still left get put into a tuple (for args),
           and any leftover kwargs get put into a dict.

        5. Pack everything into a vector; if we have nb::args or nb::kwargs, they are an
           extra tuple or dict at the end of the positional arguments.

        6. Call the function call dispatcher (func_data::impl)

        If one of these fail, move on to the next overload and keep trying
        until we get a result other than NB_NEXT_OVERLOAD.
    */

    for (int pass = (count > 1) ? 0 : 1; pass < 2; ++pass) {
        for (size_t k = 0; k < count; ++k) {
            const func_data *f = fr + k;

            const bool has_args       = f->flags & (uint32_t) func_flags::has_args,
                       has_var_args   = f->flags & (uint32_t) func_flags::has_var_args,
                       has_var_kwargs = f->flags & (uint32_t) func_flags::has_var_kwargs;

            /// Number of positional arguments
            size_t nargs_pos = f->nargs - has_var_args - has_var_kwargs;

            if (nargs_in > nargs_pos && !has_var_args)
                continue; // Too many positional arguments given for this overload

            if (nargs_in < nargs_pos && !has_args)
                continue; // Not enough positional arguments, insufficient
                          // keyword/default arguments to fill in the blanks

            memset(kwarg_used, 0, nkwargs_in * sizeof(bool));

            // 1. Copy positional arguments, potentially substitute kwargs/defaults
            size_t i = 0;
            for (; i < nargs_pos; ++i) {
                PyObject *arg = nullptr;
                bool arg_convert  = pass == 1,
                     arg_none     = false;

                if (i < nargs_in)
                    arg = args_in[i];

                if (has_args) {
                    const arg_data &ad = f->args[i];

                    if (kwargs_in && ad.name_py) {
                        PyObject *hit = nullptr;
                        for (size_t j = 0; j < nkwargs_in; ++j) {
                            PyObject *key = NB_TUPLE_GET_ITEM(kwargs_in, j);
                            #if defined(PYPY_VERSION)
                                bool match = PyUnicode_Compare(key, ad.name_py) == 0;
                            #else
                                bool match = (key == ad.name_py);
                            #endif
                            if (match) {
                                hit = args_in[nargs_in + j];
                                kwarg_used[j] = true;
                                break;
                            }
                        }

                        if (hit) {
                            if (arg)
                                break; // conflict between keyword and positional arg.
                            arg = hit;
                        }
                    }

                    if (!arg)
                        arg = ad.value;

                    arg_convert &= ad.convert;
                    arg_none = ad.none;
                }

                if (!arg || (arg == Py_None && !arg_none))
                    break;

                args[i] = arg;
                args_flags[i] = arg_convert ? (uint8_t) cast_flags::convert : (uint8_t) 0;
            }

            // Skip this overload if positional arguments were unavailable
            if (i != nargs_pos)
                continue;

            // Deal with remaining positional arguments
            if (has_var_args) {
                PyObject *tuple = PyTuple_New(
                    nargs_in > nargs_pos ? (Py_ssize_t) (nargs_in - nargs_pos) : 0);

                for (size_t j = nargs_pos; j < nargs_in; ++j) {
                    PyObject *o = args_in[j];
                    Py_INCREF(o);
                    NB_TUPLE_SET_ITEM(tuple, j - nargs_pos, o);
                }

                args[nargs_pos] = tuple;
                args_flags[nargs_pos] = 0;
                cleanup.append(tuple);
            }

            // Deal with remaining keyword arguments
            if (has_var_kwargs) {
                PyObject *dict = PyDict_New();
                for (size_t j = 0; j < nkwargs_in; ++j) {
                    PyObject *key = NB_TUPLE_GET_ITEM(kwargs_in, j);
                    if (!kwarg_used[j])
                        PyDict_SetItem(dict, key, args_in[nargs_in + j]);
                }

                args[nargs_pos + has_var_args] = dict;
                args_flags[nargs_pos + has_var_args] = 0;
                cleanup.append(dict);
            } else if (kwargs_in) {
                bool success = true;
                for (size_t j = 0; j < nkwargs_in; ++j)
                    success &= kwarg_used[j];
                if (!success)
                    continue;
            }

            if (is_constructor)
                args_flags[0] = (uint8_t) cast_flags::construct;

            try {
                // Found a suitable overload, let's try calling it
                result = f->impl((void *) f->capture, args, args_flags,
                                 (rv_policy) (f->flags & 0b111), &cleanup);

                if (NB_UNLIKELY(!result)) {
                    error_handler = nb_func_error_noconvert;
                    goto done;
                }
            } catch (builtin_exception &e) {
                if (set_builtin_exception_status(e)) {
                    result = nullptr;
                    goto done;
                } else {
                    result = NB_NEXT_OVERLOAD;
                }
            } catch (python_error &e) {
                e.restore();
                result = nullptr;
                goto done;
            } catch (...) {
                nb_func_convert_cpp_exception();
                result = nullptr;
                goto done;
            }

            if (result != NB_NEXT_OVERLOAD) {
                if (is_constructor) {
                    nb_inst *self_arg_nb = (nb_inst *) self_arg;
                    self_arg_nb->destruct = true;
                    self_arg_nb->ready = true;
                    if (NB_UNLIKELY(self_arg_nb->intrusive))
                        nb_type_data(Py_TYPE(self_arg))
                            ->set_self_py(inst_ptr(self_arg_nb), self_arg);
                }

                goto done;
            }
        }
    }

    error_handler = nb_func_error_overload;

done:
    if (NB_UNLIKELY(cleanup.used()))
        cleanup.release();

    if (NB_UNLIKELY(error_handler))
        result = error_handler(self, args_in, nargs_in, kwargs_in);

    return result;
}

/// Simplified nb_func_vectorcall variant for functions w/o keyword arguments
static PyObject *nb_func_vectorcall_simple(PyObject *self,
                                           PyObject *const *args_in,
                                           size_t nargsf,
                                           PyObject *kwargs_in) noexcept {
    uint8_t args_flags[NB_MAXARGS_SIMPLE];
    func_data *fr = nb_func_data(self);

    const size_t count         = (size_t) Py_SIZE(self),
                 nargs_in      = (size_t) NB_VECTORCALL_NARGS(nargsf);

    const bool is_method      = fr->flags & (uint32_t) func_flags::is_method,
               is_constructor = fr->flags & (uint32_t) func_flags::is_constructor;

    PyObject *result = nullptr,
             *self_arg = (is_method && nargs_in > 0) ? args_in[0] : nullptr;

    // Small array holding temporaries (implicit conversion/*args/**kwargs)
    cleanup_list cleanup(self_arg);

    // Handler routine that will be invoked in case of an error condition
    PyObject *(*error_handler)(PyObject *, PyObject *const *, size_t,
                               PyObject *) noexcept = nullptr;

    bool fail = kwargs_in != nullptr;
    PyObject *none_ptr = Py_None;
    for (size_t i = 0; i < nargs_in; ++i)
        fail |= args_in[i] == none_ptr;

    if (fail) { // keyword/None arguments unsupported in simple vectorcall
        error_handler = nb_func_error_overload;
        goto done;
    }

    for (int pass = (count > 1) ? 0 : 1; pass < 2; ++pass) {
        for (int i = 0; i < NB_MAXARGS_SIMPLE; ++i)
            args_flags[i] = (uint8_t) pass;

        if (is_constructor)
            args_flags[0] = (uint8_t) cast_flags::construct;

        for (size_t k = 0; k < count; ++k) {
            const func_data *f = fr + k;

            if (nargs_in != f->nargs)
                continue;

            try {
                // Found a suitable overload, let's try calling it
                result = f->impl((void *) f->capture, (PyObject **) args_in,
                                 args_flags, (rv_policy) (f->flags & 0b111),
                                 &cleanup);

                if (NB_UNLIKELY(!result)) {
                    error_handler = nb_func_error_noconvert;
                    goto done;
                }
            } catch (builtin_exception &e) {
                if (set_builtin_exception_status(e)) {
                    result = nullptr;
                    goto done;
                } else {
                    result = NB_NEXT_OVERLOAD;
                }
            } catch (python_error &e) {
                e.restore();
                result = nullptr;
                goto done;
            } catch (...) {
                nb_func_convert_cpp_exception();
                result = nullptr;
                goto done;
            }

            if (result != NB_NEXT_OVERLOAD) {
                if (is_constructor) {
                    nb_inst *self_arg_nb = (nb_inst *) self_arg;
                    self_arg_nb->destruct = true;
                    self_arg_nb->ready = true;
                    if (NB_UNLIKELY(self_arg_nb->intrusive))
                        nb_type_data(Py_TYPE(self_arg))
                            ->set_self_py(inst_ptr(self_arg_nb), self_arg);
                }

                goto done;
            }
        }
    }

    error_handler = nb_func_error_overload;

done:
    if (NB_UNLIKELY(cleanup.used()))
        cleanup.release();

    if (NB_UNLIKELY(error_handler))
        result = error_handler(self, args_in, nargs_in, kwargs_in);

    return result;
}

static PyObject *nb_bound_method_vectorcall(PyObject *self,
                                            PyObject *const *args_in,
                                            size_t nargsf,
                                            PyObject *kwargs_in) noexcept {
    nb_bound_method *mb = (nb_bound_method *) self;
    size_t nargs = (size_t) NB_VECTORCALL_NARGS(nargsf);

    PyObject *result;
    if (nargsf & NB_VECTORCALL_ARGUMENTS_OFFSET) {
        PyObject **args_tmp = (PyObject **) args_in - 1;
        PyObject *tmp = args_tmp[0];
        args_tmp[0] = mb->self;
        result = mb->func->vectorcall((PyObject *) mb->func, args_tmp, nargs + 1, kwargs_in);
        args_tmp[0] = tmp;
    } else {
        size_t nkwargs_in = kwargs_in ? (size_t) NB_TUPLE_GET_SIZE(kwargs_in) : 0;
        PyObject **args_tmp = (PyObject **) PyObject_Malloc((nargs + nkwargs_in + 1) * sizeof(PyObject *));
        if (!args_tmp)
            return PyErr_NoMemory();
        args_tmp[0] = mb->self;
        for (size_t i = 0; i < nargs + nkwargs_in; ++i)
            args_tmp[i + 1] = args_in[i];
        result = mb->func->vectorcall((PyObject *) mb->func, args_tmp, nargs + 1, kwargs_in);
        PyObject_Free(args_tmp);
    }

    return result;
}

PyObject *nb_method_descr_get(PyObject *self, PyObject *inst, PyObject *) {
    if (inst) {
        /* Return a bound method. This should be avoidable in most cases via the
           'CALL_METHOD' opcode and vector calls. Pytest rewrites the bytecode
           in a way that breaks this optimization :-/ */

        nb_bound_method *mb =
            PyObject_GC_New(nb_bound_method, internals->nb_bound_method);
        mb->func = (nb_func *) self;
        mb->self = inst;
        mb->vectorcall = nb_bound_method_vectorcall;

        Py_INCREF(self);
        Py_INCREF(inst);

        return (PyObject *) mb;
    } else {
        Py_INCREF(self);
        return self;
    }
}


/// Render the function signature of a single function
static void nb_func_render_signature(const func_data *f) noexcept {
    const bool is_method      = f->flags & (uint32_t) func_flags::is_method,
               has_args       = f->flags & (uint32_t) func_flags::has_args,
               has_var_args   = f->flags & (uint32_t) func_flags::has_var_args,
               has_var_kwargs = f->flags & (uint32_t) func_flags::has_var_kwargs;

    const std::type_info **descr_type = f->descr_types;

    uint32_t arg_index = 0;
    buf.put_dstr(f->name);

    for (const char *pc = f->descr; *pc != '\0'; ++pc) {
        char c = *pc;

        switch (c) {
            case '{':
                {
                    const char *arg_name = has_args ? f->args[arg_index].name : nullptr;

                    // Argument name
                    if (has_var_kwargs && arg_index + 1 == f->nargs) {
                        buf.put("**");
                        buf.put_dstr(arg_name ? arg_name : "kwargs");
                        pc += 4; // strlen("dict")
                        break;
                    }

                    if (has_var_args && arg_index + 1 + has_var_kwargs == f->nargs) {
                        buf.put("*");
                        buf.put_dstr(arg_name ? arg_name : "args");
                        pc += 5; // strlen("tuple")
                        break;
                    }

                    if (is_method && arg_index == 0) {
                        buf.put("self");

                        // Skip over type
                        while (*pc != '}') {
                            if (*pc == '%')
                                descr_type++;
                            pc++;
                        }
                        arg_index++;
                        continue;
                    } else if (arg_name) {
                        buf.put_dstr(arg_name);
                    } else {
                        buf.put("arg");
                        if (f->nargs > 1 + (uint32_t) is_method)
                            buf.put_uint32(arg_index - is_method);
                    }

                    buf.put(": ");
                    if (has_args && f->args[arg_index].none)
                        buf.put("Optional[");
                }
                break;

            case '}':
                // Default argument
                if (has_args) {
                    if (f->args[arg_index].none)
                        buf.put(']');

                    if (f->args[arg_index].value) {
                        PyObject *o = f->args[arg_index].value;
                        PyObject *str = PyObject_Str(o);
                        bool is_str = PyUnicode_Check(o);

                        if (str) {
                            Py_ssize_t size = 0;
                            const char *cstr =
                                PyUnicode_AsUTF8AndSize(str, &size);
                            if (!cstr) {
                                PyErr_Clear();
                            } else {
                                buf.put(" = ");
                                if (is_str)
                                    buf.put('\'');
                                buf.put(cstr, (size_t) size);
                                if (is_str)
                                    buf.put('\'');
                            }
                            Py_DECREF(str);
                        } else {
                            PyErr_Clear();
                        }
                    }
                }

                arg_index++;

                if (arg_index == f->nargs - has_var_args - has_var_kwargs && !has_args)
                    buf.put(", /");

                break;

            case '%':
                check(*descr_type,
                      "nb::detail::nb_func_render_signature(): missing type!");

                if (!(is_method && arg_index == 0)) {
                    auto it = internals->type_c2p.find(std::type_index(**descr_type));

                    if (it != internals->type_c2p.end()) {
                        handle th((PyObject *) it->second->type_py);
                        buf.put_dstr((borrow<str>(th.attr("__module__"))).c_str());
                        buf.put('.');
                        buf.put_dstr((borrow<str>(th.attr("__qualname__"))).c_str());
                    } else {
                        char *name = type_name(*descr_type);
                        buf.put_dstr(name);
                        free(name);
                    }
                }

                descr_type++;
                break;

            default:
                buf.put(c);
                break;
        }
    }

    check(arg_index == f->nargs && !*descr_type,
          "nanobind::detail::nb_func_render_signature(%s): arguments inconsistent.",
          f->name);
}

static PyObject *nb_func_get_name(PyObject *self) {
    func_data *f = nb_func_data(self);
    if (f->flags & (uint32_t) func_flags::has_name) {
        return PyUnicode_FromString(f->name);
    } else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

static PyObject *nb_func_get_qualname(PyObject *self) {
    func_data *f = nb_func_data(self);
    if ((f->flags & (uint32_t) func_flags::has_scope) &&
        (f->flags & (uint32_t) func_flags::has_name)) {
        PyObject *scope_name = PyObject_GetAttrString(f->scope, "__qualname__");
        if (scope_name) {
            return PyUnicode_FromFormat("%U.%s", scope_name, f->name);
        } else {
            PyErr_Clear();
            return PyUnicode_FromString(f->name);
        }
    } else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

static PyObject *nb_func_get_module(PyObject *self) {
    func_data *f = nb_func_data(self);
    if (f->flags & (uint32_t) func_flags::has_scope) {
        return PyObject_GetAttrString(
            f->scope, PyModule_Check(f->scope) ? "__name__" : "__module__");
    } else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

PyObject *nb_func_get_doc(PyObject *self, void *) {
    func_data *f = nb_func_data(self);
    uint32_t count = (uint32_t) Py_SIZE(self);

    buf.clear();

    size_t doc_count = 0;
    for (uint32_t i = 0; i < count; ++i) {
        const func_data *fi = f + i;
        if (fi->flags & (uint32_t) func_flags::raw_doc)
            return PyUnicode_FromString(fi->doc);

        nb_func_render_signature(fi);
        buf.put('\n');
        if ((fi->flags & (uint32_t) func_flags::has_doc) && fi->doc[0] != '\0')
            doc_count++;
    }

    if (doc_count > 1)
        buf.put("\nOverloaded function.\n");

    for (uint32_t i = 0; i < count; ++i) {
        const func_data *fi = f + i;

        if ((fi->flags & (uint32_t) func_flags::has_doc) && fi->doc[0] != '\0') {
            buf.put('\n');

            if (doc_count > 1) {
                buf.put_uint32(i + 1);
                buf.put(". ``");
                nb_func_render_signature(fi);
                buf.put("``\n\n");
            }

            buf.put_dstr(fi->doc);
            buf.put('\n');
        }
    }

    if (buf.size() > 0) // remove last newline
        buf.rewind(1);

    return PyUnicode_FromString(buf.get());
}

// PyGetSetDef entry for __module__ is ignored in Python 3.8
PyObject *nb_func_getattro(PyObject *self, PyObject *name_) {
    const char *name = PyUnicode_AsUTF8AndSize(name_, nullptr);

    if (!name)
        return nullptr;
    else if (strcmp(name, "__module__") == 0)
        return nb_func_get_module(self);
    else if (strcmp(name, "__name__") == 0)
        return nb_func_get_name(self);
    else if (strcmp(name, "__qualname__") == 0)
        return nb_func_get_qualname(self);
    else if (strcmp(name, "__doc__") == 0)
        return nb_func_get_doc(self, nullptr);
    else
        return PyObject_GenericGetAttr(self, name_);
}

PyObject *nb_bound_method_getattro(PyObject *self, PyObject *name_) {
    bool passthrough = false;
    if (const char *name = PyUnicode_AsUTF8AndSize(name_, nullptr)) {
        // These attributes do exist on nb_bound_method (because they
        // exist on every type) but we want to take their special handling
        // from nb_func_getattro instead.
        passthrough = (strcmp(name, "__doc__") == 0 ||
                       strcmp(name, "__module__") == 0);
    }
    if (!passthrough) {
        if (PyObject* res = PyObject_GenericGetAttr(self, name_))
            return res;
        PyErr_Clear();
    }
    nb_func *func = ((nb_bound_method *) self)->func;
    return nb_func_getattro((PyObject *) func, name_);
}

/// Excise a substring from 's'
static void strexc(char *s, const char *sub) {
    size_t len = strlen(sub);
    if (len == 0)
        return;

    char *p = s;
    while ((p = strstr(p, sub)))
        memmove(p, p + len, strlen(p + len) + 1);
}

/// Return a readable string representation of a C++ type
NB_NOINLINE char *type_name(const std::type_info *t) {
    const char *name_in = t->name();

#if defined(__GNUG__)
    int status = 0;
    char *name = abi::__cxa_demangle(name_in, nullptr, nullptr, &status);
#else
    char *name = NB_STRDUP(name_in);
    strexc(name, "class ");
    strexc(name, "struct ");
    strexc(name, "enum ");
#endif
    strexc(name, "nanobind::");
    return name;
}

NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)
