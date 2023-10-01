//
// cpp14/can_prefer_not_applicable_unsupported.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2023 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include "asio/prefer.hpp"
#include <cassert>

template <int>
struct prop
{
};

template <int>
struct object
{
};

int main()
{
  static_assert(!asio::can_prefer_v<object<1>, prop<2>>, "");
  static_assert(!asio::can_prefer_v<object<1>, prop<2>, prop<3>>, "");
  static_assert(!asio::can_prefer_v<object<1>, prop<2>, prop<3>, prop<4>>, "");
  static_assert(!asio::can_prefer_v<const object<1>, prop<2>>, "");
  static_assert(!asio::can_prefer_v<const object<1>, prop<2>, prop<3>>, "");
  static_assert(!asio::can_prefer_v<const object<1>, prop<2>, prop<3>, prop<4>>, "");
}
