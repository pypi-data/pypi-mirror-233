# Copyright (C) 2007 Jan-Klaas Kollhof
# Copyright (C) 2011-2018 The python-bitcoinlib developers
# Copyright (C) 2022 James O'Beirne
#
# This file is part of python-bitcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.
import json
import logging
import typing as t
import re
import base64
import time
import platform
import urllib.parse as urlparse
import socket
import http.client
import os
import http.client as httplib

from decimal import Decimal


DEFAULT_USER_AGENT = "BitcoinRpc/0.1"
DEFAULT_HTTP_TIMEOUT = 30

rpc_logger = logging.getLogger("rpc")
rpc_logger.setLevel(logging.INFO)


class JSONRPCError(Exception):
    """JSON-RPC protocol error base class
    Subclasses of this class also exist for specific types of errors; the set
    of all subclasses is by no means complete.
    """

    def __init__(self, rpc_error):
        super(JSONRPCError, self).__init__(
            "msg: %r  code: %r" % (rpc_error["message"], rpc_error["code"])
        )
        self.error = rpc_error

    @property
    def code(self) -> int:
        return int(self.error["code"])

    @property
    def msg(self) -> str:
        return self.error["message"]


PORTS = {
    'mainnet': 8332,
    'testnet': 18332,
    'regtest': 18443,
    'signet': 38332,
}
PORT_TO_NET = {v: k for k, v in PORTS.items()}


