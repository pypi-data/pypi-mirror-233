/*
 MIT License

  Copyright (c) 2017 - 2023 Advanced Micro Devices, Inc. All rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  */
#ifndef ROCM_CORE_WRAPPER_INCLUDE_ROCM_VERSION_H
#define ROCM_CORE_WRAPPER_INCLUDE_ROCM_VERSION_H

#ifndef ROCM_HEADER_WRAPPER_WERROR
#define ROCM_HEADER_WRAPPER_WERROR 0
#endif
#if ROCM_HEADER_WRAPPER_WERROR  /* ROCM_HEADER_WRAPPER_WERROR 1 */
#error "rocm_version.h has moved to /opt/rocm-5.7.0/include/rocm-core "
#else      /* ROCM_HEADER_WRAPPER_WERROR 0 */
#if defined(__GNUC__)
#warning "rocm_version.h has moved to /opt/rocm-5.7.0/include/rocm-core "
#else
#pragma message ("rocm_version.h has moved to /opt/rocm-5.7.0/include/rocm-core ")
#endif
#endif /* ROCM_HEADER_WRAPPER_WERROR */

#include "rocm-core/rocm_version.h"


#if 0
/* The following is a copy of the original file for the benefit of build systems which grep for values
 * in this file rather than preprocess it. This is just for backward compatibility */

////////////////////////////////////////////////////////////////////////////////
//
// MIT License
//
// Copyright (c) 2017 - 2023 Advanced Micro Devices, Inc. All rights Reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//
////////////////////////////////////////////////////////////////////////////////


#ifndef _ROCM_VERSION_H_
#define _ROCM_VERSION_H_


#ifdef __cplusplus
extern "C" {
#endif  /* __cplusplus */


#define LIB_API_PUBLIC __attribute__ ((visibility ("default")))


#define ROCM_VERSION_MAJOR   5
#define ROCM_VERSION_MINOR   7
#define ROCM_VERSION_PATCH   0

#define ROCM_BUILD_INFO	     "5.7.0.0-63-af460ac"

typedef enum {
	VerSuccess=0,
	VerIncorrecPararmeters,
	VerValuesNotDefined,
	VerErrorMAX		//This should always be last value in the enumerations
} VerErrors;


//  API for getting the verion
//  Return val :  VerErros : API execution status.  The parameters are valid only when the exetution status is SUCCESS==0
LIB_API_PUBLIC VerErrors getROCmVersion(unsigned int* Major, unsigned int* Minor, unsigned int* Patch) __attribute__((nonnull)) ;
//  Usage :
//  int mj=0,mn=0,p=0,ret=0;
//  ret=getROCMVersion(&mj,&mn,&p);
//  if(ret !=VerSuccess )  // error occured
//
//  check for the values and
//



//API for building build info on console
LIB_API_PUBLIC VerErrors printBuildInfo();


#ifdef __cplusplus
}  // end extern "C" block
#endif

#endif  //_ROCM_VERSION_H_  header guard



#endif

#endif
