import asyncio
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import warnings
from typing import Any
from typing import Awaitable
from typing import Dict
from typing import Iterable
from typing import List

import dict_tools.update
from dict_tools.data import NamespaceDict
from dict_tools.data import SafeNamespaceDict

__func_alias__ = {"profiles_": "profiles"}


def __init__(hub):
    hub.acct.CONFIG_LOAD = ["acct", "rend"]
    hub.acct.PROFILES = SafeNamespaceDict()
    hub.acct.UNLOCKED = False
    hub.acct.DEFAULT = "default"
    hub.acct.BACKEND_KEY = "acct-backends"
    hub.acct.SERIAL_PLUGIN = "msgpack"

    hub.pop.sub.add(dyne_name="crypto")
    hub.pop.sub.load_subdirs(hub.acct, recurse=True)
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.add(dyne_name="output")
    hub.pop.sub.add(dyne_name="serial")


def cli(hub):
    hub.pop.config.load(hub.acct.CONFIG_LOAD, cli="acct")
    hub.pop.loop.create()
    coro = hub.acct.init.cli_apply()
    retcode = hub.pop.Loop.run_until_complete(coro)
    sys.exit(retcode)


async def cli_apply(hub) -> int:
    hub.acct.SERIAL_PLUGIN = hub.OPT.acct.serial_plugin
    outputter = hub.OPT.rend.output or "yaml"
    if hub.SUBPARSER == "encrypt":
        retcode = await hub.acct.init.cli_encrypt(**hub.OPT.acct)
    elif hub.SUBPARSER == "decrypt":
        retcode = await hub.acct.init.cli_decrypt(outputter=outputter, **hub.OPT.acct)
    elif hub.SUBPARSER == "edit":
        retcode = await hub.acct.init.cli_edit(outputter=outputter, **hub.OPT.acct)
    else:
        retcode = 2
    return retcode


async def cli_encrypt(
    hub,
    input_file: str,
    *,
    output_file: str,
    acct_key: str = None,
    crypto_plugin: str,
    render_pipe: str,
    **kwargs,
):
    created_new_acct_key = False
    if not acct_key:
        created_new_acct_key = True
        hub.log.info(f"New acct_key generated with '{crypto_plugin}' plugin")

    new_key = await hub.crypto.init.encrypt_file(
        crypto_plugin=crypto_plugin,
        acct_file=input_file,
        acct_key=acct_key,
        output_file=output_file,
        render_pipe=render_pipe,
    )
    hub.log.info(f"Encrypted {input_file} with the {crypto_plugin} algorithm")
    if created_new_acct_key:
        # Print this to the terminal, and only this -- for easier scripting
        # Do not log it or put it in log files
        print(new_key)

    return 0


async def cli_decrypt(
    hub,
    input_file: str,
    *,
    acct_key: str = None,
    crypto_plugin: str,
    render_pipe: str,
    allowed_backend_profiles: List[str] = None,
    outputter: str = "yaml",
    **kwargs,
):
    ret = await hub.acct.init.profiles(
        crypto_plugin=crypto_plugin,
        acct_file=input_file or kwargs.get("acct_file"),
        acct_key=acct_key,
        render_pipe=render_pipe,
        allowed_backend_profiles=allowed_backend_profiles,
        hard_fail=True,
    )
    out = hub.output[outputter].display(NamespaceDict(ret))
    print(out)
    return 0


