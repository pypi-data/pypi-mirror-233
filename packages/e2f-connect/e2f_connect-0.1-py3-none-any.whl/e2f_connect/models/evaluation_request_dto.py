import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.evaluation_request_dto_metrics import EvaluationRequestDtoMetrics


T = TypeVar("T", bound="EvaluationRequestDto")


@_attrs_define
class EvaluationRequestDto:
    """
    Attributes:
        project_name (str): Project name to use for reference. Example: Your project name.
        metrics (EvaluationRequestDtoMetrics): Metrics to be used for dataset. Example: [{'name': 'Your custom metric',
            'description': 'Description of your custom metric', 'category': 'completion', 'type': 'range', 'values': {'min':
            1, 'max': 10}}, {'name': 'Your custom metric 2', 'description': 'Description of your custom metric 2',
            'category': 'completion', 'type': 'range', 'values': {'min': 1, 'max': 10}}].
        language (str): Language of the dataset. Example: en-US.
        requester_name (str): Name of the requester. Example: Your name.
        requester_email (str): Email of the requester. Example: Your email.
        file (Union[Unset, File]):
        dataset (Union[Unset, str]): Location of the dataset. Example: Link to your dataset.
        project_instructions (Union[Unset, str]): ... Example: project instruction.
        due_date (Union[Unset, str]): The date when the project should be completed. Example: 2023-12-31.
        domain (Union[Unset, List[str]]): Domain of the dataset. Example: ['Medical', ''].
    """

    project_name: str
    metrics: "EvaluationRequestDtoMetrics"
    language: str
    requester_name: str
    requester_email: str
    file: Union[Unset, File] = UNSET
    dataset: Union[Unset, str] = UNSET
    project_instructions: Union[Unset, str] = UNSET
    due_date: Union[Unset, str] = UNSET
    domain: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_name = self.project_name
        metrics = self.metrics.to_dict()

        language = self.language
        requester_name = self.requester_name
        requester_email = self.requester_email
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        dataset = self.dataset
        project_instructions = self.project_instructions
        due_date = self.due_date
        domain: Union[Unset, List[str]] = UNSET
        if not isinstance(self.domain, Unset):
            domain = self.domain

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "projectName": project_name,
                "metrics": metrics,
                "language": language,
                "requesterName": requester_name,
                "requesterEmail": requester_email,
            }
        )
        if file is not UNSET:
            field_dict["file"] = file
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if project_instructions is not UNSET:
            field_dict["projectInstructions"] = project_instructions
        if due_date is not UNSET:
            field_dict["dueDate"] = due_date
        if domain is not UNSET:
            field_dict["domain"] = domain

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        project_name = (
            self.project_name
            if isinstance(self.project_name, Unset)
            else (None, str(self.project_name).encode(), "text/plain")
        )
        metrics = (None, json.dumps(self.metrics.to_dict()).encode(), "application/json")

        language = (
            self.language if isinstance(self.language, Unset) else (None, str(self.language).encode(), "text/plain")
        )
        requester_name = (
            self.requester_name
            if isinstance(self.requester_name, Unset)
            else (None, str(self.requester_name).encode(), "text/plain")
        )
        requester_email = (
            self.requester_email
            if isinstance(self.requester_email, Unset)
            else (None, str(self.requester_email).encode(), "text/plain")
        )
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        dataset = self.dataset if isinstance(self.dataset, Unset) else (None, str(self.dataset).encode(), "text/plain")
        project_instructions = (
            self.project_instructions
            if isinstance(self.project_instructions, Unset)
            else (None, str(self.project_instructions).encode(), "text/plain")
        )
        due_date = (
            self.due_date if isinstance(self.due_date, Unset) else (None, str(self.due_date).encode(), "text/plain")
        )
        domain: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.domain, Unset):
            _temp_domain = self.domain
            domain = (None, json.dumps(_temp_domain).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "projectName": project_name,
                "metrics": metrics,
                "language": language,
                "requesterName": requester_name,
                "requesterEmail": requester_email,
            }
        )
        if file is not UNSET:
            field_dict["file"] = file
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if project_instructions is not UNSET:
            field_dict["projectInstructions"] = project_instructions
        if due_date is not UNSET:
            field_dict["dueDate"] = due_date
        if domain is not UNSET:
            field_dict["domain"] = domain

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.evaluation_request_dto_metrics import EvaluationRequestDtoMetrics

        d = src_dict.copy()
        project_name = d.pop("projectName")

        metrics = EvaluationRequestDtoMetrics.from_dict(d.pop("metrics"))

        language = d.pop("language")

        requester_name = d.pop("requesterName")

        requester_email = d.pop("requesterEmail")

        _file = d.pop("file", UNSET)
        file: Union[Unset, File]
        if isinstance(_file, Unset):
            file = UNSET
        else:
            file = File(payload=BytesIO(_file))

        dataset = d.pop("dataset", UNSET)

        project_instructions = d.pop("projectInstructions", UNSET)

        due_date = d.pop("dueDate", UNSET)

        domain = cast(List[str], d.pop("domain", UNSET))

        evaluation_request_dto = cls(
            project_name=project_name,
            metrics=metrics,
            language=language,
            requester_name=requester_name,
            requester_email=requester_email,
            file=file,
            dataset=dataset,
            project_instructions=project_instructions,
            due_date=due_date,
            domain=domain,
        )

        evaluation_request_dto.additional_properties = d
        return evaluation_request_dto

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
