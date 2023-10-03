import ctypes
import subprocess
from ctypes.util import find_library
from enum import IntEnum


lib_name = find_library('opensdg')

if not lib_name:
    raise Exception('opensdg library not found')

opensdg = ctypes.CDLL(lib_name)

SDG_MAX_PROTOCOL_BYTES = 40
SDG_MAX_OTP_BYTES = 32
SDG_MIN_OTP_LENGTH = 7

osdg_key_t = ctypes.c_ubyte * 32

class CtypesEnum(IntEnum):
    """A ctypes-compatible IntEnum superclass."""
    @classmethod
    def from_param(cls, obj):
        return int(obj)


class osdg_result_t(CtypesEnum):
    osdg_no_error = 0
    osdg_socket_error = 1
    osdg_crypto_core_error = 2
    osdg_decryption_error = 3
    osdg_protocol_error = 4
    osdg_buffer_exceeded = 5
    osdg_invalid_parameters = 6
    osdg_connection_failed = 7
    osdg_memory_error = 8
    osdg_connection_refused = 9
    osdg_too_many_connections = 10
    osdg_connection_closed = 11
    osdg_wrong_state = 12
    osdg_system_error = 13
    osdg_server_error = 14
    osdg_peer_timeout = 15

osdg_create_private_key = opensdg.osdg_create_private_key
osdg_create_private_key.argtypes = [osdg_key_t]
osdg_create_private_key.restype = None

osdg_calc_public_key = opensdg.osdg_calc_public_key
osdg_calc_public_key.argtypes = [osdg_key_t, osdg_key_t]
osdg_calc_public_key.restype = None

osdg_connection_t = ctypes.c_void_p

osdg_set_private_key = opensdg.osdg_set_private_key
osdg_set_private_key.argtypes = [osdg_connection_t, osdg_key_t]
osdg_set_private_key.restype = None

osdg_get_my_peer_id = opensdg.osdg_get_my_peer_id
osdg_get_my_peer_id.argtypes = [osdg_connection_t]
osdg_get_my_peer_id.restype = ctypes.POINTER(ctypes.c_ubyte)

class osdg_endpoint(ctypes.Structure):
    _fields_ = [("host", ctypes.c_char_p), ("port", ctypes.c_uint)]

osdg_connection_create = opensdg.osdg_connection_create
osdg_connection_create.argtypes = []
osdg_connection_create.restype = osdg_connection_t

osdg_connection_destroy = opensdg.osdg_connection_destroy
osdg_connection_destroy.argtypes = [osdg_connection_t]
osdg_connection_destroy.restype = None

osdg_set_user_data = opensdg.osdg_set_user_data
osdg_set_user_data.argtypes = [osdg_connection_t, ctypes.c_void_p]
osdg_set_user_data.restype = None

osdg_get_user_data = opensdg.osdg_get_user_data
osdg_get_user_data.argtypes = [osdg_connection_t]
osdg_get_user_data.restype = ctypes.c_void_p

osdg_connect_to_danfoss = opensdg.osdg_connect_to_danfoss
osdg_connect_to_danfoss.argtypes = [osdg_connection_t]
osdg_connect_to_danfoss.restype = osdg_result_t

osdg_connect_to_grid = opensdg.osdg_connect_to_grid
osdg_connect_to_grid.argtypes = [osdg_connection_t, ctypes.POINTER(osdg_endpoint), ctypes.c_uint]
osdg_connect_to_grid.restype = osdg_result_t

osdg_connect_to_remote = opensdg.osdg_connect_to_remote
osdg_connect_to_remote.argtypes = [osdg_connection_t, osdg_connection_t, osdg_key_t, ctypes.c_char_p]
osdg_connect_to_remote.restype = osdg_result_t

osdg_pair_remote = opensdg.osdg_pair_remote
osdg_pair_remote.argtypes = [osdg_connection_t, osdg_connection_t, ctypes.c_char_p]
osdg_pair_remote.restype = osdg_result_t

osdg_connection_close = opensdg.osdg_connection_close
osdg_connection_close.argtypes = [osdg_connection_t]
osdg_connection_close.restype = osdg_result_t

osdg_send_data = opensdg.osdg_send_data
osdg_send_data.argtypes = [osdg_connection_t, ctypes.c_void_p, ctypes.c_int]
osdg_send_data.restype = osdg_result_t

osdg_connection_state = ctypes.c_int
osdg_closed = 0
osdg_connecting = 1
osdg_connected = 2
osdg_error = 3
osdg_pairing_complete = 4

