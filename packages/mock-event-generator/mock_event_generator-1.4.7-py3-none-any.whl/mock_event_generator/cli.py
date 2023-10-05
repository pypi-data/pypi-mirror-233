"""The command line interface for the package `mock_event_generator`."""
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import certifi
import trio
from astropy.time import Time
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from typer import Argument, Exit, Option, Typer, echo

from mock_event_generator.exceptions import (
    MEGInvalidGraceDBAliasOrURLError,
    MEGValidationFailed,
)

from .cache import (
    DEFAULT_CACHE_PATH,
    EventFileCache,
    GEventCacheEntry,
    SEventCacheEntry,
)
from .creators import GEventCreator, SEventCreator
from .gracedbs import GraceDBAlias, GraceDBWithContext
from .utils import is_any_event, is_gevent, is_superevent, tree
from .validators import SEventValidator

meg = Typer(help='Mock Event Generator.')
GRACEDB_ALIASES = ', '.join(alias.value for alias in GraceDBAlias)


@meg.command()
def create(
    events: list[str] = Argument(..., help='G-events or S-events to be generated.'),
    target: str = Option(
        ...,
        help=f'GraceDB instance ({GRACEDB_ALIASES} or <URL>) to which the time-'
        'translated events are sent.',
    ),
    # username: Optional[str] = Option(
    #     None, help='Username for basic authentication on the target GraceDB server.'
    # ),
    # password: Optional[str] = Option(
    #    None, help='Password for basic authentication on the target GraceDB server.'
    # ),
    source: str = Option(
        GraceDBAlias.PLAYGROUND,
        help=f'GraceDB instance ({GRACEDB_ALIASES} or <URL>) from which the original '
        'events are downloaded.',
    ),
    group: Optional[str] = Option(
        None,
        help='Change the analysis group which identified the candidate.',
    ),
    search: Optional[str] = Option(
        None,
        help='Change the type of search of the analysis pipeline. By default, '
        "the event search is changed to 'MDC'.",
    ),
    original_search: bool = Option(
        False, help='Use the original event search type, instead of MDC.'
    ),
    cache_path: Path = Option(
        DEFAULT_CACHE_PATH, help="Directory where the event' data files are downloaded."
    ),
    refresh_cache: bool = Option(
        False, help="If set, ignore the event's potential cache entry."
    ),
    max_delay: Optional[float] = Option(
        None,
        help='Shrink the interval between the first event creation and the last upload '
        '(in seconds). By setting zero, all uploads are sent at once.',
    ),
    time_shift: bool = Option(True, help='Use current time to create events.'),
) -> None:
    """Create G-events and send them to GraceDB."""
    if search is None and not original_search:
        search = 'MDC'

    _check_event_ids(events)
    if target == 'production':
        echo('Creation of production event is deprecated!')
        raise Exit(1)

    try:
        source_client = GraceDBWithContext.meg_from_alias_or_url(source)
        target_client = GraceDBWithContext.meg_from_alias_or_url(target)
        # try:
        #     target_client = GraceDBWithContext.meg_from_alias_or_url(
        #         target, username=username, password=password
        #     )
        # except MEGInvalidGraceDBAliasOrURLError as exc:
        #     echo(exc, err=True, color=True)
        #     echo('Username/password authetication not supported')
        #     target_client = GraceDBWithContext.meg_from_alias_or_url(target)
    except MEGInvalidGraceDBAliasOrURLError as exc:
        echo(exc, err=True, color=True)
        raise Exit(1)

    cache = EventFileCache(source_client, refresh_cache, cache_path)
    now = Time.now().gps
    if time_shift is False:
        now = 0.0

    async def create_all() -> None:
        async with trio.open_nursery() as nursery:
            for event in events:
                if is_superevent(event):
                    nursery.start_soon(
                        SEventCreator.from_id(event, target_client, cache).create,
                        group,
                        search,
                        max_delay,
                    )
                else:
                    nursery.start_soon(
                        GEventCreator.from_id(event, target_client, cache).create,
                        group,
                        search,
                        now,
                        0,
                    )

    trio.run(create_all)


@meg.command()
def fetch(
    events: list[str] = Argument(..., help='G-events or S-events to be generated.'),
    source: str = Option(
        GraceDBAlias.PLAYGROUND,
        help=f'GraceDB instance ({GRACEDB_ALIASES} or <URL>) from which the original '
        'events are downloaded.',
    ),
    cache_path: Path = Option(
        DEFAULT_CACHE_PATH, help="Directory where the event' data files are downloaded."
    ),
    refresh_cache: bool = Option(
        False, help="If set, ignore the event's potential cache entry."
    ),
) -> None:
    """Fetch G-events and store them in the cache."""
    _check_event_ids(events)
    try:
        source_client = GraceDBWithContext.meg_from_alias_or_url(source)
    except MEGInvalidGraceDBAliasOrURLError as exc:
        echo(exc, err=True, color=True)
        raise Exit(1)

    cache = EventFileCache(source_client, refresh_cache, cache_path)
    for event in events:
        if is_superevent(event):
            cache.get_sevent_cache_entry(event)
        else:
            cache.get_gevent_cache_entry(event)


