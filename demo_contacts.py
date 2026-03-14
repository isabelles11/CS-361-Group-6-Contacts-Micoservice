import json
from contacts_microservice import ContactsMicroservice


def print_title(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def pretty_print(data):
    print(json.dumps(data, indent=4))


def main():
    service = ContactsMicroservice()

    user_1 = "user123"
    user_2 = "user999"

    print_title("1. Add contacts for user 1")
    result1 = service.add_contact(
        user_id=user_1,
        name="Maria Sanchez",
        email="maria@email.com",
        phone="301-555-1234"
    )
    pretty_print(result1)

    result2 = service.add_contact(
        user_id=user_1,
        name="Dr. Lee",
        email="drlee@clinic.com",
        phone=""
    )
    pretty_print(result2)

    print_title("2. Add contact for user 2 (to show privacy)")
    result3 = service.add_contact(
        user_id=user_2,
        name="John Carter",
        email="john@email.com",
        phone="555-999-8888"
    )
    pretty_print(result3)

    print_title("3. Try invalid contact input")
    invalid_result = service.add_contact(
        user_id=user_1,
        name="",
        email="bademail",
        phone=""
    )
    pretty_print(invalid_result)

    print_title("4. Edit a contact for user 1")
    contact_id_1 = result1["contact"]["contact_id"]
    edit_result = service.edit_contact(
        user_id=user_1,
        contact_id=contact_id_1,
        name="Maria S.",
        email="maria.s@email.com",
        phone="240-777-1111"
    )
    pretty_print(edit_result)

    print_title("5. List contacts for user 1 only")
    user1_contacts = service.list_contacts(user_1)
    pretty_print(user1_contacts)

    print_title("6. List contacts for user 2 only")
    user2_contacts = service.list_contacts(user_2)
    pretty_print(user2_contacts)

    print_title("7. Associate contact with a medication item")
    assoc_result_1 = service.associate_contact_with_item(
        user_id=user_1,
        contact_id=contact_id_1,
        item_type="medication",
        item_id="med001"
    )
    pretty_print(assoc_result_1)

    print_title("8. Associate another contact with a task item")
    contact_id_2 = result2["contact"]["contact_id"]
    assoc_result_2 = service.associate_contact_with_item(
        user_id=user_1,
        contact_id=contact_id_2,
        item_type="task",
        item_id="task101"
    )
    pretty_print(assoc_result_2)

    print_title("9. Try duplicate association")
    duplicate_assoc = service.associate_contact_with_item(
        user_id=user_1,
        contact_id=contact_id_1,
        item_type="medication",
        item_id="med001"
    )
    pretty_print(duplicate_assoc)

    print_title("10. Get contacts linked to medication med001")
    linked_contacts_med = service.get_contacts_for_item(
        user_id=user_1,
        item_type="medication",
        item_id="med001"
    )
    pretty_print(linked_contacts_med)

    print_title("11. Get contact details for service context")
    context_result = service.get_contact_details_for_context(
        user_id=user_1,
        item_type="task",
        item_id="task101"
    )
    pretty_print(context_result)

    print_title("12. Remove association")
    remove_result = service.remove_contact_association(
        user_id=user_1,
        contact_id=contact_id_1,
        item_type="medication",
        item_id="med001"
    )
    pretty_print(remove_result)

    print_title("13. Check medication contacts again after removal")
    linked_contacts_after = service.get_contacts_for_item(
        user_id=user_1,
        item_type="medication",
        item_id="med001"
    )
    pretty_print(linked_contacts_after)

    print_title("14. Show audit log")
    audit_log = service.get_audit_log()
    pretty_print(audit_log)


if __name__ == "__main__":
    main()