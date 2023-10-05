def foo():

    # Only used with std::string and thus C++.
    name = "vector_string_out"
    fmt.hname = name
    fmt.hnamefunc = wformat("{C_prefix}ShroudVectorStringOut", fmt)
    fmt.hnamefunc_vector_string_out = fmt.hnamefunc
    fmt.hnameproto = wformat(
        "void {hnamefunc}({C_array_type} *outdesc, std::vector<std::string> &in)", fmt)
    if literalinclude:
        fmt.lstart = "{}helper {}\n".format(cstart, name)
        fmt.lend = "\n{}helper {}".format(cend, name)
    CHelpers[name] = dict(
        name=fmt.hnamefunc,
        api="cxx",
        scope="cwrap_impl",
        dependent_helpers=["array_context"],
        proto_include=["<string>", "<vector>"],
        proto=fmt.hnameproto + ";",
        cxx_include=["<cstring>", "<cstddef>"],
        # XXX - mangle name
        source=wformat(
            """
{lstart}// helper {hname}
// Copy the std::vector<std::string> into Fortran array argument.
// Called by C++.
// out is already blank filled.
{hnameproto}
{{+
size_t nvect = std::min(outdesc->size, in.size());
size_t len = outdesc->elem_len;
char *dest = const_cast<char *>(outdesc->addr.ccharp);
//char *dest = static_cast<char *>(outdesc->cxx.addr);
for (size_t i = 0; i < nvect; ++i) {{+
std::memcpy(dest, in[i].data(), std::min(len, in[i].length()));
dest += outdesc->elem_len;
-}}
//{C_memory_dtor_function}(&data->cxx); // delete data->cxx.addr
-}}{lend}
""",
            fmt,
        ),
    )

    # Fortran interface for above function.
    # Deal with allocatable character
    fmt.hnamefunc = wformat("{C_prefix}SHROUD_copy_vector_string_and_free", fmt)
##-    FHelpers[name] = dict(
##-        dependent_helpers=["array_context"],
##-        name=fmt.hnamefunc,
##-        interface=wformat(
##-            """
##-interface+
##-! helper {hname}
##-! Copy the char* or std::string in context into c_var.
##-subroutine {hnamefunc}(context, c_var, c_var_size) &
##-     bind(c,name="{C_prefix}ShroudCopyStringAndFree")+
##-use, intrinsic :: iso_c_binding, only : C_CHAR, C_SIZE_T
##-import {F_array_type}
##-type({F_array_type}), intent(IN) :: context
##-character(kind=C_CHAR), intent(OUT) :: c_var(*)
##-integer(C_SIZE_T), value :: c_var_size
##--end subroutine {hnamefunc}
##--end interface""",
##-            fmt,
##-        ),
##-    )

    ########################################
    ########################################
    # Only used with std::string and thus C++.
    # Called from Fortran.
    # The capsule contains a pointer to a std::vector<std::string>
    # which is copied into the cdesc.
    name = "vector_string_allocatable"
    fmt.hname = name
    fmt.hnamefunc = wformat("{C_prefix}ShroudVectorStringAllocatable", fmt)
    fmt.chnamefunc = wformat("{C_prefix}ShroudVectorStringAllocatable", fmt)
    fmt.hnameproto = wformat(
        "void {hnamefunc}({C_array_type} *outdesc, {C_capsule_data_type} *vec)", fmt)
    if literalinclude:
        fmt.lstart = "{}helper {}\n".format(cstart, name)
        fmt.lend = "\n{}helper {}".format(cend, name)
    CHelpers[name] = dict(
        name=fmt.hnamefunc,
        api="c",
        scope="cwrap_impl",
        dependent_helpers=["array_context", "vector_string_out"],
        proto=fmt.hnameproto + ";",
        source=wformat(
            """
{lstart}// helper {hname}
// Copy the std::vector<std::string> into Fortran array.
// Called by Fortran to deal with allocatable character.
// out is already blank filled.
{hnameproto}
{{+
std::vector<std::string> *cxxvec =\t static_cast< std::vector<std::string> * >\t(vec->addr);
{hnamefunc_vector_string_out}(outdesc, *cxxvec);
{C_memory_dtor_function}(vec); // delete data->cxx.addr
-}}{lend}
""",
            fmt,
        ),
    )

    # Fortran interface for above function.
    # Deal with allocatable character
    fmt.hnamefunc = wformat("{C_prefix}SHROUD_vector_string_allocatable", fmt)
    FHelpers[name] = dict(
        dependent_helpers=["array_context", "capsule_data_helper"],
        name=fmt.hnamefunc,
        interface=wformat(
            """
interface+
! helper {hname}
! Copy the char* or std::string in context into c_var.
subroutine {hnamefunc}(cdesc, capsule) &
     bind(c,name="{chnamefunc}")+
import {F_array_type}, {F_capsule_data_type}
type({F_array_type}), intent(IN) :: cdesc
type({F_capsule_data_type}), intent(INOUT) :: capsule
-end subroutine {hnamefunc}
-end interface""",
            fmt,
        ),
    )

    ########################################
    ########################################
    name = "vector_string_out_len"
    fmt.hname = name
    fmt.hnamefunc = wformat("{C_prefix}ShroudVectorStringOutSize", fmt)
    fmt.hnameproto = wformat(
        "size_t {hnamefunc}(std::vector<std::string> &in)", fmt)
    if literalinclude:
        fmt.lstart = "{}helper {}\n".format(cstart, name)
        fmt.lend = "\n{}helper {}".format(cend, name)
    CHelpers[name] = dict(
        name=fmt.hnamefunc,
        api="cxx",
        scope="cwrap_impl",
        proto_include=["<string>", "<vector>"],
        proto=fmt.hnameproto + ";",
        source=wformat(
            """
{lstart}// helper {hname}
// Return the maximum string length in a std::vector<std::string>.
{hnameproto}
{{+
size_t nvect = in.size();
size_t len = 0;
for (size_t i = 0; i < nvect; ++i) {{+
len = std::max(len, in[i].length());
-}}
return len;
-}}{lend}
""",
            fmt,
        ),
    )

    ########################################
