import pytest

from drf_versioning.transform import AddField, RemoveField, Transform


def test_transform_notimplemented():
    trans = Transform()
    with pytest.raises(NotImplementedError):
        trans.to_internal_value("data", "request")
    with pytest.raises(NotImplementedError):
        trans.to_representation("data", "request", "instance")


@pytest.mark.parametrize("transform_class", [AddField, RemoveField])
@pytest.mark.parametrize(
    "incoming_data, expected_result",
    [
        ({}, {}),  # if the field isn't present, it shouldn't cause problems
        ({"foo": "this should be ignored"}, {}),
        (
            {"foo": "this should be ignored", "other": "unchanged"},
            {"other": "unchanged"},
        ),
    ],
)
def test_addfield_and_removefield_to_internal_value(
    incoming_data, expected_result, transform_class
):
    trans = transform_class()
    trans.field_name = "foo"
    assert trans.to_internal_value(data=incoming_data, request="foo") == expected_result


@pytest.mark.parametrize(
    "outgoing_data, expected_result",
    [
        ({}, {}),
        ({"foo": "this should be ignored"}, {}),
        (
            {"foo": "this should be ignored", "other": "unchanged"},
            {"other": "unchanged"},
        ),
    ],
)
def test_addfield_to_representation(outgoing_data, expected_result):
    trans = AddField()
    trans.field_name = "foo"
    assert trans.to_representation(data=outgoing_data, request=..., instance=...) == expected_result


@pytest.mark.parametrize(
    "outgoing_data, expected_result",
    [
        ({}, {"foo": 0}),
        ({"foo": "this should be ignored"}, {"foo": 0}),
        (
            {"other": "unchanged"},
            {"foo": 0, "other": "unchanged"},
        ),
    ],
)
def test_removefield_to_representation(outgoing_data, expected_result):
    trans = RemoveField()
    trans.field_name = "foo"
    trans.null_value = 0
    assert trans.to_representation(data=outgoing_data, request=..., instance=...) == expected_result
