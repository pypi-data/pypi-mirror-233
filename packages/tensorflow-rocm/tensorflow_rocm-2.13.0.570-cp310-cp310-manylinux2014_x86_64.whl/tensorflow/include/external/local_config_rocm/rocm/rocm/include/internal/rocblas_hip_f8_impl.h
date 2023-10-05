/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_INTERNAL_ROCBLAS_HIP_F8_IMPL_H
#define ROCM_SYMLINK_INTERNAL_ROCBLAS_HIP_F8_IMPL_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "../rocblas/internal/rocblas_hip_f8_impl.h"
#else
#ifndef ROCM_HEADER_WRAPPER_WERROR
#define ROCM_HEADER_WRAPPER_WERROR 0
#endif
#if ROCM_HEADER_WRAPPER_WERROR  /* ROCM_HEADER_WRAPPER_WERROR 1 */
#error "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocblas/internal/rocblas_hip_f8_impl.h by using #include <rocblas/internal/rocblas_hip_f8_impl.h>"
#else  /* ROCM_HEADER_WRAPPER_WERROR 0 */
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocblas/internal/rocblas_hip_f8_impl.h by using #include <rocblas/internal/rocblas_hip_f8_impl.h>")
#elif defined(__GNUC__)
#warning "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocblas/internal/rocblas_hip_f8_impl.h by using #include <rocblas/internal/rocblas_hip_f8_impl.h>"
#endif
#endif  /* ROCM_HEADER_WRAPPER_WERROR */
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "../rocblas/internal/rocblas_hip_f8_impl.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_INTERNAL_ROCBLAS_HIP_F8_IMPL_H */