cache = Typer()
meg.add_typer(cache, name='cache', help='Event cache utilities')


@cache.command()
def clean(
    cache_path: Path = Option(
        DEFAULT_CACHE_PATH, help="Directory where the event' data files are downloaded."
    ),
) -> None:
    """Remove the content of the cache."""
    if not cache_path.is_dir():
        echo(f'Cache path does not exist: {cache_path}', err=True)
        sys.exit(1)
    print(f'Cleaning cache: {cache_path}')
    for path in cache_path.iterdir():
        if path.is_dir() and is_any_event(path.name):
            print(f'Removing {path}')
            shutil.rmtree(path)


@cache.command('list')
def list_(
    include_files: bool = Option(False, help='If set, also display the data files.'),
    cache_path: Path = Option(
        DEFAULT_CACHE_PATH, help="Directory where the event' data files are downloaded."
    ),
) -> None:
    """List the content of the cache."""
    if not cache_path.is_dir():
        echo(f'Cache path does not exist: {cache_path}', err=True)
        sys.exit(1)
    if include_files:

        def criterion(path: Path) -> bool:
            return True

    else:

        def criterion(path: Path) -> bool:
            return path.is_dir()

    def sort_key(path: Path) -> float:
        """Sort key according to modification time (older first)."""
        return 0 if path.name == 'description.json' else path.stat().st_mtime

    print(f'Cache: {cache_path}')
    for path, line in tree(cache_path, criterion, key=sort_key):
        is_dir = path.is_dir()
        if is_dir and is_gevent(path.name):
            entry = GEventCacheEntry(path)
            description = entry.get_description()
            line = '{:20} {:12}{:12} {:12} ({:4.0f}) {:14.3f} FAR={:7.3g}'.format(
                line,
                description.pipeline,
                description.group,
                description.search,
                description.reporting_latency,
                description.gpstime,
                description.far,
            )
        elif is_dir and is_superevent(path.name):
            sentry = SEventCacheEntry(path)
            sdescription = sentry.get_description()
            line = '{:20} source: {:20}'.format(
                line,
                sdescription.source,
            )
        print(line)


@meg.command()
def ca_certificate(path: Path = Argument(..., help='The CA certificate path.')) -> None:
    """Add a Certification Authority certificate.

    The certificate is added to the CA bundle used by the requests library.
    """
    content = path.read_bytes()
    cert = x509.load_pem_x509_certificate(content, default_backend())
    if cert.not_valid_after < datetime.now():
        echo(f'The CA certificate {path.name} has expired.', err=True, color=True)
        raise Exit(1)

    original_content = Path(certifi.where())
    if content in original_content.read_bytes():
        echo(f'The CA certificate {path.name} has already been added.')
        raise Exit()

    with Path(certifi.where()).open('ba') as f:
        f.write(b'\n\n')
        f.write(content)
        f.write(b'\n')


@meg.command()
def validate(
    events: list[str] = Argument(..., help='G-events or S-events to be validated.'),
    source: str = Option(
        GraceDBAlias.PLAYGROUND,
        help=f'GraceDB instance ({GRACEDB_ALIASES} or <URL>) from which the original '
        'events are downloaded.',
    ),
    cache_path: Path = Option(
        DEFAULT_CACHE_PATH, help='Directory where the events data files are downloaded.'
    ),
    refresh_cache: bool = Option(
        False, help='If set, ignore the event potential cache entry.'
    ),
    save_plot_to: Path = Option(
        None, help='Where the latency plot and data will be saved.'
    ),
    loginfo: bool = Option(False, help='Log the collected info (for debug purpose).'),
) -> None:
    """Validate G-event or S-event."""
    _check_event_ids(events)
    try:
        source_client = GraceDBWithContext.meg_from_alias_or_url(source)
    except MEGInvalidGraceDBAliasOrURLError as exc:
        echo(exc, err=True, color=True)
        raise Exit(1)

    for event in events:
        if is_superevent(event):
            validator = SEventValidator.from_sevent_id(
                event, source_client, refresh_cache, cache_path
            )
        else:
            validator = SEventValidator.from_gevent_id(
                event, source_client, refresh_cache, cache_path
            )

        try:
            validator.loginfo = loginfo
            validator.validate(save_plot_to)
        except MEGValidationFailed as exc:
            echo(exc, err=True, color=True)
            raise Exit(2)


def _check_event_ids(events: list[str]) -> None:
    """Abort if any of the input event identifier is invalid."""
    invalid_event_ids = [repr(_) for _ in events if not is_any_event(_)]
    if not invalid_event_ids:
        return

    echo(
        f'Invalid event identifier(s): {", ".join(invalid_event_ids)}.',
        err=True,
        color=True,
    )
    raise Exit(1)
