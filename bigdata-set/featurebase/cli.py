import sys
import decimal
from . import Client, MoleculaError, TLSAuth
from argparse import ArgumentParser
import json

cli = ArgumentParser()
cli.add_argument("address", default="localhost:9000", help="vdsm host:port to connect to")
cli.add_argument("--tls-cert", help="TLS Client Certificate file (PEM-encoded)")
cli.add_argument("--tls-key", help="TLS Client Key file (PEM-encoded)")
cli.add_argument("--tls-ca", help="TLS Certificate Authority file (PEM-encoded)")
subparsers = cli.add_subparsers(dest="subcommand")


class mutex(list):
    pass


def arg(*name_or_flags, **kwargs):
    return (list(name_or_flags), kwargs)


def subcommand(args=[], parent=subparsers):
    def decorator(func):
        parser = parent.add_parser(func.__name__.replace("_", "-"), description=func.__doc__)
        for arg in args:
            if type(arg) == mutex:
                group = parser.add_mutually_exclusive_group(required=True)
                for subarg in arg:
                    group.add_argument(*subarg[0], **subarg[1])
                continue
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


def get_client(args):
    auth = None
    if args.tls_cert:
        auth = TLSAuth(args.tls_cert, args.tls_key, args.tls_ca)
    return Client(args.address, auth=auth)


@subcommand()
def get_vds_list(args):
    """
    Get a list of VDSs.
    """
    client = get_client(args)
    try:
        for vds in client.get_vds_list():
            print(json.dumps(vds, cls=DecimalEncoder))
    except MoleculaError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


@subcommand([mutex([arg("--name", help="Name of VDS"), arg("--id", help="ID of vds")])])
def get_vds(args):
    """
    Get a single VDS.
    """
    client = get_client(args)

    try:
        print(json.dumps(client.get_vds(args.id, args.name), cls=DecimalEncoder))
    except MoleculaError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


@subcommand([arg("vdsd", help="VDSD file")])
def create_vds(args):
    """
    Create a new VDS.
    """
    client = get_client(args)
    with open(args.vdsd, "r") as f:
        vdsd = f.read()
    try:
        print(json.dumps(client.create_vds(vdsd), cls=DecimalEncoder))
    except MoleculaError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


@subcommand([mutex([arg("--name", help="Name of VDS"), arg("--id", help="ID of vds")])])
def delete_vds(args):
    """
    Delete a VDS.
    """
    client = get_client(args)

    try:
        print(json.dumps(client.delete_vds(args.id, args.name), cls=DecimalEncoder))
    except MoleculaError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


@subcommand([arg("vds", help="VDS name"), arg("query", help="PQL Query")])
def query(args):
    """
    Query a VDS (PQL).
    """
    client = get_client(args)

    try:
        for row in client.query(args.vds, args.query):
            print(json.dumps(row, cls=DecimalEncoder))
    except MoleculaError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


@subcommand([arg("vds", help="VDS name"), arg("query", help="PQL query", nargs="+")])
def query_batch(args):
    """
    Query a VDS with a batch of PQL queries.
    """
    exit_code = 0
    client = get_client(args)
    futures = []

    for query in args.query:
        futures.append(client.query_future(args.vds, query))

    for future in futures:
        try:
            for row in future.result():
                print(json.dumps(row, cls=DecimalEncoder))
        except MoleculaError as e:
            print(json.dumps({"error": str(e)}))
            exit_code = 1

    sys.exit(exit_code)


@subcommand([arg("query", help="SQL Query")])
def querysql(args):
    """
    Query a VDS (SQL).
    """
    client = get_client(args)

    try:
        for row in client.querysql(sql=args.query):
            print(json.dumps(row, cls=DecimalEncoder))
    except MoleculaError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


@subcommand([arg("query", help="SQL query", nargs="+")])
def querysql_batch(args):
    """
    Query a VDS with a batch of SQL queries.
    """
    exit_code = 0
    client = get_client(args)
    futures = []

    for query in args.query:
        futures.append(client.querysql_future(query))

    for future in futures:
        try:
            for row in future.result():
                print(json.dumps(row, cls=DecimalEncoder))
        except MoleculaError as e:
            print(json.dumps({"error": str(e)}))
            exit_code = 1

    sys.exit(exit_code)


@subcommand(
    [
        arg("vds", help="VDS name"),
        arg("--field", help="Field to select (default all)", action="append"),
        mutex(
            [
                arg("--id", help="ID of record", type=int, action="append"),
                arg("--key", help="String key of record", action="append"),
            ]
        ),
    ]
)
def inspect(args):
    """
    Inspect VDS record(s).
    """
    client = get_client(args)
    try:
        for row in client.inspect(args.vds, ids=args.id, keys=args.key, fields=args.field):
            print(json.dumps(row, cls=DecimalEncoder))
    except MoleculaError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def main():
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)
