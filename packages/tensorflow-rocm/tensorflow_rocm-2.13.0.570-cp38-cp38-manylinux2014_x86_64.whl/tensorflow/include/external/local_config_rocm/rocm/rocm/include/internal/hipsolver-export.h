/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_INTERNAL_HIPSOLVER_EXPORT_H
#define ROCM_SYMLINK_INTERNAL_HIPSOLVER_EXPORT_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "../hipsolver/internal/hipsolver-export.h"
#else
#ifndef ROCM_HEADER_WRAPPER_WERROR
#define ROCM_HEADER_WRAPPER_WERROR 0
#endif
#if ROCM_HEADER_WRAPPER_WERROR  /* ROCM_HEADER_WRAPPER_WERROR 1 */
#error "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/hipsolver/internal/hipsolver-export.h by using #include <hipsolver/internal/hipsolver-export.h>"
#else  /* ROCM_HEADER_WRAPPER_WERROR 0 */
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/hipsolver/internal/hipsolver-export.h by using #include <hipsolver/internal/hipsolver-export.h>")
#elif defined(__GNUC__)
#warning "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/hipsolver/internal/hipsolver-export.h by using #include <hipsolver/internal/hipsolver-export.h>"
#endif
#endif  /* ROCM_HEADER_WRAPPER_WERROR */
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "../hipsolver/internal/hipsolver-export.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_INTERNAL_HIPSOLVER_EXPORT_H */

#if 0

/* The following is a copy of the original file for the benefit of build systems which grep for values
 * in this file rather than preprocess it. This is just for backward compatibility */

/* ************************************************************************
 * Copyright (C) 2020-2023 Advanced Micro Devices, Inc.
 * ************************************************************************ */

#ifndef HIPSOLVER_VERSION_H
#define HIPSOLVER_VERSION_H

/* the configured version and settings
 */
// clang-format off
#define hipsolverVersionMajor 1
#define hipsolverVersionMinor 8
#define hipsolverVersionPatch 1
#define hipsolverVersionTweak a293f08
// clang-format on

#endif /* HIPSOLVER_VERSION_H */

#endif
