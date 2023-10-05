/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
   */

#ifndef HSAKMT_WRAPPER_INCLUDE_HSAKMT_H
#define HSAKMT_WRAPPER_INCLUDE_HSAKMT_H

#ifndef ROCM_HEADER_WRAPPER_WERROR
#define ROCM_HEADER_WRAPPER_WERROR 0
#endif
#if ROCM_HEADER_WRAPPER_WERROR  /* ROCM_HEADER_WRAPPER_WERROR 1 */
#error "hsakmt.h has moved to /opt/rocm-5.7.0/include/hsakmt and package include paths have changed.\nInclude as \"hsakmt/hsakmt.h\" when using cmake packages."
#else  /* ROCM_HEADER_WRAPPER_WERROR 0 */
#if defined(__GNUC__)
#warning "hsakmt.h has moved to /opt/rocm-5.7.0/include/hsakmt and package include paths have changed.\nInclude as \"hsakmt/hsakmt.h\" when using cmake packages."
#else
#pragma message("hsakmt.h has moved to /opt/rocm-5.7.0/include/hsakmt and package include paths have changed.\nInclude as \"hsakmt/hsakmt.h\" when using cmake packages.")
#endif
#endif  /* ROCM_HEADER_WRAPPER_WERROR */

#include "hsakmt/hsakmt.h"


#endif
