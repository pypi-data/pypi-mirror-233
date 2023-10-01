import asyncio
import concurrent.futures
import logging

from ._asyncio_worker import AsyncioWorker
from .server import _CustomSock
from .server import _FAST_TIMEOUT
from .server import _KEEPALIVE_TIMEOUT
from .server import _NEGOTIATION_SOURCE
from .server import _NEGOTIATION_TIMEOUT
from .server import _OPS_TIMEOUT
from .server import _QUEUE_SIZE
from .server import DATASERV_PORT
from .streaming._pickle import _squash_pickle_diff_queue
from .streaming._pickle import serialize_pickle_diff
from .streaming._pickle import streaming_pickle_diff

_logger = logging.getLogger(__name__)


class DataSource(AsyncioWorker):
    """For sourcing data to the :py:class:`~nspyre.data.server.DataServer`.
    See :py:meth:`~nspyre.data.sink.DataSink.pop` for typical usage example."""

    def __init__(
        self,
        name: str,
        addr: str = 'localhost',
        port: int = DATASERV_PORT,
        auto_reconnect: bool = False,
    ):
        """
        Args:
            name: Name of the data set.
            addr: Network address of the data server.
            port: Port of the data server.
            auto_reconnect: If True, automatically reconnect to the data
                server if it is disconnected. Otherwise raise an error if
                connection fails.
        """
        super().__init__()
        # name of the dataset
        self._name = name
        # IP address of the data server to connect to
        self._addr = addr
        # port of the data server to connect to
        self._port = port
        # whether the source should try to reconnect to the data server
        self._auto_reconnect = auto_reconnect

    def start(self):
        """Connect to the data server."""
        # do this just to generate docs
        super().start()

    def stop(self):
        """Disconnect from the data server."""
        # do this just to generate docs
        super().stop()

    async def _main(self):
        """asyncio main loop"""
        try:
            # asyncio queue for buffering pickles to send to the server
            self._queue = asyncio.Queue(maxsize=_QUEUE_SIZE)
            while True:
                try:
                    # connect to the data server
                    sock_reader, sock_writer = await asyncio.wait_for(
                        asyncio.open_connection(self._addr, self._port),
                        timeout=_NEGOTIATION_TIMEOUT,
                    )
                except OSError as err:
                    _logger.warning(
                        'Source failed connecting to data server '
                        f'[{(self._addr, self._port)}].'
                    )
                    await asyncio.sleep(_FAST_TIMEOUT)
                    if self._auto_reconnect:
                        continue
                    else:
                        raise ConnectionError(
                            'Failed connecting to data server '
                            f'[{(self._addr, self._port)}].'
                        ) from err

                sock = _CustomSock(sock_reader, sock_writer)
                _logger.info(f'Source connected to data server [{sock.addr}].')

                try:
                    # notify the server that this is a data source client
                    await asyncio.wait_for(
                        sock.send_msg(_NEGOTIATION_SOURCE),
                        timeout=_NEGOTIATION_TIMEOUT,
                    )
                    # send the dataset name
                    await asyncio.wait_for(
                        sock.send_msg(self._name.encode()),
                        timeout=_NEGOTIATION_TIMEOUT,
                    )
                except (ConnectionError, asyncio.TimeoutError) as err:
                    _logger.warning(
                        'Source failed negotiation process with data server '
                        f'[{sock.addr}] - attempting reconnect.'
                    )
                    try:
                        await sock.close()
                    except IOError:
                        pass
                    await asyncio.sleep(_FAST_TIMEOUT)
                    if self._auto_reconnect:
                        continue
                    else:
                        raise ConnectionError(
                            'Failed connecting to data server '
                            f'[{(self._addr, self._port)}].'
                        ) from err

                _logger.debug(
                    f'Source finished negotiation with data server [{sock.addr}].'
                )

                # connection succeeded, so trigger the main thread to continue execution
                self._sem.release()

                while True:
                    try:
                        # get pickle data from the queue
                        pickle_diff = await asyncio.wait_for(
                            self._queue.get(), timeout=_KEEPALIVE_TIMEOUT
                        )
                        _logger.debug(
                            'Source dequeued pickle diff - sending to data server '
                            f'[{sock.addr}].'
                        )
                    except asyncio.TimeoutError:
                        # if there's no data available, send a keepalive message
                        new_data = b''
                        _logger.debug('Source sending keepalive to data server.')
                    else:
                        new_data = serialize_pickle_diff(pickle_diff)
                        _logger.debug(
                            f'Source sending pickle of [{len(new_data)}] bytes to data '
                            f'server [{sock.addr}].'
                        )

                    # send the data to the server
                    try:
                        await asyncio.wait_for(
                            sock.send_msg(new_data), timeout=_OPS_TIMEOUT
                        )
                        _logger.debug(
                            f'Source sent pickle of [{len(new_data)}] bytes to data '
                            f'server [{sock.addr}].'
                        )
                        if new_data:
                            # mark that the queue data has been fully processed
                            self._queue.task_done()
                    except (ConnectionError, asyncio.TimeoutError):
                        _logger.warning(
                            f'Source failed sending to data server [{sock.addr}] - '
                            'attempting reconnect.'
                        )
                        try:
                            await sock.close()
                        except IOError:
                            pass
                        break
        except ConnectionError as err:
            self._exc = err
            # release the main thread if there's a connection error
            self._sem.release()
        except asyncio.CancelledError as exc:
            _logger.debug(
                f'Source stopped - closing connection with data server [{sock.addr}].'
            )
            try:
                await sock.close()
            except (IOError, NameError):
                # socket is broken or hasn't been created yet
                pass
            raise asyncio.CancelledError from exc

    async def _push(self, pickle_diff):
        """Coroutine that puts a pickle onto the queue.
        Args:
            pickle_diff: PickleDiff returned by
                :py:meth:`~nspyre.data._streaming_pickle.streaming_pickle_diff`.

        Returns:
            True if successful, False otherwise
        """
        try:
            self._queue.put_nowait(pickle_diff)
        except asyncio.QueueFull as err:
            # the server isn't accepting data fast enough
            # so we will empty the queue and merge all of its entries
            _logger.debug(
                f'Data server [{(self._addr, self._port)}] can\'t keep up with source.'
            )
            if not _squash_pickle_diff_queue(self._queue, pickle_diff):
                raise RuntimeError(
                    'Maximum diff size exceeded. This is a consequence of memory '
                    'build-up due to the data server not being able to keep up with '
                    'the data rate. Reduce the data rate to allow the data server to '
                    'catch up.'
                ) from err
        except asyncio.CancelledError:
            _logger.debug('Source push cancelled.')
            raise
        else:
            _logger.debug('Source queued pickle.')

    def push(self, data):
        """Push new data to the data server.

        Args:
            data: Any python object (must be pickleable) to send. Ideally, \
                this should be a dictionary to allow for simple attribute access \
                from the sink side like :code:`sink.my_var`.
        """
        # pickle the data and generate diffs
        pickle_diff = streaming_pickle_diff(data)
        # put it on the queue
        future = asyncio.run_coroutine_threadsafe(
            self._push(pickle_diff), self._event_loop
        )
        # wait for the coroutine to return
        try:
            future.result()
        except concurrent.futures.TimeoutError:
            _logger.error(
                '_push timed out (this shouldn\'t happen since timeout is handled by '
                '_push itself).'
            )
            future.cancel()
        except concurrent.futures.CancelledError:
            logging.debug('_push was cancelled.')
        self._check_exc()

    def __str__(self):
        return f'Data Source (running={self.is_running()}) [name={self._name}, '
        f'ip={self._addr}, port={self._port}, auto_reconnect={self._auto_reconnect}]'
