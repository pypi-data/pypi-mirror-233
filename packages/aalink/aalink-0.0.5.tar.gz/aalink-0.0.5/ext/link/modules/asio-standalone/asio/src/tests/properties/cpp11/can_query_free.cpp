//
// cpp11/can_query_free.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2023 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include "asio/query.hpp"
#include <cassert>

struct prop
{
};

struct object
{
  friend constexpr int query(const object&, prop) { return 123; }
};

namespace asio {

template<>
struct is_applicable_property<object, prop>
{
  static constexpr bool value = true;
};

} // namespace asio

int main()
{
  static_assert(asio::can_query<object, prop>::value, "");
  static_assert(asio::can_query<const object, prop>::value, "");
}
