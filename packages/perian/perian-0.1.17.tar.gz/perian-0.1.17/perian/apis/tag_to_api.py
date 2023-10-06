import typing_extensions

from perian.apis.tags import TagValues
from perian.apis.tags.account_api import AccountApi
from perian.apis.tags.job_api import JobApi
from perian.apis.tags.metrics_api import MetricsApi
from perian.apis.tags.provider_api import ProviderApi
from perian.apis.tags.register_api import RegisterApi
from perian.apis.tags.selection_api import SelectionApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACCOUNT: AccountApi,
        TagValues.JOB: JobApi,
        TagValues.METRICS: MetricsApi,
        TagValues.PROVIDER: ProviderApi,
        TagValues.REGISTER: RegisterApi,
        TagValues.SELECTION: SelectionApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACCOUNT: AccountApi,
        TagValues.JOB: JobApi,
        TagValues.METRICS: MetricsApi,
        TagValues.PROVIDER: ProviderApi,
        TagValues.REGISTER: RegisterApi,
        TagValues.SELECTION: SelectionApi,
    }
)
