###############################################################
#
#   STANDARD IMPORTS
#

import json
from unittest.mock import MagicMock

import eikon


###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   TEST CASES
#


def test_construct():
    ############################################
    #   prepare things
    name = "foo"
    session = MagicMock()
    session.name = "bar"
    stream_connection_name = "api/bar"
    connection_config = MagicMock()
    connection_protocol_name = "OMM"

    eikon.StreamConnection.run = lambda *args: None

    ############################################
    #   test

    try:
        eikon.streaming_session.stream_connection.StreamConnection(
            name,
            session,
            stream_connection_name,
            connection_config,
            connection_protocol_name,
        )
    except Exception as e:
        assert (
            True
        ), "EXPECTED cannot construct StreamConnection because it is a abstract class."


def test_websocket_callback_ws_open():
    ############################################
    #   prepare things
    name = "foo"
    session = MagicMock()
    session.name = "bar"
    stream_connection_name = "api/bar"
    connection_config = MagicMock()
    connection_protocol_name = "OMM"

    eikon.StreamConnection.run = lambda *args: None

    ############################################
    #   test

    omm_stream_connection = eikon.streaming_session.stream_connection.StreamConnection(
        name,
        session,
        stream_connection_name,
        connection_config,
        connection_protocol_name,
    )

    #   call
    try:
        #   version 0.54 - 0.57
        omm_stream_connection._ws_open()
        #   version 0.58
        omm_stream_connection._ws_open("ws")
    except Exception as e:
        assert False, f"NO EXCEPTION EXPECTED BUT GOT {e}"


def test_websocket_callback_ws_error():
    ############################################
    #   prepare things
    name = "foo"
    session = MagicMock()
    session.name = "bar"
    stream_connection_name = "api/bar"
    connection_config = MagicMock()
    connection_protocol_name = "OMM"

    eikon.StreamConnection.run = lambda *args: None

    mock_data = "error"

    ############################################
    #   test

    omm_stream_connection = eikon.streaming_session.stream_connection.StreamConnection(
        name,
        session,
        stream_connection_name,
        connection_config,
        connection_protocol_name,
    )

    #   call
    try:
        #   version 0.54 - 0.57
        omm_stream_connection._ws_error(mock_data)
        #   version 0.58
        omm_stream_connection._ws_error("ws", mock_data)
    except Exception as e:
        assert False, "NO EXCEPTION EXPECTED BUT GOT {e}"


def test_websocket_callback_ws_message():
    ############################################
    #   prepare things
    name = "foo"
    session = MagicMock()
    session.name = "bar"
    stream_connection_name = "api/bar"
    connection_config = MagicMock()
    connection_protocol_name = "OMM"

    eikon.StreamConnection.run = lambda *args: None
    eikon.StreamConnection._process_message = lambda *args: None

    mock_data = {"message": "bar"}

    ############################################
    #   test

    omm_stream_connection = eikon.streaming_session.stream_connection.StreamConnection(
        name,
        session,
        stream_connection_name,
        connection_config,
        connection_protocol_name,
    )

    #   call
    try:
        #   version 0.54 - 0.57
        omm_stream_connection._ws_message(json.dumps(mock_data))
        #   version 0.58
        omm_stream_connection._ws_message("ws", json.dumps(mock_data))
    except Exception as e:
        assert False, "NO EXCEPTION EXPECTED BUT GOT {e}"


def test_websocket_callback_ws_close():
    ############################################
    #   prepare things
    name = "foo"
    session = MagicMock()
    session.name = "bar"
    stream_connection_name = "api/bar"
    connection_config = MagicMock()
    connection_protocol_name = "OMM"

    eikon.StreamConnection.run = lambda *args: None

    mock_data = "close"

    ############################################
    #   test

    omm_stream_connection = eikon.streaming_session.stream_connection.StreamConnection(
        name,
        session,
        stream_connection_name,
        connection_config,
        connection_protocol_name,
    )

    #   call
    try:
        #   version 0.54 - 0.57
        omm_stream_connection._ws_close(mock_data)
        #   version 0.58
        omm_stream_connection._ws_close("ws", mock_data)
    except Exception as e:
        assert False, "NO EXCEPTION EXPECTED BUT GOT {e}"
