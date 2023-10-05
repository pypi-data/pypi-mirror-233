/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_ROCFFT_EXPORT_H
#define ROCM_SYMLINK_ROCFFT_EXPORT_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "rocfft/rocfft-export.h"
#else
#ifndef ROCM_HEADER_WRAPPER_WERROR
#define ROCM_HEADER_WRAPPER_WERROR 0
#endif
#if ROCM_HEADER_WRAPPER_WERROR  /* ROCM_HEADER_WRAPPER_WERROR 1 */
#error "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocfft/rocfft-export.h by using #include <rocfft/rocfft-export.h>"
#else  /* ROCM_HEADER_WRAPPER_WERROR 0 */
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocfft/rocfft-export.h by using #include <rocfft/rocfft-export.h>")
#elif defined(__GNUC__)
#warning "This file is deprecated. Use the header file from /opt/rocm-5.7.0/include/rocfft/rocfft-export.h by using #include <rocfft/rocfft-export.h>"
#endif
#endif  /* ROCM_HEADER_WRAPPER_WERROR */
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "rocfft/rocfft-export.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_ROCFFT_EXPORT_H */

#if 0

/* The following is a copy of the original file for the benefit of build systems which grep for values
 * in this file rather than preprocess it. This is just for backward compatibility */

/******************************************************************************
* Copyright (C) 2016 - 2023 Advanced Micro Devices, Inc. All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*******************************************************************************/

/* the configured version and settings
 */
#ifndef ROCFFT_VERSION_H
#define ROCFFT_VERSION_H

// clang-format off
#define rocfft_version_major      1
#define rocfft_version_minor      0
#define rocfft_version_patch      23
#define rocfft_version_tweak      7520fc65
// clang-format on

#endif /* ROCFFT_VERSION_H */

#endif