osdg_set_blocking_mode = opensdg.osdg_set_blocking_mode
osdg_set_blocking_mode.argtypes = [osdg_connection_t, ctypes.c_int]
osdg_set_blocking_mode.restype = None

osdg_get_blocking_mode = opensdg.osdg_get_blocking_mode
osdg_get_blocking_mode.argtypes = [osdg_connection_t]
osdg_get_blocking_mode.restype = ctypes.c_int

osdg_get_connection_state = opensdg.osdg_get_connection_state
osdg_get_connection_state.argtypes = [osdg_connection_t]
osdg_get_connection_state.restype = osdg_connection_state

osdg_state_cb_t = ctypes.CFUNCTYPE(None, osdg_connection_t, osdg_connection_state)
osdg_receive_cb_t = ctypes.CFUNCTYPE(ctypes.c_byte, osdg_connection_t, ctypes.c_void_p, ctypes.c_uint)

osdg_set_state_change_callback = opensdg.osdg_set_state_change_callback
osdg_set_state_change_callback.argtypes = [osdg_connection_t, osdg_state_cb_t]
osdg_set_state_change_callback.restype = osdg_result_t

osdg_set_receive_data_callback = opensdg.osdg_set_receive_data_callback
osdg_set_receive_data_callback.argtypes = [osdg_connection_t, osdg_receive_cb_t]
osdg_set_receive_data_callback.restype = osdg_result_t

osdg_get_last_result = opensdg.osdg_get_last_result
osdg_get_last_result.argtypes = [osdg_connection_t]
osdg_get_last_result.restype = osdg_result_t

osdg_get_last_errno = opensdg.osdg_get_last_errno
osdg_get_last_errno.argtypes = [osdg_connection_t]
osdg_get_last_errno.restype = ctypes.c_int

osdg_get_peer_id = opensdg.osdg_get_peer_id
osdg_get_peer_id.argtypes = [osdg_connection_t]
osdg_get_peer_id.restype = ctypes.POINTER(ctypes.c_ubyte)

osdg_set_ping_interval = opensdg.osdg_set_ping_interval
osdg_set_ping_interval.argtypes = [osdg_connection_t, ctypes.c_uint]
osdg_set_ping_interval.restype = osdg_result_t

osdg_init = opensdg.osdg_init
osdg_init.argtypes = []
osdg_init.restype = osdg_result_t

osdg_shutdown = opensdg.osdg_shutdown
osdg_shutdown.argtypes = []
osdg_shutdown.restype = None

osdg_set_log_mask = opensdg.osdg_set_log_mask
osdg_set_log_mask.argtypes = [ctypes.c_uint]
osdg_set_log_mask.restype = None

class osdg_main_loop_callbacks(ctypes.Structure):
    _fields_ = [("mainloop_start", ctypes.CFUNCTYPE(None)), ("mainloop_stop", ctypes.CFUNCTYPE(None))]

osdg_set_mainloop_callbacks = opensdg.osdg_set_mainloop_callbacks
osdg_set_mainloop_callbacks.argtypes = [ctypes.POINTER(osdg_main_loop_callbacks)]
osdg_set_mainloop_callbacks.restype = None

osdg_bin_to_hex = opensdg.osdg_bin_to_hex
osdg_bin_to_hex.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_ubyte * SDG_MAX_PROTOCOL_BYTES, ctypes.c_size_t]
osdg_bin_to_hex.restype = None

osdg_hex_to_bin = opensdg.osdg_hex_to_bin
osdg_hex_to_bin.argtypes = [ctypes.c_ubyte * SDG_MAX_PROTOCOL_BYTES, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_size_t,
    ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_char_p)]
osdg_hex_to_bin.restype = ctypes.c_int

osdg_get_last_result_str = opensdg.osdg_get_last_result_str
osdg_get_last_result_str.argtypes = [osdg_connection_t, ctypes.c_char_p, ctypes.c_size_t]
osdg_get_last_result_str.restype = ctypes.c_size_t

osdg_get_result_str = opensdg.osdg_get_result_str
osdg_get_result_str.argtypes = [osdg_result_t]
osdg_get_result_str.restype = ctypes.c_char_p

class osdg_version(ctypes.Structure):
    _fields_ = [("major", ctypes.c_uint), ("minor", ctypes.c_uint), ("patch", ctypes.c_uint)]

osdg_get_version = opensdg.osdg_get_version
osdg_get_version.argtypes = [ctypes.POINTER(osdg_version)]
osdg_get_version.restype = None
