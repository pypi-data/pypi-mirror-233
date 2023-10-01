//
// execution/operation_state.hpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2023 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#ifndef ASIO_EXECUTION_OPERATION_STATE_HPP
#define ASIO_EXECUTION_OPERATION_STATE_HPP

#if defined(_MSC_VER) && (_MSC_VER >= 1200)
# pragma once
#endif // defined(_MSC_VER) && (_MSC_VER >= 1200)

#include "asio/detail/config.hpp"

#if !defined(ASIO_NO_DEPRECATED)

#include "asio/detail/type_traits.hpp"
#include "asio/execution/start.hpp"

#if defined(ASIO_HAS_DEDUCED_START_FREE_TRAIT) \
  && defined(ASIO_HAS_DEDUCED_START_MEMBER_TRAIT)
# define ASIO_HAS_DEDUCED_EXECUTION_IS_OPERATION_STATE_TRAIT 1
#endif // defined(ASIO_HAS_DEDUCED_START_FREE_TRAIT)
       //   && defined(ASIO_HAS_DEDUCED_START_MEMBER_TRAIT)

#include "asio/detail/push_options.hpp"

namespace asio {
namespace execution {
namespace detail {

template <typename T>
struct is_operation_state_base :
  integral_constant<bool,
    is_destructible<T>::value
      && is_object<T>::value
  >
{
};

} // namespace detail

/// The is_operation_state trait detects whether a type T satisfies the
/// execution::operation_state concept.
/**
 * Class template @c is_operation_state is a type trait that is derived from
 * @c true_type if the type @c T meets the concept definition for an
 * @c operation_state, otherwise @c false_type.
 */
template <typename T>
struct is_operation_state :
#if defined(GENERATING_DOCUMENTATION)
  integral_constant<bool, automatically_determined>
#else // defined(GENERATING_DOCUMENTATION)
  conditional<
    can_start<typename add_lvalue_reference<T>::type>::value
      && is_nothrow_start<typename add_lvalue_reference<T>::type>::value,
    detail::is_operation_state_base<T>,
    false_type
  >::type
#endif // defined(GENERATING_DOCUMENTATION)
{
};

#if defined(ASIO_HAS_VARIABLE_TEMPLATES)

template <typename T>
ASIO_CONSTEXPR const bool is_operation_state_v =
  is_operation_state<T>::value;

#endif // defined(ASIO_HAS_VARIABLE_TEMPLATES)

#if defined(ASIO_HAS_CONCEPTS)

template <typename T>
ASIO_CONCEPT operation_state = is_operation_state<T>::value;

#define ASIO_EXECUTION_OPERATION_STATE \
  ::asio::execution::operation_state

#else // defined(ASIO_HAS_CONCEPTS)

#define ASIO_EXECUTION_OPERATION_STATE typename

#endif // defined(ASIO_HAS_CONCEPTS)

} // namespace execution
} // namespace asio

#include "asio/detail/pop_options.hpp"

#endif // !defined(ASIO_NO_DEPRECATED)

#endif // ASIO_EXECUTION_OPERATION_STATE_HPP