async def cli_edit(
    hub,
    input_file: str,
    *,
    output_file: str = None,
    acct_key: str = None,
    crypto_plugin: str,
    render_pipe: str,
    editor: str,
    outputter: str = "yaml",
    **kwargs,
) -> int:
    editor = str(editor)
    if " " in editor:
        editor, editor_opts = str(editor).split(" ", maxsplit=1)
    else:
        editor_opts = ""
    if not shutil.which(editor):
        hub.log.critical(f"No such text editor '{editor}'")

    acct_file = input_file or kwargs.get("acct_file")
    if not acct_file:
        raise ValueError("No input file name")
    if os.path.exists(acct_file):
        # decrypt the acct file, create one in a default location if it doesn't exist
        maybe_plaintext = await hub.crypto.init.decrypt_file(
            crypto_plugin=crypto_plugin,
            acct_file=acct_file,
            acct_key=acct_key,
            render_pipe=render_pipe,
        )
        if isinstance(maybe_plaintext, dict):
            maybe_plaintext = NamespaceDict(maybe_plaintext)
    else:
        maybe_plaintext = ""
    # write the contents to a temporary file
    with tempfile.NamedTemporaryFile(
        "w+", prefix="acct-", suffix=".yaml", delete=True
    ) as fh:
        plaintext = hub.output[outputter].display(maybe_plaintext)
        fh.write(plaintext)
        fh.flush()
        # open the temporary file in the default editor
        if editor_opts:
            retcode = subprocess.call([editor] + shlex.split(editor_opts) + [fh.name])
        else:
            retcode = subprocess.call([editor, fh.name])
        if retcode:
            return retcode

        # Encrypt the temporary file, save over ACCT_FILE and delete the temporary file
        return await hub.acct.init.cli_encrypt(
            input_file=fh.name,
            # Overwrite the input file with the new contents
            output_file=output_file or input_file,
            acct_key=acct_key or None,
            crypto_plugin=crypto_plugin,
            render_pipe=render_pipe,
            **kwargs,
        )


async def profiles_(
    hub,
    acct_file: str,
    acct_key: str = None,
    crypto_plugin: str = "fernet",
    render_pipe: str = "yaml",
    allowed_backend_profiles: List[str] = None,
    hard_fail: bool = False,
) -> Dict[str, Any]:
    """
    Read profile information from a file and return the raw data
    """
    raw_profiles = await hub.crypto.init.decrypt_file(
        crypto_plugin=crypto_plugin,
        acct_file=acct_file,
        acct_key=acct_key,
        render_pipe=render_pipe,
    )
    if not raw_profiles:
        raw_profiles = {}

    backend_profiles = await hub.acct.backend.init.unlock(
        profiles=raw_profiles,
        allowed_backend_profiles=allowed_backend_profiles,
        hard_fail=hard_fail,
    )
    dict_tools.update.update(raw_profiles, backend_profiles)
    return raw_profiles


async def unlock(
    hub,
    acct_file: str,
    acct_key: str = None,
    crypto_plugin: str = "fernet",
    render_pipe: str = "yaml",
    hard_fail: bool = False,
):
    """
    Initialize the file read, then store the authentication data on the hub as hub.acct.PROFILES
    """
    if hub.acct.UNLOCKED:
        return

    raw_profiles = await hub.acct.init.profiles(
        acct_file, acct_key, crypto_plugin, render_pipe=render_pipe, hard_fail=hard_fail
    )
    hub.acct.BACKEND_KEY = raw_profiles.pop("backend_key", hub.acct.BACKEND_KEY)
    hub.acct.DEFAULT = raw_profiles.pop("default", hub.acct.DEFAULT)
    dict_tools.update.update(hub.acct.PROFILES, raw_profiles)
    hub.acct.UNLOCKED = True


async def unlock_blob(
    hub,
    acct_file_contents: str,
    acct_key: str,
    crypto_plugin: str = "fernet",
    backend_key: str = None,
    default_profile: str = None,
    allowed_backend_profiles: List[str] = None,
    hard_fail: bool = False,
):
    """
    Read acct data from a byte string
    """
    profiles = await hub.crypto.init.decrypt(
        plugin=crypto_plugin, data=acct_file_contents, key=acct_key
    )
    if backend_key is None:
        backend_key = profiles.get("backend_key", hub.acct.BACKEND_KEY)

    if default_profile is None:
        default_profile = profiles.get("default", hub.acct.DEFAULT)

    backend_profiles = await hub.acct.backend.init.unlock(
        profiles=profiles,
        backend_key=backend_key,
        allowed_backend_profiles=allowed_backend_profiles,
        hard_fail=hard_fail,
    )

    dict_tools.update.update(profiles, backend_profiles)

    return SafeNamespaceDict(
        default_profile=default_profile,
        backend_key=backend_key,
        profiles=profiles,
        sub_profiles=None,
    )


