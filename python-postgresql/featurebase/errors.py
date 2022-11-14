import grpc
from grpc import StatusCode


class MoleculaError(Exception):
    pass


class MoleculaGRPCError(MoleculaError):
    def __init__(self, grpcError):
        super(MoleculaGRPCError, self).__init__(grpcError.details())
        self.grpcError = grpcError
        self.code = grpcError.code()


class MoleculaErrorOK(MoleculaGRPCError):
    pass


class MoleculaErrorCancelled(MoleculaGRPCError):
    pass


class MoleculaErrorUnknown(MoleculaGRPCError):
    pass


class MoleculaErrorInvalidArgument(MoleculaGRPCError):
    pass


class MoleculaErrorDeadlineExceeded(MoleculaGRPCError):
    pass


class MoleculaErrorNotFound(MoleculaGRPCError):
    pass


class MoleculaErrorAlreadyExists(MoleculaGRPCError):
    pass


class MoleculaErrorPermissionDenied(MoleculaGRPCError):
    pass


class MoleculaErrorResourceExhausted(MoleculaGRPCError):
    pass


class MoleculaErrorFailedPrecondition(MoleculaGRPCError):
    pass


class MoleculaErrorAborted(MoleculaGRPCError):
    pass


class MoleculaErrorOutOfRange(MoleculaGRPCError):
    pass


class MoleculaErrorUnimplemented(MoleculaGRPCError):
    pass


class MoleculaErrorInternal(MoleculaGRPCError):
    pass


class MoleculaErrorUnavailable(MoleculaGRPCError):
    pass


class MoleculaErrorDataLoss(MoleculaGRPCError):
    pass


class MoleculaErrorUnauthenticated(MoleculaGRPCError):
    pass


def to_molecula_error(grpcError):
    code = grpcError.code()
    if code == StatusCode.OK:
        return MoleculaErrorOK(grpcError)
    elif code == StatusCode.CANCELLED:
        return MoleculaErrorCancelled(grpcError)
    elif code == StatusCode.UNKNOWN:
        return MoleculaErrorUnknown(grpcError)
    elif code == StatusCode.INVALID_ARGUMENT:
        return MoleculaErrorInvalidArgument(grpcError)
    elif code == StatusCode.DEADLINE_EXCEEDED:
        return MoleculaErrorDeadlineExceeded(grpcError)
    elif code == StatusCode.NOT_FOUND:
        return MoleculaErrorNotFound(grpcError)
    elif code == StatusCode.ALREADY_EXISTS:
        return MoleculaErrorAlreadyExists(grpcError)
    elif code == StatusCode.PERMISSION_DENIED:
        return MoleculaErrorPermissionDenied(grpcError)
    elif code == StatusCode.RESOURCE_EXHAUSTED:
        return MoleculaErrorResourceExhausted(grpcError)
    elif code == StatusCode.FAILED_PRECONDITION:
        return MoleculaErrorFailedPrecondition(grpcError)
    elif code == StatusCode.ABORTED:
        return MoleculaErrorAborted(grpcError)
    elif code == StatusCode.OUT_OF_RANGE:
        return MoleculaErrorOutOfRange(grpcError)
    elif code == StatusCode.UNIMPLEMENTED:
        return MoleculaErrorUnimplemented(grpcError)
    elif code == StatusCode.INTERNAL:
        return MoleculaErrorInternal(grpcError)
    elif code == StatusCode.UNAVAILABLE:
        return MoleculaErrorUnavailable(grpcError)
    elif code == StatusCode.DATA_LOSS:
        return MoleculaErrorDataLoss(grpcError)
    elif code == StatusCode.UNAUTHENTICATED:
        return MoleculaErrorUnauthenticated(grpcError)


class ErrorWrapper:
    def __init__(self, orig):
        self._orig = orig

    def __getattr__(self, attr):
        def wrap(func):
            def call(*args, **kwargs):
                try:
                    return ErrorWrapper(func(*args, **kwargs))
                except grpc.RpcError as e:
                    raise to_molecula_error(e)

            if hasattr(func, "future"):
                call.future = func.future
            return call

        attr = getattr(self._orig, attr)
        if callable(attr):
            return wrap(attr)
        return attr

    def __iter__(self):
        try:
            yield from self._orig
        except grpc.RpcError as e:
            raise to_molecula_error(e)
