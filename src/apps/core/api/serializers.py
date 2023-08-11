from apps.accounts.api.v1.serializers import UserMiniSerializer, BaseRoleSerializer
from apps.addresses.api.v1.serializers import RegionSerializer, DistrictSerializer
from apps.products.api.v1.serializers import ProductShortSerializer
from apps.employees.api.v1.serializers import (
    ClientMiniSerializer,
    StaffMiniSerializer,
    PartnerMiniSerializer,
    BaseEmployeeSerializer,
    EmployeeListSerializer,
    StaffPositionSerializer,
    StaffInformativeSerializer,
    EmployeeDetailSerializer,
    BasePartnerSerializer,
    AdditionalStatusSerializer,
    CreateUpdateClientSerializer,
    ClientDetailSerializer,
    ClientListSerializer,
    RefClientListSerializer,
    CRUDClientCommentSerializer,
    ClientCommentSerializer,
    PostPutDealerSerializer,
    DealerListSerializer,
    DealerDetailSerializer,
    PostPutDealerPaymentSerializer,
    DealerPaymentDetailSerializer,
    CRUDClientHistorySerializer,
    CRUDClientInterviewSerializer,
    ClientInterviewDetailSerializer,
)
from apps.main.api.v1.serializers import (
    VoucherSerializer,
    ConfirmationCodeSerializer,
    VerifySerializer,
    BaseCurrencySerializer,
    VoucherGroupSerializer
)
from apps.branches.api.v1.serializers import (
    BaseBranchSerializer,
    BranchListSerializer,
    PublicBranchSerializer,
    BranchMiniSerializer,
    StaffBranchSerializer
)

from apps.credit.api.v1.serializers import (
    DealerClientListSerializer,
    ListGuarantorUserSerializer,
    GuarantorContractSerializer,
)
