import typing_extensions

from perian.paths import PathValues
from perian.apis.paths.provider_create import ProviderCreate
from perian.apis.paths.register_gpu_create import RegisterGpuCreate
from perian.apis.paths.account_create import AccountCreate
from perian.apis.paths.selection_get_flavors import SelectionGetFlavors
from perian.apis.paths.job_create import JobCreate
from perian.apis.paths.job_get import JobGet
from perian.apis.paths.job_get_all import JobGetAll
from perian.apis.paths.metrics_liveness import MetricsLiveness
from perian.apis.paths.metrics_readiness import MetricsReadiness

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.PROVIDER_CREATE: ProviderCreate,
        PathValues.REGISTER_GPU_CREATE: RegisterGpuCreate,
        PathValues.ACCOUNT_CREATE: AccountCreate,
        PathValues.SELECTION_GETFLAVORS: SelectionGetFlavors,
        PathValues.JOB_CREATE: JobCreate,
        PathValues.JOB_GET: JobGet,
        PathValues.JOB_GETALL: JobGetAll,
        PathValues.METRICS_LIVENESS: MetricsLiveness,
        PathValues.METRICS_READINESS: MetricsReadiness,
    }
)

path_to_api = PathToApi(
    {
        PathValues.PROVIDER_CREATE: ProviderCreate,
        PathValues.REGISTER_GPU_CREATE: RegisterGpuCreate,
        PathValues.ACCOUNT_CREATE: AccountCreate,
        PathValues.SELECTION_GETFLAVORS: SelectionGetFlavors,
        PathValues.JOB_CREATE: JobCreate,
        PathValues.JOB_GET: JobGet,
        PathValues.JOB_GETALL: JobGetAll,
        PathValues.METRICS_LIVENESS: MetricsLiveness,
        PathValues.METRICS_READINESS: MetricsReadiness,
    }
)
