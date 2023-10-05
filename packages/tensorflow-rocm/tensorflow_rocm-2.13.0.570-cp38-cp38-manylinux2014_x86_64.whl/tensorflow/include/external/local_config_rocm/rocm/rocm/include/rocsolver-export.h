/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_ROCSOLVER_EXPORT_H
#define ROCM_SYMLINK_ROCSOLVER_EXPORT_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "rocsolver/rocsolver-export.h"
#else
#ifndef ROCM_HEADER_WRAPPER_WERROR
#define ROCM_HEADER_WRAPPER_WERROR 0
#endif
#if ROCM_HEADER_WRAPPER_WERROR  /* ROCM_HEADER_WRAPPER_WERROR 1 */
#error "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocsolver/rocsolver-export.h by using #include <rocsolver/rocsolver-export.h>"
#else  /* ROCM_HEADER_WRAPPER_WERROR 0 */
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocsolver/rocsolver-export.h by using #include <rocsolver/rocsolver-export.h>")
#elif defined(__GNUC__)
#warning "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocsolver/rocsolver-export.h by using #include <rocsolver/rocsolver-export.h>"
#endif
#endif  /* ROCM_HEADER_WRAPPER_WERROR */
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "rocsolver/rocsolver-export.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_ROCSOLVER_EXPORT_H */

#if 0

/* The following is a copy of the original file for the benefit of build systems which grep for values
 * in this file rather than preprocess it. This is just for backward compatibility */

/* ************************************************************************
 * Copyright (c) 2019-2023 Advanced Micro Devices, Inc.
 * ************************************************************************ */

/* the configured version and settings
 */
#ifndef ROCSOLVER_VERSION_H
#define ROCSOLVER_VERSION_H

// clang-format off
#define ROCSOLVER_VERSION_MAJOR 3
#define ROCSOLVER_VERSION_MINOR 23
#define ROCSOLVER_VERSION_PATCH 0
#define ROCSOLVER_VERSION_TWEAK 0d065ba
// clang-format on

#endif /* ROCSOLVER_VERSION_H */

#endif
