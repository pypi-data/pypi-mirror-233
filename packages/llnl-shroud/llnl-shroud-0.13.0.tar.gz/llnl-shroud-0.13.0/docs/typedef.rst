.. Copyright (c) 2017-2022, Lawrence Livermore National Security, LLC and
   other Shroud Project Developers.
   See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (BSD-3-Clause)

:orphan:

Typedef
=======

Shroud will perserve as much information of typedefs as possible.
In the simplest case, a typedef is just an alias for another type.
The C wrapper will create a new typedef with a flattened name.

The Fortran typedef will create a parameter with the kind of the typedef.


A typedef is often defined in C for structs to simplify their use.
Structure tags exist in a different namespace than type names.

.. code-block:: c

    struct tagname {
        int i;
        double d;
    };
    typedef struct tagname structtype;
    struct tagname var1;
    structtype var2;

This is the default behavior in C++.  Each struct tag can also be used
as a structtype.

Shroud treats the typedef as the name of the Fortran derived type.

.. code-block:: fortran

  type structtype, bind(C)
    integer(C_INT) :: i
    real(C_DOUBLE) :: d
  end type structtype

Any reference to ``struct tagname`` or ``structtype`` will use the same
Fortran derived type using the typedef name of ``structtype``.

.. And USING statement

   Try to keep some relationship in YAML and generated code

    declarations:
    - decl: typedef int64_t IndexType
      fields:
        # defined in SidreTypes.hpp
        c_header : axom/sidre/interface/SidreTypes.h
        cxx_header : axom/sidre/interface/SidreTypes.h
        c_type   : SIDRE_IndexType
        f_cast: int({f_var}, SIDRE_IndexType)
        f_type: integer(SIDRE_IndexType)
        f_kind: SIDRE_IndexType
        f_module_name: axom_sidre
        f_c_module:
          "--import--":
          -  SIDRE_IndexType


    ----------

    typedef int IndexType;
    IndexType var;

    typedef int LIB_xxxx;

    integer, parameter :: IndexType = C_INT
    integer(IndexType) :: var


    ----------

    typedef struct tag sname;
    sname var;

    typedef struct LIB_tag LIB_sname;

    type(sname) :: var

    ----------

    typedef int (*fcn)(int);
    fcn var;

    typedef int (*LIB_fcn)(int);


        abstract interface
            subroutine fcn(arg1) bind(C)
                implicit none
                integer(C_INT) :: arg1
            end subroutine fcn
        end abstract interface

        procedure(fcn) :: var

