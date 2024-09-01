import allure
import json


def attach(name: str, content, attachment_type=allure.attachment_type.JSON) -> None:
    """
    Universal function to attach objects to an Allure report.

    :param name: Name of the attachment.
    :param content: The content to be attached (can be a string, dictionary, or list).
    :param attachment_type: Type of the attachment. Defaults to JSON.
    """
    if isinstance(content, list):
        if all(isinstance(item, dict) for item in content):
            formatted_content = json.dumps(content, indent=4)
            allure.attach(formatted_content, name=name, attachment_type=attachment_type)
        else:
            formatted_content = "\n".join(map(str, content))
            allure.attach(
                formatted_content,
                name=name,
                attachment_type=allure.attachment_type.TEXT,
            )
    elif isinstance(content, dict):
        allure.attach(
            json.dumps(content, indent=4), name=name, attachment_type=attachment_type
        )
    elif isinstance(content, str):
        allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)
    else:
        allure.attach(
            str(content), name=name, attachment_type=allure.attachment_type.TEXT
        )
