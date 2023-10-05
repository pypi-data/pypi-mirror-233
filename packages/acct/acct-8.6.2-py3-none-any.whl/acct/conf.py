import os

if os.name == "nt":
    DEFAULT_EDITOR = "notepad"
else:
    DEFAULT_EDITOR = "vi"

CLI_CONFIG = {
    "input_file": {
        "positional": True,
        "nargs": "?",
        "subcommands": ["encrypt", "decrypt", "edit"],
    },
    "acct_key": {"subcommands": ["encrypt", "decrypt", "edit"]},
    "acct_file": {"subcommands": ["encrypt", "decrypt", "edit"]},
    "extras": {},
    "overrides": {},
    "render_pipe": {},
    "crypto_plugin": {
        "subcommands": ["encrypt", "decrypt", "edit"],
        "loaded_mod_choices_ref": "crypto",
        "dyne": "acct",
    },
    "output": {
        "source": "rend",
        "subcommands": ["decrypt", "edit"],
        "loaded_mod_choices_ref": "output",
        "dyne": "rend",
    },
    "editor": {"subcommands": ["edit"]},
    "output_file": {"subcommands": ["encrypt", "edit"]},
}
CONFIG = {
    "acct_file": {
        "os": "ACCT_FILE",
        "default": None,
        "help": "An encrypted acct file",
        "sensitive": True,
    },
    "acct_key": {
        "os": "ACCT_KEY",
        "default": None,
        "help": "The key to encrypt the file with, if no key is passed a key will be generated and displayed on after the encrypted file is created",
        "sensitive": True,
    },
    "extras": {
        "render": "json",
        "default": {},
        "help": "Additional arbitrary configuration values as a json string",
    },
    "overrides": {
        "render": "json",
        "default": {},
        "help": "Non-secure profile data that will override the values in the encrypted acct file",
    },
    "crypto_plugin": {
        "default": "fernet",
        "help": "The crypto plugin to use with acct",
    },
    "render_pipe": {
        "default": "jinja|yaml",
        "help": "The render pipe to use to parse input files before they are encrypted",
    },
    "serial_plugin": {
        "default": "msgpack",
        "help": "The pop-serial plugin to use to serialize data before it is encrypted",
    },
    "allowed_backend_profiles": {
        "default": None,
        "help": "A list of backend profile names to allow, defaults to ALL",
    },
    "output": {"source": "rend", "default": "yaml"},
    "output_file": {"default": None, "help": "The output file name when encrypting"},
    "editor": {
        "default": DEFAULT_EDITOR,
        "help": "The text editor to use",
        "os": "EDITOR",
    },
}
SUBCOMMANDS = {
    "encrypt": {x: "Use the acct command to encrypt data" for x in ("desc", "help")},
    "decrypt": {x: "Use the acct command to decrypt data" for x in ("desc", "help")},
    "edit": {
        x: "Edit the decrypted contents of the acct_file and save over the original"
        for x in ("desc", "help")
    },
}
DYNE = {
    "acct": ["acct"],
    "crypto": ["crypto"],
}
