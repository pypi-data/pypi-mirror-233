"""Tests server error handling and integration of Rpc Controller with Rpc Handler"""
import logging
import zmq
from pytest import fixture
from edgepirpc.protos import rpc_pb2 as rpc_pb, tc_pb2 as tc_pb

_logger = logging.getLogger(__name__)

# pylint: disable= no-member

@fixture(name="socket")
def fixture_test_socket():
    """Returns socket for each test"""
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.connect('tcp://localhost:5555')
    return sock

def test_bad_rpc_request_data(socket):
    """Tests error handling for data deserialization"""
    # send a bad message
    socket.send(b'BAD PROTO DATA!')
    response = socket.recv()
    # Deserialize rpc response
    response = rpc_pb.RpcResponse.FromString(response)

    assert response.error_code == rpc_pb.ErrorCode.BAD_MESSAGE_DATA

def test_incomplete_rpc_request(socket):
    """Tests error handling for a wrongful rpc request type"""
    # Set up wrongful request
    request = tc_pb.EmptyMsg()
    request = request.SerializeToString()
    # send request
    socket.send(request)
    # Get response
    response = socket.recv()
    response = rpc_pb.RpcResponse.FromString(response)

    assert response.error_code == rpc_pb.ErrorCode.INCOMPLETE_MESSAGE


def test_service_not_found(socket):
    """Test error handling for finding an rpc service"""
    # Create rpc call with bad service name
    request = rpc_pb.RpcRequest(
        service_name="bad service name",
        method_name="_",
        request_proto=b"_"
    )
    # Send
    request = request.SerializeToString()
    socket.send(request)
    # Get response
    response = socket.recv()
    response = rpc_pb.RpcResponse.FromString(response)

    assert response.error_code == rpc_pb.ErrorCode.SERVICE_NOT_FOUND

def test_method_not_found(socket):
    """Test error handling for finding an rpc service method"""
    # Create rpc call with bad method name
    request = rpc_pb.RpcRequest(
        service_name="TcService",
        method_name="bad method name",
        request_proto=b"_"
    )
    # Send
    request = request.SerializeToString()
    socket.send(request)
    # Get response
    response = socket.recv()
    response = rpc_pb.RpcResponse.FromString(response)

    assert response.error_code == rpc_pb.ErrorCode.METHOD_NOT_FOUND

def test_bad_request_proto_data(socket):
    """Test to handle the method input deserialization (request proto within rpc request)"""
    request = rpc_pb.RpcRequest(
        service_name = 'TcService',
        method_name = 'single_sample',
        request_proto = b'bad request proto data'
    )
    # Send
    request = request.SerializeToString()
    socket.send(request)
    # Get response
    response = socket.recv()
    response = rpc_pb.RpcResponse.FromString(response)

    assert response.error_code == rpc_pb.ErrorCode.BAD_MESSAGE_DATA

def test_incomplete_request_proto(socket):
    """Tests error handling for a wrongful method input (request proto within rpc request)"""
    wrong_request_proto = tc_pb.TempReading().SerializeToString()
    request = rpc_pb.RpcRequest(
        service_name = 'TcService',
        method_name = 'set_config',
        request_proto = wrong_request_proto
    )
    # Send
    request = request.SerializeToString()
    socket.send(request)
    # Get response
    response = socket.recv()
    response = rpc_pb.RpcResponse.FromString(response)

    assert response.error_code == rpc_pb.ErrorCode.INCOMPLETE_MESSAGE

def test_reset_error_state(socket):
    """Test that the state of a worker thread's error state is being reset"""

    # Send a bad message

    socket.send(b'BAD PROTO DATA!')
    response = socket.recv()
    # Deserialize rpc response
    response = rpc_pb.RpcResponse.FromString(response)
    _logger.debug("Bad request response: %s", response)
    assert response.error_code == rpc_pb.ErrorCode.BAD_MESSAGE_DATA

    # Send good messages and ensure that no error messages are being returned
    request_proto = tc_pb.EmptyMsg().SerializeToString()
    rpc_request = rpc_pb.RpcRequest(
        service_name = 'TcService',
        method_name = 'single_sample',
        request_proto = request_proto
    )
    request = rpc_request.SerializeToString()\
    # Hammer to hopefully make requests to all threads
    for i in range(10):
        socket.send(request)

        response = socket.recv()
        rpc_response = rpc_pb.RpcResponse.FromString(response)
        _logger.debug("Good request #%s response: %s", i, rpc_response)
        assert not rpc_response.HasField('error_code') and not rpc_response.HasField('error_msg')
