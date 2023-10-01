//
// experimental/detail/channel_operation.hpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2023 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#ifndef ASIO_EXPERIMENTAL_DETAIL_CHANNEL_OPERATION_HPP
#define ASIO_EXPERIMENTAL_DETAIL_CHANNEL_OPERATION_HPP

#if defined(_MSC_VER) && (_MSC_VER >= 1200)
# pragma once
#endif // defined(_MSC_VER) && (_MSC_VER >= 1200)

#include "asio/detail/config.hpp"
#include "asio/associated_allocator.hpp"
#include "asio/associated_executor.hpp"
#include "asio/associated_immediate_executor.hpp"
#include "asio/detail/initiate_post.hpp"
#include "asio/detail/initiate_dispatch.hpp"
#include "asio/detail/op_queue.hpp"
#include "asio/detail/type_traits.hpp"
#include "asio/execution/executor.hpp"
#include "asio/execution/outstanding_work.hpp"
#include "asio/executor_work_guard.hpp"
#include "asio/prefer.hpp"

#include "asio/detail/push_options.hpp"

namespace asio {
namespace experimental {
namespace detail {

// Base class for all channel operations. A function pointer is used instead of
// virtual functions to avoid the associated overhead.
class channel_operation ASIO_INHERIT_TRACKED_HANDLER
{
public:
  template <typename Executor, typename = void>
  class handler_work_base;

  template <typename Handler, typename IoExecutor, typename = void>
  class handler_work;

  void destroy()
  {
    func_(this, destroy_op, 0);
  }

protected:
  enum action
  {
    destroy_op = 0,
    immediate_op = 1,
    complete_op = 2,
    cancel_op = 3,
    close_op = 4
  };

  typedef void (*func_type)(channel_operation*, action, void*);

  channel_operation(func_type func)
    : next_(0),
      func_(func),
      cancellation_key_(0)
  {
  }

  // Prevents deletion through this type.
  ~channel_operation()
  {
  }

  friend class asio::detail::op_queue_access;
  channel_operation* next_;
  func_type func_;

public:
  // The operation key used for targeted cancellation.
  void* cancellation_key_;
};

template <typename Executor, typename>
class channel_operation::handler_work_base
{
public:
  typedef typename decay<
      typename prefer_result<Executor,
        execution::outstanding_work_t::tracked_t
      >::type
    >::type executor_type;

  handler_work_base(int, const Executor& ex)
    : executor_(asio::prefer(ex, execution::outstanding_work.tracked))
  {
  }

  const executor_type& get_executor() const ASIO_NOEXCEPT
  {
    return executor_;
  }

