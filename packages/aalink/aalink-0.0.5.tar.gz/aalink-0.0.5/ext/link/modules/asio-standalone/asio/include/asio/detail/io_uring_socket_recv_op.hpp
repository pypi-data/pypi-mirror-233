//
// detail/io_uring_socket_recv_op.hpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2023 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#ifndef ASIO_DETAIL_IO_URING_SOCKET_RECV_OP_HPP
#define ASIO_DETAIL_IO_URING_SOCKET_RECV_OP_HPP

#if defined(_MSC_VER) && (_MSC_VER >= 1200)
# pragma once
#endif // defined(_MSC_VER) && (_MSC_VER >= 1200)

#include "asio/detail/config.hpp"

#if defined(ASIO_HAS_IO_URING)

#include "asio/detail/bind_handler.hpp"
#include "asio/detail/buffer_sequence_adapter.hpp"
#include "asio/detail/socket_ops.hpp"
#include "asio/detail/fenced_block.hpp"
#include "asio/detail/handler_work.hpp"
#include "asio/detail/io_uring_operation.hpp"
#include "asio/detail/memory.hpp"

#include "asio/detail/push_options.hpp"

namespace asio {
namespace detail {

template <typename MutableBufferSequence>
class io_uring_socket_recv_op_base : public io_uring_operation
{
public:
  io_uring_socket_recv_op_base(const asio::error_code& success_ec,
      socket_type socket, socket_ops::state_type state,
      const MutableBufferSequence& buffers,
      socket_base::message_flags flags, func_type complete_func)
    : io_uring_operation(success_ec,
        &io_uring_socket_recv_op_base::do_prepare,
        &io_uring_socket_recv_op_base::do_perform, complete_func),
      socket_(socket),
      state_(state),
      buffers_(buffers),
      flags_(flags),
      bufs_(buffers),
      msghdr_()
  {
    msghdr_.msg_iov = bufs_.buffers();
    msghdr_.msg_iovlen = static_cast<int>(bufs_.count());
  }

  static void do_prepare(io_uring_operation* base, ::io_uring_sqe* sqe)
  {
    ASIO_ASSUME(base != 0);
    io_uring_socket_recv_op_base* o(
        static_cast<io_uring_socket_recv_op_base*>(base));

    if ((o->state_ & socket_ops::internal_non_blocking) != 0)
    {
      bool except_op = (o->flags_ & socket_base::message_out_of_band) != 0;
      ::io_uring_prep_poll_add(sqe, o->socket_, except_op ? POLLPRI : POLLIN);
    }
    else if (o->bufs_.is_single_buffer
        && o->bufs_.is_registered_buffer && o->flags_ == 0)
    {
      ::io_uring_prep_read_fixed(sqe, o->socket_,
          o->bufs_.buffers()->iov_base, o->bufs_.buffers()->iov_len,
          0, o->bufs_.registered_id().native_handle());
    }
    else
    {
      ::io_uring_prep_recvmsg(sqe, o->socket_, &o->msghdr_, o->flags_);
    }
  }

  static bool do_perform(io_uring_operation* base, bool after_completion)
  {
    ASIO_ASSUME(base != 0);
    io_uring_socket_recv_op_base* o(
        static_cast<io_uring_socket_recv_op_base*>(base));

    if ((o->state_ & socket_ops::internal_non_blocking) != 0)
    {
      bool except_op = (o->flags_ & socket_base::message_out_of_band) != 0;
      if (after_completion || !except_op)
      {
        if (o->bufs_.is_single_buffer)
        {
          return socket_ops::non_blocking_recv1(o->socket_,
              o->bufs_.first(o->buffers_).data(),
              o->bufs_.first(o->buffers_).size(), o->flags_,
              (o->state_ & socket_ops::stream_oriented) != 0,
              o->ec_, o->bytes_transferred_);
        }
        else
        {
          return socket_ops::non_blocking_recv(o->socket_,
              o->bufs_.buffers(), o->bufs_.count(), o->flags_,
              (o->state_ & socket_ops::stream_oriented) != 0,
              o->ec_, o->bytes_transferred_);
        }
      }
    }
    else if (after_completion)
    {
      if (!o->ec_ && o->bytes_transferred_ == 0)
        if ((o->state_ & socket_ops::stream_oriented) != 0)
          o->ec_ = asio::error::eof;
    }

    if (o->ec_ && o->ec_ == asio::error::would_block)
    {
      o->state_ |= socket_ops::internal_non_blocking;
      return false;
    }

    return after_completion;
  }

private:
  socket_type socket_;
  socket_ops::state_type state_;
  MutableBufferSequence buffers_;
  socket_base::message_flags flags_;
  buffer_sequence_adapter<asio::mutable_buffer,
      MutableBufferSequence> bufs_;
  msghdr msghdr_;
};

template <typename MutableBufferSequence, typename Handler, typename IoExecutor>
class io_uring_socket_recv_op
  : public io_uring_socket_recv_op_base<MutableBufferSequence>
{
public:
  ASIO_DEFINE_HANDLER_PTR(io_uring_socket_recv_op);

  io_uring_socket_recv_op(const asio::error_code& success_ec,
      int socket, socket_ops::state_type state,
      const MutableBufferSequence& buffers, socket_base::message_flags flags,
      Handler& handler, const IoExecutor& io_ex)
    : io_uring_socket_recv_op_base<MutableBufferSequence>(success_ec,
        socket, state, buffers, flags, &io_uring_socket_recv_op::do_complete),
      handler_(ASIO_MOVE_CAST(Handler)(handler)),
      work_(handler_, io_ex)
  {
  }

  static void do_complete(void* owner, operation* base,
      const asio::error_code& /*ec*/,
      std::size_t /*bytes_transferred*/)
  {
    // Take ownership of the handler object.
    ASIO_ASSUME(base != 0);
    io_uring_socket_recv_op* o
      (static_cast<io_uring_socket_recv_op*>(base));
    ptr p = { asio::detail::addressof(o->handler_), o, o };

    ASIO_HANDLER_COMPLETION((*o));

    // Take ownership of the operation's outstanding work.
    handler_work<Handler, IoExecutor> w(
        ASIO_MOVE_CAST2(handler_work<Handler, IoExecutor>)(
          o->work_));

    ASIO_ERROR_LOCATION(o->ec_);

    // Make a copy of the handler so that the memory can be deallocated before
    // the upcall is made. Even if we're not about to make an upcall, a
    // sub-object of the handler may be the true owner of the memory associated
    // with the handler. Consequently, a local copy of the handler is required
    // to ensure that any owning sub-object remains valid until after we have
    // deallocated the memory here.
    detail::binder2<Handler, asio::error_code, std::size_t>
      handler(o->handler_, o->ec_, o->bytes_transferred_);
    p.h = asio::detail::addressof(handler.handler_);
    p.reset();

    // Make the upcall if required.
    if (owner)
    {
      fenced_block b(fenced_block::half);
      ASIO_HANDLER_INVOCATION_BEGIN((handler.arg1_, handler.arg2_));
      w.complete(handler, handler.handler_);
      ASIO_HANDLER_INVOCATION_END;
    }
  }

private:
  Handler handler_;
  handler_work<Handler, IoExecutor> work_;
};

} // namespace detail
} // namespace asio

#include "asio/detail/pop_options.hpp"

#endif // defined(ASIO_HAS_IO_URING)

#endif // ASIO_DETAIL_IO_URING_SOCKET_RECV_OP_HPP
