//
// cpp11/can_require_concept_static.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2023 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include "asio/require_concept.hpp"
#include <cassert>

template <int>
struct prop
{
  static constexpr bool is_requirable_concept = true;
};

template <int>
struct object
{
};

namespace asio {

template<int N, int M>
struct is_applicable_property<object<N>, prop<M> >
{
  static constexpr bool value = true;
};

namespace traits {

template<int N>
struct static_require_concept<object<N>, prop<N> >
{
  static constexpr bool is_valid = true;
};

} // namespace traits
} // namespace asio

int main()
{
  static_assert(asio::can_require_concept<object<1>, prop<1>>::value, "");
  static_assert(asio::can_require_concept<const object<1>, prop<1>>::value, "");
}