  template <typename Function, typename Handler>
  void post(Function& function, Handler& handler)
  {
    typename associated_allocator<Handler>::type allocator =
      (get_associated_allocator)(handler);

#if defined(ASIO_NO_DEPRECATED)
    asio::prefer(
        asio::require(executor_, execution::blocking.never),
        execution::allocator(allocator)
      ).execute(ASIO_MOVE_CAST(Function)(function));
#else // defined(ASIO_NO_DEPRECATED)
    execution::execute(
        asio::prefer(
          asio::require(executor_, execution::blocking.never),
          execution::allocator(allocator)),
        ASIO_MOVE_CAST(Function)(function));
#endif // defined(ASIO_NO_DEPRECATED)
  }

private:
  executor_type executor_;
};

#if !defined(ASIO_NO_TS_EXECUTORS)

template <typename Executor>
class channel_operation::handler_work_base<Executor,
    typename enable_if<
      !execution::is_executor<Executor>::value
    >::type>
{
public:
  typedef Executor executor_type;

  handler_work_base(int, const Executor& ex)
    : work_(ex)
  {
  }

  executor_type get_executor() const ASIO_NOEXCEPT
  {
    return work_.get_executor();
  }

  template <typename Function, typename Handler>
  void post(Function& function, Handler& handler)
  {
    typename associated_allocator<Handler>::type allocator =
      (get_associated_allocator)(handler);

    work_.get_executor().post(
        ASIO_MOVE_CAST(Function)(function), allocator);
  }

private:
  executor_work_guard<Executor> work_;
};

#endif // !defined(ASIO_NO_TS_EXECUTORS)

template <typename Handler, typename IoExecutor, typename>
class channel_operation::handler_work :
  channel_operation::handler_work_base<IoExecutor>,
  channel_operation::handler_work_base<
      typename associated_executor<Handler, IoExecutor>::type, IoExecutor>
{
public:
  typedef channel_operation::handler_work_base<IoExecutor> base1_type;

  typedef channel_operation::handler_work_base<
      typename associated_executor<Handler, IoExecutor>::type, IoExecutor>
    base2_type;

  handler_work(Handler& handler, const IoExecutor& io_ex) ASIO_NOEXCEPT
    : base1_type(0, io_ex),
      base2_type(0, (get_associated_executor)(handler, io_ex))
  {
  }

  template <typename Function>
  void complete(Function& function, Handler& handler)
  {
    base2_type::post(function, handler);
  }

  template <typename Function>
  void immediate(Function& function, Handler& handler, ...)
  {
    typedef typename associated_immediate_executor<Handler,
      typename base1_type::executor_type>::type immediate_ex_type;

    immediate_ex_type immediate_ex = (get_associated_immediate_executor)(
        handler, base1_type::get_executor());

    (asio::detail::initiate_dispatch_with_executor<immediate_ex_type>(
          immediate_ex))(ASIO_MOVE_CAST(Function)(function));
  }

  template <typename Function>
  void immediate(Function& function, Handler&,
      typename enable_if<
        is_same<
          typename associated_immediate_executor<
            typename conditional<false, Function, Handler>::type,
            typename base1_type::executor_type>::
              asio_associated_immediate_executor_is_unspecialised,
          void
        >::value
      >::type*)
  {
    (asio::detail::initiate_post_with_executor<
        typename base1_type::executor_type>(
          base1_type::get_executor()))(
        ASIO_MOVE_CAST(Function)(function));
  }
};

template <typename Handler, typename IoExecutor>
class channel_operation::handler_work<
    Handler, IoExecutor,
    typename enable_if<
      is_same<
        typename associated_executor<Handler,
          IoExecutor>::asio_associated_executor_is_unspecialised,
        void
      >::value
    >::type> : handler_work_base<IoExecutor>
{
public:
  typedef channel_operation::handler_work_base<IoExecutor> base1_type;

  handler_work(Handler&, const IoExecutor& io_ex) ASIO_NOEXCEPT
    : base1_type(0, io_ex)
  {
  }

  template <typename Function>
  void complete(Function& function, Handler& handler)
  {
    base1_type::post(function, handler);
  }

  template <typename Function>
  void immediate(Function& function, Handler& handler, ...)
  {
    typedef typename associated_immediate_executor<Handler,
      typename base1_type::executor_type>::type immediate_ex_type;

    immediate_ex_type immediate_ex = (get_associated_immediate_executor)(
        handler, base1_type::get_executor());

    (asio::detail::initiate_dispatch_with_executor<immediate_ex_type>(
          immediate_ex))(ASIO_MOVE_CAST(Function)(function));
  }

  template <typename Function>
  void immediate(Function& function, Handler& handler,
      typename enable_if<
        is_same<
          typename associated_immediate_executor<
            typename conditional<false, Function, Handler>::type,
            typename base1_type::executor_type>::
              asio_associated_immediate_executor_is_unspecialised,
          void
        >::value
      >::type*)
  {
    base1_type::post(function, handler);
  }
};

} // namespace detail
} // namespace experimental
} // namespace asio

#include "asio/detail/pop_options.hpp"

#endif // ASIO_EXPERIMENTAL_DETAIL_CHANNEL_OPERATION_HPP