class BitcoinRPC(object):
    """An RPC proxy class."""

    def __init__(
        self,
        service_url=None,
        service_port=None,
        btc_conf_file=None,
        net_name=None,
        timeout=DEFAULT_HTTP_TIMEOUT,
        wallet_name=None,
    ):
        authpair = None
        net_name = net_name or "mainnet"
        self.timeout = timeout
        self.net_name = net_name
        if self.net_name not in PORTS:
            raise ValueError(f"unrecognized network '{self.net_name}'")

        # Figure out the path to the bitcoin.conf file
        if btc_conf_file is None:
            if platform.system() == "Darwin":
                btc_conf_file = os.path.expanduser(
                    "~/Library/Application Support/Bitcoin/"
                )
            elif platform.system() == "Windows":
                btc_conf_file = os.path.join(os.environ["APPDATA"], "Bitcoin")
            else:
                btc_conf_file = os.path.expanduser("~/.bitcoin")
            btc_conf_file = os.path.join(btc_conf_file, "bitcoin.conf")

        if not service_url:
            # Bitcoin Core accepts empty rpcuser, not specified in btc_conf_file
            conf = self._get_bitcoind_conf_from_filesystem(btc_conf_file)
            service_port = service_port or PORTS[net_name]

            conf["rpcport"] = int(conf.get("rpcport", service_port))  # type: ignore
            conf["rpchost"] = conf.get("rpcconnect", "localhost")

            service_url = f"http://{conf['rpchost']}:{conf['rpcport']}"

            authpair = self._get_bitcoind_cookie_authpair(conf, btc_conf_file, net_name)
        else:
            url = urlparse.urlparse(service_url)
            authpair = "%s:%s" % (url.username or "", url.password or "")

            # Do our best to autodetect testnet.
            if url.port:
                self.net_name = net_name = PORT_TO_NET.get(url.port, 'mainnet')

            # Try and pull in auth information from the filesystem if it's missing.
            if authpair == ":":
                conf = self._get_bitcoind_conf_from_filesystem(btc_conf_file)
                authpair = self._get_bitcoind_cookie_authpair(
                    conf, btc_conf_file, net_name
                )
                rpc_logger.debug("pulling authpair from cookie despite intaking URL")

        if wallet_name:
            service_url = service_url.rstrip("/")
            service_url += f"/wallet/{wallet_name}"

        rpc_logger.info(f"Connecting to bitcoind: {service_url}")
        self.url = service_url

        # Credential redacted
        self.public_url = re.sub(r":[^/]+@", ":***@", self.url, 1)
        self._parsed_url = urlparse.urlparse(service_url)
        self.host = self._parsed_url.hostname

        rpc_logger.info(f"Initializing RPC client at {self.public_url}")
        # XXX keep for debugging, but don't ship:
        # logger.info(f"[REMOVE THIS] USING AUTHPAIR {authpair}")

        if self._parsed_url.scheme not in ("http",):
            raise ValueError("Unsupported URL scheme %r" % self._parsed_url.scheme)

        self.__id_count = 0

        self.__auth_header = None
        if authpair:
            self.__auth_header = b"Basic " + base64.b64encode(authpair.encode("utf8"))

    def _get_bitcoind_conf_from_filesystem(self, btc_conf_file: str) -> t.Dict:
        conf = {"rpcuser": ""}

        # Extract contents of bitcoin.conf to build service_url
        try:
            with open(btc_conf_file, "r") as fd:
                for line in fd.readlines():
                    if "#" in line:
                        line = line[: line.index("#")]
                    if "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    conf[k.strip()] = v.strip()

        # Treat a missing bitcoin.conf as though it were empty
        except FileNotFoundError:
            pass

        return conf

    def _get_bitcoind_cookie_authpair(
        self, conf: dict, btc_conf_file: str, net_name: str
    ) -> t.Optional[str]:
        """Get an authpair from the cookie or configuration files."""
        authpair = ""
        cookie_dir = conf.get("datadir", os.path.dirname(btc_conf_file))
        if net_name != "mainnet":
            cookie_dir = os.path.join(cookie_dir, net_name)
        cookie_file = os.path.join(cookie_dir, ".cookie")
        try:
            with open(cookie_file, "r") as fd:
                authpair = fd.read()
                rpc_logger.debug("read authpair from cookie")
        except (IOError, FileNotFoundError) as err:
            rpc_logger.debug("couldn't read authpair from cookie", exc_info=True)
            if "rpcpassword" in conf:
                authpair = "%s:%s" % (conf["rpcuser"], conf["rpcpassword"])
                rpc_logger.debug("read authpair from conf")
            else:
                raise ValueError(
                    "Cookie file unusable (%s) and rpcpassword not specified "
                    "in the configuration file: %r" % (err, btc_conf_file)
                )

        return authpair

    @property
    def port(self) -> int:
        if self._parsed_url.port is None:
            return httplib.HTTP_PORT
        else:
            return self._parsed_url.port

    def _getconn(self, timeout=None):
        assert self._parsed_url.hostname
        return httplib.HTTPConnection(
            self._parsed_url.hostname,
            port=self.port,
            timeout=timeout,
        )

    def _call(self, service_name, *args, **kwargs):
        self.__id_count += 1
        kwargs.setdefault("timeout", self.timeout)

        postdata = json.dumps(
            {
                "version": "1.1",
                "method": service_name,
                "params": args,
                "id": self.__id_count,
            }
        )

        rpc_logger.debug(f"[{self.public_url}] calling %s%s", service_name, args)

        headers = {
            "Host": self._parsed_url.hostname,
            "User-Agent": DEFAULT_USER_AGENT,
            "Content-type": "application/json",
        }

        if self.__auth_header is not None:
            headers["Authorization"] = self.__auth_header

        path = self._parsed_url.path
        tries = 5
        backoff = 0.3
        conn = None
        while tries:
            try:
                conn = self._getconn(timeout=kwargs["timeout"])
                conn.request("POST", path, postdata, headers)
            except (BlockingIOError, http.client.CannotSendRequest, socket.gaierror):
                rpc_logger.exception(
                    f"hit request error: {path}, {postdata}, {self._parsed_url}"
                )
                tries -= 1
                if not tries:
                    raise
                time.sleep(backoff)
                backoff *= 2
            else:
                break

        assert conn
        response = self._get_response(conn)
        err = response.get("error")
        if err is not None:
            if isinstance(err, dict):
                raise JSONRPCError(
                    {
                        "code": err.get("code", -345),
                        "message": err.get("message", "error message not specified"),
                    }
                )
            raise JSONRPCError({"code": -344, "message": str(err)})
        elif "result" not in response:
            raise JSONRPCError({"code": -343, "message": "missing JSON-RPC result"})
        else:
            return response["result"]

    def _get_response(self, conn):
        http_response = conn.getresponse()
        if http_response is None:
            raise JSONRPCError(
                {"code": -342, "message": "missing HTTP response from server"}
            )

        rdata = http_response.read().decode("utf8")
        try:
            loaded = json.loads(rdata, parse_float=Decimal)
            rpc_logger.debug(f"[{self.public_url}] -> {loaded}")
            return loaded
        except Exception:
            raise JSONRPCError(
                {
                    "code": -342,
                    "message": (
                        "non-JSON HTTP response with '%i %s' from server: '%.20s%s'"
                        % (
                            http_response.status,
                            http_response.reason,
                            rdata,
                            "..." if len(rdata) > 20 else "",
                        )
                    ),
                }
            )

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            # Prevent RPC calls for non-existing python internal attribute
            # access. If someone tries to get an internal attribute
            # of RawProxy instance, and the instance does not have this
            # attribute, we do not want the bogus RPC call to happen.
            raise AttributeError

        # Create a callable to do the actual call
        def _call_wrapper(*args, **kwargs):
            return self._call(name, *args, **kwargs)

        # Make debuggers show <function bitcoin.rpc.name> rather than <function
        # bitcoin.rpc.<lambda>>
        _call_wrapper.__name__ = name
        return _call_wrapper