async def single(
    hub,
    profile_name: str,
    subs: Iterable[str],
    sub_profiles: None,
    profiles: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Retrieve a specific named profile for the given subs and profiles
    """
    if sub_profiles is not None:
        warnings.warn(
            "sub_profiles is no longer used, remove it from the call",
            DeprecationWarning,
        )

    ret = {}
    if not subs:
        hub.log.debug(f"No subs specified for profile '{profile_name}'")
        return ret

    for sub in subs:
        if sub not in profiles:
            continue

        if profile_name not in profiles[sub]:
            continue

        if ret:
            # Complain if there are multiple profiles of the same name across the specified subs
            raise ValueError(
                f"Multiple profiles named '{profile_name}' across subs: {', '.join(subs)}"
            )
        else:
            ret = SafeNamespaceDict(profiles[sub][profile_name])

    if not ret:
        clean_profiles = {
            provider: list(profiles)
            for provider, profiles in profiles.items()
            if provider in subs
        }
        hub.log.trace(f"Could not find profile '{profile_name}' in: {clean_profiles}")

    return ret


async def gather(
    hub,
    subs: Iterable[str],
    profile: str,
    profiles=None,
    sub_profiles=None,
    allowed_backend_profiles: List[str] = None,
    hard_fail: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    :param hub:
    :param subs: The subs to check for a profile
    :param profile: The name of the acct_profile to retrieve
    :param profiles: raw profiles to use if not unlocking acct first
    :param sub_profiles: Unused
    :param allowed_backend_profiles: A list of enabled backend profiles
    :param hard_fail: Raise exceptions instead of catching them
    :return: The named profile
    """
    if sub_profiles is not None:
        warnings.warn(
            "sub_profiles is no longer used, remove it from the call",
            DeprecationWarning,
        )

    # If acct is locked and we don't have new profiles then return right away
    if profiles is None:
        if hub.acct.UNLOCKED:
            profiles = hub.acct.PROFILES
        else:
            profiles = {}

    # Collect any other profiles from backends
    backend_profiles = await hub.acct.backend.init.unlock(
        profiles, allowed_backend_profiles=allowed_backend_profiles, hard_fail=hard_fail
    )
    dict_tools.update.update(profiles, backend_profiles)

    # Reliably get overrides from config
    config_overrides = hub.OPT.get("acct", {}).get("overrides")
    if config_overrides:
        # Apply overrides from config
        dict_tools.update.update(profiles, config_overrides)

    # Run the profiles through the gather plugins and update them with any changes
    processed_profiles = await hub.acct.init.process(
        subs, profiles, hard_fail=hard_fail
    )
    dict_tools.update.update(profiles, processed_profiles)

    return await hub.acct.init.single(
        profile_name=profile,
        subs=subs,
        profiles=profiles,
        sub_profiles=sub_profiles,
    )


async def process(
    hub, subs: Iterable[str], profiles: Dict[str, Any], hard_fail: bool = False
):
    """
    Process the given profiles through acct plugins.
    Acct plugins turn static profile data into connections to a server etc...
    """
    processed = SafeNamespaceDict()
    coros = []

    for sub in subs:
        if not hasattr(hub.acct, sub):
            hub.log.trace(f"{sub} does not extend acct")
            continue

        processed[sub] = {}
        for plug in hub.acct[sub]:
            try:
                if "profiles" in plug.gather.signature.parameters:
                    regex = re.compile(f"{sub}(\\.{plug.__name__})?$")
                    relevant_profiles = {
                        k: v for k, v in profiles.items() if regex.match(k)
                    }
                    ret = plug.gather(relevant_profiles)
                else:
                    # It either doesn't need to know about existing profiles or will get them from hub.acct.PROFILES
                    ret = plug.gather()

                coros.append(_keyed_coroutine(sub, hub.pop.loop.unwrap(ret)))
            except Exception as e:
                hub.log.error(
                    f"{e.__class__.__name__} gathering profiles from hub.acct.{sub}.{plug.__name__}: {e}"
                )
                if hard_fail:
                    raise

    for ret in asyncio.as_completed(coros):
        sub = None
        try:
            sub, val = await ret
            processed[sub].update(val)
        except Exception as e:
            hub.log.error(f"{e.__class__.__name__}: {sub}: await gather profiles: {e}")
            if hard_fail:
                raise

    return processed


async def _keyed_coroutine(sub: str, coro: Awaitable):
    """
    :param sub:
    :param coro:
    :return:
    """
    return sub, await coro
