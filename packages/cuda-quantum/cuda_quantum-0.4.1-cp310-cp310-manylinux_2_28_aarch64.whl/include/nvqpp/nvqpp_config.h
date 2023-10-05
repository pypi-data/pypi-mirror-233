/*************************************************************** -*- C++ -*- ***
 * Copyright (c) 2022 - 2023 NVIDIA Corporation & Affiliates.                  *
 * All rights reserved.                                                        *
 *                                                                             *
 * This source code and the accompanying materials are made available under    *
 * the terms of the Apache License 2.0 which accompanies this distribution.    *
 ******************************************************************************/

#pragma once
#define PLATFORM_SHARED_LIBRARY_SUFFIX ".so"
#define LLVM_INCLUDE_DIR "/opt/llvm/include"
#define LLVM_ROOT "/opt/llvm"
#define LLVM_LIBCXX_INCLUDE_DIR "/opt/llvm/include/c++/v1"
#define CUDAQ_LLVM_VERSION "16"

// This is used by cudaq-quake as a backup search location
// for required cudaq headers. We will search this install 
// directory first 
#define FALLBACK_CUDAQ_INCLUDE_DIR "/cuda-quantum/runtime"
