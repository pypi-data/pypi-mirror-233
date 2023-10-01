from grpc_requests import Client


class BosPlusAPI(Client):
    def __init__(self, endpoint, **kwargs):
        super().__init__(endpoint, **kwargs)
        login_data = {
            "username": kwargs["username"] if "username" in kwargs else "root",
            "password": kwargs["password"] if "password" in kwargs else "root",
        }
        self.token = self.AuthenticationService.Login(login_data)

    def _request(self, service, method, request, raw_output=False, **kwargs):
        if (service, method) != ("braiins.bos.v1.AuthenticationService", "Login"):
            metadata = list(kwargs["metadata"]) if "metadata" in kwargs else []
            metadata.append(("authorization", self.token))
            kwargs["metadata"] = metadata
            return super()._request(
                service, method, request, raw_output=raw_output, **kwargs
            )

        method_meta = self.get_method_meta(service, method)
        _request = method_meta.method_type.request_parser(
            request, method_meta.input_type
        )
        result, call = method_meta.handler.with_call(_request, **kwargs)

        for key, value in call.initial_metadata():
            if key == "authorization":
                return value

    @property
    def AuthenticationService(self):
        return self.service("braiins.bos.v1.AuthenticationService")

    @property
    def ActionsService(self):
        return self.service("braiins.bos.v1.ActionsService")

    @property
    def ConfigurationService(self):
        return self.service("braiins.bos.v1.ConfigurationService")

    @property
    def CoolingService(self):
        return self.service("braiins.bos.v1.CoolingService")

    @property
    def MinerService(self):
        return self.service("braiins.bos.v1.MinerService")

    @property
    def PoolService(self):
        return self.service("braiins.bos.v1.PoolService")

    @property
    def TunerService(self):
        return self.service("braiins.bos.v1.TunerService")

    @property
    def ApiVersionService(self):
        return self.service("braiins.bos.ApiVersionService")
