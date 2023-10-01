# BOSMiner-py

Python client to retrieve data from any miner running Braiins OS+ GRPC and Socket API


## Install

```
pip install bosminer
```

## GRPC API Client Usage

```python
from bos.bosplusapi.client import BosPlusAPI

host = 'moe.s5p8'
miner = BosPlusAPI(f'{host}:50051')

print(miner.CoolingService.GetCoolingState())
```

```json
{
   "fans": [
      {"position": 0, "rpm": 3708, "target_speed_ratio": 0.38},
      {"position": 1, "rpm": 3708, "target_speed_ratio": 0.38},
      {"position": 2, "rpm": 3708, "target_speed_ratio": 0.38},
      {"position": 3, "rpm": 3678, "target_speed_ratio": 0.38}
   ],
   "highest_temperature": {
      "location": "SENSOR_LOCATION_CHIP",
      "temperature": {
         "degree_c": 59.5
      }
   }
}
```

### Implemented Services

All available services are implemented. Check [BOS Plus API docs](https://github.com/braiins/bos-plus-api#usage).

Thanks to server reflection and the amazing [grpcrequest](https://github.com/wesky93/grpc_requests) library, you can easily explore the API and its methods.

```python
In [7]: miner.service_names
Out[7]:
('braiins.bos.ApiVersionService',
 'braiins.bos.v1.ActionsService',
 'braiins.bos.v1.AuthenticationService',
 'braiins.bos.v1.CoolingService',
 'braiins.bos.v1.PoolService',
 'braiins.bos.v1.TunerService',
 'braiins.bos.v1.ConfigurationService',
 'braiins.bos.v1.MinerService',
 'grpc.reflection.v1alpha.ServerReflection')
```

```python
In [8]: miner.MinerService.method_names
Out[8]: ('GetMinerDetails', 'GetMinerStats', 'GetHashboards')

```

```python
In [9]: miner.MinerService.GetMinerDetails()
Out[9]:
{'uid': 'PuiPCrGshtlJZzzM',
 'miner_identity': {'brand': 'MINER_BRAND_ANTMINER',
  'model': 'MINER_MODEL_ANTMINER_S19J_PRO',
  'name': 'Antminer S19J Pro'},
 'platform': 'PLATFORM_AM3_BBB',
 'bos_mode': 'BOS_MODE_SD',
 'bos_version': {'current': '2023-05-29-0-1daef48b-23.03.2-plus',
  'major': '2022-09-13-0-11012d53-22.08-plus',
  'bos_plus': True},
 'hostname': 'moe',
 'mac_address': '6c:79:b8:75:25:cc',
 'system_uptime': '193692'}
```

## Socket API Client Usage

```python
from bos.bosminer.client import BosMiner

host = 'moe.s5p8'
miner = BosMiner(host)

print(miner.fans())
```

```json
{
   "STATUS": [
      {
         "STATUS": "S",
         "When": 1684941022,
         "Code": 202,
         "Msg": "4 Fan(s)",
         "Description": "BOSer boser-buildroot 0.1.0-0ce150e9"
      }
   ],
   "FANS": [
      {
         "FAN": 0,
         "ID": 0,
         "RPM": 3226,
         "Speed": 32
      },
      {
         "FAN": 1,
         "ID": 1,
         "RPM": 3315,
         "Speed": 32
      },
      {
         "FAN": 2,
         "ID": 2,
         "RPM": 3226,
         "Speed": 32
      },
      {
         "FAN": 3,
         "ID": 3,
         "RPM": 3255,
         "Speed": 32
      }
   ],
   "id": 1
}

```

### Implemented commands

All available commands are implemented. Check [Bosminer API docs](https://docs.braiins.com/os/open-source-en/Development/1_api.html).

> The commands switchpool, enablepool, disablepool, addpool and removepool are not fully implemented in Braiins OS. The outcome of these commands is reset after restart and they do not activate the pools. This is a known issue and is being fixed.
