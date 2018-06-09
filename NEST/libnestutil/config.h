/*
 *  config.h
 *
 *  This file is part of NEST.
 *
 *  Copyright (C) 2004 The NEST Initiative
 *
 *  NEST is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  NEST is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef CONFIG_H
#define CONFIG_H
/* 
    Configuration header.
    config.h is automatically generated from config.h.in
    during the configuration process. 

    Please make all changes in config.h.in.
*/

#define NEST_VERSION_PRGNAME "nest-2.14.0"

#define NEST_VERSION_MAJOR_REVISION 2
#define NEST_VERSION_MINOR_REVISION 14
#define NEST_VERSION_PATCHLEVEL "0"

// TODO NEST_HOST and NEST_HOSTVENDOR not available with cmake
#define NEST_HOST "x86_64-pc-linux"
#define NEST_HOSTOS "linux"
#define NEST_HOSTCPU "x86_64"
#define NEST_HOSTVENDOR "pc"

#define NEST_INSTALL_PREFIX "/home/christoph/nest-simulator-2.14.0"
#define NEST_INSTALL_DATADIR "share/nest"
#define NEST_INSTALL_DOCDIR "share/doc/nest"

#define NEST_EXITCODE_ABORT 134
#define NEST_EXITCODE_SEGFAULT 139

/* Name of package */
#define PACKAGE nest

/* tics per ms in simulation */
#define CONFIG_TICS_PER_MS 1000.0

/* tics per step in simulation */
#define CONFIG_TICS_PER_STEP 100

/* define if the compiler does not include *.h headers ISO conformant */
/* #undef HAVE_ALPHA_CXX_STD_BUG */

/* define if the compiler ignores cmath makros */
/* #undef HAVE_CMATH_MAKROS_IGNORED */

/* "Define if expm1() is available" */
/* #undef HAVE_EXPM1 */

/* Is the GNU Science Library available (ver. >= 1.0)? */
/* #undef HAVE_GSL */

/* Define to 1 if you have the <inttypes.h> header file.
 * Used in sparseconfig.h.
 */
#define HAVE_INTTYPES_H 1

/* "Define if isnan() is available" */
#define HAVE_ISNAN 1

/* "Define if std::isnan() is available" */
#define HAVE_STD_ISNAN 1

/* define for istream */
#define HAVE_ISTREAM 1

/* Havel libltdl, can load dynamic modules */
#define HAVE_LIBLTDL 1

/* libneurosim support enabled? */
/* #undef HAVE_LIBNEUROSIM */

/* define if we have usable long long type.
 * Used in sparseconfig.h.
 */
#define HAVE_LONG_LONG 1

/* Define to 1 if you have the <mach/mach.h> header file. */
/* #undef HAVE_MACH_MACH_H */

/* Define to 1 if you have the <mach-o/dyld.h> header file. */
/* #undef HAVE_MACH_O_DYLD_H */

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* MPI is available. */
/* #undef HAVE_MPI */

/* MUSIC support enabled? */
/* #undef HAVE_MUSIC */

/* define if M_E is defined */
#define HAVE_M_E 1

/* define if M_PI is defined */
#define HAVE_M_PI 1

/* "Define if NAN is available" */
#define HAVE_NAN 1

/* "Define if std::nan(NULL) is available" */
#define HAVE_STD_NAN 1

/* define for ostream */
#define HAVE_OSTREAM 1

/* Use GNU libreadline */
/* #undef HAVE_READLINE */

/* define if the compiler ignores symbolic signal names in signal.h */
/* #undef HAVE_SIGUSR_IGNORED */

/* define for sstream */
#define HAVE_SSTREAM 1

/* define if the compiler fails on static template member declaration */
/* #undef HAVE_STATIC_TEMPLATE_DECLARATION_FAIL */

/* Define to 1 if you have the <stdint.h> header file.
 * Used in sparseconfig.h.
 */
#define HAVE_STDINT_H 1

/* define for STL vector capacity base unity */
#define HAVE_STL_VECTOR_CAPACITY_BASE_UNITY 1

/* define for STL vector capacity doubling strategy */
#define HAVE_STL_VECTOR_CAPACITY_DOUBLING 1

/* Define to 1 if you have the <sys/types.h> header file.
 * Used in sparseconfig.h.
 */
#define HAVE_SYS_TYPES_H 1

/* Define if the system has the type `uint16_t'.
 * Used in sparseconfig.h.
 */
#define HAVE_UINT16_T 1

/* Define if the system has the type `u_int16_t'.
 * Used in sparseconfig.h.
 */
/* #undef HAVE_U_INT16_T */

/* Tics per millisecond specified? */
#define HAVE_TICS_PER_MS 1

/* Tics per step specified? */
#define HAVE_TICS_PER_STEP 1

/* define if the compiler fails with ICE */
/* #undef HAVE_XLC_ICE_ON_USING */

/* Configuring for Blue Gene */
/* #undef IS_BLUEGENE */

/* Configuring for Blue Gene/L */
/* #undef IS_BLUEGENE_L */

/* Configuring for Blue Gene/P */
/* #undef IS_BLUEGENE_P */

/* Configuring for Blue Gene/Q */
/* #undef IS_BLUEGENE_Q */

/* Configuring for K */
/* #undef IS_K */

/* Use PS array construction semantics */
#define PS_ARRAYS 1

#endif // #ifndef CONFIG_H
