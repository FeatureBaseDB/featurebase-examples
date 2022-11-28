from decimal import Decimal
import grpc
import warnings
from .proto import vdsm_pb2
from .proto import vdsm_pb2_grpc
from .errors import MoleculaError, ErrorWrapper, to_molecula_error
from .vdsd import VDSD

# Default 100MB maximum length for gRPC messages
MAX_MESSAGE_LENGTH = 1024 * 1024 * 100


class TLSAuth:
    def __init__(self, certificate, private_key, root_certificate=None):
        # read in key and certificate
        with open(private_key, "rb") as f:
            pk = f.read()
        with open(certificate, "rb") as f:
            cert = f.read()

        root_cert = None
        if root_certificate is not None:
            with open(root_certificate, "rb") as f:
                root_cert = f.read()

        creds = grpc.ssl_channel_credentials(
            private_key=pk, certificate_chain=cert, root_certificates=root_cert
        )
        self.creds = creds

    def get_channel(self, hostport, options):
        return grpc.secure_channel(hostport, self.creds, options=options)


class Client:
    """
    Client represents a connection to the VDSM through GRPC.
    """

    def __init__(
        self, hostport="localhost:9000", auth=None, prefer_floats=False, log_warnings=True
    ):
        if log_warnings:
            warnings.simplefilter("default")
        options = [
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.lb_policy_name", "round_robin"),
        ]
        if auth != None:
            channel = auth.get_channel(hostport, options=options)
        else:
            channel = grpc.insecure_channel(hostport, options=options)

        self.stub = ErrorWrapper(vdsm_pb2_grpc.MoleculaStub(channel))
        self.prefer_floats = prefer_floats

    def create_vds(self, vdsd):
        warnings.warn(
            "Client.create_vds is deprecated. Please use Pilosa's HTTP API to create indexes.",
            DeprecationWarning,
        )
        if isinstance(vdsd, VDSD):
            vdsd = vdsd.render()
        request = vdsm_pb2.PostVDSRequest(definition=vdsd)
        response = self.stub.PostVDS(request)
        return {
            "id": response.id,
            "uri": response.uri,
        }

    def get_vds_list(self):
        request = vdsm_pb2.GetVDSsRequest()
        response = self.stub.GetVDSs(request)
        for vds in response.vdss:
            yield {
                "id": vds.id,
                "name": vds.name,
                "description": vds.description,
            }

    def get_vds(self, id=None, name=None):
        if id != None:
            warnings.warn(
                'VDS IDs are deprecated. Please use VDS names instead, e.g. get_vds(name="foo")',
                DeprecationWarning,
            )
        request = vdsm_pb2.GetVDSRequest(id=id, name=name)
        response = self.stub.GetVDS(request)
        vds = response.vds
        return {
            "id": vds.id,
            "name": vds.name,
            "description": vds.description,
        }

    def delete_vds(self, id=None, name=None):
        if id != None:
            warnings.warn(
                'VDS IDs are deprecated. Please use VDS names instead, e.g. delete_vds(name="foo")',
                DeprecationWarning,
            )
        request = vdsm_pb2.DeleteVDSRequest(id=id, name=name)
        self.stub.DeleteVDS(request)

    def query(self, vds, pql, timeout=None):
        headers = []
        request = vdsm_pb2.QueryPQLRequest(vds=vds, pql=pql)
        response = self.stub.QueryPQL(request, timeout=timeout)
        yield from _row_response(response, self.prefer_floats)

    def query_future(self, vds, pql, timeout=None):
        headers = []
        request = vdsm_pb2.QueryPQLRequest(vds=vds, pql=pql)
        response = self.stub.QueryPQLUnary.future(request, timeout=timeout)
        future = _future(response, pql, self.prefer_floats)
        return future

    def querysql(self, sql, timeout=None):
        headers = []
        request = vdsm_pb2.QuerySQLRequest(sql=sql)
        response = self.stub.QuerySQL(request, timeout=timeout)
        yield from _row_response(response, self.prefer_floats)

    def querysql_future(self, sql, timeout=None):
        headers = []
        request = vdsm_pb2.QuerySQLRequest(sql=sql)
        response = self.stub.QuerySQLUnary.future(request, timeout)
        future = _future(response, sql, self.prefer_floats)
        return future

    def inspect(self, vds, ids=None, keys=None, fields=None, timeout=None):
        warnings.warn(
            "Client.inspect is deprecated. Please use the Extract() PQL call instead",
            DeprecationWarning,
        )
        if type(ids) is list:
            ids_or_keys = vdsm_pb2.IdsOrKeys(ids=vdsm_pb2.Uint64Array(vals=ids))
        elif type(keys) is list:
            ids_or_keys = vdsm_pb2.IdsOrKeys(keys=vdsm_pb2.StringArray(vals=keys))
        else:
            raise MoleculaError(
                'Client.inspect() must be called with "ids" or "keys" set to a list.'
            )

        request = vdsm_pb2.InspectRequest(vds=vds, records=ids_or_keys, filterFields=fields)
        response = self.stub.Inspect(request, timeout=timeout)
        yield from _row_response(response, self.prefer_floats)


def _row_response(response, prefer_floats):
    for result in response:
        if result.headers:
            headers = list(result.headers)
        row = {}
        for i, h in enumerate(headers):
            attrName = result.columns[i].WhichOneof("columnVal")
            if attrName is None:
                continue
            value = getattr(result.columns[i], attrName)
            if isinstance(value, vdsm_pb2.Uint64Array) or isinstance(value, vdsm_pb2.StringArray):
                value = list(value.vals)
            elif isinstance(value, vdsm_pb2.Decimal):
                value = Decimal(value.value).scaleb(-value.scale)
                if prefer_floats:
                    value = float(value)
            row[headers[i].name] = value
        yield row


def _table_response(response, prefer_floats):
    result = response.result()
    headers = list(result.headers)
    for ro in result.rows:
        row = {}
        for i, h in enumerate(headers):
            attrName = ro.columns[i].WhichOneof("columnVal")
            if attrName is None:
                continue
            value = getattr(ro.columns[i], attrName)
            if isinstance(value, vdsm_pb2.Uint64Array) or isinstance(value, vdsm_pb2.StringArray):
                value = list(value.vals)
            elif isinstance(value, vdsm_pb2.Decimal):
                value = Decimal(value.value) / (10**value.scale)
                if prefer_floats:
                    value = float(value)
            row[headers[i].name] = value
        yield row


class _future:
    def __init__(self, response, query, prefer_floats):
        self._response = response
        self._prefer_floats = prefer_floats
        self.query = query

    def result(self):
        try:
            return list(_table_response(self._response, self._prefer_floats))
        except grpc.RpcError as e:
            raise to_molecula_error(e)
