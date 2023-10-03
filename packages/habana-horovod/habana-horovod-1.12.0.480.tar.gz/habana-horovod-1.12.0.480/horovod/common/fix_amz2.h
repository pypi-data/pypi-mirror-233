/******************************************************************************
 * Copyright (C) 2023 Habana Labs, Ltd. an Intel Company
 * All Rights Reserved.
 *
 * Unauthorized copying of this file or any element(s) within it, via any medium
 * is strictly prohibited.
 * This file contains Habana Labs, Ltd. proprietary and confidential information
 * and is subject to the confidentiality and license agreements under which it
 * was provided.
 *
 *******************************************************************************
 */

#pragma once

// Inspired by GCC's implementation:
// https://gcc.gnu.org/git/?p=gcc.git;a=blob;f=gcc/config/i386/avxintrin.h;h=678368c7d784a479c38f76def18920dbd0107dd6;hb=23f05e90ea5b60b676c69f5bf481bfd6c3a90160

#define _mm256_set_m128i(vh, vl) \
        _mm256_insertf128_si256(_mm256_castsi128_si256(vl), (vh), 1)
#define _mm256_set_m128(vh, vl) \
        _mm256_insertf128_ps(_mm256_castps128_ps256(vl), (vh), 1)
#define _mm256_set_m128d(vh, vl) \
        _mm256_insertf128_pd(_mm256_castpd128_pd256(vl), (vh), 1)
